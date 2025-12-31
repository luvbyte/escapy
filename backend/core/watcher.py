import time
import math
import asyncio

from datetime import datetime

from dataclasses import dataclass
from typing import Callable, Awaitable



class ScheduledTask:
  def __init__(
    self,
    name: str,
    interval: float,
    coro: Callable[[], Awaitable],
    next_run: float,
    remaining_runs: int,
  ):
    self.name = name
    self.interval = interval          # seconds
    self.coro = coro
    self.next_run = next_run          # monotonic time
    self.remaining_runs = remaining_runs

    # Total Runs
    self.run_counts = remaining_runs

  @property
  def meta(self):
    now = time.monotonic()
    seconds_left = max(0, math.ceil(self.next_run - now))

    # Completed
    completed = self.run_counts - self.remaining_runs

    return {
      "task": self.name,
      "interval": self.interval,
      "next": seconds_left,
      "remaining": self.remaining_runs,
      # Total runs
      "counts": self.run_counts,
      # Completed
      "completed": completed
    }

# Scheduler
class Scheduler:
  def __init__(self):
    self.tasks: list[ScheduledTask] = []
    self._stop = asyncio.Event()
    self._wakeup = asyncio.Event()

  def add_task(
    self,
    name: str,
    delay: float,
    coro: Callable[[], Awaitable],
    repeat: float | None = None,
    repeatCount: int | None = None,
  ) -> ScheduledTask:
    now = time.monotonic()
  
    task = ScheduledTask(
      name=name,
      interval=repeat or 0,
      coro=coro,
      next_run=now + delay,
      remaining_runs=repeatCount or 1,
    )

    self.tasks.append(task)
    self._wakeup.set()

    print("Job added:", name, delay, repeat, repeatCount)
    
    return task
  
  # Remove Task by Name or task
  def remove_task(self, task_or_name: str | ScheduledTask) -> bool:
    """
    Remove a scheduled task by name or by ScheduledTask instance.
    Returns True if a task was removed, False otherwise.
    """
    removed = False

    for task in self.tasks[:]:
      if task is task_or_name or task.name == task_or_name:
        self.tasks.remove(task)
        removed = True
        
        break

    if removed:
      # Wake up the scheduler to recalculate next_run timing
      self._wakeup.set()
    
    print("Task removed from scheduler : ", task_or_name)
    return removed

  async def run(self):
    while not self._stop.is_set():

      if not self.tasks:
        self._wakeup.clear()
        await self._wakeup.wait()
        continue
  
      now = time.monotonic()
  
      for task in self.tasks[:]:
        if task.next_run <= now:
          asyncio.create_task(self._run_task(task))
  
          # Decrement remaining runs if finite
          if task.remaining_runs is not None:
            task.remaining_runs -= 1
  
          # Decide whether to reschedule
          if task.interval > 0 and (task.remaining_runs is None or task.remaining_runs > 0):
            task.next_run = now + task.interval
          else:
            self.tasks.remove(task)
  
      if not self.tasks:
        continue
  
      next_time = min(t.next_run for t in self.tasks)
  
      self._wakeup.clear()
      try:
        await asyncio.wait_for(
          self._wakeup.wait(),
          timeout=max(0, next_time - time.monotonic()),
        )
      except asyncio.TimeoutError:
        pass

  async def _run_task(self, task: ScheduledTask):
    try:
      print(f"Running {task.name}")
      await task.coro()
    except Exception as e:
      print(f"Task {task.name} failed:", e)

  def stop(self):
    self._stop.set()
    self._wakeup.set()

