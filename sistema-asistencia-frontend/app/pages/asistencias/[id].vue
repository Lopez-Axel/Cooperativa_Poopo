<template>
  <div class="attendance-details-page">
    <div class="page-header" v-if="periodStore.selectedPeriod">
      <div class="header-content">
        <div class="header-text">
          <h1 class="title is-2">
            <i class="mdi mdi-calendar-check"></i>
            {{ periodStore.selectedPeriod.nombre }}
          </h1>
          <p class="subtitle">{{ formatDate(periodStore.selectedPeriod.fecha_asistencia) }}</p>
        </div>
        <button class="button is-light" @click="router.back()">
          <i class="mdi mdi-arrow-left"></i>
          <span>Volver</span>
        </button>
      </div>
    </div>

    <div v-if="attendanceStore.error || periodStore.error || cooperativistaStore.error" class="notification is-danger">
      <i class="mdi mdi-alert-circle"></i>
      {{ attendanceStore.error || periodStore.error || cooperativistaStore.error }}
    </div>

    <div class="stats-section" v-if="periodStore.selectedPeriod">
      <div class="stat-card">
        <div class="stat-header">
          <i class="mdi mdi-information-outline"></i>
          <span>Información del Período</span>
        </div>
        <div class="stat-content">
          <div class="stat-item">
            <span class="stat-label">Horario</span>
            <span class="stat-value">
              <i class="mdi mdi-clock-outline"></i>
              {{ periodStore.selectedPeriod.hora_inicio.substring(0, 5) }} - {{ periodStore.selectedPeriod.hora_fin.substring(0, 5) }}
            </span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Estado</span>
            <span v-if="periodStore.selectedPeriod.is_open" class="tag is-success">
              <i class="mdi mdi-lock-open"></i>
              Abierto
            </span>
            <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'programado'" class="tag is-info">
              <i class="mdi mdi-clock-outline"></i>
              Programado
            </span>
            <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'en_curso'" class="tag is-warning">
              <i class="mdi mdi-alert"></i>
              En Curso
            </span>
            <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'finalizado'" class="tag is-dark">
              <i class="mdi mdi-check-circle"></i>
              Finalizado
            </span>
            <span v-else class="tag is-light">
              <i class="mdi mdi-lock"></i>
              Cerrado
            </span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-header">
          <i class="mdi mdi-chart-bar"></i>
          <span>Estadísticas de Asistencia</span>
        </div>
        <div class="stat-content">
          <div class="attendance-count">
            <i class="mdi mdi-account-multiple-check"></i>
            <div class="count-text">
              <span class="count-number">{{ periodStore.selectedPeriod.total_marked }}</span>
              <span class="count-divider">/</span>
              <span class="count-total">{{ periodStore.selectedPeriod.total_expected }}</span>
            </div>
          </div>
          <div v-if="periodStore.selectedPeriod.total_expected > 0" class="progress-section">
            <progress 
              class="progress" 
              :class="{
                'is-success': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) >= 80,
                'is-warning': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) >= 50 && Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) < 80,
                'is-danger': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) < 50
              }"
              :value="periodStore.selectedPeriod.total_marked" 
              :max="periodStore.selectedPeriod.total_expected"
            ></progress>
            <span class="progress-label">
              {{ Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) }}% de asistencia
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="filters-section">
      <div class="section-header">
        <h2 class="section-title">
          <i class="mdi mdi-format-list-bulleted"></i>
          Lista de Asistencias
        </h2>
        <div class="action-buttons-group">
          <button 
            class="button is-danger"
            @click="generarPDF"
            :disabled="attendanceStore.loading || filteredAttendances.length === 0"
          >
            <i class="mdi mdi-file-pdf-box"></i>
            <span>PDF</span>
          </button>
          <button class="button is-primary" @click="showAddModal = true">
            <i class="mdi mdi-plus"></i>
            <span>Agregar Asistencia</span>
          </button>
        </div>
      </div>

      <div class="search-box">
        <i class="mdi mdi-magnify"></i>
        <input 
          class="input"
          type="text" 
          placeholder="Buscar por CI o nombre del cooperativista..." 
          v-model="searchFilter"
        >
      </div>
    </div>

    <div v-if="attendanceStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando asistencias...</p>
    </div>

    <div v-else class="table-container">
      <table class="table is-fullwidth is-hoverable">
        <thead>
          <tr>
            <th>CI</th>
            <th>Cooperativista</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th class="has-text-centered">Tipo</th>
            <th class="has-text-centered">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredAttendances.length === 0">
            <td colspan="6" class="has-text-centered empty-state">
              <i class="mdi mdi-account-off"></i>
              <p>No hay asistencias registradas</p>
            </td>
          </tr>
          <tr v-for="attendance in filteredAttendances" :key="attendance.id">
            <td>
              <span class="tag">{{ getCooperativistaById(attendance.cooperativista_id)?.ci || 'N/A' }}</span>
            </td>
            <td>
              <strong>{{ getCooperativistaById(attendance.cooperativista_id)?.nombres || 'Cooperativista no encontrado' }}</strong>
              <br>
              <small>{{ getCooperativistaById(attendance.cooperativista_id)?.apellidos || '' }}</small>
            </td>
            <td>{{ formatDate(attendance.fecha) }}</td>
            <td>
              <i class="mdi mdi-clock"></i>
              {{ attendance.hora.substring(0, 5) }}
            </td>
            <td class="has-text-centered">
              <span class="tag" :class="{
                'is-success': attendance.tipo === 'entrada',
                'is-warning': attendance.tipo === 'salida'
              }">
                <i :class="attendance.tipo === 'entrada' ? 'mdi mdi-login' : 'mdi mdi-logout'"></i>
                {{ attendance.tipo.toUpperCase() }}
              </span>
            </td>
            <td class="has-text-centered">
              <div class="action-buttons">
                <button 
                  class="button is-small is-info"
                  @click="viewLogs(attendance.id)"
                  title="Ver logs"
                >
                  <i class="mdi mdi-history"></i>
                </button>
                <button 
                  class="button is-small is-danger"
                  @click="confirmDelete(attendance.id)"
                  title="Eliminar registro"
                >
                  <i class="mdi mdi-delete"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal" :class="{ 'is-active': showAddModal }">
      <div class="modal-background" @click="closeAddModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi mdi-account-plus"></i>
            Agregar Asistencia Manual
          </p>
          <button class="delete" @click="closeAddModal"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Cooperativista *</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="manualAttendanceForm.cooperativista_id">
                  <option :value="null">Seleccione un cooperativista</option>
                  <option v-for="coop in activeCooperativistas" :key="coop.id" :value="coop.id">
                    {{ coop.ci }} - {{ coop.nombres }} {{ coop.apellidos }}
                  </option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-account"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">Tipo de Registro *</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="manualAttendanceForm.tipo">
                  <option value="entrada">Entrada</option>
                  <option value="salida">Salida</option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-swap-horizontal"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">Motivo del Registro Manual *</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="manualAttendanceForm.reason">
                  <option value="">Seleccione un motivo</option>
                  <option value="Falta de credencial">Falta de credencial</option>
                  <option value="Registro tardío">Registro tardío</option>
                  <option value="Credencial dañada">Credencial dañada</option>
                  <option value="Error en scanner">Error en scanner</option>
                  <option value="Otro">Otro motivo</option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-text-box"></i>
              </span>
            </div>
          </div>

          <div v-if="manualAttendanceForm.reason === 'Otro'" class="field">
            <label class="label">Especificar Motivo</label>
            <div class="control">
              <textarea 
                class="textarea" 
                placeholder="Describa el motivo del registro manual..."
                v-model="manualAttendanceForm.customReason"
                rows="2"
              ></textarea>
            </div>
          </div>

          <div class="notification is-info">
            <p><strong>Nota:</strong> Se creará un log con el motivo especificado para auditoría.</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="saveManualAttendance"
            :disabled="!canSaveManualAttendance || attendanceStore.loading"
          >
            <i class="mdi mdi-content-save"></i>
            <span v-if="attendanceStore.loading">Guardando...</span>
            <span v-else>Registrar Asistencia</span>
          </button>
          <button class="button" @click="closeAddModal">Cancelar</button>
        </footer>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showLogsModal }">
      <div class="modal-background" @click="showLogsModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi mdi-history"></i>
            Historial de Cambios
          </p>
          <button class="delete" @click="showLogsModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="attendanceStore.logs.length === 0" class="empty-state">
            <i class="mdi mdi-clipboard-text-off"></i>
            <p>No hay logs registrados</p>
          </div>
          <div v-else class="timeline">
            <div v-for="log in attendanceStore.logs" :key="log.id" class="timeline-item">
              <div class="timeline-marker">
                <i class="mdi mdi-flag"></i>
              </div>
              <div class="timeline-content">
                <p class="heading">{{ formatDateTime(log.created_at) }}</p>
                <p><strong>{{ log.action }}</strong></p>
                <p v-if="log.reason">{{ log.reason }}</p>
              </div>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="showLogsModal = false">Cerrar</button>
        </footer>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="showDeleteModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head has-background-danger">
          <p class="modal-card-title">
            <i class="mdi mdi-alert-circle"></i>
            Confirmar Eliminación
          </p>
          <button class="delete" @click="showDeleteModal = false"></button>
        </header>
        <section class="modal-card-body">
          <article class="message is-danger">
            <div class="message-body">
              <p class="mb-3">¿Está seguro de que desea eliminar este registro de asistencia?</p>
              <p><strong>Esta acción no se puede deshacer.</strong></p>
            </div>
          </article>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-danger" 
            @click="deleteAttendance"
            :disabled="attendanceStore.loading"
          >
            <i class="mdi mdi-delete"></i>
            <span v-if="attendanceStore.loading">Eliminando...</span>
            <span v-else>Eliminar</span>
          </button>
          <button class="button" @click="showDeleteModal = false">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import 'dayjs/locale/es'
