<template>
  <div>
    <!-- Loading -->
    <Loading v-if="loading && isImage" class="opacity-60" />
    <!-- Image -->
    <img
      v-show="!loading"
      :src="iconSrc"
      :key="iconSrc"
      class="fullscreen aspect-square object-cover rounded"
      @load="loading = false"
      @error="loading = false"
    />
  </div>
</template>

<script setup>
  import { ref, computed } from "vue";

  import { getFileURL } from "@/api/task";
  import { IMAGE_EXTENSIONS } from "@/api/utils";

  import Loading from "@/components/utils/Loading.vue";

  // Is Loading Icon
  const loading = ref(true);

  // file: Object, taskID
  const props = defineProps({
    file: {
      type: Object,
      required: true
    },
    taskID: {
      type: String,
      required: true
    }
  });

  // Icon name by suffix
  const iconName = suffix => {
    if (suffix === "" && props.file.is_dir) return "folder-icon.png";
    return "file-icon2.png";
  };

  // Is it image
  const isImage = computed(() => {
    const ext = props.file.suffix.split(".").pop().toLowerCase();
    return IMAGE_EXTENSIONS.includes(ext);
  });

  // Icon source based on file Object
  const iconSrc = computed(() => {
    const suffix = props.file.suffix;

    // If its image load as thumbnail
    if (isImage.value) {
      return getFileURL(props.taskID, props.file.path, true);
    }

    // If its not image/
    return `/assets/icons/${iconName(suffix)}`;
  });
</script>
