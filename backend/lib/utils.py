import sys
import json
import time
import inspect

from uuid import uuid4

from pathlib import Path
from pydantic import BaseModel
from importlib import import_module
from typing import Any, Callable, Union
from importlib import util as importlib_util

from fastapi import WebSocket, HTTPException

from fastapi.responses import FileResponse
from starlette.websockets import WebSocketState



# Check if func is coroutine
def is_coro(func: Any):
  return inspect.iscoroutinefunction(func)

#  Open file and load config 
def load_config(path: Path | str, _type: str = "json") -> dict[str, Any]:
  with open(path, "r") as file:
    if _type == "json":
      return json.load(file)
    else:
      return file.read()

# Parse config object with pydantic model 
def parse_config(config: dict[str, Any] | str, model_obj: Any, parse_type: str = "json", fallback: Any = None):
  try:
    config = load_config(config) if isinstance(config, (str, Path)) else config
    return model_obj(**config)
  except Exception as e:
    if fallback is None:
      raise e

  return model_obj(**fallback)

# Check if WebSocket connected
def is_websocket_connected(ws: WebSocket) -> bool:
  return ws.client_state == WebSocketState.CONNECTED

# Create dirs
def mkdir(path: str | Path) -> Path:
  path = Path(path)
  path.mkdir(parents=True, exist_ok=True)
  return path

# FileResponse
def file_response(base: Path | str, *paths: tuple[Path | str, ...]) -> FileResponse:
  base = Path(base).resolve()
  full_path = base.joinpath(*paths).resolve()

  if not full_path.is_relative_to(base):
    raise HTTPException(status_code=403, detail="Forbidden path")
  
  if not full_path.is_file():
    raise HTTPException(status_code=404, detail="File not found")

  return FileResponse(full_path)

# Checks if file is safe path
def is_safe_path(base: str | Path, *paths: tuple[Path | str, ...]) -> bool:
  base = Path(base).resolve()
  full_path = base.joinpath(*paths).resolve()
  
  return full_path.is_relative_to(base)

# Import module
def import_relative_module(path: str, name: str) -> Any:
  return import_module(path, name)

# import python module file
def dynamic_import(module_name: str, file_path: str, cache: bool = False) -> Any:
  if module_name in sys.modules:
    return sys.modules[module_name]

  file_path = Path(file_path).resolve()
  if not file_path.is_file():
    raise FileNotFoundError(f"File '{file_path}' not found.")

  spec = importlib_util.spec_from_file_location(module_name, str(file_path))
  if not spec or not spec.loader:
    raise ImportError(f"Could not load module from '{file_path}'")

  module = importlib_util.module_from_spec(spec)
  if cache:
    sys.modules[module_name] = module

  spec.loader.exec_module(module)
  return module

# Get item in list return fallback if not found
def get_item(lst: list, index: int, fallback: Any = None):
  try:
    return lst[index]
  except IndexError:
    return fallback

def generate_timestamp() -> int:
  return int(time.time() * 1000)

def generate_uuid():
  return uuid4().hex

def args_match_function(
  func,
  *args,
  check_types: bool = False,
  **kwargs
) -> tuple[bool, str | None]:
  """
  Validate whether args/kwargs match a function signature.
  
  Returns:
      (True, None) on success
      (False, error_message) on failure
  """
  try:
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()
  except TypeError as e:
    return False, str(e)

  if check_types:
    for name, value in bound.arguments.items():
      param = sig.parameters[name]
      ann = param.annotation

      if ann is inspect.Parameter.empty:
        continue

      if not isinstance(value, ann):
        return False, (
          f"Argument '{name}' must be {ann.__name__}, "
          f"got {type(value).__name__}"
        )

  return True, None

