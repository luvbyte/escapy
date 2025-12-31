<template>
  <div
    class="flex-1 flex flex-col text-xs overflow-hidden"
    :class="[
      fullScreen ? 'fixed inset-0 z-20 bg-base-100 fullscreen gap-2' : 'flex-1',
      { 'p-2': !imageZoom }
    ]"
  >
    <div v-if="!imageZoom">
      <div v-if="!fullScreen" class="divider m-0"></div>

      <!-- ToolBar -->
      <div class="flex gap-2 items-center">
        <div class="flex-1 flex items-center gap-1">
          <!-- Icon -->
          <FileIcon :taskID :file="activeFile" class="w-6" />
          <!-- FileName -->
          <h1
            class="font-heading text-sm opacity-80 font-bold max-w-42 truncate"
          >
            {{ activeFile.name }}
          </h1>
          <!-- Download Button -->
          <button @click="downloadFile">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M12 15.575q-.2 0-.375-.062T11.3 15.3l-3.6-3.6q-.3-.3-.288-.7t.288-.7q.3-.3.713-.312t.712.287L11 12.15V5q0-.425.288-.712T12 4t.713.288T13 5v7.15l1.875-1.875q.3-.3.713-.288t.712.313q.275.3.288.7t-.288.7l-3.6 3.6q-.15.15-.325.213t-.375.062M6 20q-.825 0-1.412-.587T4 18v-2q0-.425.288-.712T5 15t.713.288T6 16v2h12v-2q0-.425.288-.712T19 15t.713.288T20 16v2q0 .825-.587 1.413T18 20z"
              />
            </svg>
          </button>
        </div>

        <!-- Toggle FullScreen Button -->
        <button @click="fullScreen = !fullScreen">
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
        <button @click="close" class="btn btn-error btn-xs">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12z"
            />
          </svg>
        </button>
      </div>

      <div v-if="!fullScreen" class="divider m-0"></div>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" dim class="flex-1" />

    <!-- Preview -->
    <div v-show="!loading" class="flex-1 flex flex-col overflow-y-auto">
      <!-- Image -->
      <div
        v-if="renderType === 'image'"
        @click="imageZoom = !imageZoom"
        class="fullscreen flex justify-center items-center"
      >
        <img
          v-swipe="onSwipe"
          :src="objectUrl"
          class="fullscreen"
          :class="imageZoom ? 'object-cover' : 'object-contain'"
        />
      </div>

      <!-- JSON -->
      <pre v-else-if="renderType === 'json'">{{
        JSON.stringify(jsonContent, null, 2)
      }}</pre>

      <!-- Video -->
      <video
        v-else-if="renderType === 'video'"
        controls
        :src="objectUrl"
        class="fullscreen flex items-center justify-center aspect-auto"
      />

      <!-- Text -->
      <pre v-else-if="renderType === 'text'">{{ textContent }}</pre>

      <!-- Fallback -->
      <div
        v-else
        class="flex-1 text-heading flex items-center justify-center text-lg font-semibold opacity-80"
      >
        {{ errorText }}
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, computed, onBeforeMount, onBeforeUnmount } from "vue";

  import { getTaskFileBlob } from "@/api/task";

  import { IMAGE_EXTENSIONS } from "@/api/utils";

  import FileIcon from "./FileIcon.vue";
  import Loading from "@/components/utils/Loading.vue";

  // Props
  const props = defineProps({
    taskID: String,
    activeFile: Object,
    files: Array,
    close: Function
  });

  const emit = defineEmits(["update:activeFile"]);

  // File Mime Type
  const mimeType = ref(null);
  // File Blob
  const blob = ref(null);
  // File Object Url
  const objectUrl = ref(null);
  // If file is text type
  const textContent = ref(null);

  // If file is JSON Type
  const jsonContent = ref(null);

  const imageZoom = ref(false);

  // Loading state
  const loading = ref(false);
  // FullScreen
  const fullScreen = ref(false);

  // Error text works only if no file format found
  const errorText = ref(null);

  watch(
    () => props.activeFile,
    () => {
      getFile();
    },
    { immediate: true }
  );

  const imageFiles = computed(() =>
    props.files.filter(f => {
      if (!f.name) return false;
      const ext = f.name.split(".").pop().toLowerCase();
      return IMAGE_EXTENSIONS.includes(ext);
    })
  );

  const currentIndex = computed(() =>
    imageFiles.value.findIndex(f => f.path === props.activeFile.path)
  );

  function onSwipe(direction) {
    console.log(direction, imageFiles);

    if (!imageFiles.value.length) return;

    let newIndex = currentIndex.value;

    if (direction === "left") {
      newIndex++;
    } else if (direction === "right") {
      newIndex--;
    }

    // wrap around
    if (newIndex < 0) newIndex = imageFiles.value.length - 1;
    if (newIndex >= imageFiles.value.length) newIndex = 0;

    const nextFile = imageFiles.value[newIndex];
    if (!nextFile) return;

    emit("update:activeFile", nextFile);
  }

  // Get file
  async function getFile() {
    loading.value = true;

    try {
      const res = await getTaskFileBlob(props.taskID, props.activeFile.path);

      mimeType.value = res.mimeType;
      blob.value = res.blob;

      // revoke old URL if switching files
      if (objectUrl.value) {
        URL.revokeObjectURL(objectUrl.value);
      }

      objectUrl.value = URL.createObjectURL(res.blob);

      // If file is json type
      if (mimeType.value === "application/json") {
        const text = await res.blob.text();
        jsonContent.value = JSON.parse(text);
      } else if (mimeType.value.startsWith("text/")) {
        textContent.value = await res.blob.text();
      }
    } catch (err) {
      errorText.value = `Failed to load file`;
      console.error("Failed to load file", err);
    } finally {
      loading.value = false;
    }
  }

  // Download File
  function downloadFile() {
    if (!blob.value || !objectUrl.value) return;

    const link = document.createElement("a");
    link.href = objectUrl.value;

    // filename
    link.download = props.activeFile.name;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const renderType = computed(() => {
    if (!mimeType.value) return null;
    if (mimeType.value === "application/json") return "json";
    if (mimeType.value.startsWith("image/")) return "image";
    if (mimeType.value.startsWith("video/")) return "video";
    if (mimeType.value.startsWith("text/")) return "text";

    errorText.value = "This file type isn’t supported.";
  });

  onBeforeMount(getFile);

  onBeforeUnmount(() => {
    if (objectUrl.value) {
      URL.revokeObjectURL(objectUrl.value);
    }
  });
</script>
