// plugins/auth.client.js
export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  
  // Inicializar desde localStorage cuando carga la app
  authStore.initFromLocalStorage()
})