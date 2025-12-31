<template>
  <div
    @click.self="onClose"
    class="w-full"
    :class="{
      'fixed inset-0 z-40 p-2 fullscreen bg-base-100/90 flex flex-col overflow-hidden':
        active
    }"
  >
    <div v-if="active" class="flex flex-col gap-2 overflow-y-auto">
      <div
        @click="active = false"
        class="border rounded text-center p-1 bg-base-100 border-base-content/40 cursor-pointer px-2 font-heading"
      >
        {{ selectedTask.name }}
      </div>
      <!-- Dropdown list -->
      <div
        v-for="task in tasksList"
        :key="task.id"
        @click.stop="selectTask(task)"
        class="border rounded text-center p-1 bg-base-100 border-base-content/40 cursor-pointer px-2 font-heading"
        :class="{ hidden: task.id === selectedTask.id }"
      >
        {{ task.name }}
      </div>
    </div>
    <!-- display task -->
    <div
      v-else
      @click="active = true"
      v-swipe="onSwipe"
      class="flex items-center gap-2 border rounded p-1 border-base-content/40 text-center cursor-pointer opacity-80"
    >
      <span class="opacity-60">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M5.536 21.886a1 1 0 0 0 1.033-.064l13-9a1 1 0 0 0 0-1.644l-13-9A1 1 0 0 0 5 3v18a1 1 0 0 0 .536.886"
          />
        </svg>
      </span>
      <h1 class="flex-1 truncate">
        {{ selectedTask.name }}
      </h1>
      <span class="opacity-60">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="m4.431 12.822l13 9A1 1 0 0 0 19 21V3a1 1 0 0 0-1.569-.823l-13 9a1.003 1.003 0 0 0 0 1.645"
          />
        </svg>
      </span>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from "vue";

  const props = defineProps({
    tasksList: {
      type: Array,
      required: true
    },
    modelValue: {
      type: Object,
      required: true
    }
  });

  const emit = defineEmits(["update:modelValue", "change"]);

  const active = ref(false);

  // local mirror of v-model
  const selectedTask = ref(props.modelValue);

  // keep in sync if parent changes
  watch(
    () => props.modelValue,
    val => {
      selectedTask.value = val;
    }
  );

  function selectTask(task) {
    selectedTask.value = task;
    active.value = false;
    emit("update:modelValue", task);
    emit("change", task);
  }

  function onSwipe(direction) {
    const currentIndex = props.tasksList.findIndex(
      t => t.id === selectedTask.value.id
    );

    if (currentIndex === -1) return;

    let nextIndex = currentIndex;

    if (direction === "left") {
      nextIndex = currentIndex + 1;
    } else if (direction === "right") {
      nextIndex = currentIndex - 1;
    }

    // optional wrap-around
    if (nextIndex < 0) nextIndex = props.tasksList.length - 1;
    if (nextIndex >= props.tasksList.length) nextIndex = 0;

    const nextTask = props.tasksList[nextIndex];

    selectTask(nextTask)
  }

  function onClose() {
    active.value = false;
  }
</script>