import { useAttendanceStore } from '~/stores/attendance'
import { useAttendancePeriodStore } from '~/stores/attendancePeriod'
import { useCooperativistasStore } from '~/stores/cooperativistas'
import { useCuadrillasStore } from '~/stores/cuadrillas'
import { useSeccionesStore } from '~/stores/secciones'
import { generarReporteAsistencia } from '~/utils/reporteAsistencia'

dayjs.locale('es')

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const router = useRouter()
const route = useRoute()
const attendanceStore = useAttendanceStore()
const periodStore = useAttendancePeriodStore()
const cooperativistaStore = useCooperativistasStore()
const cuadrillasStore = useCuadrillasStore()
const seccionesStore = useSeccionesStore()

const periodId = computed(() => parseInt(route.params.id))

const showAddModal = ref(false)
const showLogsModal = ref(false)
const showDeleteModal = ref(false)
const attendanceToDelete = ref(null)
const searchFilter = ref('')

const manualAttendanceForm = ref({
  cooperativista_id: null,
  tipo: 'entrada',
  reason: '',
  customReason: ''
})

const activeCooperativistas = computed(() => {
  return cooperativistaStore.cooperativistas.filter(c => c.is_active)
})

const filteredAttendances = computed(() => {
  if (!searchFilter.value) return attendanceStore.attendances
  
  const query = searchFilter.value.toLowerCase()
  return attendanceStore.attendances.filter(attendance => {
    const coop = getCooperativistaById(attendance.cooperativista_id)
    if (!coop) return false
    
    return (
      coop.ci.toLowerCase().includes(query) ||
      coop.nombres.toLowerCase().includes(query) ||
      coop.apellidos.toLowerCase().includes(query)
    )
  })
})

