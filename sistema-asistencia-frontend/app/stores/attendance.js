import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useAttendanceStore = defineStore('attendance', {
  state: () => ({
    attendances: [],
    selectedAttendance: null,
    logs: [],
    loading: false,
    error: null
  }),

  getters: {
    validAttendances: (state) => state.attendances.filter(a => a.is_valid),
    invalidAttendances: (state) => state.attendances.filter(a => !a.is_valid),
    
    getAttendancesByCooperativista: (state) => (cooperativistaId) => {
      return state.attendances.filter(a => a.cooperativista_id === cooperativistaId)
    },
    
    getAttendancesByDate: (state) => (fecha) => {
      return state.attendances.filter(a => a.fecha === fecha)
    }
  },

  actions: {
    async fetchAttendances(filters = {}) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams()
        
        if (filters.cooperativista_id) params.append('cooperativista_id', filters.cooperativista_id)
        if (filters.period_id) params.append('period_id', filters.period_id)
        if (filters.fecha_inicio) params.append('fecha_inicio', filters.fecha_inicio)
        if (filters.fecha_fin) params.append('fecha_fin', filters.fecha_fin)
        if (filters.tipo) params.append('tipo', filters.tipo)
        if (filters.device_id) params.append('device_id', filters.device_id)
        if (filters.is_valid !== undefined) params.append('is_valid', filters.is_valid)
        if (filters.skip) params.append('skip', filters.skip)
        if (filters.limit) params.append('limit', filters.limit)
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias')
        
        this.attendances = await response.json()
        return this.attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAttendancesByPeriod(periodId) {
      return await this.fetchAttendances({ period_id: periodId, limit: 500 })
    },

    async fetchAttendance(attendanceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencia')
        
        this.selectedAttendance = await response.json()
        return this.selectedAttendance
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCooperativistaPeriodAttendance(cooperativistaId, periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/cooperativista/${cooperativistaId}/period/${periodId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al verificar asistencia')
        
        const attendance = await response.json()
        return attendance
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTodayAttendance(cooperativistaId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/cooperativista/${cooperativistaId}/today`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias de hoy')
        
        const attendances = await response.json()
        return attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAttendanceRange(cooperativistaId, fechaInicio, fechaFin) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams({
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin
        })
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/cooperativista/${cooperativistaId}/range?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias del rango')
        
        const attendances = await response.json()
        return attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createAttendance(attendanceData) {
      this.loading = true
      this.error = null
      console.log('Creating attendance with data:', attendanceData)
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(attendanceData)
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al crear asistencia')
        }
        
        const newAttendance = await response.json()
        this.attendances.unshift(newAttendance)
        return newAttendance
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateAttendance(attendanceId, updateData, changedBy = null, reason = null) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams()
        if (changedBy) params.append('changed_by', changedBy)
        if (reason) params.append('reason', reason)
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}?${params}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updateData)
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al actualizar asistencia')
        }
        
        const updatedAttendance = await response.json()
        const index = this.attendances.findIndex(a => a.id === attendanceId)
        if (index !== -1) {
          this.attendances[index] = updatedAttendance
        }
        return updatedAttendance
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteAttendance(attendanceId, changedBy = null, reason = null) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams()
        if (changedBy) params.append('changed_by', changedBy)
        if (reason) params.append('reason', reason)
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}?${params}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al eliminar asistencia')
        }
        
        this.attendances = this.attendances.filter(a => a.id !== attendanceId)
        return true
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAttendanceLogs(attendanceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}/logs`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener logs de asistencia')
        
        this.logs = await response.json()
        return this.logs
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})