<script setup>
  import { ref, onBeforeMount, onMounted } from "vue";

  import { connect } from "@/api/client";
  import { healthCheck } from "@/api";

  import { applyTheme, getTheme } from "@/api/config";

  const health = ref(null);

  onBeforeMount(async () => {
    health.value = await healthCheck();
    if (health.value) {
      connect();
    }
  });

  onMounted(() => {
    applyTheme(getTheme())
  });
</script>

<template>
  <div id="main">
    <Transition name="fade">
      <div
        v-if="!health"
        class="h-dvh bg-base-100 flex flex-col justify-center items-center"
      >
        <!-- loading -->
        <div v-if="health === false">SERVER NOT RESPONDING</div>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="64"
          height="64"
          viewBox="0 0 24 24"
        >
          <circle cx="18" cy="12" r="0" fill="currentColor">
            <animate
              attributeName="r"
              begin=".67"
              calcMode="spline"
              dur="1.5s"
              keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
              repeatCount="indefinite"
              values="0;2;0;0"
            />
          </circle>
          <circle cx="12" cy="12" r="0" fill="currentColor">
            <animate
              attributeName="r"
              begin=".33"
              calcMode="spline"
              dur="1.5s"
              keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
              repeatCount="indefinite"
              values="0;2;0;0"
            />
          </circle>
          <circle cx="6" cy="12" r="0" fill="currentColor">
            <animate
              attributeName="r"
              begin="0"
              calcMode="spline"
              dur="1.5s"
              keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8"
              repeatCount="indefinite"
              values="0;2;0;0"
            />
          </circle>
        </svg>
      </div>
      <div v-else class="h-dvh flex flex-col font-body">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </Transition>
  </div>
</template>
