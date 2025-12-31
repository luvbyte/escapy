import inspect
from fastapi import Request, HTTPException
from typing import List, Any, Literal

from .errors import ESError


class ESException(HTTPException):
  def __init__(self, err, status_code=404, detail=None):
    super().__init__(status_code=status_code, detail=detail or str(err))

def get_escapy(request: Request):
  escapy = request.app.state.escapy

  # token = request.headers.get("X-AUTH-TOKEN")
  token = request.cookies.get("escapy_token")

  if not token or not escapy.auth.check_token(token):
    raise HTTPException(status_code=401, detail="Unauthorized")

  return escapy