const canSaveManualAttendance = computed(() => {
  const hasReason = manualAttendanceForm.value.reason && 
    (manualAttendanceForm.value.reason !== 'Otro' || manualAttendanceForm.value.customReason)
  
  return !!manualAttendanceForm.value.cooperativista_id && hasReason
})

const getCooperativistaById = (id) => {
  return cooperativistaStore.cooperativistas.find(c => c.id === id)
}

const formatDate = (dateString) => {
  const date = dayjs(`${dateString}T00:00:00`)
  return date.locale('es').format('dddd, D [de] MMMM [de] YYYY')
}

const formatDateTime = (dateTimeString) => {
  return dayjs(dateTimeString).locale('es').format('D [de] MMMM [de] YYYY, HH:mm:ss')
}

const loadData = async () => {
  try {
    await periodStore.fetchPeriod(periodId.value)
    await attendanceStore.fetchByPeriod(periodId.value)
    await cooperativistaStore.cargarCooperativistas()
    await cuadrillasStore.fetchCuadrillas()
    await seccionesStore.fetchSecciones()
  } catch (error) {
    console.error('Error al cargar datos:', error)
  }
}

const saveManualAttendance = async () => {
  try {
    const reason = manualAttendanceForm.value.reason === 'Otro' 
      ? manualAttendanceForm.value.customReason 
      : manualAttendanceForm.value.reason

    await attendanceStore.registerManualAttendance(
      manualAttendanceForm.value.cooperativista_id,
      periodId.value,
      manualAttendanceForm.value.tipo,
      reason
    )

    closeAddModal()
    await loadData()
  } catch (error) {
    console.error('Error al registrar asistencia manual:', error)
  }
}

