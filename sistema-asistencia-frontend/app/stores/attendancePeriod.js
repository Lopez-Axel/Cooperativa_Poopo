import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useAttendancePeriodStore = defineStore('attendancePeriod', {
  state: () => ({
    periods: [],
    selectedPeriod: null,
    periodStats: null,
    loading: false,
    error: null
  }),

  getters: {
    activePeriods: (state) => state.periods.filter(p => p.is_active),
    openPeriods: (state) => state.periods.filter(p => p.is_open && p.is_active),
    closedPeriods: (state) => state.periods.filter(p => !p.is_open && p.is_active),
    
    getPeriodStatus: (state) => (period) => {
      if (!period.fecha_asistencia || !period.hora_inicio || !period.hora_fin) return 'invalid'
      
      const now = new Date()
      const periodStart = new Date(period.fecha_asistencia + 'T' + period.hora_inicio)
      const periodEnd = new Date(period.fecha_asistencia + 'T' + period.hora_fin)
      
      if (now < periodStart) return 'programado'
      if (now >= periodStart && now <= periodEnd) return 'en_curso'
      if (now > periodEnd) return 'finalizado'
      
      return 'invalid'
    }
  },

  actions: {
    async checkAndOpenPeriods() {
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/check-and-open`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al verificar períodos')
        
        const result = await response.json()
        return result
      } catch (error) {
        console.error('Error al verificar períodos:', error)
        return null
      }
    },

    async fetchPeriods(skip = 0, limit = 100, activeOnly = false) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams({ skip, limit, active_only: activeOnly })
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener períodos')
        
        this.periods = await response.json()
        
        await this.checkAndOpenPeriods()
        
        const responseUpdated = await fetch(`${authStore.apiUrl}/api/attendance/periods?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        if (responseUpdated.ok) {
          this.periods = await responseUpdated.json()
        }
        
        return this.periods
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener período')
        
        this.selectedPeriod = await response.json()
        return this.selectedPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPeriodsByMonth(year, month) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/month/${year}/${month}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener períodos del mes')
        
        const periods = await response.json()
        return periods
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPeriodByDate(fecha) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/date/${fecha}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('No hay período activo para esta fecha')
        
        const period = await response.json()
        return period
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createPeriod(periodData) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(periodData)
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al crear período')
        }
        
        const newPeriod = await response.json()
        this.periods.unshift(newPeriod)
        return newPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updatePeriod(periodId, updateData) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updateData)
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al actualizar período')
        }
        
        const updatedPeriod = await response.json()
        const index = this.periods.findIndex(p => p.id === periodId)
        if (index !== -1) {
          this.periods[index] = updatedPeriod
        }
        return updatedPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async closePeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}/close`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al cerrar período')
        }
        
        const closedPeriod = await response.json()
        const index = this.periods.findIndex(p => p.id === periodId)
        if (index !== -1) {
          this.periods[index] = closedPeriod
        }
        return closedPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async openPeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}/open`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al abrir período')
        }
        
        const openedPeriod = await response.json()
        const index = this.periods.findIndex(p => p.id === periodId)
        if (index !== -1) {
          this.periods[index] = openedPeriod
        }
        return openedPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async deactivatePeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}/deactivate`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al desactivar período')
        }
        
        const deactivatedPeriod = await response.json()
        const index = this.periods.findIndex(p => p.id === periodId)
        if (index !== -1) {
          this.periods[index] = deactivatedPeriod
        }
        return deactivatedPeriod
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async deletePeriod(periodId, confirm = '') {
      if (confirm !== 'DELETE_PERMANENTLY') {
        throw new Error('Debe confirmar la eliminación')
      }
      
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams({ confirm })
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/periods/${periodId}/hard-delete?${params}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al eliminar período')
        }
        
        this.periods = this.periods.filter(p => p.id !== periodId)
        return true
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})