from typing import Any
from fastapi import WebSocket

from lib.utils import is_websocket_connected



# Client conncetions
class Connection:
  def __init__(self, websocket: WebSocket) -> None:
    self.websocket: WebSocket = websocket
  
  # Main function
  async def send_json(self, data: Any) -> None:
    if not is_websocket_connected(self.websocket):
      return
    try:
      await self.websocket.send_json(data)
    except Exception as e:
      print("Error send ws message reason:", e)

  # Send event to client 
  async def send_event(self, event: str, payload: Any):
    await self.send_json({
      "event": event,
      "payload": payload
    })

# Client connections
class Connections:
  def __init__(self) -> None:
    self._active = set() # Active 
  
  def get_active_count(self):
    return len(self._active)
  
  def add(self, websocket: WebSocket) -> Connection:
    connection = Connection(websocket)
    self._active.add(connection)
    
    print(f"[+] Connection: {websocket} Active: {len(self._active)}")

    return connection

  def remove(self, connection: Connection) -> None:
    self._active.discard(connection)

    print(f"[-] Disconnected: {connection.websocket} Active: {len(self._active)}")

  async def broadcast(self, data: Any) -> None:
    for connection in self._active:
      await connection.send_json(data)

  async def broadcast_event(self, event: str, payload: Any) -> None:
    await self.broadcast({ "event": event, "payload": payload })
