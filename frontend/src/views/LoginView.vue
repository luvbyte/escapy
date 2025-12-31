<template>
  <div class="flex-1 flex items-center justify-center">
    <div class="card w-full max-w-sm bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title justify-center">Escapy Login</h2>

        <form @submit.prevent="login">
          <div class="form-control mt-4">
            <input
              v-model="access_key"
              type="access_key"
              placeholder="Access Key"
              class="input input-bordered focus:outline-none placeholder:opacity-60"
              required
            />
          </div>

          <div class="form-control mt-3">
            <button class="btn btn-primary" :disabled="loading">
              {{ loading ? "Logging in..." : "Login" }}
            </button>
          </div>

          <p v-if="error" class="text-error mt-2 text-sm">
            {{ error }}
          </p>
        </form>
      </div>
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
      // Optional: redirect
      window.location.href = "/";
    } catch (err) {
      error.value = err.message || "Login failed";
    } finally {
      loading.value = false;
    }
  };
</script>
