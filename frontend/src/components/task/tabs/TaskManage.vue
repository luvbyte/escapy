<template>
  <div class="flex-1">
    <div class="divider">ACCESS KEYS</div>

    <div v-if="accessKeys" class="flex flex-wrap gap-1 whitespace-nowrap">
      <div
        v-for="key in accessKeys"
        class="flex gap-1 overflow-x-scroll scrollbar-hide"
      >
        <button
          class="text-xs btn btn-xs btn-primary font-heading font-semibold"
          :class="{ 'opacity-40': !key.active }"
          @click="toggleKey(key, key.active)"
        >
          {{ key.name }}
        </button>
      </div>
    </div>

    <div class="divider">Export</div>
    <div class="flex flex-col gap-2">
      <button class="btn btn-sm btn-info w-full" disabled>DOWNLOAD</button>
      <button class="btn btn-sm btn-success btn-outline w-full" disabled>
        BACKUP
      </button>
    </div>

    <div class="divider">Danger</div>
    <div class="flex flex-col gap-2">
      <button
        class="btn btn-sm btn-error w-full"
        :disabled="loading.reset"
        @click="debouncedReset"
      >
        RESET
      </button>

      <button
        class="btn btn-sm btn-error btn-outline w-full"
        :disabled="loading.delete"
        @click="debouncedDelete"
      >
        DELETE
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref, onBeforeMount, reactive } from "vue";
  import {
    deleteTask,
    resetTask,
    fetchTaskAccessKeys,
    updateTaskAccessKeys
  } from "@/api/task";
  import { toast } from "@/api/utils";
  import { debounce } from "lodash-es";

  import { useRouter, useRoute } from "vue-router";

  const router = useRouter();

  const props = defineProps({
    task: {
      type: Object,
      required: true
    }
  });

  const accessKeys = ref(null);
  const loading = ref({
    reset: false,
    delete: false
  });

  const debouncedUpdateKeys = debounce(async () => {
    try {
      await updateTaskAccessKeys(props.task.id, accessKeys.value);
    } catch (err) {
      toast(err, "error");
    }
  }, 500);

  function toggleKey(key, active) {
    const index = accessKeys.value.indexOf(key);
    if (index === -1) return;

    accessKeys.value[index].active = !active;
    debouncedUpdateKeys();
  }

  // Safety
  function onDeleteTask() {
    router.push({
      name: "home"
    });
  }

  async function handleAction(
    action,
    apiCall,
    successMessage,
    onSuccess = null
  ) {
    if (loading.value[action]) return;

    loading.value[action] = true;
    try {
      const { res } = await apiCall(props.task.id);
      if (res === "ok") {
        toast(successMessage, "success");
        onSuccess && onSuccess();
      }
    } catch (err) {
      toast(err, "error");
    } finally {
      loading.value[action] = false;
    }
  }

  // Debounced versions
  const debouncedReset = debounce(
    () => handleAction("reset", resetTask, "Task Reset"),
    2000,
    { leading: true, trailing: false }
  );

  const debouncedDelete = debounce(
    () => handleAction("delete", deleteTask, "Task Deleted", onDeleteTask),
    500,
    { leading: true, trailing: false }
  );

  onBeforeMount(async () => {
    accessKeys.value = await fetchTaskAccessKeys(props.task.id);
  });
</script>
