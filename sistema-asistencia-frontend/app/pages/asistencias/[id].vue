<template>
  <div class="container">
    <div class="hero is-info is-bold mb-5" v-if="periodStore.selectedPeriod">
      <div class="hero-body">
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <div>
                <h1 class="title has-text-white">{{ periodStore.selectedPeriod.nombre }}</h1>
                <p class="subtitle has-text-white-bis">{{ formatDate(periodStore.selectedPeriod.fecha_asistencia) }}</p>
              </div>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <button class="button is-light" @click="router.back()">
                <span class="icon">
                  <i class="mdi mdi-arrow-left"></i>
                </span>
                <span>Volver</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="attendanceStore.error || periodStore.error || cooperativistaStore.error" class="notification is-danger is-light">
      <button class="delete" @click="clearErrors"></button>
      <strong>Error:</strong> {{ attendanceStore.error || periodStore.error || cooperativistaStore.error }}
    </div>

    <div class="box" v-if="periodStore.selectedPeriod">
      <div class="columns is-multiline">
        <div class="column is-6">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control">
              <div class="tags has-addons">
                <span class="tag is-dark">
                  <span class="icon">
                    <i class="mdi mdi-clock-outline"></i>
                  </span>
                  <span>Horario</span>
                </span>
                <span class="tag is-info is-medium">
                  {{ periodStore.selectedPeriod.hora_inicio.substring(0, 5) }} - {{ periodStore.selectedPeriod.hora_fin.substring(0, 5) }}
                </span>
              </div>
            </div>
            <div class="control">
              <div class="tags has-addons">
                <span class="tag is-dark">
                  <span class="icon">
                    <i class="mdi mdi-information"></i>
                  </span>
                  <span>Estado</span>
                </span>
                <span v-if="periodStore.selectedPeriod.is_open" class="tag is-success is-medium">
                  <span class="icon">
                    <i class="mdi mdi-lock-open"></i>
                  </span>
                  <span>Abierto</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'programado'" class="tag is-info is-medium">
                  <span class="icon">
                    <i class="mdi mdi-clock-outline"></i>
                  </span>
                  <span>Programado</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'en_curso'" class="tag is-primary is-medium">
                  <span class="icon">
                    <i class="mdi mdi-clock"></i>
                  </span>
                  <span>En Curso</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(periodStore.selectedPeriod) === 'finalizado'" class="tag is-dark is-medium">
                  <span class="icon">
                    <i class="mdi mdi-check-circle"></i>
                  </span>
                  <span>Finalizado</span>
                </span>
                <span v-else class="tag is-light is-medium">
                  <span class="icon">
                    <i class="mdi mdi-lock"></i>
                  </span>
                  <span>Cerrado</span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-6">
          <div class="field is-grouped is-grouped-multiline is-pulled-right">
            <div class="control">
              <div class="tags has-addons">
                <span class="tag is-dark">
                  <span class="icon">
                    <i class="mdi mdi-account-multiple-check"></i>
                  </span>
                  <span>Asistencias</span>
                </span>
                <span class="tag is-primary is-medium">
                  <strong>{{ periodStore.selectedPeriod.total_marked }}</strong> / {{ periodStore.selectedPeriod.total_expected }}
                </span>
              </div>
            </div>
            <div class="control" v-if="periodStore.selectedPeriod.total_expected > 0">
              <div class="tags has-addons">
                <span class="tag is-dark">
                  <span class="icon">
                    <i class="mdi mdi-percent"></i>
                  </span>
                  <span>Porcentaje</span>
                </span>
                <span class="tag is-medium" :class="{
                  'is-success': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) >= 80,
                  'is-warning': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) >= 50 && Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) < 80,
                  'is-danger': Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) < 50
                }">
                  {{ Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h2 class="title is-4">Lista de Asistencias</h2>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <button class="button is-primary" @click="showAddModal = true">
              <span class="icon">
                <i class="mdi mdi-plus-circle"></i>
              </span>
              <span>Agregar Asistencia Manual</span>
            </button>
          </div>
        </div>
      </div>

      <div class="field">
        <label class="label">Buscar por CI o Nombre</label>
        <div class="control has-icons-left has-icons-right">
          <input 
            class="input is-medium" 
            type="text" 
            placeholder="Ingrese CI o nombre del cooperativista..." 
            v-model="searchFilter"
          >
          <span class="icon is-left is-medium">
            <i class="mdi mdi-magnify"></i>
          </span>
          <span class="icon is-right is-medium" v-if="searchFilter">
            <a @click="searchFilter = ''">
              <i class="mdi mdi-close-circle"></i>
            </a>
          </span>
        </div>
      </div>
    </div>

    <div class="box">
      <div v-if="attendanceStore.loading" class="has-text-centered py-6">
        <span class="icon is-large has-text-primary">
          <i class="mdi mdi-loading mdi-spin mdi-48px"></i>
        </span>
        <p class="mt-3">Cargando asistencias...</p>
      </div>

      <div v-else-if="filteredAttendances.length === 0" class="has-text-centered py-6">
        <span class="icon is-large has-text-grey-light">
          <i class="mdi mdi-account-off mdi-48px"></i>
        </span>
        <p class="mt-3 has-text-grey">No hay asistencias registradas</p>
      </div>

      <div v-else class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
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
            <tr v-for="attendance in filteredAttendances" :key="attendance.id">
              <td>
                <span class="tag is-medium">{{ getCooperativistaById(attendance.cooperativista_id)?.ci || 'N/A' }}</span>
              </td>
              <td>
                <strong>{{ getCooperativistaById(attendance.cooperativista_id)?.nombres || 'Cooperativista no encontrado' }}</strong>
                <br>
                <small class="has-text-grey">{{ getCooperativistaById(attendance.cooperativista_id)?.apellidos || '' }}</small>
              </td>
              <td>{{ formatDate(attendance.fecha) }}</td>
              <td>
                <span class="icon-text">
                  <span class="icon has-text-info">
                    <i class="mdi mdi-clock"></i>
                  </span>
                  <span>{{ attendance.hora.substring(0, 5) }}</span>
                </span>
              </td>
              <td class="has-text-centered">
                <span class="tag is-medium" :class="{
                  'is-success': attendance.tipo === 'entrada',
                  'is-warning': attendance.tipo === 'salida'
                }">
                  <span class="icon">
                    <i :class="attendance.tipo === 'entrada' ? 'mdi mdi-login' : 'mdi mdi-logout'"></i>
                  </span>
                  <span>{{ attendance.tipo.toUpperCase() }}</span>
                </span>
              </td>
              <td>
                <div class="buttons are-small is-centered">
                  <button 
                    class="button is-info"
                    @click="viewLogs(attendance.id)"
                    title="Ver logs"
                  >
                    <span class="icon">
                      <i class="mdi mdi-history"></i>
                    </span>
                  </button>
                  <button 
                    class="button is-danger"
                    @click="confirmDelete(attendance.id)"
                    title="Eliminar registro"
                  >
                    <span class="icon">
                      <i class="mdi mdi-delete"></i>
                    </span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showAddModal }">
      <div class="modal-background" @click="closeAddModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-account-plus"></i>
              </span>
              <span>Agregar Asistencia Manual</span>
            </span>
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

          <div class="notification is-info is-light">
            <p><strong>Nota:</strong> Se creará un log con el motivo especificado para auditoría.</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="saveManualAttendance"
            :disabled="!canSaveManualAttendance || attendanceStore.loading"
          >
            <span class="icon">
              <i class="mdi mdi-content-save"></i>
            </span>
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
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-history"></i>
              </span>
              <span>Historial de Cambios</span>
            </span>
          </p>
          <button class="delete" @click="showLogsModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="attendanceStore.logs.length === 0" class="has-text-centered py-6">
            <p class="has-text-grey">No hay logs registrados</p>
          </div>
          <div v-else class="timeline">
            <div v-for="log in attendanceStore.logs" :key="log.id" class="timeline-item">
              <div class="timeline-marker is-icon">
                <i class="mdi mdi-flag"></i>
              </div>
              <div class="timeline-content">
                <p class="heading">{{ formatDateTime(log.created_at) }}</p>
                <p><strong>{{ log.action }}</strong></p>
                <p v-if="log.reason" class="has-text-grey">{{ log.reason }}</p>
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
          <p class="modal-card-title has-text-white">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-alert-circle"></i>
              </span>
              <span>Confirmar Eliminación</span>
            </span>
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
            <span class="icon">
              <i class="mdi mdi-delete"></i>
            </span>
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

