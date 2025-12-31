<template>
  <div class="flex-1 flex justify-end overflow-hidden">
    <div
      v-if="tasksList.length > 0 && selectedTask"
      class="w-full h-full flex flex-col gap-2 p-2 bg-base-200 shadow-xl"
    >
      <!-- Task 
      <div class="flex items-center gap-2">
        <select
          v-model="selectedTask"
          @change="onTaskChange"
          class="w-full select select-sm"
        >
          <option v-for="task in tasksList" :key="task.id" :value="task">
            {{ task.name }}
          </option>
        </select>
      </div>
      -->
      <TaskListDropdown
        :tasksList
        v-model="selectedTask"
        @change="onTaskChange"
      />

      <!-- Task Card -->
      <TaskInfoCard :task="selectedTask" />

      <!-- Error Text -->
      <h1 v-if="errorText" class="text-error text-sm">{{ errorText }}</h1>

      <!-- Action Buttons -->
      <div
        v-if="!(selectedTask.once && selectedTask.completed)"
        class="flex justify-end gap-1"
      >
        <div class="flex-1 flex flex-col items-center">
          <!-- Start -->
          <button
            v-if="selectedTask.status_code % 2 === 0"
            class="btn btn-primary btn-sm btn-outline w-full font-heading"
            @click="taskCommand('start')"
          >
            START
          </button>
          <!-- Stop -->
          <button
            v-if="selectedTask.can_stop && selectedTask.status_code % 2 !== 0"
            class="btn btn-error btn-sm w-full font-heading"
            @click="taskCommand('stop')"
          >
            STOP
          </button>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mt-2 flex justify-center gap-1 bg-base-200 rounded-full">
        <button
          v-for="(tab, index) in tabsList"
          :key="index"
          @click="selectedTab = index"
          class="p-1 px-3 rounded-full text-sm font-medium transition-all"
          :class="
            index === selectedTab
              ? 'bg-primary text-primary-content shadow'
              : 'text-base-content/70 hover:bg-base-300'
          "
        >
          {{ tab }}
        </button>
      </div>

      <!-- Task Info -->
      <TaskInfo v-if="selectedTab === 0" :task="selectedTask" />
      <!-- Task Dashboard -->
      <TaskDashboard v-else-if="selectedTab === 1" :taskID="selectedTask.id" />
      <!-- Task Access -->
      <TaskAccess v-show="selectedTab === 2" :task="selectedTask" />
      <!-- Task Shell -->
      <TaskShell v-show="selectedTab === 3" :taskID="selectedTask.id" />
      <!-- Task Options -->
      <TaskTab v-if="selectedTab === 4" :task="selectedTask" />
    </div>
    <div
      v-else
      class="fullscreen bg-base-200 flex justify-center items-center font-heading"
    >
      <div v-if="tasksList.length > 0" class="flex flex-col">
        <h1 class="opacity-60">TASK NOT FOUND</h1>
        <button
          @click="onDisplayTasks"
          class="btn btn-sm btn-soft btn-secondary"
        >
          DISPLAY TASKS
        </button>
      </div>
      <h1 v-else class="opacity-60">NO ACTIVE TASKS</h1>
    </div>
  </div>
</template>

<script setup>
  import { ref, onBeforeMount, onBeforeUnmount } from "vue";
  import { useRouter, useRoute } from "vue-router";

  import { getActiveTasks, runTaskShellCommand } from "@/api/task";
  import { onMessage, offMessage } from "@/api/client";

  import TaskInfoCard from "@/components/task/TaskInfoCard.vue";
  import TaskListDropdown from "@/components/task/TaskListDropdown.vue";

  import TaskInfo from "@/components/task/tabs/TaskInfo.vue";
  import TaskShell from "@/components/task/tabs/TaskShell.vue";
  import TaskAccess from "@/components/task/tabs/TaskAccess.vue";
  import TaskDashboard from "@/components/task/tabs/TaskDashboard.vue";
  import TaskTab from "@/components/task/tabs/TaskTab.vue";

  const route = useRoute();
  const router = useRouter();

  const tasksList = ref([]);
  const selectedTask = ref(null);
  // 0 - About | Frame
  const selectedTab = ref(0);
  const tabsList = ["Info", "Dashboard", "Access", "Shell", "Task"];

  function onTaskChange() {
    if (selectedTask.value) {
      selectedTab.value = 0;
      router.replace({
        params: { id: selectedTask.value.id }
      });
    } else {
      router.replace({
        params: { id: undefined } // removes optional param
      });
    }
  }

  function onDisplayTasks() {
    selectedTask.value = tasksList.value[0] || null;

    onTaskChange();
  }

  const errorText = ref(null);

  function selectTask(task) {
    selectedTask.value = task;
  }

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

    // Task Update
    if (event === "task-status-update") {
      tasksList.value = await getActiveTasks();
      // If its selected task
      if (payload.id === selectedTask.value.id) {
        selectedTask.value = payload;
      }
    }
    // Task deleted
    else if (event === "task-delete") {
      tasksList.value = await getActiveTasks();

      if (payload.id === selectedTask.value.id) {
        selectedTask.value = tasksList.value[0] || null;
      }
    }
  }

  async function updateTasks() {
    tasksList.value = await getActiveTasks();
  }

  onBeforeMount(async () => {
    await updateTasks();

    const taskId = route.params.id;

    selectedTask.value = taskId
      ? tasksList.value.find(t => String(t.id) === String(taskId)) || null
      : tasksList.value[0] || null;

    onTaskChange();

    onMessage(onClientData);
  });
  onBeforeUnmount(() => {
    offMessage(onClientData);
  });
</script>
