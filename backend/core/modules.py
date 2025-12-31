import os
import pwd
import shlex
import asyncio
import signal

from pathlib import Path
from pydantic import BaseModel

from lib.utils import parse_config, file_response, dynamic_import

from .models import ModuleConfigModel, ShellOptionsModel



class TaskModule:
  async def run(self, *args):
    pass
  
  async def stop(self, *args):
    pass


class ShellTaskModule(TaskModule):
  def __init__(self, name, path, config):
    super().__init__()
    self.name = name # Module name
    self.path = path # Module path

    # Command config
    self.config: ShellOptionsModel = config

    # Live output timeout 
    self.stdout_timeout = 30

    self.process = None

  # Drop process privilages
  def drop_privileges(self, uid_name="nobody"):
    def _drop():
      # Get the uid/gid from the username
      pw_record = pwd.getpwnam(uid_name)
      uid = pw_record.pw_uid
      gid = pw_record.pw_gid
  
      # Remove group privileges
      os.setgroups([])
  
      # Drop gid first, then uid
      os.setgid(gid)
      os.setuid(uid)
  
      # Extra safety: ensure no privilege escalation
      os.umask(0o077)

    return _drop

  # Read process stream
  async def read_stream(self, stream, callback):
    while True:
      line = await stream.readline()
      if not line:
        break
      # dashboard - stdout, stderr
      await callback(line.decode().rstrip(), self.config.message)

  # Parse command
  def parse_command(self, options):
    command = self.config.command.strip().format(**options)

    return [
      str(self.path / arg) if arg.startswith("./") else arg
      for arg in shlex.split(command)
    ] if not self.config.shell else command

  # Run process
  async def run(self, dashboard, options) -> tuple[str, str]:
    command = self.parse_command(options)

    # Using user privilages
    user = self.config.user.strip()

    if user == "root":
      preexec = os.setsid
    else:
      drop = self.drop_privileges(user)
  
      def preexec():
        os.setsid()     # create new process group
        drop()          # drop privileges
  
    if self.config.shell:
      self.process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(dashboard.storage.files_path),
        preexec_fn=preexec,
      )
    else:
      self.process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(dashboard.storage.files_path),
        preexec_fn=preexec,
      )

    # Output
    await asyncio.gather(
      self.read_stream(self.process.stdout, dashboard.stdout),
      self.read_stream(self.process.stderr, dashboard.stderr),
    )

  # Stop process
  async def stop(self):
    if not self.process:
      return

    if self.process.returncode is None:
      try:
        os.killpg(self.process.pid, signal.SIGKILL)
        await self.process.wait()
      except ProcessLookupError:
        pass

class DynamicTaskModule(TaskModule):
  def __init__(self, name: str, path, config):
    super().__init__()
    self.name = name
    self.path = path
    self.config = config

    self.module = dynamic_import(name, self.path / self.config.run)
    self.task = None

  async def run(self, dashboard, options):
    func = getattr(self.module, "run", None)
    if not func:
      return

    # Function wrapper
    async def wrapper():
      try:
        return await func(dashboard, options)
      except asyncio.CancelledError:
        return

    self.task = asyncio.create_task(wrapper())
    return await self.task

  async def stop(self):
    if not self.task:
      return
    self.task.cancel()


# Global - Module object
class Module:
  def __init__(self, path):
    self.path = path
    self.name = self.path.name
    self.config = parse_config(path / "escapy.json", ModuleConfigModel)

  def get_options(self):
    return self.config.options or {}
  
  def _get_icon(self) -> str:
    icon_path = self.path / "public" / self.config.icon

    if icon_path.is_file():
      return f"/module/public/{self.name}/{self.config.icon}"

    return "/static/default-module-icon.png"
  
  def get_public_file(self, path: str):
    return file_response(self.path / "public", path)

  @property
  def meta(self):
    return {
      "name": self.name,
      "title": self.config.title,
      "about": self.config.about,
      "author": self.config.author,
      
      "icon": self._get_icon()
    }
  
  # Creare Task Module Object
  def create(self):
    # Module Type
    if isinstance(self.config.run, str):
      return DynamicTaskModule(self.name, self.path, self.config)
    else:
      return ShellTaskModule(self.name, self.path, self.config.run)

  def __call__(self):
    return self.create()

class Modules:
  def __init__(self, storage):
    self.path = Path("modules").resolve()

    self.storage = storage
    self._modules = self.__load_modules()

  def __load_module(self, path: Path):
    try:
      return Module(path)
    except Exception as e:
      print(f"[-] Failed to load module: {path} \nReason: {e}")
      return None

  def __load_modules(self):
    return {m.name: m for m in
      (self.__load_module(path) for path in self.path.iterdir())
      if m is not None
    }

  def get_module(self, name: str):
    return self._modules[name]

  def get_modules_list(self):
    return { name: module.meta for name, module in self._modules.items() }

  def get_module_options(self, name: str):
    return self.get_module(name).get_options()
