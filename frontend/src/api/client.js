import { WS_URL } from "./config.js";

// WebSocket
let ws = null;
let reconnecting = false; // Reconnect state
let reconnectDelay = 1000; // starting 1 second

// WebSocket message events callbacks
const messageCallbacks = [];
// Websocket task- event callbacks
const taskMessageCallbacks = [];

// Connect WebSocket
export const connect = () => {
  if (ws && ws.readyState === WebSocket.OPEN) return; // Already connected

  console.log("Connecting ws: ", WS_URL);
  // connting ws
  ws = new WebSocket(WS_URL + "/client");

  // Connection open
  ws.onopen = e => {
    console.log("WebSocket Connected!!!");
    reconnecting = false;
    reconnectDelay = 2000;
  };

  // Connection close
  ws.onclose = () => {
    console.log("WebSocket Disconnected!!!");
    attemptReconnect();
  };

  // On error
  ws.onerror = err => {
    console.log("WebSocket Error: ", err);
    ws?.close();
  };

  ws.onmessage = e => {
    const data = JSON.parse(e.data);

    // emiting callbacks
    messageCallbacks.forEach(callback => {
      callback(data);
    });

    // Callbacks which starts with task-
    if (data.event.startsWith("task-")) {
      // emiting callbacks
      taskMessageCallbacks.forEach(callback => {
        callback(data);
      });
    }
  };
};

// Attempt to Reconnect
function attemptReconnect() {
  if (reconnecting) return;
  reconnecting = true;

  console.log(`Reconnecting in ${reconnectDelay / 1000}s...`);

  setTimeout(() => {
    console.log("Reconnect attempt...");
    connect();
    // increase delay by 2 - untill max of 8 seconds
    reconnectDelay = Math.min(reconnectDelay * 2, 8000);
  }, reconnectDelay);
}

// send heartbeat message for ws close event
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    console.log("User returned");

    // ping event
    sendEvent("ping");

    if (!ws || ws.readyState === WebSocket.CLOSED) {
      console.log("Reconnecting WebSocket after visibility change...");
      connect();
    }
  }
});

// on any message
export function onMessage(callback) {
  messageCallbacks.push(callback);
}

// of any mesaage
export function offMessage(callback) {
  const index = messageCallbacks.indexOf(callback);
  if (index !== -1) {
    messageCallbacks.splice(index, 1);
  }
}

// on any message
export function onTaskMessage(callback) {
  taskMessageCallbacks.push(callback);
}

// of any mesaage
export function offTaskMessage(callback) {
  const index = taskMessageCallbacks.indexOf(callback);
  if (index !== -1) {
    taskMessageCallbacks.splice(index, 1);
  }
}

// send json event
export function sendEvent(event, payload = {}) {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    console.warn("WebSocket not ready — buffering message");
    attemptReconnect();
    return;
  }
  ws.send(
    JSON.stringify({
      event,
      payload
    })
  );
}
