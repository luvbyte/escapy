<template>
  <div class="flex-1 flex flex-col overflow-hidden text-[11px] gap-2">
    <!-- Toolbar -->
    <div class="flex items-center justify-end py-1 gap-2">
      <!-- Clear Button -->
      <button
        @click="alerts.length = 0"
        class="btn btn-xs rounded btn-error btn-soft"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="26"
          height="26"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M6 13h12c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1m-2 4h12c.55 0 1-.45 1-1s-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1m3-9c0 .55.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1"
          />
        </svg>
      </button>
      <!-- Refresh Button -->
      <button
        @click="refreshTaskAlerts"
        class="btn btn-xs rounded btn-success btn-soft"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M21.074 12.154a.75.75 0 0 1 .672.82c-.49 4.93-4.658 8.776-9.724 8.776c-2.724 0-5.364-.933-7.238-2.68L3 20.85a.75.75 0 0 1-.75-.75v-3.96c0-.714.58-1.29 1.291-1.29h3.97a.75.75 0 0 1 .75.75l-2.413 2.407c1.558 1.433 3.78 2.243 6.174 2.243c4.29 0 7.817-3.258 8.232-7.424a.75.75 0 0 1 .82-.672m-18.82-1.128c.49-4.93 4.658-8.776 9.724-8.776c2.724 0 5.364.933 7.238 2.68L21 3.15a.75.75 0 0 1 .75.75v3.96c0 .714-.58 1.29-1.291 1.29h-3.97a.75.75 0 0 1-.75-.75l2.413-2.408c-1.558-1.432-3.78-2.242-6.174-2.242c-4.29 0-7.817 3.258-8.232 7.424a.75.75 0 1 1-1.492-.148"
          />
        </svg>
      </button>
    </div>

    <!-- Loading Panel -->
    <Loading v-if="isLoading" />
    <!-- Task Alerts Box -->
    <div
      v-show="!isLoading"
      ref="alertsBoxRef"
      @scroll="onScroll"
      class="flex-1 flex flex-col overflow-auto text-xs gap-2"
    >
      <div
        v-for="(alert, i) in alerts"
        :key="alert.id"
        class="alert alert-xs shadow"
        :class="alertClass(alert.priority)"
      >
        <!-- Alert -->
        <div class="flex flex-col w-full">
          <div class="flex justify-between items-center gap-2 font-heading">
            <span class="badge badge-outline font-semibold uppercase">
              {{ alert.priority }}
            </span>
            <span class="text-xs opacity-70">
              <TimeStamp :timestamp="alert.timestamp" :showDate="false" />
            </span>
          </div>
          <div class="mt-1 text-sm font-medium">
            {{ alert.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onBeforeMount, onBeforeUnmount, nextTick } from "vue";

  import { fetchTaskAlerts } from "@/api/task";
  import { onTaskMessage, offTaskMessage } from "@/api/client";

  import { formatTimestamp } from "@/api/utils";

  import Loading from "@/components/utils/Loading.vue";
  import TimeStamp from "@/components/utils/TimeStamp.vue";

  // TaskID
  const props = defineProps({
    taskID: {
      type: String,
      required: true
    }
  });

  // UI state
  const alertsBoxRef = ref(null);
  const alerts = ref([]);
  const isAtBottom = ref(true);
  const isLoading = ref(false);

  function alertClass(priority) {
    switch (priority) {
      case "error":
        return "alert-error";
      case "warning":
        return "alert-warning";
      case "success":
        return "alert-success";
      default:
        return "alert-info";
    }
  }

  // Scroll helpers
  function scrollToBottom() {
    const el = alertsBoxRef.value;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }

  // Detect user scrolling
  function onScroll() {
    const el = alertsBoxRef.value;
    if (!el) return;

    const threshold = 20;
    isAtBottom.value =
      el.scrollHeight - el.scrollTop - el.clientHeight < threshold;
  }

  // Load all alerts
  async function loadAlerts() {
    if (isLoading.value) return;

    isLoading.value = true;

    const el = alertsBoxRef.value;
    const wasAtBottom = isAtBottom.value;

    const res = await fetchTaskAlerts(props.taskID);
    alerts.value = res.items ?? res; // support either shape

    await nextTick();

    if (wasAtBottom) {
      scrollToBottom();
    }

    isLoading.value = false;
  }

  // Real-time updates
  async function onMessage(data) {
    if (data.event === "task-alert" && data.payload.taskID === props.taskID) {
      alerts.value.push(data.payload.alert);

      await nextTick();
      if (isAtBottom.value) {
        scrollToBottom();
      }
    }
  }

  // Manual refresh (optional)
  async function refreshTaskAlerts() {
    await loadAlerts();

    await nextTick();
    scrollToBottom();
  }

  // Lifecycle
  onBeforeMount(async () => {
    onTaskMessage(onMessage);

    await refreshTaskAlerts();
  });

  onBeforeUnmount(() => {
    offTaskMessage(onMessage);
  });
</script>
