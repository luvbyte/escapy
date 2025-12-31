<template>
  <div
    class="flex-1 flex flex-col gap-2 overflow-hidden"
    :class="{ 'fixed inset-0 p-2 z-20 bg-base-100 ': fullScreen }"
  >
    <!-- Sudo Commands -->
    <div
      ref="messagesRef"
      class="rounded flex-1 flex flex-col overflow-y-auto border border-base-content/20 text-[11px] p-2 font-mono"
      @scroll="onScroll"
    >
      <div
        v-for="(message, index) in messages"
        :key="index"
        v-html="message"
        class="animate__animated animate__fadeIn"
      ></div>
    </div>
    <div class="flex items-center gap-2">
      <button
        @click="fullScreen = !fullScreen"
        class="py-1 flex items-center opacity-80"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M3 21v-5h2v3h3v2zm13 0v-2h3v-3h2v5zM3 8V3h5v2H5v3zm16 0V5h-3V3h5v5z"
          />
        </svg>
      </button>
      <input
        v-model="textInput"
        @keyup.enter="run"
        class="flex-1 input input-sm text-sm opacity-80 bg-transparent focus:outline-none px-2 placeholder:opacity-40"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false"
        inputmode="text"
        placeholder="Type here..."
      />

      <Transition name="slide-left">
        <button v-if="textInput.trim() !== ''" @click="run" class="py-1">
          <svg
            v-if="waiting"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8A8 8 0 0 1 12 20Z"
              opacity="0.5"
            />
            <path
              fill="currentColor"
              d="M20 12h2A10 10 0 0 0 12 2V4A8 8 0 0 1 20 12Z"
            >
              <animateTransform
                attributeName="transform"
                dur="1s"
                from="0 12 12"
                repeatCount="indefinite"
                to="360 12 12"
                type="rotate"
              />
            </path>
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <g fill="none">
              <path
                fill="currentColor"
                d="m7.24 4.535l11.944 5.658c1.525.722 1.525 2.892 0 3.614L7.24 19.466c-1.415.67-3.017-.472-2.844-2.028l.58-5.216a2 2 0 0 0 0-.442l-.58-5.216c-.173-1.557 1.429-2.7 2.844-2.029"
                opacity="0.16"
              />
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m5 12l-.604-5.437C4.223 5.007 5.825 3.864 7.24 4.535l11.944 5.658c1.525.722 1.525 2.892 0 3.614L7.24 19.466c-1.415.67-3.017-.472-2.844-2.028zm0 0h7"
              />
            </g>
          </svg>
        </button>
      </Transition>
    </div>
  </div>
</template>

<script setup>
  import { ref, onBeforeMount, nextTick } from "vue";
  import { sanitizeHTML } from "@/api/purify";
  import { runTaskShellCommand } from "@/api/task";

  const props = defineProps({
    taskID: String
  });

  const fullScreen = ref(false);
  const textInput = ref("");
  const messages = ref([]);

  const messagesRef = ref();
  const isAtBottom = ref(true);

  const waiting = ref(false);

  // ScrollBottom
  function scrollToBottom() {
    const el = messagesRef.value;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }

  // Detect user scrolling
  function onScroll() {
    const el = messagesRef.value;
    if (!el) return;

    const threshold = 20;
    isAtBottom.value =
      el.scrollHeight - el.scrollTop - el.clientHeight < threshold;
  }

  // clear messages
  const clear = () => {
    messages.value.length = 0;
  };

  async function _run(command, heading = true) {
    if (command.trim() === "") return;

    waiting.value = true;

    const { res, cmd, result } = await runTaskShellCommand(
      props.taskID,
      command
    );

    //
    if (heading) {
      messages.value.push(
        `<div class='divider divider-start my-2 opacity-80'>${cmd}</div>`
      );
    }

    if (res === "ok") {
      messages.value.push(sanitizeHTML(result));
    } else {
      messages.value.push(
        sanitizeHTML(`<div class='text-error'>Error: ${result}</div>`)
      );
    }

    await nextTick();
    // scroll bottom
    if (isAtBottom) {
      scrollToBottom();
    }

    waiting.value = false;
  }

  // run command
  async function run() {
    const command = textInput.value.trim();

    if (command === "") return;

    if (command === "clear") clear();
    else await _run(textInput.value);

    textInput.value = "";
  }

  onBeforeMount(async () => {
    await _run("intro", false);
  });
</script>
