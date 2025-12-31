import bcrypt
from pydantic import BaseModel

from fastapi import HTTPException

from lib.utils import generate_uuid



class AuthConfigModel(BaseModel):
  access_key: str
  secret: str

class Auth:
  def __init__(self):
    # Access Admin
    self._config = AuthConfigModel(**{
      "access_key": "1234",
      "secret": generate_uuid()
    })

    self._password = self._config.access_key + self._config.secret
    self.token = bcrypt.hashpw(self._password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

  def generate_token(self, access_key: str) -> str:
    if access_key == self._config.access_key:
      return self.token

    raise HTTPException(status_code=404, detail="Invalid Access Key")

  def check_token(self, token: str):
    if token == token:
      return True
    
    return False
