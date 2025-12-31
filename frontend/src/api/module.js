import { api, handleError } from "./config";

// Get modules list
export async function getModulesList() {
  try {
    const { data } = await api.get("/module/list");

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Get module options
export async function getModuleOptions(name) {
  try {
    const { data } = await api.get("/module/options", {
      params: { name }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}
