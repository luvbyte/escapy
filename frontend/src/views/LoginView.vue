<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 px-4">
    <div class="w-full max-w-sm space-y-6">
      <h2 class="text-2xl font-semibold text-center">Escapy Login</h2>

      <form @submit.prevent="login" class="space-y-4">
        <input
          v-model="access_key"
          type="password"
          placeholder="Access Key (1234)"
          class="input input-bordered w-full focus:outline-none placeholder:opacity-60"
          required
        />

        <button class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>

        <p v-if="error" class="text-error text-sm text-center">
          {{ error }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { api } from "@/api/config";

  const access_key = ref("");
  const loading = ref(false);
  const error = ref("");

  const login = async () => {
    loading.value = true;
    error.value = "";

    try {
      await api.post("/login", {
        access_key: access_key.value
      });

      window.location.href = "/";
    } catch (err) {
      error.value = err.message || "Login failed";
    } finally {
      loading.value = false;
    }
  };
</script>
