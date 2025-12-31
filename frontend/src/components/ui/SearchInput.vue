<template>
  <div class="relative transition-all duration-200">
    <input
      type="search"
      v-model="localValue"
      class="w-full input bg-transparent font-heading placeholder:opacity-60 focus:outline-none"
      :class="getInputSize()"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup>
  import { computed } from "vue";

  const props = defineProps({
    modelValue: {
      type: String,
      default: ""
    },
    placeholder: {
      type: String,
      default: "Search"
    },
    size: {
      type: String,
      required: false
    }
  });

  const getInputSize = () => {
    return (
      {
        xs: "input-xs text-[0.6rem]",
        sm: "input-sm",
        md: "input-md",
        lg: "input-lg"
      }[props.size] || "input-sm"
    );
  };

  const emit = defineEmits(["update:modelValue"]);

  const localValue = computed({
    get: () => props.modelValue,
    set: value => emit("update:modelValue", value)
  });

  function clear() {
    emit("update:modelValue", "");
  }
</script>
