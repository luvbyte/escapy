<template>
  <!-- Task Dashboard -->
  <div class="flex-1 rounded border-2 border-base-content/60 overflow-hidden">
    <Dashboard :src="getDashboardURL(taskID)" />
  </div>
</template>

<script setup>
  import { getDashboardURL } from "@/api/task";
  import Dashboard from "@/components/Dashboard.vue";

  defineProps({
    taskID: String
  });
</script>
