/* ===============================
   Task ID
================================ */
function getTaskIdFromUrl() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  return parts[2] ?? null;
}

const taskID = getTaskIdFromUrl();

/* ===============================
   WebSocket setup
================================ */
const protocol = location.protocol === "https:" ? "wss" : "ws";
const wsUrl = `${protocol}://${location.host}/task/${taskID}`;

const $statusText = $("#status-text");
const $console = $("#console");

let ws = null;
let reconnecting = false;
let reconnectDelay = 2000;

/* ===============================
   Scroll helpers
================================ */
const isUserAtBottom = () => {
  const el = $console[0];
  if (!el) return true;

  const threshold = 20;
  return el.scrollHeight - el.scrollTop - el.clientHeight <= threshold;
};

const scrollToBottom = () => {
  const el = $console[0];
  if (!el) return;

  el.scrollTop = el.scrollHeight;
};

/* ===============================
   Message handling
================================ */
const appendMessage = (message, scroll = false) => {
  const shouldScroll = scroll || isUserAtBottom();

  let content;
  switch (message.type) {
    case "html":
      content = sanitizeHTML(message.message);
      $console.append($("<div>").append(content));
      break;

    case "raw_html":
      $console.append(message.message);
      break;
  
    case "text":
    default:
      $console.append($("<p>").text(message.message));
      break;
  }

  if (shouldScroll) {
    scrollToBottom();
  }
};
/* ===============================
   Fetch message history
================================ */
const fetchMessages = async () => {
  const res = await fetch("/task/messages?task_id=" + taskID);
  const messages = await res.json();

  $console.empty();

  messages.forEach(message => {
    appendMessage(message, true);
  });
};

/* ===============================
   Task metadata
================================ */
function updateTaskMeta(meta) {
  $("#status-task-name").text(meta.name);
  $("#status-task-id").text(meta.id);
  $("#status-task-module").text(meta.module.name);
  $("#status-task-created_at").text(formatTimestamp(meta.created_at));
  $("#status-task-status").text(meta.status_text);
}

/* ===============================
   Event routing
================================ */
function onEvent(event, payload) {
  switch (event) {
    case "task-status-update":
      updateTaskMeta(payload);
      break;
    case "task-message":
      appendMessage(payload.message);
      break;
    case "eval":
      eval(payload.code ?? "");
      break;
  }
}

/* ===============================
   Send event
================================ */
function sendEvent(event, payload = {}) {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;

  ws.send(
    JSON.stringify({
      event,
      payload
    })
  );
}

/* ===============================
   WebSocket connection
================================ */
const connect = () => {
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    reconnecting = false;

    console.log("ws: connected");
    $statusText.text("connected");

    fetchMessages();
  };

  ws.onmessage = event => {
    const data = JSON.parse(event.data);
    if (data?.event && data?.payload) {
      onEvent(data.event, data.payload);
    }
  };

  ws.onclose = () => {
    $statusText.text("closed");
    attemptReconnect();
  };

  ws.onerror = () => {
    $statusText.text("error");
    ws.close();
  };
};

/* ===============================
   Visibility heartbeat
================================ */
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    sendEvent("ping");

    if (!ws || ws.readyState === WebSocket.CLOSED) {
      connect();
    }
  }
});

/* ===============================
   Reconnect logic
================================ */
function attemptReconnect() {
  if (reconnecting) return;

  reconnecting = true;
  $statusText.text("Reconnecting...");

  setTimeout(() => {
    connect();
  }, reconnectDelay);
}

/* ===============================
   DOM Ready
================================ */
$(() => connect());

/* ===============================
   Security
================================ */
function sanitizeHTML(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_ATTR: ["class", "style", "href", "src", "alt", "title"],
    ALLOWED_TAGS: [
      "pre",
      "div",
      "span",
      "p",
      "b",
      "i",
      "u",
      "strong",
      "em",
      "ul",
      "ol",
      "li",
      "br",
      "img",
      "a",
      "h1",
      "h2",
      "h3"
    ],
    FORBID_TAGS: ["script", "iframe", "object", "embed"],
    FORBID_ATTR: ["onerror", "onclick", "onload"]
  });
}

/* ===============================
   Timestamp formatting
================================ */
function formatTimestamp(timestamp) {
  if (!timestamp) return "";

  const now = new Date();
  const date = new Date(timestamp);
  const diffMs = now - date;

  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  if (diffSec < 60) return diffSec <= 1 ? "just now" : `${diffSec} seconds ago`;
  if (diffMin < 60) return `${diffMin} min ago`;
  if (diffHour < 24) return `${diffHour} hours ago`;

  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
  ];
  const month = months[date.getMonth()];
  const day = date.getDate();

  let hour = date.getHours();
  const minute = String(date.getMinutes()).padStart(2, "0");
  const ampm = hour >= 12 ? "PM" : "AM";
  hour = hour % 12 || 12;

  const timeStr = `${hour}:${minute} ${ampm}`;
  const year = date.getFullYear();
  const thisYear = now.getFullYear();

  return year === thisYear
    ? `${month} ${day} at ${timeStr}`
    : `${year} ${month} ${day} at ${timeStr}`;
}
