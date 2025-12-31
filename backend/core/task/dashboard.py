import json
from pathlib import Path

from lib.utils import file_response, generate_uuid



# AccessKeys
class AccessKeys:
  def __init__(self):
    self._full_keys = {
      "task-update-status",
      "task-message",
      "task-delete",
      "task-log",
      "task-alert",
    }

    self._fixed_keys = {
      "task-message",
      "task-delete",
      "task-update-status",
    }

    self._keys = set(self._fixed_keys)

  def check(self, key: str):
    return key in self._keys

  def is_fixed_key(self, key):
    return key in self._fixed_keys

  def add(self, name: str):
    self._keys.add(name)
    return self

  def update(self, keys: list[str]):
    # Keep fixed keys, replace the rest
    self._keys = set(self._fixed_keys)
    for key in keys:
      self._keys.add(key)

  def remove(self, key):
    if not self.is_fixed_key(key):
      self._keys.discard(key)

  def get_keys(self):
    return [
      {"name": key, "active": key in self._keys}
      for key in self._full_keys
      if not self.is_fixed_key(key)
    ]


# Dashboard - html code that renders
# Uses webview for connection
class Dashboard:
  def __init__(self, task):
    self.access_keys = AccessKeys()

    self._task = task

    # dashboard files path
    self._dashboard_path = self.__get_dashboard_path()

  @property
  def module(self): # Module in use
    return self._task.module

  @property
  def storage(self):
    return self._task.storage

  async def init(self):
    pass

  # Get Dashboard Path UI
  def __get_dashboard_path(self) -> Path:
    dashboard_path = self.module.path / self.module.config.dashboard
    return dashboard_path if dashboard_path.is_dir() else Path("web/dashboard")

  # Get dashboard file
  def _file(self, path: str):
    return file_response(self._dashboard_path, path)
  
  # Get access keys 
  def get_access_keys(self):
    return self.access_keys.get_keys()
  
  # Check access key for checking if present
  def check_access_key(self, name: str):
    return self.access_keys.check(name)
  
  # Updating keys
  def update_access_keys(self, keys: list[str]):
    self.access_keys.update(keys)
  
  # Send message with msg_type: text | html | unsafe_html
  async def message(self, message: str, msg_type = "html"):
    await self._task.message(message, msg_type=msg_type)

  # Print / message - text
  async def print(self, *message, sep: str = " ", end: str = "\n"):
    await self.message(sep.join([str(msg) for msg in message]) + end, msg_type="text")

  # Print error text
  async def print_error(self, *message):
    text = " ".join([str(msg) for msg in message])
    await self.message(f"<div class='text-red-400'>ERROR: {text}</div>", msg_type="html")

  # Custom Message
  async def custom_message(self, event, message):
    if event == "print":
      await self.print(message)

  # Process output
  async def stdout(self, text, message_config):
    if isinstance(message_config, str):
      return await self.message(text, msg_type=message_config)

    # -------- Custom Message Types
    try:
      # TODO: optimize finds
      data = json.loads(text).values()
      await self.custom_message(data["es-event"], data["es-message"])
    except Exception:
      if message_config.fallback == "ignore":
        return # ignore message
      else: # add message
        await self.message(text, msg_type=message_config.fallback)

  # Process error
  async def stderr(self, text, message_config):
    await self.print_error(text)

