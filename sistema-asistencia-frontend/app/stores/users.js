// stores/users.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useUsersStore = defineStore('users', {
  state: () => ({
    users: [],
    loading: false,
    error: null,
    pagination: {
      skip: 0,
      limit: 20,
      total: 0
    },
    filters: {
      search: '',
      is_active: null,
      is_superuser: null
    }
  }),
  
  actions: {
    async fetchUsers() {
      this.loading = true
      this.error = null
      
      try {
        const config = useRuntimeConfig()
        const authStore = useAuthStore()
        
        const params = new URLSearchParams({
          skip: this.pagination.skip.toString(),
          limit: this.pagination.limit.toString()
        })
        
        if (this.filters.search) {
          params.append('search', this.filters.search)
        }
        if (this.filters.is_active !== null) {
          params.append('is_active', this.filters.is_active.toString())
        }
        if (this.filters.is_superuser !== null) {
          params.append('is_superuser', this.filters.is_superuser.toString())
        }
        
        const response = await $fetch(`${authStore.apiUrl}/api/users?${params}`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.users = response
        this.loading = false
      } catch (error) {
        this.error = error.data?.detail || 'Error al cargar usuarios'
        this.loading = false
        console.error('Error fetching users:', error)
      }
    },
    
    async createUser(userData) {
      try {
        const config = useRuntimeConfig()
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/users/`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${authStore.token}`
          },
          body: userData
        })
        
        await this.fetchUsers()
        return { success: true, data: response }
      } catch (error) {
        return { 
          success: false, 
          error: error.data?.detail || 'Error al crear usuario' 
        }
      }
    },
    
    async updateUser(userId, userData) {
      try {
        const config = useRuntimeConfig()
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/users/${userId}`, {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${authStore.token}`
          },
          body: userData
        })
        
        await this.fetchUsers()
        return { success: true, data: response }
      } catch (error) {
        return { 
          success: false, 
          error: error.data?.detail || 'Error al actualizar usuario' 
        }
      }
    },
    
    async deleteUser(userId) {
      try {
        const config = useRuntimeConfig()
        const authStore = useAuthStore()
        
        await $fetch(`${authStore.apiUrl}/api/users/${userId}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        await this.fetchUsers()
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.data?.detail || 'Error al eliminar usuario' 
        }
      }
    },
    
    setSearch(search) {
      this.filters.search = search
      this.pagination.skip = 0
    },
    
    setActiveFilter(value) {
      this.filters.is_active = value
      this.pagination.skip = 0
    },
    
    setSuperuserFilter(value) {
      this.filters.is_superuser = value
      this.pagination.skip = 0
    },
    
    nextPage() {
      if (this.users.length === this.pagination.limit) {
        this.pagination.skip += this.pagination.limit
      }
    },
    
    prevPage() {
      if (this.pagination.skip > 0) {
        this.pagination.skip = Math.max(0, this.pagination.skip - this.pagination.limit)
      }
    },
    
    resetFilters() {
      this.filters = {
        search: '',
        is_active: null,
        is_superuser: null
      }
      this.pagination.skip = 0
    }
  },
  
  getters: {
    currentPage: (state) => Math.floor(state.pagination.skip / state.pagination.limit) + 1,
    hasNextPage: (state) => state.users.length === state.pagination.limit,
    hasPrevPage: (state) => state.pagination.skip > 0
  }
})