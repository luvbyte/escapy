<template>
  <div
    ref="boxRef"
    @scroll="onScroll"
    class="flex-1 flex flex-col overflow-auto text-xs"
  >
    <slot />
  </div>
</template>

<script setup>
  import { ref } from "vue";

  const boxRef = ref(null);
  const isAtBottom = ref(true);

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

  defineExpose({ scrollToBottom, isAtBottom });
</script>
