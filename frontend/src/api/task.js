import { api, handleError, API_URL } from "./config";
import axios from "axios";

// Get task info
export async function fetchTaskInfo(taskID) {
  try {
    const { data } = await api.get("/task/info", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

export async function getTaskModuleOptions(taskID) {
  try {
    const { data } = await api.get("/task/module/options", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

export async function updateTaskModuleOptions(taskID, options) {
  try {
    const { data } = await api.post("/task/module/options", {
      task_id: taskID,
      options
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Fetch Task Messages
export async function fetchTaskMessages(taskID) {
  try {
    const { data } = await api.get("/task/messages", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(e);
  }
}

// Fetch Task Alerts
export async function fetchTaskAlerts(taskID) {
  try {
    const { data } = await api.get("/task/alerts", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Fetch Task Logs
export async function fetchTaskLogs(taskID) {
  try {
    const { data } = await api.get("/task/logs", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Get Task File
export async function getTaskFileList(taskID, path, hiddenFiles = true) {
  try {
    const { data } = await api.get("/task/file/list", {
      params: {
        path: path,
        task_id: taskID,
        hidden_files: hiddenFiles
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Delete task files
export async function deleteTaskFiles(taskID, files) {
  try {
    const { data } = await api.delete("/task/file", {
      data: {
        task_id: taskID,
        files: files
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Get task file blob
export async function getTaskFileBlob(taskID, path) {
  try {
    const response = await api.get("/task/file", {
      params: {
        path: path,
        task_id: taskID
      },
      responseType: "blob"
    });

    return {
      blob: response.data,
      mimeType: response.headers["content-type"]
    };
  } catch (err) {
    handleError(err);
  }
}

// send task command
export async function runTaskShellCommand(taskID, command) {
  try {
    const { data } = await api.post("/task/shell", {
      id: taskID,
      command: command
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Get active tasks list
export async function getActiveTasks() {
  try {
    const { data } = await api.get("/task/list");

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Task Keys
export async function fetchTaskAccessKeys(taskID) {
  try {
    const { data } = await api.get("/task/access-keys", {
      params: { task_id: taskID }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

export async function updateTaskAccessKeys(taskID, keys) {
  try {
    const { data } = await api.post("/task/access/key", {
      task_id: taskID,
      keys: keys
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// create & run task
export async function runTask(name, module, config) {
  try {
    const { data } = await api.post("/task/create", {
      name,
      module,
      config
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// Delete task
export async function deleteTask(taskID) {
  try {
    const { data } = await api.delete("/task/delete", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

export async function resetTask(taskID) {
  try {
    const { data } = await api.get("/task/reset", {
      params: {
        task_id: taskID
      }
    });

    return data;
  } catch (err) {
    handleError(err);
  }
}

// TaslDashUrL
export const getDashboardURL = task_id => {
  return API_URL + `/task/dashboard/${task_id}/index.html`;
};

// Get Task File URL
export const getFileURL = (taskID, path, preview = false) => {
  return (
    API_URL + `/task/file?task_id=${taskID}&path=${path}&preview=${preview}`
  );
};
