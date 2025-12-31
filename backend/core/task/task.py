import asyncio
from uuid import uuid4
from pathlib import Path

from typing import List, Any, Literal

from core.modules import Module, TaskModule
from core.connections import Connections
from core.storage import Storage, TaskStorage

from core.watcher import ScheduledTask

from lib.events import Events
from lib.utils import file_response, generate_timestamp, generate_uuid, is_safe_path, is_coro, args_match_function

from .shell import TaskShell
from .dashboard import Dashboard
from .config import TaskConfig


class BaseMessage:
  def __init__(self, message):
    self.id: str = generate_uuid()
    self.timestamp: int = generate_timestamp()
    
    self.message: str = message
  
  @property
  def _data(self) -> dict[str, str,]:
    return {
      "id": self.id,
      "timestamp": self.timestamp,
      "message": self.message
    }

class Message(BaseMessage):
  def __init__(self, message, msg_type: str):
    super().__init__(message)

    self.type = msg_type
  
  @property
  def data(self):
    return {
      "type": self.type,
      **self._data
    }

class Log(BaseMessage):
  def __init__(self, message, level: str):
    super().__init__(message)

    self.level = level
  
  @property
  def data(self):
    return {
      "level": self.level,
      **self._data
    }

class Alert(BaseMessage):
  def __init__(self, message, priority: str):
    super().__init__(message)

    self.priority = priority
  
  @property
  def data(self):
    return {
      "priority": self.priority,
      **self._data
    }


