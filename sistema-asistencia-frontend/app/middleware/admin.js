// middleware/admin.js
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  
  // Si el store no está inicializado, intentar desde localStorage
  if (!authStore.isAuthenticated && process.client) {
    authStore.initFromLocalStorage()
  }
  
  // Verificar autenticación
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Verificar privilegios de superusuario
  if (!authStore.isSuperuser) {
    return navigateTo('/dashboard')
  }
})