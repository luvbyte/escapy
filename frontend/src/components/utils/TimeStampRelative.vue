<template>
  <span>{{ formattedTime }}</span>
</template>

<script setup>
  import { computed, ref, watch, onMounted, onUnmounted } from "vue";
  import { formatTimestamp } from "@/api/utils";

  const props = defineProps({
    timestamp: {
      type: [String, Number, Date],
      required: true
    }
  });

  const now = ref(Date.now());
  let interval = null;

  /* ---------------------------
   Smart interval calculation
---------------------------- */
  function getIntervalDelay(timestamp) {
    const age = Math.abs(Date.now() - new Date(timestamp).getTime());

    if (age < 60_000) return 3_000; // < 1 min
    if (age < 3_600_000) return 30_000; // < 1 hour
    if (age < 86_400_000) return 300_000; // < 1 day

    return null; // too old → no updates
  }

  /* ---------------------------
   Interval control
---------------------------- */
  function startInterval() {
    stopInterval();

    if (document.hidden) return;

    const delay = getIntervalDelay(props.timestamp);
    if (!delay) return;

    interval = setInterval(() => {
      now.value = Date.now();
    }, delay);
  }

  function stopInterval() {
    if (interval) {
      clearInterval(interval);
      interval = null;
    }
  }

  /* ---------------------------
   Visibility handling
---------------------------- */
  function handleVisibilityChange() {
    if (document.hidden) {
      stopInterval();
    } else {
      // Sync immediately when tab becomes active
      now.value = Date.now();
      startInterval();
    }
  }

  /* ---------------------------
   Lifecycle
---------------------------- */
  onMounted(() => {
    document.addEventListener("visibilitychange", handleVisibilityChange);
    startInterval();
  });

  onUnmounted(() => {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
    stopInterval();
  });

  watch(() => props.timestamp, startInterval);

  /* ---------------------------
   Computed
---------------------------- */
  const formattedTime = computed(() => {
    now.value; // reactive trigger
    return formatTimestamp(props.timestamp);
  });
</script>
