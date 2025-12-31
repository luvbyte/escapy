from fastapi import (
  APIRouter,
  Depends,
  HTTPException,
  UploadFile,
  File, 
  Form, 
)
from fastapi.responses import FileResponse, StreamingResponse
import zipfile
import io
import os
import shutil
from tempfile import SpooledTemporaryFile

from PIL import Image
from hashlib import md5
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
from typing import Literal, List, Any
from core.models import CreateTaskModel

from lib.utils import is_safe_path
from core.task import get_full_task_info
from core.utils import ESException, get_escapy

from fastapi.concurrency import run_in_threadpool

# For Thumbnail Generation
IMAGE_EXTENSIONS = { ".jpg", ".jpeg", ".png", ".webp" }


# Router /task
router = APIRouter(tags=["Task"])



# Task Command
class TaskCommandModel(BaseModel):
  id: str
  command: str

# Task module options update model /module/options
class TaskModuleOptionsUpdateModel(BaseModel):
  task_id: str
  options: dict[str, Any]

class TaskFilesDeleteRouteModel(BaseModel):
  task_id: str
  files: list[str]



# Get task full info
@router.get("/info")
def get_task_info(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    
    return get_full_task_info(task)
  except Exception as e:
    raise ESException(e)


# Returns Active Tasks List
@router.get("/list")
def get_active_tasks(escapy=Depends(get_escapy)):
  try:
    return escapy.get_active_tasks()
  except Exception as e:
    raise ESException(e)


# Get module options
@router.get("/module/options")
async def get_task_module_options(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)

    return task.config.get_raw_options()

  except Exception as e:
    raise
    raise ESException(e)

# Update module options
@router.post("/module/options")
async def update_module_options(payload: TaskModuleOptionsUpdateModel, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(payload.task_id)
    
    task.config.update_options(payload.options)
    
    return { "res": "ok" }

  except Exception as e:
    raise ESException(e)


# Task Messages /task/messages
@router.get("/messages")
def get_task_messages(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    return task.get_messages()
  except Exception as e:
    raise ESException(e)

# Task alerts
@router.get("/alerts")
def get_task_alerts(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    return task.get_alerts()
  except Exception as e:
    raise ESException(e)

# Task logs
@router.get("/logs")
def get_task_logs(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    return task.get_logs()
  except Exception as e:
    raise ESException(e)


# Task Dashboard WebView
@router.get("/dashboard/{task_id}/{path:path}")
def task_dashboard(task_id: str, path: str, escapy=Depends(get_escapy)):
  try:
    return escapy.task_dashboard(task_id, path)
  except Exception as e:
    raise ESException(e)


# Create Task
@router.post("/create")
async def create_task(payload: CreateTaskModel, escapy=Depends(get_escapy)):
  try:
    task_id = await escapy.create_task(payload.name, payload.module, payload.config)
    return { "task": task_id }

  except Exception as e:
    raise
    raise ESException(e)

@router.get("/reset")
async def reset_task(task_id: str, escapy=Depends(get_escapy)):
  try:
    await escapy.reset_task(task_id)

    return { "res": "ok" }

  except Exception as e:
    raise
    raise ESException(e)

@router.delete("/delete")
async def delete_task(task_id: str, escapy=Depends(get_escapy)):
  try:
    await escapy.delete_task(task_id)

    return { "res": "ok" }
  except Exception as e:
    raise
    raise ESException(e)

# Task shell command
@router.post("/shell")
async def task_command(payload: TaskCommandModel, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(payload.id)
    return await task.shell.run(payload.command)
  except Exception as e:
    raise ESException(e)


# Task Access Keys
@router.get("/access-keys")
def get_access_keys(task_id: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    # Returns all keys active, inactive
    return task.dashboard.get_access_keys()
  
  except Exception as e:
    raise
    raise ESException(e)

class UpdateAccessKeysModel(BaseModel):
  task_id: str
  keys: list[Any]

@router.post("/access/key")
def update_access_key(payload: UpdateAccessKeysModel, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(payload.task_id)
    
    task.dashboard.update_access_keys([key["name"] for key in payload.keys if key["active"]])
    return task.dashboard.get_access_keys()
  
  except Exception as e:
    raise
    raise ESException(e)

@router.get("/file")
async def task_file(task_id: str, path: str = "", preview: bool = False, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    base = task.storage.path.resolve()
    full_path = (base / path).resolve()

    # Security check
    if not is_safe_path(base, full_path):
      raise HTTPException(status_code=403, detail="Forbidden Path")

    if not full_path.exists() and full_path.is_dir():
      raise HTTPException(status_code=404, detail="Invalid Path")

    # Never generate previews from thumbnails
    if ".thumbnails" in full_path.parts:
      return FileResponse(path=full_path)

    # ---------- FILE HANDLING ----------
    if full_path.is_file():
      suffix = full_path.suffix.lower()

      if preview and suffix in IMAGE_EXTENSIONS:
        thumb_root = base / ".thumbnails"
        thumb_root.mkdir(exist_ok=True)

        rel_path = full_path.relative_to(base).as_posix()
        hash_name = md5(rel_path.encode("utf-8")).hexdigest()
        thumb_path = thumb_root / f"{hash_name}.jpg"

        if not thumb_path.exists():
          with Image.open(full_path) as img:
            img = img.convert("RGB")
            img.thumbnail((512, 512))
            img.save(thumb_path, "JPEG", quality=70, optimize=True)

        return FileResponse(thumb_path)

      return FileResponse(full_path)
  
  except Exception as e:
      raise ESException(e)


@router.get("/file/list")
async def task_file_details(task_id: str, path: str, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(task_id)
    base = task.storage.path
    full_path = base / path

    # Security check
    if not is_safe_path(base, path):
      raise HTTPException(status_code=403, detail="Forbidden Path")

    if not full_path.exists() or full_path.is_file():
      raise HTTPException(status_code=404, detail="Invalid Path")

    # ---------- DIRECTORY LISTING ----------
    def get_file_meta(path: Path):
      stat = path.stat()
      return {
        "name": path.name,
        "hash_name": md5(path.name.encode("utf-8")).hexdigest(),
        "path": str(path.relative_to(base)),
        "suffix": path.suffix,
        "is_dir": path.is_dir(),
        "is_file": path.is_file(),
        "size": stat.st_size if path.is_file() else None,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
      }
    
    return [get_file_meta(p) for p in full_path.iterdir() if not p.name.startswith(".")]
  except Exception as e:
    raise ESException(e)

# Delete task files 
@router.delete("/file")
async def delete_file(payload: TaskFilesDeleteRouteModel, escapy=Depends(get_escapy)):
  try:
    task = escapy.tasks.get_task(payload.task_id)
    base_path = task.storage.path

    # Resolve and validate paths
    to_remove: list[Path] = [
      base_path / path
      for path in payload.files
      if is_safe_path(base_path, path)
    ]

    if not to_remove:
      raise HTTPException(status_code=400, detail="No valid files to delete")

    deleted = []
    skipped = []

    for path in to_remove:
      if not path.exists():
        skipped.append(str(path))
        continue

      if path.is_file() or path.is_symlink():
        path.unlink()
      elif path.is_dir():
        shutil.rmtree(path)

      deleted.append(str(path))

    return {
      "deleted": deleted,
      "skipped": skipped,
    }

  except HTTPException:
    raise
  except Exception as e:
    raise ESException(e)


# Upload task files
@router.post("/file/upload")
async def upload_files(
  task_id: str = Form(None),
  path: str = Form(None),
  files: List[UploadFile] = File(...),
  escapy=Depends(get_escapy)
):
  task = escapy.tasks.get_task(task_id)

  # Build full path
  if not is_safe_path(task.storage.path, path):
    raise HTTPException(status_code=403, detail="Forbidden Path")

  upload_dir = task.storage.path / path
  upload_dir.mkdir(parents=True, exist_ok=True)
  
  # Saved Files
  saved_files = []

  for file in files:
    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

    saved_files.append({
      "filename": file.filename,
      "path": str(file_path)
    })

  return {
    "message": "Files uploaded successfully",
    "task_id": task_id,
    "path": path,
    "files": saved_files
  }


