<template>
  <div
    class="fullscreen flex flex-col gap-2 overflow-hidden"
    :class="{ 'fixed inset-0 p-2 z-20 bg-base-100': fullScreen }"
  >
    <!-- Statusbar -->
    <div v-if="!uploadProgress" class="flex items-center gap-1">
      <!-- Add Files Button -->
      <label class="btn btn-sm btn-soft btn-primary">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 1024 1024"
        >
          <path
            fill="currentColor"
            d="M854.6 288.6L639.4 73.4c-6-6-14.1-9.4-22.6-9.4H192c-17.7 0-32 14.3-32 32v832c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V311.3c0-8.5-3.4-16.7-9.4-22.7M790.2 326H602V137.8zm1.8 562H232V136h302v216a42 42 0 0 0 42 42h216zM544 472c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v108H372c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h108v108c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V644h108c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8H544z"
          />
        </svg>
        <input type="file" multiple class="hidden" @change="handleFiles" />
      </label>
      <!-- Upload Button -->
      <button
        class="btn btn-sm btn-secondary btn-soft disabled:opacity-50"
        @click="uploadFiles"
        :disabled="!files.length || uploadProgress > 0"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <g
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          >
            <path
              fill="currentColor"
              fill-opacity="0"
              stroke-dasharray="20"
              stroke-dashoffset="20"
              d="M12 15h2v-6h2.5l-4.5 -4.5M12 15h-2v-6h-2.5l4.5 -4.5"
            >
              <animate
                attributeName="d"
                begin="0.5s"
                dur="1.5s"
                repeatCount="indefinite"
                values="M12 15h2v-6h2.5l-4.5 -4.5M12 15h-2v-6h-2.5l4.5 -4.5;M12 15h2v-3h2.5l-4.5 -4.5M12 15h-2v-3h-2.5l4.5 -4.5;M12 15h2v-6h2.5l-4.5 -4.5M12 15h-2v-6h-2.5l4.5 -4.5"
              />
              <animate
                fill="freeze"
                attributeName="fill-opacity"
                begin="0.7s"
                dur="0.5s"
                values="0;1"
              />
              <animate
                fill="freeze"
                attributeName="stroke-dashoffset"
                dur="0.4s"
                values="20;0"
              />
            </path>
            <path stroke-dasharray="14" stroke-dashoffset="14" d="M6 19h12">
              <animate
                fill="freeze"
                attributeName="stroke-dashoffset"
                begin="0.5s"
                dur="0.2s"
                values="14;0"
              />
            </path>
          </g>
        </svg>
      </button>
      <!-- Expand -->
      <div class="flex-1"></div>
      <!-- FullScreen Button -->
      <button
        class="btn btn-sm btn-secondary btn-soft disabled:opacity-50"
        @click="fullScreen = !fullScreen"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M3 21v-5h2v3h3v2zm13 0v-2h3v-3h2v5zM3 8V3h5v2H5v3zm16 0V5h-3V3h5v5z"
          />
        </svg>
      </button>
      <!-- Close Button -->
      <button
        class="btn btn-sm btn-secondary btn-soft disabled:opacity-50"
        @click="close"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z"
          />
        </svg>
      </button>
    </div>

    <!-- Upload Progress -->
    <div v-if="uploadProgress > 0" class="w-full mt-2">
      <progress
        class="progress progress-primary w-full"
        :value="uploadProgress"
        max="100"
      ></progress>

      <div class="text-xs text-center mt-1 opacity-70">
        Uploading... {{ uploadProgress }}%
      </div>
    </div>

    <!-- Current Path -->
    <div
      class="text-sm font-heading opacity-80 divider m-0 overflow-x-auto scrollbar-hide"
    >
      {{ currentPath }}
    </div>

    <!-- Files Grid -->
    <div
      v-if="files.length && !uploadProgress"
      class="grid grid-cols-4 gap-4 pb-2 overflow-y-auto overflow-x-hidden"
    >
      <div
        v-for="(file, index) in files"
        :key="index"
        class="relative rounded-lg bg-base-300 text-base-content"
      >
        <!-- Image Preview -->
        <img
          v-if="file.preview"
          :src="file.preview"
          class="aspect-square object-cover rounded"
        />

        <!-- Non-image -->
        <div
          v-else
          class="aspect-square text-xs p-2 break-words text-center overflow-y-auto"
        >
          {{ file.name }}
        </div>

        <!-- Remove Button -->
        <button
          @click="removeFile(index)"
          class="absolute -top-1 -right-1 btn z-90 btn-circle btn-soft btn-error btn-xs"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { api } from "@/api/config";

  const props = defineProps({
    taskID: String,
    currentPath: String,
    close: Function
  });

  const files = ref([]);
  const uploadProgress = ref(0);

  const fullScreen = ref(false);

  // Upload Files
  async function uploadFilesBackup() {
    if (!files.value.length) return;

    const formData = new FormData();

    files.value.forEach(item => {
      formData.append("files", item.file);
    });

    formData.append("task_id", props.taskID);
    formData.append("path", props.currentPath);

    try {
      const response = await api.post("/task/file/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        onUploadProgress: progressEvent => {
          const percent = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          uploadProgress.value = percent;
          console.log("Upload progress:", percent + "%");
        }
      });

      console.log("Upload success:", response.data);

      // cleanup
      files.value.forEach(f => {
        if (f.preview) URL.revokeObjectURL(f.preview);
      });
      files.value = [];

      props.close(true); // close refresh list
    } catch (error) {
      console.error("Upload failed:", error);
    }
  }

  async function uploadFiles() {
    if (!files.value.length) return;

    const formData = new FormData();

    files.value.forEach(item => {
      formData.append("files", item.file);
    });

    formData.append("task_id", props.taskID);
    formData.append("path", props.currentPath);

    uploadProgress.value = 0;

    try {
      const response = await api.post("/task/file/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        onUploadProgress: progressEvent => {
          uploadProgress.value = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
        }
      });

      // cleanup
      files.value.forEach(f => f.preview && URL.revokeObjectURL(f.preview));
      files.value = [];

      setTimeout(() => {
        uploadProgress.value = 0;
      }, 500);

      props.close(true);
    } catch (error) {
      console.error("Upload failed:", error);
      uploadProgress.value = 0;
    }
  }

  function handleFiles(event) {
    const selected = Array.from(event.target.files);

    selected.forEach(file => {
      const isImage = file.type.startsWith("image/");
      files.value.push({
        file,
        name: file.name,
        preview: isImage ? URL.createObjectURL(file) : null
      });
    });

    event.target.value = "";
  }

  function removeFile(index) {
    const file = files.value[index];
    if (file.preview) URL.revokeObjectURL(file.preview);
    files.value.splice(index, 1);
  }
</script>
