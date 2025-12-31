from pathlib import Path
from lib.utils import parse_config

from .auth import Auth
from .tasks import Tasks
from .storage import Storage
from .models import EScapyConfigModel
from .connections import Connections, Connection


# Escapy Config
class ESConfig:
  def __init__(self, config_path: str) -> None:
    self._config = parse_config(config_path, EScapyConfigModel, fallback={})
    
    self.web_path = Path("web/dist").resolve()

# Core Escapy
class EScapy:
  def __init__(self, config: str = "config.json") -> None:
    self.config = ESConfig(config)
    self.storage = Storage()
    self.auth = Auth()
    # client connections 
    self.connections = Connections()
    # Tasks
    self.tasks = Tasks(self.connections, self.storage)
  
  # Lifecycle start
  async def on_start(self) -> None:
    await self.tasks.init()

  # Lifecycle stop
  async def on_stop(self) -> None:
    await self.tasks.on_close()

  # Get escapy basic info
  def get_info(self) -> dict:
    tasks_list = self.tasks._running
    return {
      "tasks_count": len(tasks_list),
      "installed_modules_count": len(self.tasks.modules._modules),
      "completed_tasks_count": len([t for t in tasks_list.values() if t.completed])
    }
  
  # Returns active tasks 
  def get_active_tasks(self) -> list:
    return self.tasks.get_active_tasks()
  
  # Get modules list
  def get_modules_list(self) -> list:
    return self.tasks.get_modules_list()

  # Get Task config # Un
  def get_task_config(self, task_id: str):
    return self.tasks.get_task_config(task_id)
  
  # Get module options 
  def get_module_options(self, name: str):
    return self.tasks.get_module_options(name)
  
  # Create Task
  async def create_task(self, name: str, module: str, config):
    return await self.tasks.create_task(name, module, config)
  
  # Get task dashboard file
  def task_dashboard(self, task_id: str, path: str):
    return self.tasks.task_dashboard(task_id, path)
  
  # On task client connect / dashboard
  async def on_task_connect(self, task_id, websocket):
    # create connection
    task = self.tasks.get_task(task_id)
    connection = await task.add_connection(websocket)

    return (task, connection)
  
  # On task client disconnect
  async def on_task_disconnect(self, task, connection):
    await task.remove_connection(connection)
  
  # On task client data
  async def on_task_data(self, task, connection, data):
    await task.on_data(connection, data)
  
  # Client connections
  async def on_client_connect(self, websocket):
    return self.connections.add(websocket)
  
  # Client Disconnect
  async def on_client_disconnect(self, connection):
    self.connections.remove(connection)
  
  # On client data
  async def on_client_data(self, connection, data):
    pass
  
  # Delete Task 
  async def reset_task(self, task_id: str):
    await self.tasks.reset_task(task_id)

  async def delete_task(self, task_id: str):
    await self.tasks.delete_task(task_id)

