import { API_URL } from "./config";

import { useToast } from "vue-toastification";

// Resolve image url
export function resolveImageURL(url) {
  if (!url || url.startsWith("http")) return url;

  return API_URL + url;
}

// Toast a notification
export const toast = (message, type = "info") => {
  const _toast = useToast();

  const func =
    {
      info: _toast.info,
      success: _toast.success,
      warning: _toast.warning,
      error: _toast.error
    }[type] || _toast;

  func(message, {
    position: "top-center",
    timeout: 2031,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: false,
    icon: true,
    rtl: false
  });
};

// Format timestamp
export function formatTimestamp(timestamp) {
  if (!timestamp) return "";
  const now = new Date();
  const date = new Date(timestamp);

  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  // --- Recent times ---
  if (diffSec < 60) {
    return diffSec <= 1 ? "Just now" : `${diffSec} seconds ago`;
  }

  if (diffMin < 60) {
    return `${diffMin} min ago`;
  }

  if (diffHour < 24) {
    return `${diffHour} hours ago`;
  }

  // --- Date formatting helpers ---
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
  const month = months[date.getMonth()];
  const day = date.getDate();

  let hour = date.getHours();
  const minute = date.getMinutes().toString().padStart(2, "0");
  const ampm = hour >= 12 ? "PM" : "AM";
  hour = hour % 12 || 12; // convert to 12-hour clock

  const timeStr = `${hour}:${minute} ${ampm}`;

  const thisYear = now.getFullYear();
  const year = date.getFullYear();

  // --- Today ---
  if (diffDay === 0) {
    return timeStr;
  }

  // --- Yesterday or older within same year ---
  if (year === thisYear) {
    return `${month} ${day} at ${timeStr}`;
  }

  // --- Previous years ---
  return `${year} ${month} ${day} at ${timeStr}`;
}

// Image Extensions
export const IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "svg"];
