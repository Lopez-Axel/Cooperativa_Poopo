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
      is_active: null, // null = todos, true = activos, false = inactivos
      searchQuery: ''
    }
  }),

  actions: {
    async fetchSecciones() {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        console.log('API URL:', authStore.apiUrl)
        console.log('Token:', authStore.token)
        const response = await $fetch(`${authStore.apiUrl}/api/secciones`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        this.secciones = response
      } catch (error) {
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
        await $fetch(`${authStore.apiUrl}/api/secciones/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: { is_active: false }
        })
        
        // Actualizar localmente
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

      // Filtro por estado activo/inactivo
      if (state.filters.is_active !== null) {
        filtered = filtered.filter(s => s.is_active === state.filters.is_active)
      }

      // Búsqueda difusa con Fuse.js (solo en nombre)
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