onMounted(() => {
  loadData()
})

useHead({
  title: 'Detalle de Período de Asistencia'
})
</script>

<style scoped>
.timeline {
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
  padding-bottom: 1.5rem;
  border-left: 2px solid #dbdbdb;
  padding-left: 2rem;
}

.timeline-item:last-child {
  border-left: none;
}

.timeline-marker {
  position: absolute;
  left: -0.65rem;
  top: 0;
  width: 1.3rem;
  height: 1.3rem;
  border-radius: 50%;
  background: #3273dc;
  border: 2px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-marker.is-icon {
  background: #48c774;
}

.timeline-marker i {
  font-size: 0.7rem;
  color: white;
}

.timeline-content .heading {
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
}

.index_home-page {
  min-height: calc(100vh - 200px);
  padding: 1.5rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
  width: 100%;
  position: relative;
}

.index_home-welcome-section {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 30px rgba(76, 175, 80, 0.2), 0 0 60px rgba(255, 215, 0, 0.1);
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-welcome-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  animation: index_home-float 20s infinite linear;
  z-index: 0;
}

.index_home-welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  position: relative;
  z-index: 1;
  flex-wrap: wrap;
}

.index_home-welcome-text {
  flex: 1;
  min-width: 300px;
}

.index_home-welcome-text .index_home-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 800;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
  font-size: 1.75rem;
}

