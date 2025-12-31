<script setup>
  import { ref, onBeforeMount, reactive, computed } from "vue";
  import { useRouter } from "vue-router";

  import { runTask } from "@/api/task";
  import { getModulesList } from "@/api/module";
  import { resolveImageURL } from "@/api/utils";

  import Loading from "@/components/utils/Loading.vue";

  import Panel from "./Panel.vue";
  import ModuleOptions from "./ModuleOptions.vue";
  import SelectModuleList from "./SelectModuleList.vue";

  const router = useRouter();

  const modules = ref({});
  const selectedModule = ref(null);

  const isAboutExpanded = ref(false);

  const moduleOptionsRef = ref();

  // Task Name Reference
  const taskName = ref("");
  const props = defineProps(["close"]);

  const loading = ref(false);

  function secondsUntil(datetimeLocalValue) {
    const target = new Date(datetimeLocalValue);
    const now = new Date();
    return Math.max(0, Math.floor((target - now) / 1000));
  }

  // Task Options
  const taskCreateOptions = reactive({
    once: false,
    autostart: false,

    delay: "",
    delaySeconds: "",

    // Repeat Intervel
    repeat: "",
    repeatCount: "", // empty for unlimited runs

    signal: ""
  });

  // Check if value is number type
  function isNumber(value) {
    return typeof value === "number";
  }

  // Returna value if number else null
  const isNumberOrNull = value => {
    return isNumber(value) ? value : null;
  };

  // Get delay time or null
  const getDelay = computed(() => {
    let delay = null;

    // datetime-local → seconds
    if (taskCreateOptions.delay !== "") {
      delay = secondsUntil(taskCreateOptions.delay);
    }

    // seconds input
    if (
      isNumber(taskCreateOptions.delaySeconds) &&
      taskCreateOptions.delaySeconds >= 0
    ) {
      if (delay !== null) {
        delay += taskCreateOptions.delaySeconds;
      } else {
        delay = taskCreateOptions.delaySeconds;
      }
    }

    return delay; // number | null
  });

  // On create task
  async function onCreateTask() {
    if (!selectedModule.value || !taskName.value) return;

    if (loading.value) return;

    loading.value = true;

    try {
      console.log(taskCreateOptions);

      // Get delay in seconds
      // Combines both

      const taskOptions = {
        once: taskCreateOptions.once,
        autostart: taskCreateOptions.autostart,

        delay: getDelay.value,

        repeat: isNumberOrNull(taskCreateOptions.repeat),
        repeat_count: isNumberOrNull(taskCreateOptions.repeatCount),

        signal: taskCreateOptions.signal
      };

      console.log(taskOptions);

      // Task Config
      const taskConfig = {
        ...taskOptions,
        // module options
        options: moduleOptionsRef.value.getOptions()
      };

      console.log(taskConfig);

      // Returns task ID
      const { task } = await runTask(
        taskName.value,
        selectedModule.value.name,
        taskConfig
      );
      // If redirect
      if (taskCreateOptions.autostart) {
        router.push({
          name: "task",
          params: { id: task }
        });
      } else {
        props.close();
      }
    } catch (err) {
      toast("Error Creating Task", "error");
    } finally {
      loading.value = false;
    }
  }

  // Select active module
  function selectModule(module) {
    selectedModule.value = module;
  }
  // on close button click
  function onClose() {
    if (selectedModule.value) selectedModule.value = null;
    else props.close();
  }

  // On before mounted
  onBeforeMount(async () => {
    modules.value = await getModulesList();

    console.log(modules.value);
  });
</script>

