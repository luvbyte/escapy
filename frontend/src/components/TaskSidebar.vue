<template>
  <div
    @click.self="close"
    class="fixed z-20 inset-0 fullscreen flex justify-end"
  >
    <div
      v-if="tasksList.length > 0"
      class="w-full h-full flex flex-col gap-2 p-2 bg-base-200 shadow-xl"
    >
      <!-- Task -->
      <div class="flex items-center gap-2">
        <select v-model="selectedTask" class="w-full select select-sm">
          <option v-for="task in tasksList" :key="task.id" :value="task">
            {{ task.name }}
          </option>
        </select>

        <button @click="close" class="btn btn-sm btn-soft">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="m12 12.708l-5.246 5.246q-.14.14-.344.15t-.364-.15t-.16-.354t.16-.354L11.292 12L6.046 6.754q-.14-.14-.15-.344t.15-.364t.354-.16t.354.16L12 11.292l5.246-5.246q.14-.14.345-.15q.203-.01.363.15t.16.354t-.16.354L12.708 12l5.246 5.246q.14.14.15.345q.01.203-.15.363t-.354.16t-.354-.16z"
            />
          </svg>
        </button>
      </div>

      <!-- Task Card -->
      <div>
        <div
          @click="redirectTask"
          class="relative group cursor-pointer rounded-lg p-3 transition-all duration-200 glass shadow-md hover:shadow-lg hover:scale-[1.01]"
          :class="
            selectedTask.completed
              ? 'bg-secondary/80 text-secondary-content'
              : 'bg-primary/80 text-primary-content'
          "
        >
          <!-- Time Ago -->
          <div
            class="absolute top-2 right-2 text-xs opacity-70 px-2 py-0.5 rounded-full flex flex-col"
          >
            <span>{{ formatTimestamp(selectedTask.created_at) }} </span>
            <span v-if="selectedTask.completed_at"
              >{{ formatTimestamp(selectedTask.completed_at) }}
            </span>
          </div>
          <!-- Task Name -->
          <h1 class="font-semibold truncate">
            {{ selectedTask.name }}
          </h1>

          <!-- Module Title -->
          <p class="text-sm opacity-80 truncate">
            {{ selectedTask.module.title }}
          </p>

          <!-- Footer -->
          <div class="flex items-center justify-between text-xs opacity-70">
            <span>ID: {{ selectedTask.id }}</span>

            <span
              class="rounded-full px-2 py-0.5 text-[11px] border bg-base-100 border-base-content/80"
              :class="
                selectedTask.status_code === 6 ? 'text-error' : 'text-success'
              "
            >
              {{ selectedTask.status_text }}
            </span>
          </div>
        </div>
      </div>

      <!-- Error Text -->
      <h1 v-if="errorText" class="text-error text-sm">{{ errorText }}</h1>

      <!-- Action Buttons -->
      <div
        v-if="!(selectedTask.once && selectedTask.completed)"
        class="flex flex-col justify-end gap-1"
      >
        <!-- Start -->
        <button
          v-if="selectedTask.status_code % 2 === 0"
          class="btn btn-success btn-soft btn-sm w-full rounded"
          @click="taskCommand('start')"
        >
          START
        </button>
        <!-- Stop -->
        <button
          v-if="selectedTask.can_stop && selectedTask.status_code % 2 !== 0"
          class="btn btn-error btn-soft btn-sm w-full rounded"
          @click="taskCommand('stop')"
        >
          STOP
        </button>
      </div>

      <!-- Task Info -->
      <div class="card bg-base-200 text-sm">
        <div class="divider m-0">Info</div>

        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-base-content/60">Status Code</span>
            <span class="font-medium">{{ selectedTask.status_code }}</span>
          </div>

          <div class="flex justify-between">
            <span class="text-base-content/60">Status Text</span>
            <span class="font-medium">{{ selectedTask.status_text }}</span>
          </div>

          <div class="flex justify-between">
            <span class="text-base-content/60">Once</span>
            <span class="font-medium">{{
              selectedTask.once ? "Yes" : "No"
            }}</span>
          </div>

          <div class="flex justify-between">
            <span class="text-base-content/60">Stoppable</span>
            <span class="font-medium">{{
              selectedTask.can_stop ? "Yes" : "No"
            }}</span>
          </div>

          <!-- Schedule -->
          <div v-if="selectedTask.schedule">
            <div class="divider m-0">Schedule</div>
            <!-- Timeout -->
            <div class="flex justify-between" v-if="selectedTask.schedule.next">
              <span class="text-base-content/60">Starting</span>
              <TimeLeft :next="selectedTask.schedule.next" />
            </div>
            <!-- Interval -->
            <div class="flex justify-between">
              <span class="text-base-content/60">Interval (seconds)</span>
              <span class="font-medium">{{
                selectedTask.schedule.interval
              }}</span>
            </div>
            <!-- Total -->
            <div class="flex justify-between">
              <span class="text-base-content/60">Total</span>
              <span class="font-medium">{{
                selectedTask.schedule.counts
              }}</span>
            </div>
            <!-- Remaining -->
            <div class="flex justify-between">
              <span class="text-base-content/60">Remaining</span>
              <span class="font-medium">{{
                selectedTask.schedule.remaining
              }}</span>
            </div>
            <!-- Completed -->
            <div class="flex justify-between">
              <span class="text-base-content/60">Completed</span>
              <span class="font-medium">{{
                selectedTask.schedule.completed
              }}</span>
            </div>
          </div>

          <div v-if="selectedTask.error" class="flex justify-between">
            <span class="text-base-content/60">Error</span>
            <span class="font-medium">{{ selectedTask.error }}</span>
          </div>
        </div>
      </div>

      <!-- MANAGE -->
      <div class="flex-1 flex flex-col gap-2 overflow-y-auto"></div>
    </div>
    <div
      v-else
      class="w-[80%] h-full bg-base-200 flex justify-center items-center font-heading"
    >
      <h1 class="opacity-60">NO ACTIVE TASKS</h1>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onBeforeMount, onBeforeUnmount } from "vue";

  import { runTaskShellCommand, getActiveTasks } from "@/api/task";
  import { formatTimestamp } from "@/api/utils";

  import { onMessage, offMessage } from "@/api/client";
  import { useRouter } from "vue-router";

  import TimeLeft from "./utils/TimeLeft.vue";

  const props = defineProps(["close", "tasksList"]);

  const router = useRouter();

  const tasksList = ref(props.tasksList);
  const selectedTask = ref(props.tasksList?.[0] ?? null);

  const errorText = ref(null);

  console.log(props.tasksList);

  // Task Command
  const taskCommand = async command => {
    if (!selectedTask.value) return;

    try {
      await runTaskShellCommand(selectedTask.value.id, command);
    } catch (err) {
      errorText.value = err;
    }
  };

  // onClientData ws events
  async function onClientData(data) {
    const event = data.event;
    const payload = data.payload;

    console.log(payload);
    //
    if (event === "task-status-update") {
      tasksList.value = await getActiveTasks();
      if (payload.id === selectedTask.value.id) {
        selectedTask.value = payload;
      }
    }
  }

  function redirectTask() {
    if (!selectedTask.value) return;

    router.push({
      name: "task",
      params: { id: selectedTask.value.id }
    });
  }

  onBeforeMount(async () => {
    onMessage(onClientData);
  });
  onBeforeUnmount(() => {
    offMessage(onClientData);
  });
</script>