const viewLogs = async (attendanceId) => {
  try {
    await attendanceStore.fetchLogs(attendanceId)
    showLogsModal.value = true
  } catch (error) {
    console.error('Error al obtener logs:', error)
  }
}

const confirmDelete = (attendanceId) => {
  attendanceToDelete.value = attendanceId
  showDeleteModal.value = true
}

const deleteAttendance = async () => {
  try {
    await attendanceStore.deleteAttendance(attendanceToDelete.value, 'DELETE_PERMANENTLY')
    showDeleteModal.value = false
    attendanceToDelete.value = null
    await loadData()
  } catch (error) {
    console.error('Error al eliminar asistencia:', error)
  }
}

const closeAddModal = () => {
  showAddModal.value = false
  manualAttendanceForm.value = {
    cooperativista_id: null,
    tipo: 'entrada',
    reason: '',
    customReason: ''
  }
}

const clearErrors = () => {
  attendanceStore.error = null
  periodStore.error = null
  cooperativistaStore.error = null
}

const generarPDF = async () => {
  try {
    if (!periodStore.selectedPeriod) {
      alert('No se ha cargado el período')
      return
    }

    if (filteredAttendances.value.length === 0) {
      alert('No hay asistencias para generar el reporte')
      return
    }

    const getCooperativistaByIdLocal = (id) => {
      return cooperativistaStore.cooperativistas.find(c => c.id === id)
    }

    const getCuadrillaById = (id) => {
      return cuadrillasStore.cuadrillas.find(c => c.id === id)
    }

    const getSeccionById = (id) => {
      return seccionesStore.secciones.find(s => s.id === id)
    }

    await generarReporteAsistencia(
      periodStore.selectedPeriod,
      filteredAttendances.value,
      getCooperativistaByIdLocal,
      getCuadrillaById,
      getSeccionById
    )

  } catch (error) {
    console.error('Error al generar PDF:', error)
    alert('Error al generar el PDF. Por favor, intente nuevamente.')
  }
}

onMounted(() => {
  loadData()
})

useHead({
  title: 'Detalle de Período de Asistencia'
})
</script>

<style scoped>
.attendance-details-page {
  min-height: 100vh;
  background: #0d1b0d;
  color: #e0f2f1;
  padding: 2rem;
  margin: -1.5rem -1.5rem;
}

.page-header {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 2px solid rgba(255, 215, 0, 0.3);
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.header-text .title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.header-text .title i {
  font-size: 2rem;
}

.header-text .subtitle {
  color: #c8e6c9;
  font-weight: 600;
}

.button {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 700;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border: none;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.button.is-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.button.is-light {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
}

.button.is-light:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.button.is-danger {
  background: rgba(244, 67, 54, 0.3);
  color: #ffcdd2;
  border-color: rgba(244, 67, 54, 0.5);
}

.button.is-danger:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.5);
  transform: translateY(-2px);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.notification.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(211, 47, 47, 0.3));
  color: #ffcdd2;
  border: 1px solid rgba(244, 67, 54, 0.5);
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.9));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #ffd700;
  font-weight: 700;
  font-size: 1.1rem;
}

.stat-header i {
  font-size: 1.5rem;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #90a4ae;
  font-weight: 600;
}

.stat-value {
  color: #c8e6c9;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.attendance-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
}

.attendance-count i {
  font-size: 2.5rem;
  color: #ffd700;
}

