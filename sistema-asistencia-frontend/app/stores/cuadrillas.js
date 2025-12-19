// stores/cuadrillas.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import Fuse from 'fuse.js'

export const useCuadrillasStore = defineStore('cuadrillas', {
  state: () => ({
    cuadrillas: [],
    secciones: [], // Para agrupar
    loading: false,
    error: null,
    filters: {
      is_active: null,
      seccion_id: null,
      searchQuery: ''
    }
  }),

  actions: {
    async fetchCuadrillas() {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/cuadrillas/`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        this.cuadrillas = await response.json()
      } catch (error) {
        this.error = error.message || 'Error al cargar cuadrillas'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSecciones() {
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/secciones`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        this.secciones = await response.json()
      } catch (error) {
        throw error
      }
    },

    async createCuadrilla(cuadrillaData) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/cuadrillas/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(cuadrillaData)
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        const data = await response.json()
        this.cuadrillas.push(data)
        return data
      } catch (error) {
        this.error = error.message || 'Error al crear cuadrilla'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateCuadrilla(id, cuadrillaData) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/cuadrillas/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(cuadrillaData)
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        const data = await response.json()
        const index = this.cuadrillas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.cuadrillas[index] = data
        }
        
        return data
      } catch (error) {
        this.error = error.message || 'Error al actualizar cuadrilla'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteCuadrilla(id) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/cuadrillas/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ is_active: false })
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        const cuadrilla = this.cuadrillas.find(c => c.id === id)
        if (cuadrilla) {
          cuadrilla.is_active = false
        }
        
        return true
      } catch (error) {
        this.error = error.message || 'Error al desactivar cuadrilla'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getCuadrillaDetails(id) {
      this.loading = true
      this.error = null
      
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/cuadrillas/${id}/details`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        
        return await response.json()
      } catch (error) {
        this.error = error.message || 'Error al cargar detalles de cuadrilla'
        throw error
      } finally {
        this.loading = false
      }
    },

    setSearchQuery(query) {
      this.filters.searchQuery = query
    },

    setActiveFilter(value) {
      this.filters.is_active = value
    },

    setSeccionFilter(value) {
      this.filters.seccion_id = value
    },

    resetFilters() {
      this.filters = {
        is_active: null,
        seccion_id: null,
        searchQuery: ''
      }
    }
  },

  getters: {
    cuadrillasFiltradas: (state) => {
      let filtered = state.cuadrillas

      // Filtro por estado activo/inactivo
      if (state.filters.is_active !== null) {
        filtered = filtered.filter(c => c.is_active === state.filters.is_active)
      }

      // Filtro por sección
      if (state.filters.seccion_id !== null) {
        filtered = filtered.filter(c => c.id_seccion === state.filters.seccion_id)
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

    cuadrillasAgrupadasPorSeccion: (state) => {
      const agrupadas = {}
      
      state.secciones.forEach(seccion => {
        agrupadas[seccion.id] = {
          seccion: seccion,
          cuadrillas: []
        }
      })

      state.cuadrillas.forEach(cuadrilla => {
        if (agrupadas[cuadrilla.id_seccion]) {
          agrupadas[cuadrilla.id_seccion].cuadrillas.push(cuadrilla)
        }
      })

      return Object.values(agrupadas)
    },

    hasActiveFilters: (state) => {
      return state.filters.is_active !== null || 
             state.filters.seccion_id !== null || 
             state.filters.searchQuery.trim() !== ''
    }
  }
})