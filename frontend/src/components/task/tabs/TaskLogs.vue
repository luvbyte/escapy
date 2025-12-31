<template>
  <div class="flex-1 flex flex-col overflow-hidden text-[11px] gap-2">
    <!-- Toolbar -->
    <div class="flex items-center justify-end py-1 gap-1">
      <!-- options -->
      <button
        @click="textWrap = !textWrap"
        class="btn btn-xs rounded"
        :class="textWrap ? 'btn-secondary text-secondary-content' : 'btn-soft'"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M21 5H3v2h18zM3 19h7v-2H3zm0-6h15c1 0 2 .43 2 2s-1 2-2 2h-2v-2l-4 3l4 3v-2h2c2.95 0 4-1.27 4-4c0-2.72-1-4-4-4H3z"
          />
        </svg>
      </button>
      <!-- options -->
      <button
        @click="logs.length = 0"
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
      <!-- Refresh -->
      <button
        @click="refreshTaskLogs"
        class="btn btn-xs rounded btn-success btn-soft"
      >
        <svg
          class="active:rotate-180 transition transition-transform duration-300"
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

      <!-- Search -->
      <button
        @click="showSearchBar = !showSearchBar"
        class="btn btn-xs rounded btn-success btn-soft"
        :class="{ 'btn-active': showSearchBar }"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 16 16"
        >
          <path
            fill="none"
            stroke="currentColor"
            d="M2 8h3m-3 4.5h4m-4-9h12m-2.479 7.021l2.066 2.066m-1.18-4.131a2.951 2.951 0 1 1-5.902 0a2.951 2.951 0 0 1 5.902 0Z"
            stroke-width="1"
          />
        </svg>
      </button>
    </div>

    <Transition name="slide-down">
      <SearchInput v-if="showSearchBar" v-model="searchText" class="w-full" />
    </Transition>

    <!-- Task Logs -->
    <Loading v-if="isLoading" />
    <div
      v-show="!isLoading"
      ref="logsBoxRef"
      @scroll="onScroll"
      :class="[
        'flex-1 flex flex-col overflow-auto text-sm ',
        textWrap ? 'overflow-x-hidden' : 'overflow-x-auto whitespace-nowrap'
      ]"
    >
      <div
        v-for="log in logsList"
        :key="log.id"
        class="text-base-content animate__animated animate__fadeIn"
      >
        <span
          class="opacity-60 font-bold uppercase px-1"
          :class="logClass(log.level)"
        >
          {{ getLogPrefix(log.level) }}
        </span>

        <span class="opacity-40 px-1">
          <TimeStamp :timestamp="log.timestamp" :showDate="false" />
        </span>

        <span>
          {{ log.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onBeforeMount, onBeforeUnmount, nextTick } from "vue";

  import { fetchTaskLogs } from "@/api/task";
  import { onTaskMessage, offTaskMessage } from "@/api/client";

  import Loading from "@/components/utils/Loading.vue";
  import TimeStamp from "@/components/utils/TimeStamp.vue";

  import SearchInput from "@/components/ui/SearchInput.vue";

  const props = defineProps({
    taskID: {
      type: String,
      required: true
    }
  });

  // UI state
  const searchText = ref("");
  const showSearchBar = ref(false);

  const textWrap = ref(false);
  const logsBoxRef = ref(null);
  const logs = ref([]);
  const isAtBottom = ref(true);
  const isLoading = ref(false);

  function logClass(level) {
    return (
      {
        success: "text-success",
        warning: "text-info",
        error: "text-error"
      }[level] || "text-base-content"
    );
  }

  function getLogPrefix(level) {
    return "➣";
  }

  // computed based on search
  const logsList = computed(() => {
    if (!searchText.value.trim()) {
      return logs.value;
    }

    const query = searchText.value.toLowerCase();

    return logs.value.filter(msg => msg.message.toLowerCase().includes(query));
  });

  // Scroll helpers
  function scrollToBottom() {
    const el = logsBoxRef.value;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }

  // Detect user scrolling
  function onScroll() {
    const el = logsBoxRef.value;
    if (!el) return;

    const threshold = 20;
    isAtBottom.value =
      el.scrollHeight - el.scrollTop - el.clientHeight < threshold;
  }

  // Load all logs
  async function loadLogs() {
    if (isLoading.value) return;

    isLoading.value = true;

    const el = logsBoxRef.value;
    const wasAtBottom = isAtBottom.value;

    const res = await fetchTaskLogs(props.taskID);
    logs.value = res.items ?? res; // support either shape

    await nextTick();

    if (wasAtBottom) {
      scrollToBottom();
    }

    isLoading.value = false;
  }

  // Real-time updates
  async function onMessage(data) {
    if (data.event === "task-log" && data.payload.taskID === props.taskID) {
      logs.value.push(data.payload.log);

      await nextTick();
      if (isAtBottom.value) {
        scrollToBottom();
      }
    }
  }

  // Manual refresh (optional)
  async function refreshTaskLogs() {
    await loadLogs();

    await nextTick();
    scrollToBottom();
  }

  // Lifecycle
  onBeforeMount(async () => {
    onTaskMessage(onMessage);
    await refreshTaskLogs();
  });

  onBeforeUnmount(() => {
    offTaskMessage(onMessage);
  });
</script>
