import { api, handleError } from "./config";

// TaskInfo
export async function fetchInfo() {
  try {
    const { data } = await api.get("/info");

    return data;
  } catch (err) {
    handleError(err);
  }
}

// healthCheck
export async function healthCheck() {
  try {
    const { data } = await api.get("/health");

    return data;
  } catch (err) {
    handleError(err);
  }
}
