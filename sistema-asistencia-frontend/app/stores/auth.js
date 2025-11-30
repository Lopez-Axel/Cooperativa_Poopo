// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
    isAuthenticated: false,
    apiUrl: 'https://cooperativapoopo-production-450b.up.railway.app' 
  }),
  
  actions: {
    async login(username, password) {
      try {
        const config = useRuntimeConfig()
        const response = await $fetch(`${this.apiUrl}/api/auth/login`, {
          method: 'POST',
          body: { username, password }
        })
        
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.data?.detail || 'Error al iniciar sesión' 
        }
      }
    },
    
    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      navigateTo('/login')
    },
    
    checkAuth() {
      if (process.client) {
        const token = localStorage.getItem('token')
        const user = localStorage.getItem('user')
        
        if (token && user) {
          this.token = token
          this.user = JSON.parse(user)
          this.isAuthenticated = true
        }
      }
    }
  },
  
  getters: {
    isSuperuser: (state) => state.user?.is_superuser || false,
    username: (state) => state.user?.username || '',
    fullName: (state) => state.user?.full_name || ''
  }
})