<script setup>
  import { ref } from "vue";
  import CreateTask from "@/components/CreateTask.vue";
  import TasksList from "@/components/TasksList.vue";

  const showCreateTask = ref(false);
</script>

<template>
  <div class="relative flex-1 flex flex-col">
    <!-- create task -->
    <Transition name="slide-up">
      <CreateTask
        v-if="showCreateTask"
        :close="() => (showCreateTask = false)"
      />
    </Transition>
    
    <TasksList v-if="!showCreateTask" />
    <!-- create btn -->
    <div
      @click="showCreateTask = true"
      class="absolute bottom-6 right-6 btn btn-lg btn-circle btn-primary"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="28"
        height="28"
        viewBox="0 0 24 24"
      >
        <g
          fill="none"
          stroke="currentColor"
          stroke-dasharray="16"
          stroke-dashoffset="16"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
        >
          <path d="M5 12h14">
            <animate
              fill="freeze"
              attributeName="stroke-dashoffset"
              dur="0.4s"
              values="16;0"
            />
          </path>
          <path d="M12 5v14">
            <animate
              fill="freeze"
              attributeName="stroke-dashoffset"
              begin="0.4s"
              dur="0.4s"
              values="16;0"
            />
          </path>
        </g>
      </svg>
    </div>
  </div>
</template>
