import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import TaskView from "@/views/TaskView.vue";
import TaskManage from "@/views/TaskManage.vue";
import LoginView from "@/views/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: HomeView,
      name: "home"
    },
    {
      path: "/task/:id",
      component: TaskView,
      name: "task"
    },
    {
      path: "/manage/:id?",
      component: TaskManage,
      name: "manage"
    },
    {
      path: "/login",
      component: LoginView,
      name: "login"
    }
  ]
});

export default router;
