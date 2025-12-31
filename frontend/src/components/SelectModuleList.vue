<script setup>
  import { ref, computed } from "vue";
  import { resolveImageURL } from "@/api/utils";

  import SearchInput from "@/components/ui/SearchInput.vue";

  const props = defineProps({
    modules: {
      type: Object,
      required: true
    },
    selectModule: {
      type: Function,
      required: true
    }
  });

  const searchText = ref("");

  const modulesList = computed(() => {
    if (!searchText.value) return props.modules;

    const query = searchText.value.toLowerCase();

    return Object.fromEntries(
      Object.entries(props.modules).filter(
        ([_, module]) =>
          module.name?.toLowerCase().includes(query) ||
          module.title?.toLowerCase().includes(query) ||
          module.author?.toLowerCase().includes(query)
      )
    );
  });
</script>

<template>
  <!-- Modules Select -->
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- Search -->
    <SearchInput v-model="searchText" class="p-2 glass bg-secondary/60 text-secondary-content" />
    <!-- Modules List -->
    <div class="flex-1 overflow-y-auto">
      <div
        v-for="(module, name) in modulesList"
        @click="selectModule(module)"
        :key="module.name"
        class="border-b border-base-content/20 flex items-center text-sm gap-2 p-1 px-2"
      >
        <img :src="resolveImageURL(module.icon)" class="w-16 h-16 rounded" />
        <div>
          <span class="font-heading font-semibold">
            {{ module.title }}
          </span>
          <div class="flex items-center gap-1">
            <span class="opacity-40">{{ module.name }}</span>
            •
            <span class="opacity-80">{{ module.author }}</span>
          </div>
          <div class="opacity-40 truncate">{{ module.about }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
