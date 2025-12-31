<template>
  <span>{{ remaining }}</span>
</template>

<script setup>
  import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";

  const props = defineProps({
    next: {
      type: Number,
      required: true
    }
  });

  const emit = defineEmits(["finished"]);

  const remaining = ref(props.next);
  let timer = null;

  function start() {
    remaining.value = props.next;

    timer = setInterval(() => {
      if (remaining.value > 0) {
        remaining.value -= 1;
      }

      if (remaining.value === 0) {
        clearInterval(timer);
        timer = null;
        emit("finished");
      }
    }, 1000);
  }

  onMounted(start);
  onBeforeUnmount(() => clearInterval(timer));

  // Restart if backend pushes new value
  watch(
    () => props.next,
    () => {
      clearInterval(timer);
      start();
    }
  );
</script>
