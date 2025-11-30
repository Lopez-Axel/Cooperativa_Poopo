import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useAttendancePeriodStore = defineStore('attendancePeriod', {
  state: () => ({
    periods: [],
    currentPeriods: [],
    openPeriods: [],
    selectedPeriod: null,
    periodStats: null,
    loading: false,
    error: null,
    durationShortcuts: [
      { label: '+30 min', minutes: 30 },
      { label: '+1 hora', minutes: 60 },
      { label: '+2 horas', minutes: 120 }
    ]
  }),

  getters: {
    activePeriods: (state) => state.periods.filter(p => p.is_active),
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
    },
    
    isOpenOutOfTime: (state) => (period) => {
      const status = state.getPeriodStatus(period)
      return period.is_open && (status === 'programado' || status === 'finalizado')
    }
  },

  actions: {
    async fetchPeriods(filters = {}) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams()
        
        if (filters.mes) params.append('mes', filters.mes)
        if (filters.anio) params.append('anio', filters.anio)
        if (filters.is_active !== undefined) params.append('is_active', filters.is_active)
        if (filters.is_open !== undefined && filters.is_open !== null) params.append('is_open', filters.is_open)
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener períodos')
        
        this.periods = await response.json()
        return this.periods
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentPeriods() {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/current`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener períodos actuales')
        
        this.currentPeriods = await response.json()
        return this.currentPeriods
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchOpenPeriods() {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/open`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener períodos abiertos')
        
        this.openPeriods = await response.json()
        return this.openPeriods
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
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}`, {
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

    async fetchPeriodStats(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}/stats`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener estadísticas')
        
        this.periodStats = await response.json()
        return this.periodStats
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createPeriod(periodData) {
      const now = new Date()
      const periodDateTime = new Date(periodData.fecha_asistencia + 'T' + periodData.hora_inicio)
      
      if (periodDateTime < now) {
        throw new Error('No se puede crear un período con fecha/hora anterior al momento actual')
      }
      
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...periodData,
            total_expected: 894,
            created_by: authStore.user.id
          })
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
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}`, {
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

    async openPeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}/open`, {
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

    async closePeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}/close?closed_by=${authStore.user.id}`, {
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

    async deletePeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance-periods/${periodId}`, {
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
    },

    async extendPeriodDuration(periodId, additionalMinutes) {
      this.loading = true
      this.error = null
      try {
        const period = this.periods.find(p => p.id === periodId)
        if (!period || period.is_open) {
          throw new Error('No se puede modificar la duración de un período abierto')
        }
        
        const endTime = new Date(`2000-01-01T${period.hora_fin}`)
        const newEndTime = new Date(endTime.getTime() + (additionalMinutes * 60000))
        
        const endHour = String(newEndTime.getHours()).padStart(2, '0')
        const endMinute = String(newEndTime.getMinutes()).padStart(2, '0')
        const newEndTimeString = `${endHour}:${endMinute}:00`
        
        await this.updatePeriod(periodId, {
          hora_fin: newEndTimeString
        })
        
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