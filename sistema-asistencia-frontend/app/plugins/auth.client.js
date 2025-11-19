// plugins/auth.client.js
export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  authStore.checkAuth()
})