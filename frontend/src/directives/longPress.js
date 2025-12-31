export default {
  mounted(el, binding) {
    const delay = binding.arg ? Number(binding.arg) : 500;
    let timer = null;
    let longPressed = false;

    const start = e => {
      longPressed = false;

      timer = setTimeout(() => {
        longPressed = true;
        binding.value(e);

        // prevent click after long press
        e.preventDefault();
        e.stopPropagation();
      }, delay);
    };

    const cancel = e => {
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }

      if (longPressed) {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    // Mouse
    el.addEventListener("mousedown", start);
    el.addEventListener("mouseup", cancel);
    el.addEventListener("mouseleave", cancel);

    // Touch
    el.addEventListener("touchstart", start, { passive: false });
    el.addEventListener("touchend", cancel);
    el.addEventListener("touchmove", cancel);

    el._longPressCleanup = () => {
      el.removeEventListener("mousedown", start);
      el.removeEventListener("mouseup", cancel);
      el.removeEventListener("mouseleave", cancel);
      el.removeEventListener("touchstart", start);
      el.removeEventListener("touchend", cancel);
      el.removeEventListener("touchmove", cancel);
    };
  },

  unmounted(el) {
    el._longPressCleanup?.();
  }
};
