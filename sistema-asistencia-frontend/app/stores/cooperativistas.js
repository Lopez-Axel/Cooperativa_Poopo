// stores/cooperativistas.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useCuadrillasStore } from './cuadrillas'
import { useSeccionesStore } from './secciones'

export const useCooperativistasStore = defineStore('cooperativistas', {
  state: () => ({
    cooperativistas: [],
    loading: false,
    error: null,
    filtros: {
      id_seccion: null,
      id_cuadrilla: null,
      search: '',
      is_active: true,
      ocupacion: null,
      estado_asegurado: null,
      fecha_ingreso_desde: null,
      fecha_ingreso_hasta: null,
      solo_cargos_especiales: false
    }
  }),

  getters: {
    listaCooperativistas: (state) => state.cooperativistas,

    getCuadrilla: (state) => (cooperativista) => {
      if (!cooperativista.id_cuadrilla) return null
      const cuadrillasStore = useCuadrillasStore()
      return cuadrillasStore.cuadrillas.find(c => c.id === cooperativista.id_cuadrilla)
    },

    getSeccion: (state) => (cooperativista) => {
      if (!cooperativista.id_cuadrilla) return null
      const cuadrillasStore = useCuadrillasStore()
      const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === cooperativista.id_cuadrilla)
      if (!cuadrilla || !cuadrilla.id_seccion) return null
      
      const seccionesStore = useSeccionesStore()
      return seccionesStore.secciones.find(s => s.id === cuadrilla.id_seccion)
    },

    secciones: (state) => {
      const cuadrillasStore = useCuadrillasStore()
      const seccionesStore = useSeccionesStore()
      
      const seccionIds = new Set(
        state.cooperativistas
          .filter(c => c.id_cuadrilla)
          .map(c => {
            const cuadrilla = cuadrillasStore.cuadrillas.find(cu => cu.id === c.id_cuadrilla)
            return cuadrilla?.id_seccion
          })
          .filter(id => id != null)
      )
      
      return Array.from(seccionIds)
        .map(id => seccionesStore.secciones.find(s => s.id === id))
        .filter(s => s != null)
        .sort((a, b) => a.nombre.localeCompare(b.nombre))
    },

    cuadrillas: (state) => {
      const cuadrillasStore = useCuadrillasStore()
      
      const cuadrillaIds = new Set(
        state.cooperativistas
          .filter(c => c.id_cuadrilla)
          .map(c => c.id_cuadrilla)
      )
      
      return Array.from(cuadrillaIds)
        .map(id => cuadrillasStore.cuadrillas.find(c => c.id === id))
        .filter(c => c != null)
        .sort((a, b) => a.nombre.localeCompare(b.nombre))
    },

    ocupaciones: (state) => {
      const ocupacionesSet = new Set(
        state.cooperativistas
          .filter(c => c.ocupacion)
          .map(c => c.ocupacion)
      )
      return Array.from(ocupacionesSet).sort()
    },

    estadosAsegurado: (state) => {
      const estadosSet = new Set(
        state.cooperativistas
          .filter(c => c.estado_asegurado)
          .map(c => c.estado_asegurado)
      )
      return Array.from(estadosSet).sort()
    },

    cooperativistasFiltrados: (state) => {
      const cuadrillasStore = useCuadrillasStore()
      let resultado = state.cooperativistas

      // Filtrar por estado activo
      if (state.filtros.is_active !== null) {
        resultado = resultado.filter(c => c.is_active === state.filtros.is_active)
      }

      // Filtrar por sección (a través de cuadrilla)
      if (state.filtros.id_seccion !== null) {
        resultado = resultado.filter(c => {
          if (!c.id_cuadrilla) return false
          const cuadrilla = cuadrillasStore.cuadrillas.find(cu => cu.id === c.id_cuadrilla)
          return cuadrilla?.id_seccion === state.filtros.id_seccion
        })
      }

      // Filtrar por cuadrilla
      if (state.filtros.id_cuadrilla) {
        resultado = resultado.filter(c => c.id_cuadrilla === state.filtros.id_cuadrilla)
      }

      // Filtrar por ocupación
      if (state.filtros.ocupacion) {
        resultado = resultado.filter(c => c.ocupacion === state.filtros.ocupacion)
      }

      // Filtrar por estado asegurado
      if (state.filtros.estado_asegurado) {
        resultado = resultado.filter(c => c.estado_asegurado === state.filtros.estado_asegurado)
      }

      // Filtrar por fecha de ingreso desde
      if (state.filtros.fecha_ingreso_desde) {
        resultado = resultado.filter(c => {
          if (!c.fecha_ingreso) return false
          return new Date(c.fecha_ingreso) >= new Date(state.filtros.fecha_ingreso_desde)
        })
      }

      // Filtrar por fecha de ingreso hasta
      if (state.filtros.fecha_ingreso_hasta) {
        resultado = resultado.filter(c => {
          if (!c.fecha_ingreso) return false
          return new Date(c.fecha_ingreso) <= new Date(state.filtros.fecha_ingreso_hasta)
        })
      }

      // Filtrar solo cargos especiales
      if (state.filtros.solo_cargos_especiales) {
        resultado = resultado.filter(c => {
          const rol = c.rol_cuadrilla ? c.rol_cuadrilla.toLowerCase() : ''
          return rol.includes('jefe') || rol.includes('tesorero') || rol.includes('delegado')
        })
      }

      // Filtrar por búsqueda
      if (state.filtros.search) {
        const searchLower = state.filtros.search.toLowerCase()
        resultado = resultado.filter(c => {
          const nombreCompleto = `${c.nombres} ${c.apellido_paterno} ${c.apellido_materno}`.toLowerCase()
          const ci = c.ci ? c.ci.toLowerCase() : ''
          const qr = c.qr_code ? c.qr_code.toLowerCase() : ''
          return nombreCompleto.includes(searchLower) || 
                 ci.includes(searchLower) || 
                 qr.includes(searchLower)
        })
      }

      return resultado
    },

    cooperativistasPorSeccion: (state) => {
      const cuadrillasStore = useCuadrillasStore()
      const seccionesStore = useSeccionesStore()
      const grupos = {}
      
      state.cooperativistas
        .filter(c => c.is_active && c.id_cuadrilla)
        .forEach(c => {
          const cuadrilla = cuadrillasStore.cuadrillas.find(cu => cu.id === c.id_cuadrilla)
          if (!cuadrilla || !cuadrilla.id_seccion) return
          
          const seccionId = cuadrilla.id_seccion
          if (!grupos[seccionId]) {
            grupos[seccionId] = {
              seccion: seccionesStore.secciones.find(s => s.id === seccionId),
              cooperativistas: []
            }
          }
          grupos[seccionId].cooperativistas.push(c)
        })
      
      return grupos
    },

    // Cooperativistas agrupados por cuadrilla
    cooperativistasPorCuadrilla: (state) => {
      const cuadrillasStore = useCuadrillasStore()
      const grupos = {}
      
      state.cooperativistas
        .filter(c => c.is_active && c.id_cuadrilla)
        .forEach(c => {
          const cuadrillaId = c.id_cuadrilla
          if (!grupos[cuadrillaId]) {
            grupos[cuadrillaId] = {
              cuadrilla: cuadrillasStore.cuadrillas.find(cu => cu.id === cuadrillaId),
              cooperativistas: []
            }
          }
          grupos[cuadrillaId].cooperativistas.push(c)
        })
      
      return grupos
    },

    // Obtener jefes y tesoreros
    jefesYTesoreros: (state) => {
      return state.cooperativistas.filter(c => {
        if (!c.is_active) return false
        const rol = c.rol_cuadrilla ? c.rol_cuadrilla.toLowerCase() : ''
        return rol.includes('jefe') || rol.includes('tesorero')
      })
    }
  },

  actions: {
    async cargarCooperativistas() {
      if (this._loadingPromise) {
        return this._loadingPromise
      }

      this._loadingPromise = (async () => {
        this.loading = true
        this.error = null
        this.cooperativistas = []

        try {
          const authStore = useAuthStore()
          
          const response = await $fetch(`${authStore.apiUrl}/api/cooperativistas/`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${authStore.token}`
            }
          })

          this.cooperativistas = response

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

    async obtenerPorQR(qr_code) {
      try {
        const authStore = useAuthStore()
        
        const cooperativista = await $fetch(`${authStore.apiUrl}/api/cooperativistas/qr/${qr_code}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        return cooperativista
      } catch (error) {
        console.error('Error obteniendo cooperativista por QR:', error)
        throw error
      }
    },

    async crearCooperativista(datos) {
      try {
        const authStore = useAuthStore()
        
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

    async toggleActivacion(id, is_active) {
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/cooperativistas/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: { is_active }
        })
        
        // Actualizar en la lista local
        const index = this.cooperativistas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.cooperativistas[index] = response
        }
        
        return response
      } catch (error) {
        console.error('Error cambiando estado:', error)
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
        
        // Remover de la lista local
        const index = this.cooperativistas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.cooperativistas.splice(index, 1)
        }
        
        return response
      } catch (error) {
        console.error('Error eliminando cooperativista:', error)
        throw error
      }
    },

    // Helpers para obtener nombres
    getCuadrillaName(id_cuadrilla) {
      if (!id_cuadrilla) return 'Sin Cuadrilla'
      const cuadrillasStore = useCuadrillasStore()
      const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === id_cuadrilla)
      return cuadrilla ? cuadrilla.nombre : 'N/A'
    },

    getSeccionName(id_cuadrilla) {
      if (!id_cuadrilla) return 'Sin Sección'
      const cuadrillasStore = useCuadrillasStore()
      const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === id_cuadrilla)
      if (!cuadrilla || !cuadrilla.id_seccion) return 'N/A'
      
      const seccionesStore = useSeccionesStore()
      const seccion = seccionesStore.secciones.find(s => s.id === cuadrilla.id_seccion)
      return seccion ? seccion.nombre : 'N/A'
    },

    // Establecer filtros
    setFiltros(filtros) {
      this.filtros = { ...this.filtros, ...filtros }
    },

    // Limpiar filtros
    limpiarFiltros() {
      this.filtros = {
        id_seccion: null,
        id_cuadrilla: null,
        search: '',
        is_active: true,
        ocupacion: null,
        estado_asegurado: null,
        fecha_ingreso_desde: null,
        fecha_ingreso_hasta: null,
        solo_cargos_especiales: false
      }
    }
  }
})