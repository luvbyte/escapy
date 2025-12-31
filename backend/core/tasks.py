import asyncio

from .task import Task
from .watcher import Scheduler
from .modules import Modules, Module



# Tasks Manager
class Tasks:
  def __init__(self, connections, storage):
    self._running: dict[str, Task] = {}
    # Tasks count id
    # self._tasks_count = 0
    # running tasks 
    self.storage = storage
    # Modules
    self.modules = Modules(self.storage)
    
    # client connections
    self.connections = connections
    # Scheduler
    self.scheduler = Scheduler()

  async def init(self):
    asyncio.create_task(self.scheduler.run())

  async def on_close(self):
    self.scheduler.stop()

  # running tasks
  def _get_active_tasks(self) -> list[str]:
    return [task.meta for task in self._running.values()]

  def get_active_tasks(self):
    return sorted(
      self._get_active_tasks(),
      key=lambda d: d.get("created_at", 0),
      reverse=True,
    )

  def get_task(self, task_id: str):
    return self._running[task_id]
  
  def get_task_config(self, task_id: str):
    return self.get_task(task_id).config

  def get_modules_list(self):
    return self.modules.get_modules_list()

  def get_module_options(self, name: str):
    return self.modules.get_module_options(name)

  async def create_task(self, name: str, module, config):
    task = Task(name, config, self.modules.get_module(module), self.connections, self.storage)
    self._running[task.id] = task

    # Init task
    await task.init()

    # Auto start prevents schedule
    if task.config.autostart:
      await task.run()
    
    # Schedule
    elif task.config.delay is not None:
      task.schedule = self.scheduler.add_task(
        task.id,
        task.config.delay,
        task._schedule_run,
        # Bot can be none based on once value in config
        task.config.repeat,
        task.config.repeat_count
      )

    # log
    await task.log("Task Created")

    return task.id

  async def delete_task(self, task_id: str):
    task = self.get_task(task_id)

    # Removing task schedukers
    self.scheduler.remove_task(task_id)
    # Deleting
    await task.delete()

    # Remove from list
    del self._running[task_id]

  async def reset_task(self, task_id: str):
    await self.get_task(task_id).reset()

  # Get Task dashboard
  def task_dashboard(self, task_id: str, path: str):
    return self.get_task(task_id).dashboard_file(path)

