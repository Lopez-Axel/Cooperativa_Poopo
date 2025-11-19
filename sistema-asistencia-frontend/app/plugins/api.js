// plugins/api.js
export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  const config = useRuntimeConfig()
  
  const api = $fetch.create({
    baseURL: 'http://localhost:8000',
    
    onRequest({ options }) {
      if (authStore.token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${authStore.token}`
        }
      }
    },
    
    onResponseError({ response }) {
      if (response.status === 401) {
        authStore.logout()
      }
    }
  })
  
  return {
    provide: {
      api
    }
  }
})