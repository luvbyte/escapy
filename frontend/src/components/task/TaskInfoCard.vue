<template>
  <div
    @click="redirectTask"
    class="relative group cursor-pointer rounded-xl p-4 border glass shadow-md"
    :class="
      task.completed
        ? 'bg-secondary/80 border-secondary/40 text-secondary-content'
        : 'bg-primary/80 border-primary/40 text-primary-content'
    "
  >
    <!-- Timestamp -->
    <div
      class="absolute top-3 right-3 text-[11px] opacity-70 px-2 py-1 rounded-lg bg-base-100/70 text-base-content shadow-sm"
    >
      <div class="flex flex-col items-end gap-0.5 font-heading">
        <TimeStamp :timestamp="task.created_at" />
        <TimeStampRelative
          v-if="task.completed_at"
          :timestamp="task.completed_at"
        />
      </div>
    </div>

    <!-- Task Name -->
    <h1 class="font-semibold leading-tight truncate mb-1">
      {{ task.name }}
    </h1>

    <!-- Module Title -->
    <p class="text-sm opacity-80 truncate mb-3">
      {{ task.module.title }}
    </p>

    <!-- Footer -->
    <div class="flex items-center justify-between text-xs opacity-70">
      <span class="tracking-tight">#{{ task.id }}</span>

      <span
        class="rounded-full px-2.5 py-1 text-[11px] font-medium bg-base-100/80 shadow-sm text-base-content"
      >
        {{ task.status_text }}
      </span>
    </div>

    <!-- Completed Overlay -->
    <div
      v-if="task.completed"
      class="absolute inset-0 rounded-xl bg-base-100/5 pointer-events-none"
    />
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";

  import TimeStamp from "@/components/utils/TimeStamp.vue";
  import TimeStampRelative from "@/components/utils/TimeStampRelative.vue";

  const router = useRouter();

  const props = defineProps(["task"]);

  function redirectTask() {
    router.push({
      name: "task",
      params: { id: props.task.id }
    });
  }
</script>
