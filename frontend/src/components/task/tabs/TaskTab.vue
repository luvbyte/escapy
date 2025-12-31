<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- Tabs Head -->
    <div class="flex justify-center gap-1 py-1 pb-2 bg-base-200 rounded-full">
      <button
        v-for="(tab, index) in tabsList"
        :key="index"
        @click="selectedTab = index"
        class="p-1 px-3 rounded-full text-sm font-medium transition-all"
        :class="
          index === selectedTab
            ? 'bg-secondary text-secondary-content shadow'
            : 'text-base-content/70 hover:bg-base-300'
        "
      >
        {{ tab }}
      </button>
    </div>

    <!-- Tabs Body -->
    <TaskManage v-if="selectedTab === 0" :task />
    <TaskOptions v-else-if="selectedTab === 1" :task />
  </div>
</template>

<script setup>
  import { ref } from "vue";

  import TaskOptions from "./TaskOptions.vue";
  import TaskManage from "./TaskManage.vue";

  // Task Object
  defineProps({
    task: Object
  });

  // Tabs List
  const tabsList = ["Manage", "Options"];

  // Active Tab
  const selectedTab = ref(0);
</script>
