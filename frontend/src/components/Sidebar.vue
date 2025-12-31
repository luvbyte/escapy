<template>
  <div @click.self="close" class="fixed z-20 inset-0 fullscreen">
    <div class="w-[80%] h-full flex flex-col p-2 bg-base-200 shadow-xl">
      <pre
        class="text-[0.6rem] flex flex-col pt-8 flex justify-center items-center"
      >
___________ _________                           
\_   _____//   _____/ ____ _____  ______ ___.__.
 |    __)_ \_____  \_/ ___\\__  \ \____ <   |  |
 |        \/        \  \___ / __ \|  |_> >___  |
/_______  /_______  /\___  >____  /   __// ____|
        \/        \/     \/     \/|__|   \/     
</pre
      >
      <p class="text-xs text-center font-mono py-4 pb-6">
        {{ info.version }}
      </p>
      <!-- themes -->
      <div class="flex flex-col overflow-hidden text-xs">
        <div class="divider m-0 uppercase">Theme - {{ currentTheme }}</div>
        <div
          class="rounded grid grid-rows-2 grid-flow-col space-x-1 space-y-1 py-2 overflow-x-auto scrollbar-hide"
        >
          <div
            v-for="theme in themes"
            :data-theme="theme"
            @click="setTheme(theme)"
            class="w-12 h-12 shrink-0 rounded-full base-border flex items-center justify-center gap-1 p-1 active:border-base-content"
          >
            <div class="w-1 h-4 bg-primary rounded"></div>
            <div class="w-1 h-4 bg-secondary rounded"></div>
            <div class="w-1 h-4 bg-info rounded"></div>
            <div class="w-1 h-4 bg-primary rounded"></div>
          </div>
        </div>
        <div class="divider m-0"></div>
      </div>

      <div class="flex-1">
        <div v-if="info" class="fullscreen flex flex-col opacity-60">
          <!-- Modules count -->
          <div class="flex justify-between">
            <span>Available Modules</span>
            <span>{{ info.installed_modules_count }}</span>
          </div>
          <!-- Running count -->
          <div class="flex justify-between">
            <span>Active Tasks</span>
            <span>{{ info.tasks_count }}</span>
          </div>
          <!-- Running count -->
          <div class="flex justify-between">
            <span>Completed Tasks</span>
            <span>{{ info.completed_tasks_count }}</span>
          </div>
        </div>
      </div>

      <!-- footer -->
      <pre class="flex justify-center items-center text-xs">
        
♡  ∩_∩
 （„• ֊ •„)♡
┏ • UU • - • - • - • - • - • - • ღ❦ღ┓</pre
      >
      <div class="text-sm text-center my-4">
        <span class="text-info">Escapy</span> ツ
        <span class="text-success">{{ info.author }} ᥫ᭡</span>
      </div>
      <pre class="flex justify-center items-center text-xs">
┗ღ❦ღ • - • - • - • - • - • -- •- •  ┛
      </pre>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, onBeforeMount } from "vue";
  import { fetchInfo } from "@/api";

  import { getTheme, applyTheme } from "@/api/config";

  defineProps(["close"]);

  // Daisyui themes
  const themes = [
    "retro",
    "dracula",
    "light",
    "black",
    "dark",
    "cupcake",
    "bumblebee",
    "emerald",
    "corporate",
    "synthwave",
    "valentine",
    "halloween",
    "garden",
    "forest",
    "lofi",
    "pastel",
    "fantasy",
    "wireframe",
    "luxury",
    "dim",
    "cmyk",
    "autumn",
    "business",
    "acid",
    "lemonade",
    "night",
    "coffee",
    "winter",
    "nord",
    "sunset",
    "caramellatte",
    "abyss",
    "silk"
  ];

  const currentTheme = ref(getTheme());
  const info = ref({});

  function setTheme(name) {
    applyTheme(name);
    currentTheme.value = name;
  }

  onMounted(async () => {
    applyTheme(currentTheme.value);
    // fetch info
    info.value = await fetchInfo();
  });
</script>
