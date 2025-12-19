// stores/secciones.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import Fuse from 'fuse.js'

export const useSeccionesStore = defineStore('secciones', {
  state: () => ({
    secciones: [],
    loading: false,
    error: null,
    filters: {
      is_active: null,
      searchQuery: ''
    }
  }),

  actions: {
// stores/secciones.js
async fetchSecciones() {
  this.loading = true
  this.error = null
  
  try {
    const authStore = useAuthStore()
    
    const url = `${authStore.apiUrl}/api/secciones`
    
    const response = await $fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      // Evitar que Nuxt modifique la URL
      baseURL: '',
      // Deshabilitar cualquier interceptor
      retry: false,
      onRequest({ request, options }) {
        console.log('📤 Request URL:', request)
      }
    })
    
    this.secciones = response
  } catch (error) {
    console.error('❌ Error:', error)
    this.error = error.data?.detail || 'Error al cargar secciones'
    throw error
  } finally {
    this.loading = false
  }
},

    async createSeccion(seccionData) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        
        // SIN trailing slash
        const response = await $fetch(`${authStore.apiUrl}/api/secciones`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: seccionData
        })
        
        this.secciones.push(response)
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al crear sección'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateSeccion(id, seccionData) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        
        // SIN trailing slash
        const response = await $fetch(`${authStore.apiUrl}/api/secciones/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: seccionData
        })
        
        const index = this.secciones.findIndex(s => s.id === id)
        if (index !== -1) {
          this.secciones[index] = response
        }
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al actualizar sección'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteSeccion(id) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        
        // SIN trailing slash - soft delete usando PUT
        await $fetch(`${authStore.apiUrl}/api/secciones/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: { is_active: false }
        })
        
        const seccion = this.secciones.find(s => s.id === id)
        if (seccion) {
          seccion.is_active = false
        }
        
        return true
      } catch (error) {
        this.error = error.data?.detail || 'Error al desactivar sección'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getSeccionDetails(id) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        
        // SIN trailing slash
        const response = await $fetch(`${authStore.apiUrl}/api/secciones/${id}/details`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al cargar detalles de sección'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCooperativistasActivos() {
      try {
        const authStore = useAuthStore()
        
        // SIN trailing slash
        const response = await $fetch(`${authStore.apiUrl}/api/cooperativistas/active`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        return response
      } catch (error) {
        throw error
      }
    },

    setSearchQuery(query) {
      this.filters.searchQuery = query
    },

    setActiveFilter(value) {
      this.filters.is_active = value
    },

    resetFilters() {
      this.filters = {
        is_active: null,
        searchQuery: ''
      }
    }
  },

  getters: {
    seccionesFiltradas: (state) => {
      let filtered = state.secciones

      if (state.filters.is_active !== null) {
        filtered = filtered.filter(s => s.is_active === state.filters.is_active)
      }

      if (state.filters.searchQuery.trim() !== '') {
        const fuse = new Fuse(filtered, {
          keys: ['nombre'],
          threshold: 0.3,
          includeScore: true
        })
        
        const results = fuse.search(state.filters.searchQuery)
        filtered = results.map(result => result.item)
      }

      return filtered
    },

    hasActiveFilters: (state) => {
      return state.filters.is_active !== null || state.filters.searchQuery.trim() !== ''
    }
  }
})