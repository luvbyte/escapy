import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";

import "./style.css";
import "animate.css";

import { vSwipe } from "@/directives/swipe.js";
import longPress from "@/directives/longPress";

// main.js
import Toast from "vue-toastification";
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";

const app = createApp(App);

app.directive("swipe", vSwipe);
app.directive("long-press", longPress);

app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 6,
  newestOnTop: true
});
app.use(router);

app.mount("#app");
