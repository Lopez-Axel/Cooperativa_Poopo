// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  
  // Si el store no está inicializado, intentar desde localStorage
  if (!authStore.isAuthenticated && process.client) {
    authStore.initFromLocalStorage()
  }
  
  // Si aún no está autenticado, redirigir a login
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
})