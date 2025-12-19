// middleware/auth.js
export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = useAuthStore()
  
  // Si no está autenticado, intentar cargar desde storage primero
  if (!authStore.isAuthenticated) {
    await authStore.initFromStorage()
  }
  
  // Si después de intentar cargar aún no está autenticado, redirigir
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Validar token periódicamente
  const lastCheck = sessionStorage.getItem('lastTokenCheck')
  const now = Date.now()
  
  if (!lastCheck || now - parseInt(lastCheck) > 5 * 60 * 1000) {
    const isValid = await authStore.validateToken()
    if (!isValid) {
      return navigateTo('/login')
    }
    sessionStorage.setItem('lastTokenCheck', now.toString())
  }
})