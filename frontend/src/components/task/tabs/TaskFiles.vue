<template>
  <div
    class="relative flex-1 flex flex-col overflow-hidden text-sm select-none"
  >
    <!-- Confirm Dialouge -->
    <TaskDeleteFiles
      v-if="showDelete"
      :taskID="task.id"
      :files="selectedFiles"
      :close="closeDelete"
    />
    <!-- File Preview -->
    <TaskFileView
      v-if="activeFile"
      :taskID="task.id"
      :activeFile
      :files
      @update:activeFile="activeFile = $event"
      :close="() => (activeFile = null)"
    />

    <!-- Uploader -->
    <TaskFileUploader
      v-if="showTaskFileUploader"
      :taskID="task.id"
      :currentPath
      :close="closeUploader"
    />
    <!-- Explorer -->
    <div
      v-show="!showTaskFileUploader && !activeFile"
      class="fullscreen flex flex-col overflow-hidden"
    >
      <!-- Statusbar -->
      <div class="flex items-center gap-1 justify-end">
        <!-- Reload Button -->
        <button
          @click="refreshFilesList"
          :disabled="loading"
          class="btn btn-xs btn-soft btn-primary rounded"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            class="active:rotate-180 transition transition-transform duration-300"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 16h5v5M10 8H5V3m14.418 6.003A8 8 0 0 0 5.086 7.976m-.504 7.021a8 8 0 0 0 14.331 1.027"
            />
          </svg>
        </button>
        <!-- Grid / List Toggle Buttons -->
        <div class="btn-group">
          <!-- List Button -->
          <button
            class="btn btn-xs rounded"
            :class="{ 'btn-primary': viewMode === 'list' }"
            @click="viewMode = 'list'"
          >
            LIST
          </button>
          <!-- Grid Button -->
          <button
            class="btn btn-xs rounded"
            :class="{ 'btn-primary': viewMode === 'grid' }"
            @click="viewMode = 'grid'"
          >
            GRID
          </button>
        </div>
        <!-- Select Button  -->

        <button
          class="btn btn-xs btn-primary"
          v-if="files.length > 0"
          :class="selectMode ? 'btn-active' : 'btn-ghost'"
          @click="toggleSelectMode"
        >
          <svg
            v-if="selectMode"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M6.758 17.243L12.001 12m5.243-5.243L12 12m0 0L6.758 6.757M12.001 12l5.243 5.243"
            />
          </svg>

          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
          >
            <path
              fill="currentColor"
              d="M11.2 1H8.8c-.857 0-1.44 0-1.89.038c-.438.035-.663.1-.819.18a2 2 0 0 0-.874.874a2 2 0 0 0-.153.462C5.01 2.803 4.803 3 4.548 3c-.282 0-.51-.24-.47-.518a2.7 2.7 0 0 1 .248-.844a3.02 3.02 0 0 1 1.31-1.31C6.278 0 7.116 0 8.796 0h2.4c1.68 0 2.52 0 3.16.327a3.02 3.02 0 0 1 1.31 1.31c.327.642.327 1.48.327 3.16v2.4c0 1.68 0 2.52-.327 3.16a3 3 0 0 1-1.31 1.31a2.7 2.7 0 0 1-.844.248c-.279.04-.518-.188-.518-.47c0-.255.197-.462.446-.516c.209-.046.365-.104.462-.153c.376-.192.682-.498.874-.874c.08-.156.145-.381.18-.82c.037-.45.038-1.03.038-1.89v-2.4c0-.856-.001-1.44-.038-1.89c-.036-.437-.101-.662-.18-.818a2 2 0 0 0-.874-.874c-.156-.08-.381-.145-.819-.18c-.45-.037-1.03-.038-1.89-.038zM8.83 8.12a.5.5 0 0 1 .054.705l-3 3.5a.497.497 0 0 1-.733.028l-2-2a.5.5 0 0 1 .707-.707l1.62 1.62l2.65-3.09a.5.5 0 0 1 .705-.054z"
            />
            <path
              fill="currentColor"
              fill-rule="evenodd"
              d="M.327 5.64C0 6.282 0 7.12 0 8.8v2.4c0 1.68 0 2.52.327 3.16a3.02 3.02 0 0 0 1.31 1.31c.642.327 1.48.327 3.16.327h2.4c1.68 0 2.52 0 3.16-.327a3 3 0 0 0 1.31-1.31c.327-.642.327-1.48.327-3.16V8.8c0-1.68 0-2.52-.327-3.16a3 3 0 0 0-1.31-1.31c-.642-.327-1.48-.327-3.16-.327h-2.4c-1.68 0-2.52 0-3.16.327a3.02 3.02 0 0 0-1.31 1.31m6.87-.638h-2.4c-.857 0-1.44 0-1.89.038c-.438.035-.663.1-.819.18a2 2 0 0 0-.874.874c-.08.156-.145.38-.18.819c-.037.45-.038 1.03-.038 1.89v2.4c0 .857.001 1.44.038 1.89c.036.438.101.663.18.819c.192.376.498.682.874.874c.156.08.381.145.819.18c.45.036 1.03.037 1.89.037h2.4c.857 0 1.44 0 1.89-.037c.438-.036.663-.101.819-.18c.376-.192.682-.498.874-.874c.08-.156.145-.381.18-.82c.037-.45.038-1.03.038-1.89v-2.4c0-.856-.001-1.44-.038-1.89c-.036-.437-.101-.662-.18-.818a2 2 0 0 0-.874-.874c-.156-.08-.381-.145-.819-.18c-.45-.037-1.03-.038-1.89-.038"
              clip-rule="evenodd"
            />
          </svg>
        </button>
        <!-- Live Mode Toggle Button-->
        <button
          class="btn btn-xs rounded btn-ghost"
          :class="{
            'btn-primary btn-active animate__animated animate__bounceIn animate__infinite':
              liveMode
          }"
          @click="liveMode = !liveMode"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M5.99 4.929a.75.75 0 0 1 0 1.06a8.5 8.5 0 0 0 0 12.021a.75.75 0 0 1-1.061 1.06c-3.905-3.905-3.905-10.236 0-14.141a.75.75 0 0 1 1.06 0m13.081 0c3.905 3.905 3.905 10.237 0 14.142a.75.75 0 0 1-1.06-1.06a8.5 8.5 0 0 0 0-12.022a.75.75 0 1 1 1.06-1.06M8.818 7.757a.75.75 0 0 1 0 1.06a4.5 4.5 0 0 0 0 6.365a.75.75 0 0 1-1.06 1.06a6 6 0 0 1 0-8.485a.75.75 0 0 1 1.06 0m7.425 0a6 6 0 0 1 0 8.485a.75.75 0 1 1-1.061-1.06a4.5 4.5 0 0 0 0-6.364a.75.75 0 0 1 1.06-1.06M12 10.5a1.5 1.5 0 1 1 0 3a1.5 1.5 0 0 1 0-3"
            />
          </svg>
        </button>
        <!-- Upload -->
        <button
          @click="showTaskFileUploader = true"
          class="btn btn-xs btn-primary btn-soft rounded"
        >
          Upload
        </button>
      </div>

      <!-- Path -->
      <div class="flex items-center gap-1 py-2">
        <!-- select all -->
        <button
          v-if="selectMode"
          @click="toggleSelectAllFiles"
          class="btn btn-xs btn-success btn-ghost rounded"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.2 0 .375.038t.35.112L17.875 5H5v14h14v-6.65l2-2V19q0 .825-.587 1.413T19 21zm6.525-4l-5.65-5.65l1.4-1.4l4.25 4.25L20.7 5.025L22.125 6.4z"
            />
          </svg>
        </button>

        <!-- Back Button -->
        <button
          v-if="currentPath !== '' && !selectMode"
          class="btn btn-xs btn-success btn-soft"
          @click="goUp"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <g fill="none">
              <path
                d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"
              />
              <path
                fill="currentColor"
                d="M6.046 11.677A7.5 7.5 0 0 1 20 15.5a1 1 0 1 0 2 0A9.5 9.5 0 0 0 4.78 9.963l-.537-3.045a1 1 0 1 0-1.97.347l1.042 5.909a1 1 0 0 0 .412.645a1.1 1.1 0 0 0 .975.125l5.68-1.001a1 1 0 1 0-.347-1.97z"
              />
            </g>
          </svg>
        </button>

        <!-- Path Text -->
        <p
          ref="pathLabelRef"
          v-if="!selectMode"
          class="flex-1 opacity-60 whitespace-nowrap pr-1 scrollbar-hide overflow-x-auto"
        >
          {{ currentPath }}
        </p>

        <!-- Delete Button  -->
        <button
          v-if="selectMode && selectedFiles.length > 0"
          class="btn btn-xs btn-error btn-soft rounded"
          @click="showDelete = true"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M7 21q-.825 0-1.412-.587T5 19V6H4V4h5V3h6v1h5v2h-1v13q0 .825-.587 1.413T17 21zM17 6H7v13h10zM9 17h2V8H9zm4 0h2V8h-2zM7 6v13z"
            />
          </svg>
        </button>
      </div>

      <!-- Loading -->
      <Loading v-if="loading && !liveMode" />

      <!-- Files -->
      <div
        v-show="!(loading && !liveMode)"
        ref="filesPanelRef"
        class="overflow-y-auto overflow-x-hidden py-2"
        :class="
          viewMode === 'grid'
            ? 'grid grid-cols-4 sm:grid-cols-3 md:grid-cols-4 gap-2 items-center'
            : 'flex-1 flex flex-col gap-1'
        "
      >
        <!-- File -->
        <div
          v-for="file in files"
          :key="file.hash_name"
          @click="selectFile(file)"
          class="rounded cursor-pointer"
          :class="[
            viewMode === 'grid'
              ? 'py-2 flex flex-col items-center text-center gap-2'
              : 'py-1 flex items-center gap-2',

            isSeleted(file)
              ? 'bg-info/80 text-info-content'
              : 'hover:bg-base-300'
          ]"
        >
          <!-- File Icon -->
          <FileIcon
            :file
            :taskID="task.id"
            :class="viewMode === 'grid' ? 'w-20' : 'w-12'"
          />
          <!-- File Text -->
          <span class="truncate w-full">
            {{ file.name }}
          </span>
        </div>
        <!-- If Empty Directory -->
        <div
          v-if="files.length === 0"
          class="text-center opacity-60 py-4 col-span-full"
        >
          Empty directory
        </div>
      </div>
    </div>
    <div></div>

    <!-- files complete -->
  </div>
