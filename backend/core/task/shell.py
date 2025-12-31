import shlex
import inspect

from pathlib import Path

from lib.utils import is_coro, args_match_function



# Task Shell - Tab 
# cmd_<command> is command and takes args
# help_<command> is help for that command
# Response can be html code it will render safely with all tags
class TaskShell:
  def __init__(self, task):
    self._task = task

    self._templates: Path = Path("templates/shell")
    self.results: list[str] = []

    # Alias commands
    self.alias = {
      "?": "help"
    }

  # Load & format
  def load_template(self, name: str, *args):
    try:
      with open(self._templates / f"{name}.txt") as file:
        return file.read().strip().format(*args)
      
    except Exception:
      raise Exception("Internal Error loading response template")

  # ---------> Defaults
  async def default(self, command, args):
    return f"<span class='opacity-80'>{command}: command not found</span>"

  # Default cmd_help
  async def default_help(self, command: str):
    func = getattr(self, f"cmd_{command}", None)
    if not func:
      return f"{command}: No help found"

    sig = inspect.signature(func)

    args = []
    for name, param in sig.parameters.items():
      # skip self
      if name == "self":
        continue

      # include only parameters annotated as str
      if param.annotation is str:
        # optional vs required
        if param.default is inspect.Parameter.empty:
          args.append(f"<{name}>")
        else:
          args.append(f"[{name}]")

    args_str = " ".join(args)
    return f"Usage: {command} {args_str}".rstrip()
  
  # ---------> commands
  def _get_help(self) -> str:
    rows = []

    for attr_name in dir(self):
      if not attr_name.startswith("cmd_"):
        continue

      method = getattr(self, attr_name)
      if not callable(method):
        continue

      name = attr_name[4:]
      doc = inspect.getdoc(method) or ""
      description = doc.splitlines()[0] if doc else "-"

      rows.append(
        f"""
        <tr class="hover">
          <td class="font-mono">{name}</td>
          <td class="font-mono opacity-80">{description}</td>
        </tr>
        """
      )

    return f"""
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full text-xs">
          <thead>
            <tr>
              <th class="font-mono">Commands</th>
              <th class="font-mono">Description</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    """

  async def cmd_help(self, command: str = None):
    """Prints Help"""
    # If command
    if command:
      func = getattr(self, f"help_{command}", None)
      # Default help function
      if not func:
        return await self.default_help(command)
      # helo_cmd function
      return await func() if is_coro(func) else func()
    
    return self._get_help()

  # intro
  def cmd_intro(self):
    """Task Intro"""
    return self.load_template("intro", self._task.name)
  # stop
  async def cmd_stop(self):
    """Stop Task"""
    await self._task.stop()
    
    return "Task Stopped"
  # start
  async def cmd_start(self):
    """Run Task"""
    await self._task.run()

    return "Task Started"

  def cmd_meta(self) -> str:
    """Get Task Details"""
    def render_dict(d: dict, indent: int = 0) -> str:
        pad = " " * indent
        html = ""

        for key, value in d.items():
            if isinstance(value, dict):
                html += (
                    f"{pad}<div><strong>{key}</strong>:</div>\n"
                    f"{pad}<div style='margin-left: 2ch;'>\n"
                    f"{render_dict(value, indent + 2)}"
                    f"{pad}</div>\n"
                )
            else:
                html += f"{pad}<div><strong>{key}</strong>: {value}</div>\n"

        return html

    return render_dict(self._task.meta)

  # ---------> run
  async def _run(self, command: str, args: list[str]):
    func = getattr(self, f"cmd_{command}", None)
    if func is None:
      return await self.default(command, args)
    
    # Args Match Check
    ok, err = args_match_function(func, *args)
    if ok:
      return await func(*args) if is_coro(func) else func(*args)
    else:
      return f"<p>Error: {command}: {err}<p><p>{await self.default_help(command)}</p>"

  async def run(self, command: str) -> str:
    command = command.strip()
    if not command:
      raise ValueError("Command cannot be empty")

    split_command = shlex.split(command)

    # Actuall command
    cmd = split_command[0]
    # Args
    args = split_command[1:]

    # Alias if found else command
    alias_cmd = self.alias.get(cmd, cmd)

    try:
      result = self._result(cmd, args, await self._run(alias_cmd, args))
    except Exception as e:
      result = self._result(cmd, args, f"Error: {e}", error=True)

    self.results.append(result)
    return result

  def _result(self, cmd: str, args: list[str], text, error=False):
    return { "cmd": cmd, "args": args, "res": "!ok" if error else "ok", "result": text }