.index_home-welcome-text .index_home-subtitle {
  color: #a5d6a7;
  margin: 0;
  font-weight: 500;
  font-size: 1.1rem;
}

.index_home-date-time-box {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 1.25rem 1.75rem;
  text-align: center;
  border: 2px solid rgba(255, 215, 0, 0.4);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  min-width: 180px;
  position: relative;
  z-index: 1;
}

.index_home-current-date {
  color: #c8e6c9;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: capitalize;
  margin-bottom: 0.5rem;
}

.index_home-current-time {
  color: #ffd700;
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.index_home-main-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
}

.index_home-stat-box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  border: 2px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-stat-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.index_home-stat-box:hover::before {
  left: 100%;
}

.index_home-stat-box:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 30px rgba(158, 157, 36, 0.3), 0 0 50px rgba(255, 215, 0, 0.15);
}

.index_home-stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #0d1b0d;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.index_home-stat-box:hover .index_home-stat-icon {
  transform: scale(1.08) rotate(5deg);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
}

.index_home-stat-info {
  flex: 1;
}

.index_home-stat-number {
  font-size: 2.25rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.4rem;
  text-shadow: 0 3px 15px rgba(255, 215, 0, 0.3);
}

.index_home-stat-title {
  font-weight: 700;
  font-size: 1rem;
  color: #e0f2f1;
  margin-bottom: 0.4rem;
  letter-spacing: 0.4px;
}

.index_home-stat-footer {
  color: #a5d6a7;
  font-size: 0.85rem;
  font-weight: 500;
}

.index_home-secondary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.index_home-info-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(135deg, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-info-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #ffd700, #9e9d24);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.index_home-info-card:hover::after {
  transform: scaleX(1);
}

.index_home-info-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 6px 25px rgba(158, 157, 36, 0.25);
}

.index_home-info-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #e0f2f1;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.4);
  transition: all 0.3s ease;
}

.index_home-info-card:hover .index_home-info-icon {
  transform: scale(1.08);
  background: linear-gradient(135deg, #9e9d24 0%, #cddc39 100%);
  color: #0d1b0d;
}

.index_home-info-content {
  flex: 1;
}

.index_home-info-value {
  font-size: 2rem;
  font-weight: 900;
  background: linear-gradient(135deg, #9e9d24, #cddc39);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.4rem;
  text-shadow: 0 3px 12px rgba(158, 157, 36, 0.3);
}

.index_home-info-label {
  font-size: 0.9rem;
  color: #c8e6c9;
  font-weight: 600;
  letter-spacing: 0.3px;
}

@keyframes index_home-float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-80px) rotate(360deg);
  }
}