</template>

<script setup>
  import {
    ref,
    computed,
    onBeforeMount,
    onUnmounted,
    watch,
    nextTick
  } from "vue";
  import { getTaskFileList } from "@/api/task";

  import FileIcon from "./FileIcon.vue";
  import TaskFileView from "./TaskFileView.vue";
  import TaskFileUploader from "./TaskFileUploader.vue";
  import TaskDeleteFiles from "./TaskDeleteFiles.vue";

  import Loading from "@/components/utils/Loading.vue";

  // task
  const props = defineProps({
    task: Object
  });

  const refreshInterval = 2000; // 2 seconds
  // --------- Long press select
  const selectMode = ref(false);
  const selectedFiles = ref([]);
  const showDelete = ref(false);

  function closeDelete(refresh = false) {
    selectMode.value = false;
    selectedFiles.value = [];

    showDelete.value = false;
    if (refresh) refreshFilesList();
  }

  // Check if file is selected
  const isSeleted = file => {
    const index = selectedFiles.value.indexOf(file);

    if (index < 0) return false;

    return true;
  };

  // Toggle selectedFiles
  function toggleSelectAllFiles() {
    if (selectedFiles.value.length >= files.value.length) {
      // unselect all
      selectedFiles.value = [];
    } else {
      // select all
      selectedFiles.value = [...files.value];
    }
  }

  function toggleSelectMode() {
    selectMode.value = !selectMode.value;
    selectedFiles.value = [];
  }
  // ---------------------------

  // Files List
  const files = ref([]);
  // Active File / Selected
  const activeFile = ref(null);
  // CurrentActivePath
  const currentPath = ref("files");
  // Loading state
  const loading = ref(false);

  // Files View Mode - list | grid
  const viewMode = ref("grid");
  // Live reload Mode
  const liveMode = ref(false);

  // Files Panel Reference
  const filesPanelRef = ref();
  // Path Label Reference - for scrolling right
  const pathLabelRef = ref();

  // Live reload interval
  let liveInterval = null;

  const showTaskFileUploader = ref(false);

  // If buttom
  function isAtBottom(el, threshold = 20) {
    if (!el) return true;

    return el.scrollHeight - el.scrollTop - el.clientHeight <= threshold;
  }

  // Scroll element to bottom
  function scrollToBottom(el) {
    if (!el) return;

    el.scrollTo({
      top: el.scrollHeight,
      behavior: "smooth"
    });
  }

  // Scroll FilePath label to right
  function scrollToRight(el) {
    if (!el) return;

    el.scrollTo({
      left: el.scrollWidth - el.clientWidth,
      behavior: "smooth"
    });
  }

  // Load files
  async function loadFiles(path = currentPath.value) {
    try {
      loading.value = true;

      const panel = filesPanelRef.value;
      const shouldAutoScroll = isAtBottom(panel);

      files.value = await getTaskFileList(props.task.id, path);
      currentPath.value = path;

      // Wait for DOM update
      await nextTick();

      // Auto scroll only if user was already at bottom and live mode
      if (shouldAutoScroll && liveMode.value) {
        scrollToBottom(panel);
      }

      // scroll right path label
      scrollToRight(pathLabelRef.value);
    } catch (err) {
      console.error("Failed to load files:", err);
    } finally {
      loading.value = false;
    }
  }

  function closeUploader(refresh = false) {
    showTaskFileUploader.value = false;
    if (refresh) refreshFilesList();
  }

  // Handle file click
  async function selectFile(file) {
    if (selectMode.value) {
      // Selecte mode
      const index = selectedFiles.value.indexOf(file);
      if (index !== -1) {
        selectedFiles.value.splice(index, 1);
        if (selectedFiles.value.length <= 0) {
          selectMode.value = false;
        }
      } else {
        selectedFiles.value.push(file);
      }

      return;
    }

    if (file.is_dir) {
      await loadFiles(file.path);
    } else {
      activeFile.value = file;
    }
  }

  // Refresh files
  async function refreshFilesList() {
    console.log("reftesh");
    await loadFiles(currentPath.value);
  }

  // Go up one directory
  async function goUp() {
    if (!currentPath.value) return;

    const parts = currentPath.value.split("/");
    parts.pop();
    await loadFiles(parts.join("/"));
  }

  //  liveMode
  watch(liveMode, enabled => {
    if (enabled) {
      // Start polling
      liveInterval = setInterval(() => {
        refreshFilesList();
      }, refreshInterval);
    } else {
      // Stop polling
      clearInterval(liveInterval);
      liveInterval = null;
    }
  });

  // Cleanup on destroy
  onUnmounted(() => {
    clearInterval(liveInterval);

    // Live Mode on running
    liveMode.value = props.task.completed;
  });

  // Load root directory on load
  onBeforeMount(async () => {
    await refreshFilesList();
    // await loadFiles(currentPath.value);
  });
</script>
