<script setup>
  import { ref, computed, onBeforeMount, onBeforeUnmount } from "vue";

  import { getActiveTasks } from "@/api/task";
  import { toast, formatTimestamp } from "@/api/utils";

  import { useRouter } from "vue-router";

  import { onMessage, offMessage } from "@/api/client";

  import Sidebar from "@/components/Sidebar.vue";
  import TaskSidebar from "@/components/TaskSidebar.vue";

  import TaskInfoCard from "@/components/task/TaskInfoCard.vue";

  import SearchInput from "@/components/ui/SearchInput.vue";

  const router = useRouter();

  const tasks = ref([]);
  const showSidebar = ref(false);
  const showTaskSidebar = ref(false);

  const searchText = ref("");

  // Tasks List
  const tasksList = computed(() => {
    if (!searchText.value) return tasks.value;

    const query = searchText.value.toLowerCase();

    return tasks.value.filter(
      task =>
        task.name?.toLowerCase().includes(query) ||
        task.id?.toLowerCase().includes(query) ||
        task.module.name?.toLowerCase().includes(query)
    );
  });

  async function onClientData(data) {
    const event = data.event;
    const payload = data.payload;
    // refresh tasks on events
    if (event.startsWith("task-")) {
      tasks.value = await getActiveTasks();
    }
  }

  // go to /manage
  function toManage() {
    router.push({
      name: "manage"
    });
  }

  onBeforeMount(async () => {
    tasks.value = await getActiveTasks();

    onMessage(onClientData);
  });
  onBeforeUnmount(() => {
    offMessage(onClientData);
  });
</script>

<template>
  <div class="fixed inset-0 fullscreen flex flex-col overflow-hidden">
    <!-- Top Header -->
    <div
      class="py-3 px-2 flex items-center gap-1 bg-primary text-primary-content glass font-heading"
    >
      <button @click="showSidebar = true">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            fill-rule="evenodd"
            d="M3.25 7A.75.75 0 0 1 4 6.25h16a.75.75 0 0 1 0 1.5H4A.75.75 0 0 1 3.25 7"
            clip-rule="evenodd"
          />
          <path
            fill="currentColor"
            d="M3.25 12a.75.75 0 0 1 .75-.75h11a.75.75 0 0 1 0 1.5H4a.75.75 0 0 1-.75-.75"
            opacity="0.7"
          />
          <path
            fill="currentColor"
            d="M3.25 17a.75.75 0 0 1 .75-.75h5a.75.75 0 0 1 0 1.5H4a.75.75 0 0 1-.75-.75"
            opacity="0.4"
          />
        </svg>
      </button>
      <h1 class="flex-1">EScapy</h1>

      <button @click="toManage" class="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="22"
          height="22"
          viewBox="0 0 24 24"
        >
          <g
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
          >
            <path
              d="M20 16V8c0-2.828 0-4.243-.879-5.121C18.243 2 16.828 2 14 2h-4c-2.828 0-4.243 0-5.121.879C4 3.757 4 5.172 4 8v8c0 2.828 0 4.243.879 5.121C5.757 22 7.172 22 10 22h4c2.828 0 4.243 0 5.121-.879C20 20.243 20 18.828 20 16"
            />
            <path
              d="M15.5 2h-7c0 1.414 0 2.121.44 2.56c.439.44 1.146.44 2.56.44h1c1.414 0 2.121 0 2.56-.44c.44-.439.44-1.146.44-2.56M8 15h4m-4-4h8"
            />
          </g>
        </svg>
        <h1>Task</h1>
      </button>
    </div>

    <!-- Search
    <div class="relative p-2 bg-primary/60 glass">
    </div>
    -->
    <SearchInput
      v-model="searchText"
      class="bg-primary/60 p-2 glass text-primary-content"
    />

    <div
      v-if="tasks.length > 0"
      class="mt-2 px-2 flex-1 flex flex-col overflow-y-auto gap-2"
    >
      <TaskInfoCard v-for="task in tasksList" :task :key="task.id" />
    </div>
    <!-- if no active tasks -->
    <div
      v-else
      class="flex-1 flex flex-col justify-center items-center opacity-60"
    >
      <h1>NO ACTIVE TASKS</h1>
      <p class="opacity-40">Create clicking '+' button at buttom</p>
    </div>
  </div>

  <!-- sidebar -->
  <Transition name="slide-right">
    <Sidebar v-if="showSidebar" :close="() => (showSidebar = false)" />
  </Transition>
  <!-- Tasks sidebar -->
  <Transition name="slide-left">
    <TaskSidebar
      v-if="showTaskSidebar"
      ref="taskSidebarRef"
      :tasksList
      :close="() => (showTaskSidebar = false)"
    />
  </Transition>
</template>
