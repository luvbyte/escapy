<template>
  <div class="fullscreen flex flex-col overflow-hidden">
    <div v-if="hasOptions" class="py-2 flex justify-end gap-1">
      <button
        @click="ModuleOptionsRef?.resetOptions"
        class="btn btn-xs btn-ghost rounded"
      >
        RESET
      </button>
      <button
        @click="updateOptions"
        class="btn btn-xs btn-primary btn-outline rounded"
      >
        UPDATE
      </button>
    </div>
    <ModuleOptions
      ref="ModuleOptionsRef"
      :taskID="task.id"
      @options-updated="onOptionsUpdate"
      class="overflow-y-auto"
    />
  </div>
</template>

<script setup>
  import { ref, computed } from "vue";
  import { updateTaskModuleOptions } from "@/api/task";

  import { toast } from "@/api/utils";

  import ModuleOptions from "@/components/ModuleOptions.vue";

  const props = defineProps({
    task: Object
  });

  const hasOptions = ref(false);
  const ModuleOptionsRef = ref(null);

  function onOptionsUpdate(options) {
    hasOptions.value = Object.keys(options).length > 0;
  }

  async function updateOptions() {
    if (!ModuleOptionsRef.value) return;

    const { res } = await updateTaskModuleOptions(
      props.task.id,
      ModuleOptionsRef.value.getOptions()
    );

    if (res === "ok") toast("Successfully Updated");
    else toast("Error updating", "error");
  }
</script>
