<template>
  <div class="flex flex-col">
    <div
      v-for="(option, name) in options"
      :key="name"
      class="w-full flex flex-col"
    >
      <!-- Label -->
      <label class="divider mt-2 opacity-60">
        {{ option.label }}
      </label>

      <!-- Text Input -->
      <input
        v-if="option.type === 'input'"
        :type="option.itype"
        v-model="option.value"
        @input="onOptionChange(name, option)"
        class="w-full input input-sm bg-transparent focus:outline-none placeholder:opacity-60"
        :placeholder="option.placeholder"
        :required="option.required"
        :minlength="option.minlength"
        :maxlength="option.maxlength"
        :pattern="option.pattern"
      />

      <!-- Textarea -->
      <textarea
        v-else-if="option.type === 'textarea'"
        v-model="option.value"
        @input="onOptionChange(name, option)"
        class="w-full textarea textarea-sm bg-transparent focus:outline-none placeholder:opacity-60"
        rows="3"
        :placeholder="option.placeholder"
        :required="option.required"
        :minlength="option.minlength"
        :maxlength="option.maxlength"
      ></textarea>

      <!-- Color -->
      <input
        v-else-if="option.type === 'color'"
        type="color"
        v-model="option.value"
        @input="onOptionChange(name, option)"
        class="w-10 h-8 border rounded cursor-pointer"
      />

      <!-- Number -->
      <input
        v-else-if="option.type === 'number'"
        type="number"
        v-model.number="option.value"
        @change="onOptionChange(name, option)"
        class="w-full input input-sm bg-transparent focus:outline-none placeholder:opacity-60"
        :placeholder="option.placeholder"
        :min="option.min"
        :max="option.max"
        :step="option.step || 1"
      />

      <!-- Range -->
      <input
        v-else-if="option.type === 'range'"
        type="range"
        v-model.number="option.value"
        :min="option.min"
        :max="option.max"
        :step="option.step || 1"
        @input="onOptionChange(name, option)"
      />

      <!-- Select -->
      <select
        v-else-if="option.type === 'select'"
        v-model="option.value"
        @change="onOptionChange(name, option)"
        class="select select-sm bg-transparent w-full"
        :required="option.required"
      >
        <option value="" disabled>Select...</option>
        <option v-for="(opt, label) in option.options" :key="opt" :value="opt">
          {{ label }}
        </option>
      </select>

      <!-- Checkbox -->
      <label
        v-else-if="option.type === 'checkbox'"
        class="flex items-center gap-2 cursor-pointer"
      >
        <input
          type="checkbox"
          v-model="option.value"
          @change="onOptionChange(name, option)"
          class="checkbox checkbox-sm"
        />
        <span>{{ option.label }}</span>
      </label>

      <!-- Toggle -->
      <label
        v-else-if="option.type === 'toggle'"
        class="flex items-center gap-2 cursor-pointer"
      >
        <input
          type="checkbox"
          v-model="option.value"
          @change="onOptionChange(name, option)"
          class="toggle toggle-sm"
        />
        <span>{{ option.label }}</span>
      </label>

      <!-- Flag (Boolean CLI flag) -->
      <label
        v-else-if="option.type === 'flag'"
        class="flex items-center justify-between gap-3 cursor-pointer"
      >
        <div class="flex flex-col">
          <span class="text-sm pl-1">
            {{ option.label }}
            <span class="opacity-50 ml-1 font-mono text-xs">
              {{ option.prefix }}
            </span>
          </span>
        </div>

        <input
          type="checkbox"
          v-model="option.value"
          @change="onOptionChange(name, option)"
          class="toggle"
        />
      </label>

      <!-- Unknown -->
      <div v-else class="text-red-500 text-xs">
        Unknown option type: {{ option.type }}
      </div>

      <!-- Info -->
      <p class="p-1 text-xs opacity-60">{{ option.info }}</p>

      <!-- Error -->
      <p v-if="errors[name]" class="text-xs text-error px-1">
        {{ errors[name] }}
      </p>
    </div>
  </div>
</template>

<script setup>
  import { reactive, onBeforeMount } from "vue";
  import { getModuleOptions } from "@/api/module";
  import { getTaskModuleOptions } from "@/api/task";

  // moduleName for creating
  // taskID for updating
  const props = defineProps({
    moduleName: {
      type: String,
      required: false
    },
    taskID: {
      type: String,
      required: false
    }
  });

  const emit = defineEmits(["options-updated"]);

  /* -------------------- STATE -------------------- */
  const options = reactive({});
  const errors = reactive({});

  /* -------------------- DEBOUNCE -------------------- */
  function debounce(fn, delay = 500) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  }

  const debouncedValidators = {};

  /* -------------------- VALIDATION -------------------- */
  function validateOption(name, option) {
    let error = "";

    if (option.required) {
      const empty =
        option.value === null ||
        option.value === undefined ||
        option.value === "";
      if (empty) error = "This field is required";
    }

    if (!error && option.minlength && option.value?.length < option.minlength) {
      error = `Minimum ${option.minlength} characters`;
    }

    if (!error && option.maxlength && option.value?.length > option.maxlength) {
      error = `Maximum ${option.maxlength} characters`;
    }

    if (!error && option.pattern) {
      const re = new RegExp(option.pattern);
      if (!re.test(option.value)) error = "Invalid format";
    }

    if (!error && typeof option.validate === "function") {
      const result = option.validate(option.value);
      if (result !== true) error = result;
    }

    errors[name] = error;
  }

  /* -------------------- HANDLERS -------------------- */
  function onOptionChange(name, option) {
    if (!debouncedValidators[name]) {
      debouncedValidators[name] = debounce((n, o) => validateOption(n, o), 500);
    }

    debouncedValidators[name](name, option);
  }

  /* -------------------- FETCH -------------------- */
  async function fetchOptions() {
    let data = {};
    if (props.taskID) {
      data = await getTaskModuleOptions(props.taskID);
    } else {
      data = await getModuleOptions(props.moduleName);
    }

    // Emiting
    emit("options-updated", data);

    Object.assign(
      options,
      Object.fromEntries(
        Object.entries(data).map(([name, option]) => [
          name,
          {
            ...option,
            serverValue: option.value
          }
        ])
      )
    );
  }

  /* -------------------- EXPOSE -------------------- */
  function getOptionsOriginal() {
    // Immediate (non-debounced) validation on submit
    Object.entries(options).forEach(([name, option]) =>
      validateOption(name, option)
    );

    if (Object.values(errors).some(Boolean)) return null;

    // - \/
    return Object.fromEntries(
      Object.entries(options).map(([key, option]) => {
        const { prefix, value } = option;

        // If flag type
        if (option.type === "flag") {
          return [key, prefix && value ? prefix : ""];
        }

        // prefix + value or value
        return [key, prefix && value ? `${prefix} ${value}` : value];
      })
    );
  }

  function getOptions() {
    // Validate first
    Object.entries(options).forEach(([name, option]) =>
      validateOption(name, option)
    );

    if (Object.values(errors).some(Boolean)) return null;

    return Object.fromEntries(
      Object.entries(options).map(([key, option]) => {
        const { prefix, value, type } = option;

        let result = "";

        if (type === "flag") {
          result = prefix && value ? prefix : "";
        } else {
          result = prefix && value ? `${prefix} ${value}` : value;
        }

        return [
          key,
          {
            value: option.value,
            result
          }
        ];
      })
    );
  }

  const resetOptions = () => {
    // Reset options
    fetchOptions();
  };

  defineExpose({ getOptions, resetOptions, options });

  onBeforeMount(fetchOptions);
</script>
