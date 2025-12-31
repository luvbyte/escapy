<template>
  <time :datetime="isoString">
    {{ formatted }}
  </time>
</template>

<script setup>
  import { computed } from "vue";

  const props = defineProps({
    /**
     * Date | number | ISO string
     */
    timestamp: {
      type: [String, Number, Date],
      required: true
    },

    /**
     * Show year or not (optional)
     */
    showYear: {
      type: Boolean,
      default: false
    },

    /**
     * Show month + day or not (optional)
     */
    showDate: {
      type: Boolean,
      default: true
    }
  });

  const date = computed(() => new Date(props.timestamp));

  const formatted = computed(() => {
    const d = date.value;

    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ];

    const month = months[d.getMonth()];
    const day = d.getDate();
    const year = d.getFullYear();

    let hour = d.getHours();
    const minute = d.getMinutes().toString().padStart(2, "0");
    const ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12 || 12;

    const time = `${hour}:${minute} ${ampm}`;

    const parts = [];

    if (props.showDate) {
      parts.push(`${month} ${day}`);
    }

    if (props.showYear) {
      parts.push(year);
    }

    return parts.length ? `${parts.join(", ")} at ${time}` : time;
  });

  const isoString = computed(() => date.value.toISOString());
  const fullDate = computed(() => date.value.toLocaleString());
</script>