.count-text {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.count-number {
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.count-divider {
  font-size: 1.5rem;
  color: #90a4ae;
}

.count-total {
  font-size: 1.5rem;
  color: #c8e6c9;
  font-weight: 700;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress {
  height: 0.75rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.progress::-webkit-progress-bar {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
}

.progress::-webkit-progress-value {
  border-radius: 6px;
  transition: width 0.3s ease;
}

.progress.is-success::-webkit-progress-value {
  background: linear-gradient(90deg, #4caf50, #81c784);
}

.progress.is-warning::-webkit-progress-value {
  background: linear-gradient(90deg, #ff9800, #ffb74d);
}

.progress.is-danger::-webkit-progress-value {
  background: linear-gradient(90deg, #f44336, #ef5350);
}

.progress-label {
  text-align: center;
  color: #90a4ae;
  font-size: 0.9rem;
}

.filters-section {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.9));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-buttons-group {
  display: flex;
  gap: 0.75rem;
}

.search-box {
  position: relative;
  width: 100%;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
  font-size: 1.25rem;
  z-index: 1;
}

.search-box .input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box .input::placeholder {
  color: #90a4ae;
}

.search-box .input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #c8e6c9;
}

.loader {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 215, 0, 0.3);
  border-top: 4px solid #ffd700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.table-container {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.9));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.table {
  width: 100%;
  background: transparent;
  color: #e0f2f1;
}

.table thead th {
  background: rgba(15, 31, 15, 0.9);
  color: #ffd700;
  font-weight: 800;
  text-transform: uppercase;
  padding: 1rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.5);
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.table tbody tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.2s ease;
}

.table tbody tr:hover {
  background: rgba(255, 215, 0, 0.05);
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
  color: #c8e6c9;
}

.table tbody td strong {
  color: #e0f2f1;
}

.table tbody td small {
  color: #90a4ae;
}

.empty-state {
  padding: 4rem 2rem !important;
  text-align: center;
}

.empty-state i {
  font-size: 4rem;
  color: #90a4ae;
  display: block;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #90a4ae;
  font-size: 1.1rem;
}

.tag {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
}

.tag.is-success {
  background: rgba(76, 175, 80, 0.3);
  color: #81c784;
  border-color: rgba(76, 175, 80, 0.5);
}

.tag.is-danger {
  background: rgba(244, 67, 54, 0.3);
  color: #ffcdd2;
  border-color: rgba(244, 67, 54, 0.5);
}

.tag.is-warning {
  background: rgba(255, 152, 0, 0.3);
  color: #ffb74d;
  border-color: rgba(255, 152, 0, 0.5);
}

.tag.is-info {
  background: rgba(77, 182, 172, 0.3);
  color: #4db6ac;
  border-color: rgba(77, 182, 172, 0.5);
}

.tag.is-dark {
  background: rgba(96, 125, 139, 0.3);
  color: #b0bec5;
  border-color: rgba(96, 125, 139, 0.5);
}

.tag.is-light {
  background: rgba(255, 255, 255, 0.1);
  color: #e0f2f1;
  border-color: rgba(255, 255, 255, 0.2);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.button.is-small {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
}

.button.is-small.is-info {
  background: rgba(77, 182, 172, 0.3);
  color: #4db6ac;
  border-color: rgba(77, 182, 172, 0.5);
}

.button.is-small.is-info:hover {
  background: rgba(77, 182, 172, 0.5);
}

.button.is-small.is-danger {
  background: rgba(244, 67, 54, 0.3);
  color: #ffcdd2;
  border-color: rgba(244, 67, 54, 0.5);
}

.button.is-small.is-danger:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.5);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
}

.modal.is-active {
  display: flex;
}

.modal-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
}

.modal-card {
  position: relative;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.98));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.modal-card-head {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border: none;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.modal-card-head.has-background-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.8), rgba(211, 47, 47, 0.9));
}

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  margin: 0;
  font-size: 1.25rem;
}