/* Responsive Design */
@media screen and (max-width: 1024px) {
  .index_home-page {
    padding: 1.25rem;
    margin: -1.5rem -1rem;
  }
  
  .index_home-main-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .index_home-secondary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .index_home-welcome-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  
  .index_home-date-time-box {
    width: 100%;
    min-width: unset;
  }
  
  .index_home-welcome-text .index_home-title {
    font-size: 1.5rem;
  }
  
  .index_home-welcome-text .index_home-subtitle {
    font-size: 1rem;
  }
}

@media screen and (max-width: 768px) {
  .index_home-page {
    padding: 1rem;
    margin: -1rem -0.75rem;
  }
  
  .index_home-welcome-section {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 14px;
  }
  
  .index_home-main-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .index_home-secondary-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .index_home-stat-box {
    padding: 1.25rem;
    border-radius: 12px;
  }
  
  .index_home-stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.75rem;
  }
  
  .index_home-stat-number {
    font-size: 2rem;
  }
  
  .index_home-info-card {
    padding: 1.25rem;
    border-radius: 12px;
  }
  
  .index_home-info-icon {
    width: 55px;
    height: 55px;
    font-size: 1.5rem;
  }
  
  .index_home-info-value {
    font-size: 1.75rem;
  }
  
  .index_home-current-time {
    font-size: 1.5rem;
  }
  
  .index_home-current-date {
    font-size: 0.85rem;
  }
}

@media screen and (max-width: 480px) {
  .index_home-page {
    padding: 0.75rem;
    margin: -0.75rem -0.5rem;
  }
  
  .index_home-welcome-section {
    padding: 1.25rem 1rem;
    border-radius: 12px;
    border-width: 2px;
  }
  
  .index_home-welcome-text .index_home-title {
    font-size: 1.25rem;
    line-height: 1.3;
  }
  
  .index_home-welcome-text .index_home-subtitle {
    font-size: 0.9rem;
  }
  
  .index_home-stat-box {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1rem;
  }
  
  .index_home-stat-number {
    font-size: 1.75rem;
  }
  
  .index_home-stat-title {
    font-size: 0.95rem;
  }
  
  .index_home-stat-footer {
    font-size: 0.8rem;
  }
  
  .index_home-info-card {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .index_home-info-value {
    font-size: 1.5rem;
  }
  
  .index_home-info-label {
    font-size: 0.85rem;
  }
  
  .index_home-date-time-box {
    padding: 1rem;
  }
  
  .index_home-current-time {
    font-size: 1.25rem;
  }
  
  .index_home-current-date {
    font-size: 0.8rem;
  }
}

/* Para tablets en modo paisaje */
@media (min-width: 769px) and (max-width: 1024px) and (orientation: landscape) {
  .index_home-main-stats {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .index_home-secondary-stats {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .index_home-welcome-content {
    flex-direction: row;
  }
  
  .index_home-date-time-box {
    width: auto;
    min-width: 180px;
  }
}

/* Para pantallas muy grandes */
@media (min-width: 1400px) {
  .index_home-page {
    padding: 2rem;
    max-width: 1400px;
    margin: -2rem auto;
  }
  
  .index_home-welcome-section {
    padding: 3rem;
    margin-bottom: 2.5rem;
  }
  
  .index_home-main-stats {
    gap: 1.5rem;
  }
  
  .index_home-stat-box {
    padding: 2rem;
  }
  
  .index_home-stat-number {
    font-size: 2.5rem;
  }
  
  .index_home-stat-icon {
    width: 80px;
    height: 80px;
    font-size: 2.25rem;
  }
  
  .index_home-info-card {
    padding: 2rem;
  }
  
  .index_home-info-value {
    font-size: 2.25rem;
  }
  
  .index_home-info-icon {
    width: 70px;
    height: 70px;
    font-size: 2rem;
  }
}
</style>