<template>
  <Panel class="flex-1 flex flex-col overflow-hidden">
    <!-- Topbar -->
    <div
      class="p-3 px-2 flex justify-between items-center bg-secondary text-secondary-content glass"
    >
      <div class="flex-1 font-heading">
        <Transition name="slide-up" mode="out-in">
          <h1 v-if="!selectedModule" key="module">Select Task Module</h1>
          <h1 v-else key="task">Create Task</h1>
        </Transition>
      </div>

      <!-- Top Close Button -->
      <button @click="onClose" class="active:scale-110">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="28"
          height="28"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z"
          />
        </svg>
      </button>
    </div>

    <!-- Sub Topbar -->
    <Transition name="slide-right">
      <div
        v-if="selectedModule"
        class="w-full glass bg-secondary/60 text-secondary-content flex justify-between items-center overflow-hidden"
      >
        <!-- Top Header Box -->
        <div class="p-2 overflow-x-auto whitespace-nowrap">
          <div class="inline-flex items-center gap-2">
            <!-- Title -->
            <span class="font-semibold leading-tight">
              {{ selectedModule.title }}
            </span>

            <!-- Author -->
            <span class="text-sm">
              <span class="font-medium">@{{ selectedModule.name }}</span>
              <span class="px-1">•</span>
              <span>{{ selectedModule.author }}</span>
            </span>
          </div>
        </div>

        <!-- CREATE Button -->
        <button
          @click="onCreateTask"
          class="h-full flex items-center gap-1 px-3 bg-secondary/40 font-heading"
        >
          CREATE
          <svg
            v-if="loading"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8A8 8 0 0 1 12 20Z"
              opacity="0.5"
            />
            <path
              fill="currentColor"
              d="M20 12h2A10 10 0 0 0 12 2V4A8 8 0 0 1 20 12Z"
            >
              <animateTransform
                attributeName="transform"
                dur="1s"
                from="0 12 12"
                repeatCount="indefinite"
                to="360 12 12"
                type="rotate"
              />
            </path>
          </svg>

          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-width="1.5"
              d="M3 12v6.967c0 2.31 2.534 3.769 4.597 2.648l3.203-1.742M3 8V5.033c0-2.31 2.534-3.769 4.597-2.648l12.812 6.968a2.998 2.998 0 0 1 0 5.294l-6.406 3.484"
            />
          </svg>
        </button>
      </div>
    </Transition>

    <div class="flex-1 flex flex-col overflow-hidden">
      <Transition name="fade">
        <!-- Modules Select -->
        <SelectModuleList v-if="!selectedModule" :modules :selectModule />
        <!-- Task Create -->
        <div
          v-else
          class="fullscreen flex flex-col gap-3 overflow-y-auto scroll-smooth"
        >
          <!-- Task Options -->
          <!-- Banner -->
          <div
            class="p-1 text-center font-heading bg-secondary/40 glass text-secondary-content"
          >
            Task Options
          </div>
          <div class="px-2 flex flex-col gap-1">
            <!-- Task Name -->
            <input
              class="input input-sm w-full input-secondary placeholder:opacity-40 focus:outline-none"
              v-model="taskName"
              placeholder="Task Name (required)"
            />
            <!-- Redirect To Task Dashboard checkbox -->
            <label class="mt-2 flex justify-between">
              <span class="opacity-80"
                >To Dashboard (<span class="opacity-80">autostart</span>)</span
              >
              <input
                type="checkbox"
                v-model="taskCreateOptions.autostart"
                class="toggle"
              />
            </label>

            <!-- Once checkbox -->
            <label class="mt-2 flex justify-between">
              <span class="opacity-80">Once</span>
              <input
                type="checkbox"
                v-model="taskCreateOptions.once"
                class="toggle"
              />
            </label>

            <div v-if="!taskCreateOptions.autostart">
              <!-- Schedule Time -->
              <label class="mt-2 flex justify-between items-center gap-2">
                <span class="opacity-80">Time</span>

                <input
                  v-model="taskCreateOptions.delay"
                  type="datetime-local"
                  class="flex-1 input input-sm focus:outline-none"
                />
                <input
                  v-model.number="taskCreateOptions.delaySeconds"
                  type="number"
                  min="0"
                  class="w-32 input input-sm focus:outline-none placeholder:opacity-60"
                  placeholder="Delay (sec)"
                />
              </label>

              <!-- Repeat Task -->
              <label
                v-if="getDelay !== null && !taskCreateOptions.once"
                class="mt-2 flex justify-between items-center gap-2"
              >
                <span class="opacity-80">Repeat</span>

                <input
                  v-model.number="taskCreateOptions.repeatCount"
                  type="number"
                  min="0"
                  class="input input-sm focus:outline-none placeholder:opacity-60"
                  placeholder="Count"
                />
                <input
                  v-model.number="taskCreateOptions.repeat"
                  type="number"
                  min="0"
                  class="input input-sm focus:outline-none placeholder:opacity-60"
                  placeholder="Delay (sec)"
                />
              </label>
            </div>

            <!-- Task Start Signal -->
            <label
              v-if="getDelay === null && !taskCreateOptions.autostart"
              class="mt-2 flex justify-between items-center gap-2 whitespace-nowrap"
            >
              <span class="opacity-80">Start Signal</span>

              <input
                v-model="taskCreateOptions.signal"
                type="input"
                class="w-full input input-sm focus:outline-none"
              />
            </label>
          </div>
          <!-- Banner -->
          <div
            class="sticky top-0 z-30 p-1 text-center font-heading bg-secondary/40 glass text-secondary-content"
          >
            Module Options
          </div>

          <!-- Debugging
          <pre>{{ taskCreateOptions }}</pre>
          <div>{{ getDelay }}</div>
          
          -->

          <!-- Module Options -->
          <ModuleOptions
            ref="moduleOptionsRef"
            class="px-2"
            :moduleName="selectedModule.name"
          />
          <!-- Scroll Padding -->
          <div class="min-h-4"></div>
        </div>
      </Transition>
    </div>
  </Panel>
</template>
