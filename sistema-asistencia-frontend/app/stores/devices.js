// stores/devices.js
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useDevicesStore = defineStore('devices', {
  state: () => ({
    devices: [],
    loading: false,
    error: null,
    activationStats: null,
    exportData: null,
    filters: {
      cuadrilla: null,
      seccion: null,
      is_active: null,
      is_activated: null,
      is_blocked: null
    }
  }),

  getters: {
    devicesFiltrados: (state) => {
      let resultado = state.devices

      if (state.filters.cuadrilla) {
        resultado = resultado.filter(d => d.cooperativista?.cuadrilla === state.filters.cuadrilla)
      }

      if (state.filters.is_active !== null) {
        resultado = resultado.filter(d => d.is_active === state.filters.is_active)
      }

      if (state.filters.is_activated !== null) {
        resultado = resultado.filter(d => d.is_activated === state.filters.is_activated)
      }

      if (state.filters.is_blocked !== null) {
        resultado = resultado.filter(d => d.is_blocked === state.filters.is_blocked)
      }

      return resultado
    },

    devicesPendientes: (state) => state.devices.filter(d => !d.is_activated),
    devicesActivados: (state) => state.devices.filter(d => d.is_activated),
    devicesBloqueados: (state) => state.devices.filter(d => d.is_blocked),

    totalDevices: (state) => state.devices.length,
    totalActivados: (state) => state.devices.filter(d => d.is_activated).length,
    totalPendientes: (state) => state.devices.filter(d => !d.is_activated).length,
    porcentajeActivacion: (state) => {
      if (state.devices.length === 0) return 0
      return Math.round((state.devices.filter(d => d.is_activated).length / state.devices.length) * 100)
    }
  },

  actions: {
    async fetchDevices(params = {}) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const queryParams = new URLSearchParams()
        
        if (params.cooperativista_id) queryParams.append('cooperativista_id', params.cooperativista_id)
        if (params.cuadrilla) queryParams.append('cuadrilla', params.cuadrilla)
        if (params.is_active !== undefined) queryParams.append('is_active', params.is_active)
        if (params.is_activated !== undefined) queryParams.append('is_activated', params.is_activated)
        if (params.is_blocked !== undefined) queryParams.append('is_blocked', params.is_blocked)
        if (params.limit) queryParams.append('limit', params.limit)
        if (params.skip) queryParams.append('skip', params.skip)
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/?${queryParams}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        this.devices = response
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al obtener dispositivos'
        throw error
      } finally {
        this.loading = false
      }
    },

    async generateBatch(batchData) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/generate-batch`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: batchData
        })
        
        // Recargar dispositivos después de generar
        await this.fetchDevices()
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al generar dispositivos'
        throw error
      } finally {
        this.loading = false
      }
    },

    async activateDevice(activationData) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/activate`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: activationData
        })
        
        // Actualizar en la lista local
        const index = this.devices.findIndex(d => d.id === response.id)
        if (index !== -1) {
          this.devices[index] = response
        }
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al activar dispositivo'
        throw error
      } finally {
        this.loading = false
      }
    },

    async exportCuadrilla(cuadrilla) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/export/cuadrilla/${cuadrilla}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        this.exportData = response
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al exportar cuadrilla'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchActivationStats() {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/stats/activation`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        this.activationStats = response
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al obtener estadísticas'
        throw error
      } finally {
        this.loading = false
      }
    },

    async blockDevice(deviceId, reason) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/${deviceId}/block`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: { block_reason: reason }
        })
        
        // Recargar dispositivos
        await this.fetchDevices()
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al bloquear dispositivo'
        throw error
      } finally {
        this.loading = false
      }
    },

    async unblockDevice(deviceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/${deviceId}/unblock`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        // Recargar dispositivos
        await this.fetchDevices()
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al desbloquear dispositivo'
        throw error
      } finally {
        this.loading = false
      }
    },

    async revokeDevice(deviceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await $fetch(`${authStore.apiUrl}/api/devices/${deviceId}/revoke`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        // Recargar dispositivos
        await this.fetchDevices()
        
        return response
      } catch (error) {
        this.error = error.data?.detail || 'Error al revocar dispositivo'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDevice(deviceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        await $fetch(`${authStore.apiUrl}/api/devices/${deviceId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        // Eliminar de la lista local
        this.devices = this.devices.filter(d => d.id !== deviceId)
        
        return true
      } catch (error) {
        this.error = error.data?.detail || 'Error al eliminar dispositivo'
        throw error
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    limpiarFiltros() {
      this.filters = {
        cuadrilla: null,
        seccion: null,
        is_active: null,
        is_activated: null,
        is_blocked: null
      }
    }
  }
})