.modal-card-head.has-background-danger .modal-card-title {
  background: white;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modal-card-title i {
  font-size: 1.5rem;
}

.delete {
  background: rgba(255, 215, 0, 0.3);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.delete::before, .delete::after {
  background: #ffd700;
  content: '';
  height: 2px;
  left: 25%;
  position: absolute;
  top: 50%;
  width: 50%;
  transition: all 0.3s ease;
}

.delete::before {
  transform: translateY(-50%) rotate(45deg);
}

.delete::after {
  transform: translateY(-50%) rotate(-45deg);
}

.delete:hover {
  background: rgba(255, 215, 0, 0.5);
  transform: scale(1.1);
}

.delete:hover::before, .delete:hover::after {
  background: #ff6f00;
}

.modal-card-body {
  padding: 2rem;
  overflow-y: auto;
  flex-grow: 1;
  background: transparent;
}

.modal-card-foot {
  background: rgba(15, 31, 15, 0.9);
  border: none;
  padding: 1.5rem;
  gap: 0.75rem;
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
}

.field {
  margin-bottom: 1.25rem;
}

.label {
  color: #e0f2f1;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: block;
}

.control {
  position: relative;
}

.control .input,
.control .textarea,
.control .select select {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  padding-left: 2.75rem;
  transition: all 0.3s ease;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  width: 100%;
  box-sizing: border-box;
}

.control .textarea {
  padding-left: 0.75rem;
}

.control .input::placeholder,
.control .textarea::placeholder {
  color: #90a4ae;
}

.control .input:focus,
.control .textarea:focus,
.control .select select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.control .icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
}

.message {
  border-radius: 8px;
  overflow: hidden;
}

.message.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(211, 47, 47, 0.2));
  border: 1px solid rgba(244, 67, 54, 0.5);
}

.message-body {
  color: #ffcdd2;
  padding: 1rem;
}

.notification.is-info {
  background: linear-gradient(135deg, rgba(77, 182, 172, 0.2), rgba(38, 166, 154, 0.2));
  color: #4db6ac;
  border: 1px solid rgba(77, 182, 172, 0.3);
  padding: 1rem;
  border-radius: 8px;
}

.timeline {
  padding: 1rem 0;
}

.timeline-item {
  position: relative;
  padding-left: 2.5rem;
  padding-bottom: 1.5rem;
  border-left: 2px solid rgba(255, 215, 0, 0.3);
}

.timeline-item:last-child {
  border-left: none;
  padding-bottom: 0;
}

.timeline-marker {
  position: absolute;
  left: -0.6rem;
  top: 0;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  border: 2px solid rgba(255, 215, 0, 0.5);
  border-radius: 50%;
  width: 1.2rem;
  height: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-marker i {
  font-size: 0.7rem;
  color: #0d1b0d;
}

.timeline-content {
  padding-left: 0.5rem;
}

.timeline-content .heading {
  color: #90a4ae;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.timeline-content strong {
  color: #e0f2f1;
}

.timeline-content p {
  margin-bottom: 0.25rem;
}

.modal.is-active .modal-card {
  animation: modal-slideIn 0.3s ease-out;
}

@keyframes modal-slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.has-text-centered {
  text-align: center;
}

.control .select {
  width: 100%;
}

.control .select select {
  width: 100%;
  cursor: pointer;
}

.control .select::after {
  border-color: #9e9d24;
  right: 1.125em;
  z-index: 4;
}

.control .select select:focus + .icon {
  color: #ffd700;
}

.checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
  accent-color: #ffd700;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #c8e6c9;
}

.mb-3 {
  margin-bottom: 0.75rem;
}

.modal-card-foot .button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border: none;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.modal-card-foot .button.is-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.modal-card-foot .button {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.75rem 1.5rem;
}

.modal-card-foot .button:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

@media screen and (max-width: 1023px) {
  .attendance-details-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-text .title {
    font-size: 1.5rem;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .action-buttons-group {
    justify-content: stretch;
  }
  
  .action-buttons-group .button {
    flex: 1;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .modal {
    padding: 10px;
  }
  
  .modal-card {
    max-height: calc(100vh - 20px);
    max-width: 100%;
  }
  
  .modal-card-body {
    padding: 1.5rem;
  }
  
  .modal-card-head {
    padding: 1.25rem;
  }
  
  .modal-card-foot {
    padding: 1.25rem;
    flex-direction: column;
  }
  
  .modal-card-foot .button {
    width: 100%;
    justify-content: center;
  }
}
</style>