# Task
class Task:
  def __init__(self, name: str, config, module: Module, connections: Connections, storage: Storage):
    self.name: str = name
    self.id: str = uuid4().hex
    # module object
    self.module: Module = module # Global Module Object
    # Events
    self.events: Events = Events()
    # Task Storage Object
    self.storage: TaskStorage = storage.create_task_storage(self.id)
    # Client connections
    self.client_connections: Connections = connections
    # Task + Module config
    self.config: TaskConfig = TaskConfig(config, self.module.get_options())
    # Task Module (unique)
    self.task_module: TaskModule = module()
    # connections - dashboard
    self.connections: Connections = Connections()
    # dashboard 
    self.dashboard: Dashboard = Dashboard(self)

    # Task Shell
    self.shell: TaskShell = TaskShell(self)

    # Messages
    self.messages: list[Message] = []
    # Alerts
    self.alerts: list[Alert] = []
    # Logs
    self.logs: list[Log] = []
    # Run counts
    self.runs_count: int = 0

    # Task Schedule if selected
    self.schedule: ScheduledTask = None

    # Can Stop - from module 
    self.can_stop: bool = True

    # Task Options
    # Can run only once
    self.once: bool = self.config.once
    # Public run signal
    self.signal: str | None = self.config.signal 

    # Created 
    self.created_at: int = generate_timestamp()
    # Last completed timestamp
    self.completed_at: int | None = None

    # Status
    self.completed: bool = False
    # 2 - created | 3 - started | 4 - success 
    # 6 - Error | 8 - stopped
    self.status_code: int = 2  # TODO create enum
    # Task Module Runtime Error object
    self._error: Exception = None

  @property   # is running
  def is_running(self) -> bool:
    return self.status_code == 3

  @property   # Get Error as text
  def error(self) -> str | None:
    return str(self._error) if self._error else None

  @property # task status in text
  def status_text(self) -> str:
    if self.status_code == 2:
      return "Created"
    elif self.status_code == 3:
      return "Started"
    elif self.status_code == 4:
      return "Success"
    elif self.status_code == 6:
      return "Error"
    elif self.status_code == 8:
      return "Stopped"
    elif self.status_code == 9:
      return "Deleted"

    return "Unknown"

  @property # Task meta
  def meta(self) -> dict:
    return {
      "id": self.id,
      "name": self.name,
      "module": self.module.meta,

      "created_at": self.created_at,
      "completed_at": self.completed_at, # null | str
      
      "error": self.error,
      "completed": self.completed,
      "status_code": self.status_code,
      "status_text": self.status_text,

      "schedule": self.schedule.meta if self.schedule else None,

      "once": self.once,
      "can_stop": self.can_stop
    }

  # Init Task Async
  async def init(self) -> None:
    await self.dashboard.init()

    self.storage.save_meta(self.meta)

    # Add message
    await self.log("Task Intialized")

  # Add Message
  # message: text
  # msg_type: text | html | unsafe_html
  async def message(self, message: str, msg_type: str = "html") -> Message:
    msg = Message(message, msg_type)

    self.messages.append(msg)
    # Broadcast message to all clients
    await self.broadcast_event("task-message", { "message": msg.data, "taskID": self.id })

    return msg

  # Add Alert
  # message: text
  # priority: info | error | warning | success
  async def alert(self, message, priority="info") -> Alert:
    alert = Alert(message, priority)

    self.alerts.append(alert)
    await self.broadcast_event("task-alert", { "taskID": self.id, "alert": alert.data })
    
    return alert

  # Add Log
  # message: string
  # level: info | error | warning | success
  async def log(self, message, level="info") -> Log:
    log = Log(message, level)

    self.logs.append(log)
    await self.broadcast_event("task-log", { "taskID": self.id, "log": log.data })

  # on new dashboard websocket connection
  async def add_connection(self, websocket):
    connection = self.connections.add(websocket)
  
    await self.events.emit_async("ws:connect", connection)
    # Task Status 
    await connection.send_event("task-status-update", self.meta)

    return connection

  # on dashboard websocket connection disconnect
  async def remove_connection(self, connection):
    self.connections.remove(connection)

    await self.events.emit_async("ws:disconnect", connection)

  # on dashboard websocket websocket data
  async def on_data(self, connection, data):
    await self.events.emit_async("ws:data", connection, data)

  # MAIN ENTRY broadcast for all connections
  async def broadcast(self, data, clients=True, key: str | None = None):
    # Checks permission for dahsboard clients
    if key and self.dashboard.check_access_key(key):
      await self.connections.broadcast(data)

    if clients:
      await self.client_connections.broadcast(data)

  # Broadcast event
  # For key checking access key on dashboard messages
  async def broadcast_event(self, event, payload, clients=True):
    await self.broadcast({
      "event": event, "payload": payload
    }, key=event, clients=clients)

  # main run 
  async def __run(self):
    # Updating state variables
    self.completed_at = None
    self.status_code = 3
    self.completed = False
    self.runs_count += 1

    # Broadcast to clients & dashboard connections
    await self.log("Task Started")
    await self.broadcast_event("task-status-update", self.meta)
    # Setting status
    # Run Module 
    try:
      # Start task
      await self.task_module.run(self.dashboard, self.config.options)
      
      # Log
      await self.log("Task Successfull", "success")

      # If stopped 
      if self.status_code != 8:
        # Success
        self.status_code = 4

    except Exception as e:
      self._error = e
  
      await self.log(f"Task Error: {e}", "error")
      await self.dashboard.print_error(e)

      # If error
      self.status_code = 6
    finally:
      # Task Completed
      self.completed_at = generate_timestamp()
      self.completed = True
    
    await self.log("Task Completed")
    # Broadcast to clients conncetions 
    await self.broadcast_event("task-status-update", self.meta)

  # task run checks and starts here
  async def run(self) -> None:
    if self.is_running:
      raise Exception("Task already running")

    if self.once and self.completed:
      raise Exception("Can't run task more than once")

    # Task
    asyncio.create_task(self.__run())

  # On schedule run
  async def _schedule_run(self) -> None:
    # Log
    await self.log("Task starting from scheduler")
    await self.run()

  # File Response - dashboard
  def dashboard_file(self, path) -> Path:
    return self.dashboard._file(path)

  # Stop Task
  async def stop(self, force: bool = False) -> None:
    if not self.can_stop and not force:
      raise Exception("Task Unstopabble!!!")
    self.status_code = 8
    await self.task_module.stop()
    # Log
    await self.log("Task force stopped" if force else "Task Stopped", "warning")
  
  # Force stop task
  async def force_stop(self):
    await self.stop(True)

  # Backup task - can restore
  async def backup(self):
    pass
  
  # Reset task states and messages
  async def reset(self):
    self.force_stop()

    self.messages.clear()
    self.logs.clear()
    self.alerts.clear()
    
    self.status_code = 2
    self.runs_count = 0
    # Status
    self.completed: bool = False
    self.completed_at = None

    self._error = None
    
    # Updated event
    await self.broadcast_event("task-status-update", self.meta)

  # Task Delete
  async def delete(self):
    await self.force_stop()
    await self.backup()

    self.status_code = 9
    
    await self.broadcast_event("task-delete", self.meta)

  # ------- Getters
  def get_messages(self) -> list[Message]:
    return [msg.data for msg in self.messages]
  
  def get_alerts(self) -> list[Alert]:
    return [msg.data for msg in self.alerts]

  def get_logs(self) -> list[Log]:
    return [msg.data for msg in self.logs]


# GET FULL TASK INFO for task info tab
# Make sure its in same pattern to render correctly
# heading: { name: value }
def get_full_task_info(task: Task):
  return {
    # Meta
    "about": {
      # Task About Basic information
      "name": task.name,
      "Using": task.module.name,
      "signal": task.signal or "-"
    },
    "counts": {
      "connections": task.connections.get_active_count(),
      "clients": task.client_connections.get_active_count(),
      "messages": len(task.messages),
      "alerts": len(task.alerts),
      "logs": len(task.logs),
      "runs": task.runs_count
    }
  }

