import json

from pathlib import Path
from lib.utils import mkdir



# Task Storage
class TaskStorage:
  def __init__(self, path: Path, task_id: str):
    self._storage_path = path
    # Task storage path
    self.path = mkdir(self._storage_path / task_id)
    # Files Path
    self.files_path = mkdir(self.path / "files")
    
    # cache image files
    self.cache_images = True

  # Clear storage
  def clear(self):
    pass # delete files 

  def save(self, filename: str, data, mode="w"):
    with open(self.path / filename, mode) as file:
      file.write(data)

  def save_json(self, filename, data, indent=2):
    with open(self.path / f"{filename}.json", "w", encoding="utf-8") as file:
      json.dump(data, file, indent=indent, ensure_ascii=False)

  # Save Meta File
  def save_meta(self, meta):
    self.save_json("meta", meta)

# Storage
class Storage:
  def __init__(self):
    self.path: Path = mkdir("../storage").resolve()

  def create_task_storage(self, task_id):
    return TaskStorage(self.path, task_id)
