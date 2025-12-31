<template>
  <div
    @click.self="close"
    class="fixed inset-0 z-40 bg-base-100 fullscreen gap-2 flex flex-col items-center justify-center p-2"
  >
    <div class="text-md font-heading text-center">
      Do you want to delete {{ selectedFiles.length }} files ?
    </div>

    <Loading v-if="loading" class="h-1/2 w-full" />
    <div
      v-else
      class="border border-base-content/60 h-1/2 w-full rounded overflow-y-auto"
    >
      <!-- File -->
      <div
        v-for="file in selectedFiles"
        class="relative rounded cursor-pointer py-1 px-2 flex items-center gap-2"
      >
        <!-- File Icon -->
        <FileIcon :file :taskID class="w-12" />
        <!-- File Text -->
        <span class="truncate w-full">
          {{ file.name }}
        </span>

        <button @click="removeFileFromList(file)" class="p-2 px-2">
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
    </div>

    <!-- Error -->
    <p class="py-1 text-error">{{ errorText }}</p>

    <!-- Files List -->
    <div v-if="!loading" class="flex justify-end gap-1">
      <button @click="close" class="btn btn-sm btn-success btn-success">
        Cancel
      </button>
      <button @click="deleteFiles" class="btn btn-sm btn-error btn-outline">
        Delete
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { deleteTaskFiles } from "@/api/task";
  import FileIcon from "./FileIcon.vue";

  import Loading from "@/components/utils/Loading.vue";

  const props = defineProps({
    taskID: String,
    files: Array,
    close: Function
  });

  const selectedFiles = ref(props.files);

  const loading = ref(false);
  const errorText = ref("");

  function removeFileFromList(file) {
    const index = selectedFiles.value.indexOf(file);

    if (index !== -1) {
      selectedFiles.value.splice(index, 1);
    }

    if (selectedFiles.value <= 0) props.close();
  }

  async function deleteFiles() {
    const filesList = selectedFiles.value.map(file => file.path);

    try {
      loading.value = true;

      await deleteTaskFiles(props.taskID, filesList);

      props.close(true);
    } catch (error) {
      errorText.value = error;
      console.error("Failed to delete files:", error);
    } finally {
      loading.value = true;
    }
  }
</script>
