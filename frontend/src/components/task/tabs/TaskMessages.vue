<template>
  <div class="flex-1 flex flex-col overflow-hidden text-[11px] gap-2">
    <!-- Toolbar -->
    <div class="flex items-center justify-end py-1 gap-1">
      <div class="flex-1 text-sm font-heading flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <g
            fill="none"
            stroke="currentColor"
            stroke-linejoin="round"
            stroke-width="1"
          >
            <path
              d="M19.5 4.5h-18l3 5v7a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-9a3 3 0 0 0-3-3Z"
            />
            <path stroke-linecap="round" d="M7.5 8h12m-12 3.5h12M7.5 15H16" />
          </g></svg
        >{{ messages.length }}
      </div>
      <!-- Clear Button -->
      <button
        @click="messages.length = 0"
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
        @click="refreshTaskMessages"
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
      <!-- Render HTML Button -->
      <button
        @click="render = !render"
        class="btn btn-xs rounded"
        :class="!render ? 'btn-secondary' : 'btn-soft'"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M19.5 14v-3.343c0-.818 0-1.226-.152-1.594c-.152-.367-.441-.657-1.02-1.235l-4.736-4.736c-.499-.499-.748-.748-1.058-.896a2 2 0 0 0-.197-.082C12.014 2 11.661 2 10.956 2c-3.245 0-4.868 0-5.967.886a4 4 0 0 0-.603.603C3.5 4.59 3.5 6.211 3.5 9.456V14m9-11.5V3c0 2.828 0 4.243.879 5.121C14.257 9 15.672 9 18.5 9h.5M5.5 17v2.5m0 0V22m0-2.5h-3m0-2.5v2.5m0 0V22M9 17v5m0-5H7.5M9 17h1.5m2 5v-5l2 2.5l2-2.5v5m2.5-5v5h2.5"
          />
        </svg>
      </button>
      <!-- Text Wrap Button -->
      <button
        @click="preWrap = !preWrap"
        class="btn btn-xs rounded"
        :class="preWrap ? 'btn-secondary' : 'btn-soft'"
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
      <!-- Search -->
      <button
        @click="showSearchBar = !showSearchBar"
        class="btn btn-xs rounded"
        :class="showSearchBar ? 'btn-success' : 'btn-soft'"
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
    <!-- Messages -->
    <Loading v-if="isLoading" />
    <div
      v-show="!isLoading"
      ref="messagesBoxRef"
      @scroll="onScroll"
      class="flex-1 flex flex-col overflow-auto text-xs"
    >
      <div
        v-for="(message, i) in messagesList"
        class="animate__animated animate__fadeIn"
      >
        <div v-if="render && message.type !== 'text'">
          <!-- render html -->
          <div v-html="sanitizeHTML(message.message)"></div>
        </div>
        <pre v-else :class="{ 'whitespace-pre-wrap break-words': preWrap }">{{
          message.message
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onBeforeMount, onBeforeUnmount, nextTick } from "vue";

  import { fetchTaskMessages } from "@/api/task";
  import { onTaskMessage, offTaskMessage } from "@/api/client";

  import { sanitizeHTML } from "@/api/purify";

  import Loading from "@/components/utils/Loading.vue";
  import SearchInput from "@/components/ui/SearchInput.vue";

  const props = defineProps({
    taskID: {
      type: String,
      required: true
    }
  });

  const render = ref(true);

  // UI state
  const searchText = ref("");
  const showSearchBar = ref(false);

  const preWrap = ref(false);
  const messagesBoxRef = ref(null);
  const messages = ref([]);
  const isAtBottom = ref(true);
  const isLoading = ref(false);

  // computed based on search
  const messagesList = computed(() => {
    if (!searchText.value.trim()) {
      return messages.value;
    }

    const query = searchText.value.toLowerCase();

    return messages.value.filter(msg =>
      msg.message.toLowerCase().includes(query)
    );
  });

  // Scroll helpers
  function scrollToBottom() {
    const el = messagesBoxRef.value;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }

  // Detect user scrolling
  function onScroll() {
    const el = messagesBoxRef.value;
    if (!el) return;

    const threshold = 20;
    isAtBottom.value =
      el.scrollHeight - el.scrollTop - el.clientHeight < threshold;
  }

  // Load all messages
  async function loadMessages() {
    if (isLoading.value) return;

    isLoading.value = true;

    const el = messagesBoxRef.value;
    const wasAtBottom = isAtBottom.value;

    const res = await fetchTaskMessages(props.taskID);
    messages.value = res.items ?? res; // support either shape

    await nextTick();

    if (wasAtBottom) {
      scrollToBottom();
    }

    isLoading.value = false;
  }

  // Real-time updates
  async function onMessage(data) {
    if (data.event === "task-message" && data.payload.taskID === props.taskID) {
      messages.value.push(data.payload.message);

      await nextTick();
      if (isAtBottom.value) {
        scrollToBottom();
      }
    }
  }

  // Manual refresh (optional)
  async function refreshTaskMessages() {
    await loadMessages();

    await nextTick();
    scrollToBottom();
  }

  // Lifecycle
  onBeforeMount(async () => {
    onTaskMessage(onMessage);
    // Load Messages
    await refreshTaskMessages();
  });

  onBeforeUnmount(() => {
    offTaskMessage(onMessage);
  });
</script>
