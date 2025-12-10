// stores/cooperativistas.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useCooperativistasStore = defineStore('cooperativistas', {
  state: () => ({
    cooperativistas: [],
    loading: false,
    error: null,
    filtros: {
      seccion: null,
      cuadrilla: null,
      search: '',
      is_active: true
    }
  }),

  getters: {
    // Lista completa de cooperativistas
    listaCooperativistas: (state) => state.cooperativistas,

    // Secciones únicas
    secciones: (state) => {
      const seccionesSet = new Set(
        state.cooperativistas
          .filter(c => c.seccion != null)
          .map(c => c.seccion)
      )
      return Array.from(seccionesSet).sort((a, b) => a - b)
    },

    // Cuadrillas únicas
    cuadrillas: (state) => {
      const cuadrillasSet = new Set(
        state.cooperativistas
          .filter(c => c.cuadrilla)
          .map(c => c.cuadrilla)
      )
      return Array.from(cuadrillasSet).sort()
    },

    ocupaciones: (state) => {
      const ocupacionesSet = new Set(
        state.cooperativistas
          .filter(c => c.ocupacion)
          .map(c => c.ocupacion)
      )
      return Array.from(ocupacionesSet).sort()
    },

    // Cooperativistas filtrados
    cooperativistasFiltrados: (state) => {
      let resultado = state.cooperativistas

      // Filtrar por estado activo
      if (state.filtros.is_active !== null) {
        resultado = resultado.filter(c => c.is_active === state.filtros.is_active)
      }

      // Filtrar por sección
      if (state.filtros.seccion !== null) {
        resultado = resultado.filter(c => c.seccion === state.filtros.seccion)
      }

      // Filtrar por cuadrilla
      if (state.filtros.cuadrilla) {
        resultado = resultado.filter(c => c.cuadrilla === state.filtros.cuadrilla)
      }

      // Filtrar por búsqueda
      if (state.filtros.search) {
        const searchLower = state.filtros.search.toLowerCase()
        resultado = resultado.filter(c => {
          const nombreCompleto = `${c.nombres} ${c.apellido_paterno} ${c.apellido_materno}`.toLowerCase()
          const ci = c.ci ? c.ci.toLowerCase() : ''
          const codigo = c.codigo_unico ? c.codigo_unico.toLowerCase() : ''
          return nombreCompleto.includes(searchLower) || 
                 ci.includes(searchLower) || 
                 codigo.includes(searchLower)
        })
      }

      return resultado
    },

    // Cooperativistas agrupados por sección
    cooperativistasPorSeccion: (state) => {
      const grupos = {}
      state.cooperativistas
        .filter(c => c.is_active && c.seccion != null)
        .forEach(c => {
          if (!grupos[c.seccion]) {
            grupos[c.seccion] = []
          }
          grupos[c.seccion].push(c)
        })
      return grupos
    },

    // Cooperativistas agrupados por cuadrilla
    cooperativistasPorCuadrilla: (state) => {
      const grupos = {}
      state.cooperativistas
        .filter(c => c.is_active && c.cuadrilla)
        .forEach(c => {
          if (!grupos[c.cuadrilla]) {
            grupos[c.cuadrilla] = []
          }
          grupos[c.cuadrilla].push(c)
        })
      return grupos
    },

    // Obtener jefes de cuadrilla
    jefesYTesoreros: (state) => {
      return state.cooperativistas.filter(c => {
        const ocupacion = c.ocupacion ? c.ocupacion.toLowerCase() : ''
        const jefe = c.jefe_cuadrilla ? c.jefe_cuadrilla.toLowerCase() : ''
        return ocupacion.includes('jefe') || 
               ocupacion.includes('tesorero') ||
               jefe.includes('jefe') || 
               jefe.includes('tesorero')
      })
    }
  },

  actions: {
    async cargarCooperativistas() {

        // ⚠️ Si ya hay una carga en progreso, REUTILIZA la misma promesa.
        if (this._loadingPromise) {
          return this._loadingPromise;
        }

        this._loadingPromise = (async () => {

          this.loading = true
          this.error = null

          this.cooperativistas = []

          try {
            const authStore = useAuthStore()

            let offset = 0
            const limit = 500
            let hasMore = true
            let totalCargados = 0
            
            while (hasMore) {
              const response = await $fetch(`${authStore.apiUrl}/api/cooperativistas/`, {
                method: 'GET',
                headers: {
                  'Authorization': `Bearer ${authStore.token}`
                },
                params: {
                  limit,
                  offset
                }
              })

              this.cooperativistas.push(...response)
              totalCargados += response.length

              hasMore = response.length === limit
              offset += limit
            }

            return this.cooperativistas

          } catch (error) {
            this.error = error.message || 'Error cargando cooperativistas'
            console.error("❌ Error:", error)
            throw error

          } finally {
            this.loading = false
            this._loadingPromise = null
          }

        })()

        return this._loadingPromise
      },


    async obtenerCooperativista(id) {
      try {
        const authStore = useAuthStore()
        const config = useRuntimeConfig()
        
        const cooperativista = await $fetch(`${authStore.apiUrl}/api/cooperativistas/${id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        return cooperativista
      } catch (error) {
        console.error('Error obteniendo cooperativista:', error)
        throw error
      }
    },

    async obtenerPorCodigo(codigo) {
      try {
        const authStore = useAuthStore()
        const config = useRuntimeConfig()
        
        const cooperativista = await $fetch(`${authStore.apiUrl}/api/cooperativistas/codigo/${codigo}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        return cooperativista
      } catch (error) {
        console.error('Error obteniendo cooperativista por código:', error)
        throw error
      }
    },

    async crearCooperativista(datos) {
      try {
        const authStore = useAuthStore()
        const config = useRuntimeConfig()
        
        const nuevoCooperativista = await $fetch(`${authStore.apiUrl}/api/cooperativistas/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: datos
        })
        
        // Agregar a la lista local
        this.cooperativistas.push(nuevoCooperativista)
        
        return nuevoCooperativista
      } catch (error) {
        console.error('Error creando cooperativista:', error)
        throw error
      }
    },

    async actualizarCooperativista(id, datos) {
      try {
        const authStore = useAuthStore()
        const config = useRuntimeConfig()
        
        const cooperativistaActualizado = await $fetch(`${authStore.apiUrl}/api/cooperativistas/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: datos
        })
        
        // Actualizar en la lista local
        const index = this.cooperativistas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.cooperativistas[index] = cooperativistaActualizado
        }
        
        return cooperativistaActualizado
      } catch (error) {
        console.error('Error actualizando cooperativista:', error)
        throw error
      }
    },

    async eliminarCooperativista(id) {
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/cooperativistas/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        // Actualizar el cooperativista en la lista local (marcarlo como inactivo)
        const index = this.cooperativistas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.cooperativistas[index].is_active = false
        }
        
        return response
      } catch (error) {
        console.error('Error desactivando cooperativista:', error)
        throw error
      }
    },

    // Establecer filtros
    setFiltros(filtros) {
      this.filtros = { ...this.filtros, ...filtros }
    },

    // Limpiar filtros
    limpiarFiltros() {
      this.filtros = {
        seccion: null,
        cuadrilla: null,
        search: '',
        is_active: true
      }
    }
  }
})