<template>
  <Loading v-if="!loaded" class="text-primary" />
  <iframe
    v-show="loaded"
    :src
    @load="loaded = true"
    class="fullscreen overflow-hidden"
  ></iframe>
</template>

<script setup>
  import { ref } from "vue";
  import Loading from "@/components/utils/Loading.vue";
  const loaded = ref(false);

  defineProps(["src"]);
</script>
