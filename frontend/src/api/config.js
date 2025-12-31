import axios from "axios";
const { protocol, hostname, port } = window.location;

// Default Theme
export const DEFAULT_THEME = "dracula";

// will set in .env later
const DEV = true;

// Build base origin (includes port if present)
const origin = protocol + "//" + hostname + (port ? `:${port}` : "");

// API URL
export const API_URL = DEV ? "http://localhost:8000" : origin;

// WS URL
export const WS_URL = DEV
  ? "ws://localhost:8000"
  : (protocol === "https:" ? "wss://" : "ws://") +
    hostname +
    (port ? `:${port}` : "") +
    "/ws";

// axios instance
export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, //
  headers: {
    Accept: "application/json"
  }
});

// RESPONSE INTERCEPTOR
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status;

    if (status === 401) {
      // Optional: clear auth data
      localStorage.removeItem("escapy_token");
      sessionStorage.clear();

      // Redirect to login
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
      return;
    }

    return Promise.reject(error);
  }
);

// ERROR HANDLER for request
export function handleError(error) {
  const message =
    error.response?.data?.detail ||
    error.response?.data?.message ||
    error.message ||
    "Unknown error";

  console.error(message);

  throw new Error(message);
}
