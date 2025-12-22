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
    getAttendancesByCooperativista: (state) => (cooperativistaId) => {
      return state.attendances.filter(a => a.cooperativista_id === cooperativistaId)
    },
    
    getAttendancesByDate: (state) => (fecha) => {
      return state.attendances.filter(a => a.fecha === fecha)
    }
  },

  actions: {
    async fetchAttendances(skip = 0, limit = 100) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams({ skip, limit })
        
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

    async fetchByCooperativista(cooperativistaId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/cooperativista/${cooperativistaId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias')
        
        const attendances = await response.json()
        return attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchByPeriod(periodId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/period/${periodId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias del período')
        
        this.attendances = await response.json()
        return this.attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchByDate(fecha) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/date/${fecha}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener asistencias de la fecha')
        
        const attendances = await response.json()
        return attendances
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async registerAttendance(qrCode, periodId = null, tipo = 'entrada') {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/scan`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            qr_code: qrCode,
            period_id: periodId,
            tipo: tipo
          })
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al registrar asistencia')
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

    async registerManualAttendance(cooperativistaId, periodId = null, tipo = 'entrada', reason = null) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/manual`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            cooperativista_id: cooperativistaId,
            period_id: periodId,
            tipo: tipo,
            reason: reason
          })
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Error al registrar asistencia manual')
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

    async updateAttendance(attendanceId, updateData) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}`, {
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

    async deleteAttendance(attendanceId, confirm = '') {
      if (confirm !== 'DELETE_PERMANENTLY') {
        throw new Error('Debe confirmar la eliminación')
      }
      
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const params = new URLSearchParams({ confirm })
        
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}/hard-delete?${params}`, {
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

    async fetchLogs(attendanceId) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const response = await fetch(`${authStore.apiUrl}/api/attendance/${attendanceId}/logs`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) throw new Error('Error al obtener logs')
        
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