<template>
  <div class="flex-1 bg-base-100">
    <Dashboard :src="getDashboardURL(route.params.id)" />
  </div>
</template>

<script setup>
  // Dont change anything
  import { onBeforeMount } from "vue";
  import { useRoute } from "vue-router";

  import { getDashboardURL } from "@/api/task";

  import Dashboard from "@/components/Dashboard.vue";

  const route = useRoute();
</script>
