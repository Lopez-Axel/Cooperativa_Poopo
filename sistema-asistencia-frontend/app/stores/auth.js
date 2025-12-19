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
        const response = await $fetch(`${this.apiUrl}/api/auth/login`, {
          method: 'POST',
          body: { username, password }
        })
        
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        
        if (process.client) {
          sessionStorage.setItem('token', response.access_token)
          sessionStorage.setItem('user', JSON.stringify(response.user))
        }
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.data?.detail || 'Error al iniciar sesión' 
        }
      }
    },
    
    async validateToken() {
      if (!this.token) return false
      
      try {
        const response = await $fetch(`${this.apiUrl}/api/users/me`, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })
        
        this.user = response
        return true
      } catch (error) {
        console.log('Token inválido:', error)
        this.logout()
        return false
      }
    },
    
    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      if (process.client) {
        sessionStorage.removeItem('token')
        sessionStorage.removeItem('user')
      }
      
      navigateTo('/login')
    },
    
    async initFromStorage() {
      if (!process.client) return
      
      const token = sessionStorage.getItem('token')
      const user = sessionStorage.getItem('user')
      
      if (!token || !user) return
      
      // Carga el estado temporal
      this.token = token
      this.user = JSON.parse(user)
      this.isAuthenticated = true
      
      // Valida que el token sigue siendo válido en el backend
      await this.validateToken()
    }
  },
  
  getters: {
    isSuperuser: (state) => state.user?.is_superuser || false,
    username: (state) => state.user?.username || '',
    fullName: (state) => state.user?.full_name || ''
  }
})