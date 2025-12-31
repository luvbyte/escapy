from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager
from core import EScapy, __version__, __author__
from lib.utils import file_response, import_module

from core.models import LoginRequest

import os



escapy = EScapy()


@asynccontextmanager
async def lifespan(app: FastAPI):
  await escapy.on_start()
  yield
  await escapy.on_stop()


app = FastAPI(lifespan=lifespan)
app.state.escapy = escapy # Global State

# Cors
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],          # Allow all origins 
  allow_credentials=True,
  allow_methods=["*"],          # Allow all HTTP methods
  allow_headers=["*"],          # Allow all headers
)


app.mount("/static", StaticFiles(directory="web/static"), name="static")


# Dynamically loading routes
for file in os.listdir("core/routes"):
  if file.endswith(".py") and file not in ("__init__.py",):
    module_name = file[:-3]  # remove .py
    module = import_module(f"core.routes.{module_name}")

    # attach router if exists
    if hasattr(module, "router"):
      app.include_router(getattr(module, "router"), prefix=f"/{module_name}")

# Health check
@app.get("/health")
def health():
  return { 
    "status": "ok",
    "version": __version__,
    "author": __author__
  }

# Escapy Info
@app.get("/info")
def info():
  try:
    return {
      **health(),
      **escapy.get_info()
    }
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

# Token
@app.get("/token")
def generate_token(access_key: str):
  try:
    token = escapy.auth.generate_token(access_key)
    
    return { "token": token }
  except Exception as e:
    raise e

# Login Post
@app.post("/login")
def generate_auth_token(payload: LoginRequest):
  try:
    token = escapy.auth.generate_token(payload.access_key)
    
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
      key="escapy_token",
      value=token,
      httponly=True,
      max_age=60 * 60 * 24 # 1 day (optional)
    )

    return response
  except Exception as e:
    raise e

# Home / Root
@app.get("/{path:path}")
def home(path: str):
  if path == "":
    path = "index.html"
  
  return file_response(escapy.config.web_path, path)



# ws: /task/taskID - Task Monitor 
@app.websocket("/task/{task_id}")
async def on_task_connect(websocket: WebSocket, task_id: str):
  await websocket.accept()
  # Check if valid task_id

  try:
    task, connection = await escapy.on_task_connect(task_id, websocket)
  except Exception as e:
    await websocket.close(reason=str(e))
    return

  try:
    while True:
      data = await websocket.receive_json()
      await escapy.on_task_data(task, connection, data)

  except WebSocketDisconnect:
    await escapy.on_task_disconnect(task, connection)
  except Exception as e:
    print("Unknown Error: ", e)


@app.websocket("/client")
async def on_client_connect(websocket: WebSocket):
  await websocket.accept()
  # Check if valid task_id
  try:
    connection = await escapy.on_client_connect(websocket)
  except Exception as e:
    await websocket.close(reason=str(e))
    return

  try:
    while True:
      data = await websocket.receive_json()
      await escapy.on_client_data(connection, data)

  except WebSocketDisconnect:
    await escapy.on_client_disconnect(connection)
  except Exception as e:
    print("Unknown Error: ", e)



if __name__ == "__main__":
  import uvicorn
  
  uvicorn.run(app)

  