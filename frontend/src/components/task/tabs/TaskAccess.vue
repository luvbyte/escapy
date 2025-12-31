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
    <TaskFiles v-show="selectedTab === 0" :task />
    <TaskMessages v-if="selectedTab === 1" :taskID="task.id" />
    <TaskAlerts v-if="selectedTab === 2" :taskID="task.id" />
    <TaskLogs v-if="selectedTab === 3" :taskID="task.id" />
  </div>
</template>

<script setup>
  import { ref } from "vue";

  import TaskFiles from "./TaskFiles.vue";
  import TaskMessages from "./TaskMessages.vue";
  import TaskAlerts from "./TaskAlerts.vue";
  import TaskLogs from "./TaskLogs.vue";

  // Task Object
  defineProps({
    task: Object
  });

  // Tabs List
  const tabsList = ["Files", "Messages", "Alerts", "Logs"];

  // Active Tab
  const selectedTab = ref(0);
</script>
