<template>
  <div class="card bg-base-200 text-sm">
    <div class="divider m-0">Info</div>

    <div class="space-y-2">
      <div class="flex justify-between">
        <span class="text-base-content/60">Status Code</span>
        <span class="font-medium">{{ task.status_code }}</span>
      </div>

      <div class="flex justify-between">
        <span class="text-base-content/60">Status Text</span>
        <span class="font-medium">{{ task.status_text }}</span>
      </div>

      <div class="flex justify-between">
        <span class="text-base-content/60">Once</span>
        <span class="font-medium">{{ task.once ? "Yes" : "No" }}</span>
      </div>

      <div class="flex justify-between">
        <span class="text-base-content/60">Stoppable</span>
        <span class="font-medium">{{ task.can_stop ? "Yes" : "No" }}</span>
      </div>

      <!-- Schedule -->
      <div v-if="task.schedule">
        <div class="divider m-0">Schedule</div>
        <!-- Timeout -->
        <div class="flex justify-between" v-if="task.schedule.next">
          <span class="text-base-content/60">Starting</span>
          <TimeLeft :next="task.schedule.next" />
        </div>
        <!-- Interval -->
        <div class="flex justify-between">
          <span class="text-base-content/60">Interval (seconds)</span>
          <span class="font-medium">{{ task.schedule.interval }}</span>
        </div>
        <!-- Total -->
        <div class="flex justify-between">
          <span class="text-base-content/60">Total</span>
          <span class="font-medium">{{ task.schedule.counts }}</span>
        </div>
        <!-- Remaining -->
        <div class="flex justify-between">
          <span class="text-base-content/60">Remaining</span>
          <span class="font-medium">{{ task.schedule.remaining }}</span>
        </div>
        <!-- Completed -->
        <div class="flex justify-between">
          <span class="text-base-content/60">Completed</span>
          <span class="font-medium">{{ task.schedule.completed }}</span>
        </div>
      </div>

      <div v-if="task.error" class="flex justify-between">
        <span class="text-base-content/60">Error</span>
        <span class="font-medium">{{ task.error }}</span>
      </div>
    </div>

    <!-- Task Info -->
    <div class="flex flex-col">
      <div v-for="(info, name) in taskInfo" :key="name">
        <!-- Header -->
        <div class="divider m-0 capitalize">{{ name }}</div>
        <!-- task info -->
        <div
          v-for="(infoValue, infoName) in info"
          :key="infoName"
          class="flex justify-between"
        >
          <span class="text-base-content/60 capitalize">{{ infoName }}</span>
          <span class="font-medium">{{ infoValue }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onBeforeMount, watch } from "vue";
  import { fetchTaskInfo } from "@/api/task";

  import TimeLeft from "@/components/utils/TimeLeft.vue";

  const props = defineProps({
    task: Object
  });

  const taskInfo = ref({});

  watch(
    () => props.task,
    () => {
      updateTaskInfo();
    },
    { deep: true, immediate: true }
  );

  async function updateTaskInfo() {
    taskInfo.value = await fetchTaskInfo(props.task.id);
  }

  onBeforeMount(async () => {
    await updateTaskInfo();
  });
</script>
