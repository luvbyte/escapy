from fastapi import APIRouter, Depends, HTTPException, Request

from core.utils import ESException, get_escapy


# Router /module
router = APIRouter(tags=["Module"])



# Get all available modules list
@router.get("/list")
def get_modules_list(escapy=Depends(get_escapy)):
  try:
    return escapy.get_modules_list()
  except Exception as e:
    raise ESException(e)


# Get module options
@router.get("/options")
def get_module_options(name: str, escapy=Depends(get_escapy)):
  try:
    return escapy.get_module_options(name)
  except Exception as e:
    raise ESException(e)


# Module public files
@router.get("/public/{name}/{path:path}")
def get_module_public_file(name: str, path: str, escapy=Depends(get_escapy)):
  try:
    module = escapy.tasks.modules.get_module(name)

    return module.get_public_file(path)
  except Exception as e:
    raise ESException(e)

