<template>
  <div class="container">
    <div class="hero is-primary is-bold mb-5">
      <div class="hero-body">
        <h1 class="title">Gestión de Períodos de Asistencia</h1>
        <p class="subtitle">Administra períodos mensuales con apertura automática</p>
      </div>
    </div>

    <div v-if="periodStore.error" class="notification is-danger is-light">
      <button class="delete" @click="periodStore.error = null"></button>
      <strong>Error:</strong> {{ periodStore.error }}
    </div>

    <div class="columns">
      <div class="column">
        <div class="box">
          <button class="button is-primary is-medium" @click="showCreateModal = true">
            <span class="icon">
              <i class="mdi mdi-plus-circle"></i>
            </span>
            <span>Crear Nuevo Período</span>
          </button>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-5 mb-4">Filtros de Búsqueda</h2>
      <div class="columns">
        <div class="column is-3">
          <div class="field">
            <label class="label">Mes</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="filters.mes">
                  <option :value="null">Todos los meses</option>
                  <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-calendar-month"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">Año</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="filters.anio">
                  <option :value="null">Todos los años</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-calendar"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">Estado</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="filters.activeOnly">
                  <option :value="false">Todos</option>
                  <option :value="true">Solo activos</option>
                </select>
              </div>
              <span class="icon is-left">
                <i class="mdi mdi-filter"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">&nbsp;</label>
            <button class="button is-info is-fullwidth" @click="loadPeriods">
              <span class="icon">
                <i class="mdi mdi-magnify"></i>
              </span>
              <span>Buscar</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <div v-if="periodStore.loading" class="has-text-centered py-6">
        <span class="icon is-large has-text-primary">
          <i class="mdi mdi-loading mdi-spin mdi-48px"></i>
        </span>
        <p class="mt-3">Cargando períodos...</p>
      </div>

      <div v-else-if="filteredPeriods.length === 0" class="has-text-centered py-6">
        <span class="icon is-large has-text-grey-light">
          <i class="mdi mdi-calendar-blank mdi-48px"></i>
        </span>
        <p class="mt-3 has-text-grey">No hay períodos registrados</p>
      </div>

      <div v-else class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>Período</th>
              <th>Fecha</th>
              <th>Horario</th>
              <th class="has-text-centered">Duración</th>
              <th class="has-text-centered">Estado</th>
              <th class="has-text-centered">Asistencias</th>
              <th class="has-text-centered">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="period in filteredPeriods" :key="period.id">
              <td>
                <strong>{{ period.nombre }}</strong>
                <br>
                <small class="has-text-grey">{{ period.descripcion }}</small>
              </td>
              <td>{{ formatDate(period.fecha_asistencia) }}</td>
              <td>
                <span class="icon-text">
                  <span class="icon has-text-info">
                    <i class="mdi mdi-clock-start"></i>
                  </span>
                  <span>{{ period.hora_inicio.substring(0, 5) }}</span>
                </span>
                <br>
                <span class="icon-text">
                  <span class="icon has-text-danger">
                    <i class="mdi mdi-clock-end"></i>
                  </span>
                  <span>{{ period.hora_fin.substring(0, 5) }}</span>
                </span>
              </td>
              <td class="has-text-centered">
                <span class="tag is-medium">
                  <span class="icon">
                    <i class="mdi mdi-timer"></i>
                  </span>
                  <span>{{ calculateDuration(period.hora_inicio, period.hora_fin) }}</span>
                </span>
              </td>
              <td class="has-text-centered">
                <span v-if="period.is_open" class="tag is-success is-medium">
                  <span class="icon">
                    <i class="mdi mdi-lock-open"></i>
                  </span>
                  <span>Abierto</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(period) === 'en_curso'" class="tag is-warning is-medium">
                  <span class="icon">
                    <i class="mdi mdi-alert"></i>
                  </span>
                  <span>En Curso (Cerrado)</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(period) === 'programado'" class="tag is-info is-medium">
                  <span class="icon">
                    <i class="mdi mdi-clock-outline"></i>
                  </span>
                  <span>Programado</span>
                </span>
                <span v-else-if="periodStore.getPeriodStatus(period) === 'finalizado'" class="tag is-dark is-medium">
                  <span class="icon">
                    <i class="mdi mdi-check-circle"></i>
                  </span>
                  <span>Finalizado</span>
                </span>
                <span v-else class="tag is-light is-medium">
                  <span class="icon">
                    <i class="mdi mdi-help-circle"></i>
                  </span>
                  <span>Cerrado</span>
                </span>
              </td>
              <td class="has-text-centered">
                <div class="field is-grouped is-grouped-centered">
                  <p class="control">
                    <span class="tag is-large">
                      <strong>{{ period.total_marked }}</strong> / {{ period.total_expected }}
                    </span>
                  </p>
                </div>
                <div v-if="period.total_expected > 0" class="mt-2">
                  <progress 
                    class="progress is-small" 
                    :class="{
                      'is-success': Math.round((period.total_marked / period.total_expected) * 100) >= 80,
                      'is-warning': Math.round((period.total_marked / period.total_expected) * 100) >= 50 && Math.round((period.total_marked / period.total_expected) * 100) < 80,
                      'is-danger': Math.round((period.total_marked / period.total_expected) * 100) < 50
                    }"
                    :value="period.total_marked" 
                    :max="period.total_expected"
                  >
                    {{ Math.round((period.total_marked / period.total_expected) * 100) }}%
                  </progress>
                  <small class="has-text-grey">{{ Math.round((period.total_marked / period.total_expected) * 100) }}%</small>
                </div>
              </td>
              <td>
                <div class="buttons are-small is-centered">
                  <button 
                    class="button is-primary"
                    @click="viewPeriodDetails(period.id)"
                    title="Ver Detalles"
                  >
                    <span class="icon">
                      <i class="mdi mdi-eye"></i>
                    </span>
                  </button>
                  
                  <button 
                    v-if="!period.is_open"
                    class="button is-success"
                    @click="openPeriod(period.id)"
                    :disabled="periodStore.loading"
                    title="Abrir Período"
                  >
                    <span class="icon">
                      <i class="mdi mdi-lock-open"></i>
                    </span>
                  </button>
                  
                  <button 
                    v-if="period.is_open" 
                    class="button is-warning"
                    @click="closePeriod(period.id)"
                    :disabled="periodStore.loading"
                    title="Cerrar Período"
                  >
                    <span class="icon">
                      <i class="mdi mdi-lock"></i>
                    </span>
                  </button>
                  
                  <button 
                    v-if="periodStore.getPeriodStatus(period) !== 'en_curso'"
                    class="button is-light"
                    @click="editPeriod(period)"
                    title="Editar"
                  >
                    <span class="icon">
                      <i class="mdi mdi-pencil"></i>
                    </span>
                  </button>
                  
                  <button 
                    class="button is-danger"
                    @click="confirmDeactivate(period.id)"
                    :disabled="periodStore.loading || period.is_open"
                    title="Desactivar"
                  >
                    <span class="icon">
                      <i class="mdi mdi-cancel"></i>
                    </span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showCreateModal || showEditModal }">
      <div class="modal-background" @click="closeModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-calendar-plus"></i>
              </span>
              <span>{{ showEditModal ? 'Editar Período' : 'Crear Nuevo Período' }}</span>
            </span>
          </p>
          <button class="delete" @click="closeModal"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nombre del Período *</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                placeholder="Ej: Reunión Mensual - Enero 2025" 
                v-model="formData.nombre"
              >
              <span class="icon is-left">
                <i class="mdi mdi-format-title"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">Descripción</label>
            <div class="control">
              <textarea 
                class="textarea" 
                placeholder="Descripción opcional del período..."
                v-model="formData.descripcion"
                rows="2"
              ></textarea>
            </div>
          </div>

          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Mes *</label>
                <div class="control has-icons-left">
                  <div class="select is-fullwidth">
                    <select v-model="formData.mes">
                      <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
                    </select>
                  </div>
                  <span class="icon is-left">
                    <i class="mdi mdi-calendar-month"></i>
                  </span>
                </div>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Año *</label>
                <div class="control has-icons-left">
                  <div class="select is-fullwidth">
                    <select v-model="formData.anio">
                      <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                    </select>
                  </div>
                  <span class="icon is-left">
                    <i class="mdi mdi-calendar"></i>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Fecha de Asistencia *</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="date" 
                v-model="formData.fecha_asistencia"
              >
              <span class="icon is-left">
                <i class="mdi mdi-calendar-today"></i>
              </span>
            </div>
          </div>

          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Hora de Inicio *</label>
                <div class="control has-icons-left">
                  <input 
                    class="input" 
                    type="time" 
                    v-model="formData.hora_inicio"
                  >
                  <span class="icon is-left">
                    <i class="mdi mdi-clock-start"></i>
                  </span>
                </div>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Hora de Fin *</label>
                <div class="control has-icons-left">
                  <input 
                    class="input" 
                    type="time" 
                    v-model="formData.hora_fin"
                  >
                  <span class="icon is-left">
                    <i class="mdi mdi-clock-end"></i>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="notification is-info is-light">
            <p><strong>Nota:</strong> El período se abrirá automáticamente cuando llegue la hora de inicio.</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="savePeriod"
            :disabled="!canSavePeriod || periodStore.loading"
          >
            <span class="icon">
              <i class="mdi mdi-content-save"></i>
            </span>
            <span v-if="periodStore.loading">Guardando...</span>
            <span v-else>{{ showEditModal ? 'Actualizar' : 'Crear Período' }}</span>
          </button>
          <button class="button" @click="closeModal">Cancelar</button>
        </footer>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showDeactivateModal }">
      <div class="modal-background" @click="showDeactivateModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head has-background-warning">
          <p class="modal-card-title">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-alert-circle"></i>
              </span>
              <span>Confirmar Desactivación</span>
            </span>
          </p>
          <button class="delete" @click="showDeactivateModal = false"></button>
        </header>
        <section class="modal-card-body">
          <article class="message is-warning">
            <div class="message-body">
              <p class="mb-3">¿Está seguro de que desea desactivar este período?</p>
              <p>El período será marcado como inactivo pero no se eliminará permanentemente.</p>
            </div>
          </article>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-warning" 
            @click="deactivatePeriod"
            :disabled="periodStore.loading"
          >
            <span class="icon">
              <i class="mdi mdi-cancel"></i>
            </span>
            <span v-if="periodStore.loading">Desactivando...</span>
            <span v-else>Desactivar</span>
          </button>
          <button class="button" @click="showDeactivateModal = false">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import 'dayjs/locale/es'
import { useAttendancePeriodStore } from '~/stores/attendancePeriod'

dayjs.locale('es')

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const router = useRouter()
const periodStore = useAttendancePeriodStore()

const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeactivateModal = ref(false)
const periodToDeactivate = ref(null)
const editingPeriodId = ref(null)

const filters = ref({
  mes: null,
  anio: null,
  activeOnly: true
})

const formData = ref({
  nombre: '',
  descripcion: '',
  mes: new Date().getMonth() + 1,
  anio: new Date().getFullYear(),
  fecha_asistencia: '',
  hora_inicio: '07:00',
  hora_fin: '19:00'
})

const years = computed(() => {
  const currentYear = new Date().getFullYear()
  return [currentYear - 1, currentYear, currentYear + 1]
})

const filteredPeriods = computed(() => {
  return periodStore.periods.filter(p => {
    if (filters.value.activeOnly && !p.is_active) return false
    return true
  })
})

const canSavePeriod = computed(() => {
  return !!formData.value.nombre &&
         !!formData.value.fecha_asistencia &&
         !!formData.value.hora_inicio &&
         !!formData.value.hora_fin
})

const getMonthName = (month) => {
  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ]
  return months[month - 1]
}

const formatDate = (dateString) => {
  const date = dayjs(`${dateString}T00:00:00`)
  return date.locale('es').format('dddd, D [de] MMMM [de] YYYY')
}

const calculateDuration = (startTime, endTime) => {
  if (!startTime || !endTime) return ''
  const start = dayjs(`2000-01-01T${startTime}`)
  let end = dayjs(`2000-01-01T${endTime}`)

  if (end.isBefore(start)) {
    end = end.add(1, 'day')
  }

  const diffMinutes = end.diff(start, 'minute')
  const hours = Math.floor(diffMinutes / 60)
  const minutes = diffMinutes % 60

  if (hours > 0) {
    return minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`
  }
  return `${minutes}m`
}

const loadPeriods = async () => {
  try {
    await periodStore.fetchPeriods(0, 100, filters.value.activeOnly)
  } catch (error) {
    console.error('Error al cargar períodos:', error)
  }
}

const openPeriod = async (periodId) => {
  if (!confirm('¿Abrir este período para que los cooperativistas puedan marcar asistencia?')) {
    return
  }

  try {
    await periodStore.openPeriod(periodId)
    await loadPeriods()
  } catch (error) {
    console.error('Error al abrir período:', error)
  }
}

const closePeriod = async (periodId) => {
  if (!confirm('¿Cerrar este período? Los cooperativistas ya no podrán marcar asistencia.')) {
    return
  }

  try {
    await periodStore.closePeriod(periodId)
    await loadPeriods()
  } catch (error) {
    console.error('Error al cerrar período:', error)
  }
}

const viewPeriodDetails = (periodId) => {
  router.push(`/asistencias/${periodId}`)
}

const editPeriod = (period) => {
  editingPeriodId.value = period.id
  formData.value = {
    nombre: period.nombre,
    descripcion: period.descripcion || '',
    mes: period.mes,
    anio: period.anio,
    fecha_asistencia: period.fecha_asistencia,
    hora_inicio: period.hora_inicio ? period.hora_inicio.substring(0, 5) : '07:00',
    hora_fin: period.hora_fin ? period.hora_fin.substring(0, 5) : '19:00'
  }
  showEditModal.value = true
}

const savePeriod = async () => {
  try {
    const data = {
      nombre: formData.value.nombre,
      descripcion: formData.value.descripcion,
      mes: parseInt(formData.value.mes),
      anio: parseInt(formData.value.anio),
      fecha_asistencia: formData.value.fecha_asistencia,
      hora_inicio: formData.value.hora_inicio + ':00',
      hora_fin: formData.value.hora_fin + ':00'
    }

    if (showEditModal.value) {
      await periodStore.updatePeriod(editingPeriodId.value, data)
    } else {
      await periodStore.createPeriod(data)
    }

    closeModal()
    await loadPeriods()
  } catch (error) {
    console.error('Error al guardar período:', error)
  }
}

const confirmDeactivate = (periodId) => {
  periodToDeactivate.value = periodId
  showDeactivateModal.value = true
}

const deactivatePeriod = async () => {
  try {
    await periodStore.deactivatePeriod(periodToDeactivate.value)
    showDeactivateModal.value = false
    periodToDeactivate.value = null
    await loadPeriods()
  } catch (error) {
    console.error('Error al desactivar período:', error)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingPeriodId.value = null
  formData.value = {
    nombre: '',
    descripcion: '',
    mes: new Date().getMonth() + 1,
    anio: new Date().getFullYear(),
    fecha_asistencia: '',
    hora_inicio: '07:00',
    hora_fin: '19:00'
  }
}

onMounted(() => {
  loadPeriods()
})

useHead({
  title: 'Gestión de Períodos de Asistencia'
})
</script>


<style scoped>
.container {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(135deg, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.hero.is-primary.is-bold {
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

.hero.is-primary.is-bold::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  animation: hero-float 20s infinite linear;
  z-index: 0;
}

.hero-body {
  position: relative;
  z-index: 1;
}

.hero-body .title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 800;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
  font-size: 2rem;
}

.hero-body .subtitle {
  color: #a5d6a7;
  margin: 0;
  font-weight: 500;
  font-size: 1.1rem;
}

/* Notification */
.notification.is-danger.is-light {
  background: linear-gradient(135deg, rgba(211, 47, 47, 0.15), rgba(244, 67, 54, 0.1));
  backdrop-filter: blur(10px);
  border: 2px solid rgba(244, 67, 54, 0.4);
  border-radius: 12px;
  color: #ffcdd2;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
  margin-bottom: 1.5rem;
}

.notification.is-danger.is-light strong {
  color: #ffebee;
}

.notification .delete {
  background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
  border: 2px solid #ffd700;
  transition: all 0.3s ease;
}

.notification .delete:hover {
  transform: scale(1.1);
}

/* Box styling */
.box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  backdrop-filter: blur(10px);
  border-radius: 14px;
  border: 2px solid rgba(46, 125, 50, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  margin-bottom: 1.5rem;
}

.box:hover {
  border-color: rgba(255, 215, 0, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.15);
}

.box .title {
  color: #ffd700;
  font-weight: 700;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

/* Buttons */
.button {
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.button:hover::before {
  width: 300px;
  height: 300px;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border-color: #ffd700;
  color: #0d1b0d;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.button.is-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
  background: linear-gradient(135deg, #ff9800 0%, #ffd700 50%, #cddc39 100%);
}

.button.is-info {
  background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
  border-color: #2e7d32;
  color: #e0f2f1;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
}

.button.is-info:hover:not(:disabled) {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
}

.button.is-success {
  background: linear-gradient(135deg, #388e3c 0%, #43a047 100%);
  border-color: #388e3c;
  color: #e0f2f1;
  box-shadow: 0 4px 15px rgba(56, 142, 60, 0.3);
}

.button.is-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #43a047 0%, #4caf50 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(56, 142, 60, 0.4);
}

.button.is-warning {
  background: linear-gradient(135deg, #f57c00 0%, #ff9800 100%);
  border-color: #f57c00;
  color: #fff3e0;
  box-shadow: 0 4px 15px rgba(245, 124, 0, 0.3);
}

.button.is-warning:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff9800 0%, #ffa726 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
}

.button.is-danger {
  background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
  border-color: #d32f2f;
  color: #ffebee;
  box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);
}

.button.is-danger:hover:not(:disabled) {
  background: linear-gradient(135deg, #f44336 0%, #ef5350 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
}

.button.is-light {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(158, 157, 36, 0.1));
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #c8e6c9;
}

.button.is-light:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(158, 157, 36, 0.2));
  border-color: #ffd700;
  color: #ffd700;
  transform: translateY(-3px);
}

/* MODIFICADO: Form elements con más padding para inputs */
.field .label {
  color: #e0f2f1;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  letter-spacing: 0.3px;
}

.control .input,
.control .textarea,
.control .select select {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  backdrop-filter: blur(10px);
  border: 2px solid rgba(46, 125, 50, 0.5);
  border-radius: 10px;
  color: #c8e6c9;
  font-weight: 500;
  padding: 0.625rem 0.875rem 0.625rem 3rem; /* MODIFICADO: Más padding a la izquierda */
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 100%;
  font-size: 0.95rem;
  position: relative;
}

.control .input:focus,
.control .textarea:focus,
.control .select select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2), 0 4px 15px rgba(255, 215, 0, 0.3);
  outline: none;
  transform: translateY(-2px);
}

.control .input::placeholder,
.control .textarea::placeholder {
  color: rgba(165, 214, 167, 0.6);
  font-weight: 500;
  font-size: 0.9rem;
  margin-left: 0.5rem; /* MODIFICADO: Espacio adicional para placeholder */
}

.control .select select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9)) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffd700'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E") no-repeat right 0.875rem center/16px 16px;
  padding-right: 2.5rem;
  padding-left: 3rem; /* MODIFICADO: Más padding a la izquierda para select */
  height: 2.75rem;
  cursor: pointer;
}

.control .select select:focus {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.95)) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffd700'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E") no-repeat right 0.875rem center/16px 16px;
}

.control .select select option {
  background: #0f1f0f;
  color: #c8e6c9;
  padding: 0.5rem;
}

.control.has-icons-left {
  position: relative;
}

.control.has-icons-left .icon.is-left {
  position: absolute;
  left: 1rem; /* MODIFICADO: Posición del ícono más a la izquierda */
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  color: #ffd700;
  font-size: 1.2rem;
  pointer-events: none; /* MODIFICADO: Para que no interfiera con clics */
}

/* MODIFICADO: Ajuste para inputs con íconos - texto más a la derecha */
.control.has-icons-left .input {
  padding-left: 3.5rem; /* MODIFICADO: Más padding para inputs con íconos */
}

/* MODIFICADO: Textarea necesita padding especial */
.control .textarea {
  padding-left: 1rem; /* MODIFICADO: Textarea menos padding porque no tiene ícono */
  min-height: 100px;
  resize: vertical;
}

/* MODIFICADO: Para inputs de tipo date y time */
.control .input[type="date"],
.control .input[type="time"] {
  padding-left: 3rem; /* MODIFICADO: Padding consistente */
  color-scheme: dark; /* Para modo oscuro en navegadores */
}

.help.is-danger {
  color: #ff5252;
  font-weight: 600;
  margin-top: 0.25rem;
  font-size: 0.85rem;
}

/* Table styling */
.table-container {
  background: linear-gradient(135deg, rgba(15, 31, 15, 0.9), rgba(10, 26, 10, 0.9));
  backdrop-filter: blur(10px);
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(46, 125, 50, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.table {
  background: transparent;
  color: #c8e6c9;
}

.table thead th {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  color: #ffd700;
  font-weight: 700;
  border-color: rgba(255, 215, 0, 0.3);
  padding: 1rem 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
}

.table tbody tr {
  background: rgba(15, 31, 15, 0.7);
  transition: all 0.3s ease;
}

.table tbody tr:nth-child(even) {
  background: rgba(26, 46, 26, 0.7);
}

.table tbody tr:hover {
  background: rgba(46, 125, 50, 0.2);
  transform: translateX(4px);
}

.table td {
  border-color: rgba(255, 215, 0, 0.1);
  padding: 0.875rem 0.75rem;
  vertical-align: middle;
}

.table td small.has-text-grey {
  color: #a5d6a7 !important;
  font-size: 0.85rem;
}

/* Tags */
.tag {
  border-radius: 8px;
  font-weight: 600;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.tag.is-success {
  background: linear-gradient(135deg, #388e3c 0%, #43a047 100%);
  border-color: #388e3c;
  color: #e0f2f1;
}

.tag.is-warning {
  background: linear-gradient(135deg, #f57c00 0%, #ff9800 100%);
  border-color: #f57c00;
  color: #fff3e0;
}

.tag.is-info {
  background: linear-gradient(135deg, #0288d1 0%, #03a9f4 100%);
  border-color: #0288d1;
  color: #e1f5fe;
}

.tag.is-primary {
  background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
  border-color: #1976d2;
  color: #e3f2fd;
}

.tag.is-danger {
  background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
  border-color: #d32f2f;
  color: #ffebee;
}

.tag.is-dark {
  background: linear-gradient(135deg, #424242 0%, #616161 100%);
  border-color: #424242;
  color: #f5f5f5;
}

.tag.is-medium {
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
}

.tag.is-large {
  font-size: 1rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 215, 0, 0.4);
  color: #ffd700;
}

.tag .icon {
  margin-right: 0.25rem;
}

/* Progress bar */
.progress {
  background: rgba(15, 31, 15, 0.8);
  border-radius: 10px;
  border: 2px solid rgba(46, 125, 50, 0.3);
  overflow: hidden;
  height: 0.75rem;
}

.progress::-webkit-progress-bar {
  background: rgba(15, 31, 15, 0.8);
}

.progress::-webkit-progress-value {
  background: linear-gradient(135deg, #2e7d32, #4caf50);
  border-radius: 10px;
}

.progress.is-success::-webkit-progress-value {
  background: linear-gradient(135deg, #388e3c, #4caf50);
}

.progress.is-warning::-webkit-progress-value {
  background: linear-gradient(135deg, #f57c00, #ff9800);
}

.progress.is-danger::-webkit-progress-value {
  background: linear-gradient(135deg, #d32f2f, #f44336);
}

/* Dropdown */
.dropdown.is-hoverable .dropdown-trigger .button {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(158, 157, 36, 0.1));
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #c8e6c9;
  transition: all 0.3s ease;
}

.dropdown.is-hoverable:hover .dropdown-trigger .button {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(158, 157, 36, 0.2));
  border-color: #ffd700;
  color: #ffd700;
}

.dropdown-menu {
  background: linear-gradient(135deg, rgba(15, 31, 15, 0.95), rgba(10, 26, 10, 0.95));
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 215, 0, 0.4);
  border-radius: 10px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  min-width: 180px;
}

.dropdown-content {
  background: transparent;
  border-radius: 8px;
  overflow: hidden;
}

.dropdown-item {
  color: #c8e6c9;
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 6px;
  margin: 0.25rem;
  padding: 0.5rem 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background: rgba(46, 125, 50, 0.3);
  color: #ffd700;
  transform: translateX(4px);
}

.dropdown-item .icon {
  font-size: 1rem;
}

/* Modal */
.modal-card {
  background: linear-gradient(135deg, #0f1f0f 0%, #0a1a0a 100%);
  border-radius: 16px;
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  max-width: 600px;
}

.modal-card-head {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%);
  border-bottom: 2px solid rgba(255, 215, 0, 0.4);
  padding: 1.5rem;
}

.modal-card-head.has-background-danger {
  background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
  border-bottom: 2px solid rgba(255, 215, 0, 0.4);
}

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-card-head.has-background-danger .modal-card-title {
  -webkit-text-fill-color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.modal-card-body {
  background: linear-gradient(135deg, rgba(15, 31, 15, 0.9), rgba(10, 26, 10, 0.9));
  padding: 1.5rem;
  color: #e0f2f1;
}

.modal-card-foot {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-top: 2px solid rgba(255, 215, 0, 0.3);
  padding: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Message boxes */
.message {
  background: linear-gradient(135deg, rgba(211, 47, 47, 0.1), rgba(244, 67, 54, 0.05));
  border: 2px solid rgba(244, 67, 54, 0.3);
  border-radius: 10px;
}

.message-body {
  background: transparent;
  color: #ffcdd2;
  font-weight: 600;
}

.notification.is-info.is-light {
  background: linear-gradient(135deg, rgba(2, 136, 209, 0.1), rgba(3, 169, 244, 0.05));
  border: 2px solid rgba(3, 169, 244, 0.3);
  border-radius: 10px;
  color: #b3e5fc;
  font-weight: 600;
}

/* Stats boxes */
.box.has-background-success-light {
  background: linear-gradient(135deg, rgba(56, 142, 60, 0.15), rgba(76, 175, 80, 0.1));
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
}

.box.has-background-warning-light {
  background: linear-gradient(135deg, rgba(245, 124, 0, 0.15), rgba(255, 152, 0, 0.1));
  border: 2px solid rgba(255, 152, 0, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
}

.box.has-background-info-light {
  background: linear-gradient(135deg, rgba(2, 136, 209, 0.15), rgba(3, 169, 244, 0.1));
  border: 2px solid rgba(3, 169, 244, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
}

.box.has-background-light {
  background: linear-gradient(135deg, rgba(158, 157, 36, 0.1), rgba(255, 215, 0, 0.05));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
}

.box .heading {
  color: #a5d6a7;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.box .title {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2rem;
  margin: 0;
  border: none;
  font-weight: 800;
}

/* Loading states */
.has-text-centered.py-6 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.icon.is-large.has-text-primary .mdi-spin {
  animation: spin 1s linear infinite;
  color: #ffd700;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.icon.is-large.has-text-grey-light .mdi {
  color: rgba(165, 214, 167, 0.5);
  font-size: 3rem;
}

.has-text-grey {
  color: #a5d6a7 !important;
  font-weight: 600;
}

/* Animation */
@keyframes hero-float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-80px) rotate(360deg);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* MODIFICADO: Responsive Design con ajustes para inputs */
@media screen and (max-width: 1024px) {
  .container {
    padding: 1.25rem;
    margin: -1.5rem -1rem;
  }
  
  .hero.is-primary.is-bold {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .hero-body .title {
    font-size: 1.5rem;
  }
  
  .hero-body .subtitle {
    font-size: 1rem;
  }
  
  .box {
    padding: 1.25rem;
  }
  
  .columns {
    flex-wrap: wrap;
  }
  
  .column.is-3 {
    width: 50%;
  }
  
  .column.is-6 {
    width: 50%;
  }
  
  .table {
    font-size: 0.9rem;
  }
  
  .buttons.are-small .button {
    padding: 0.375rem 0.75rem;
    font-size: 0.85rem;
  }
  
  /* MODIFICADO: Ajuste responsivo para inputs */
  .control .input,
  .control .textarea,
  .control .select select {
    padding-left: 2.8rem; /* Un poco menos en tablets */
  }
  
  .control.has-icons-left .input {
    padding-left: 3rem;
  }
  
  .control.has-icons-left .icon.is-left {
    left: 0.8rem;
    font-size: 1rem;
  }
  
  .control .textarea {
    padding-left: 0.875rem;
  }
}

@media screen and (max-width: 768px) {
  .container {
    padding: 1rem;
    margin: -1rem -0.75rem;
  }
  
  .hero.is-primary.is-bold {
    padding: 1.25rem;
    margin-bottom: 1.25rem;
    border-radius: 14px;
  }
  
  .hero-body .title {
    font-size: 1.25rem;
  }
  
  .hero-body .subtitle {
    font-size: 0.9rem;
  }
  
  .box {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 12px;
  }
  
  .box .title {
    font-size: 1.1rem;
  }
  
  .column.is-3 {
    width: 100%;
    margin-bottom: 0.75rem;
  }
  
  .column.is-6 {
    width: 100%;
    margin-bottom: 0.75rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .table {
    min-width: 800px;
  }
  
  .modal-card {
    margin: 0 1rem;
    max-width: calc(100% - 2rem);
  }
  
  .buttons.are-small {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .buttons.are-small .button {
    flex: 1 0 calc(50% - 0.5rem);
    min-width: 45px;
  }
  
  .tag.is-medium {
    font-size: 0.85rem;
    padding: 0.375rem 0.625rem;
  }
  
  .progress {
    height: 0.625rem;
  }
}

@media screen and (max-width: 480px) {
  .container {
    padding: 0.75rem;
    margin: -0.75rem -0.5rem;
  }
  
  .hero.is-primary.is-bold {
    padding: 1rem;
    margin-bottom: 1rem;
    border-width: 2px;
  }
  
  .hero-body .title {
    font-size: 1.1rem;
  }
  
  .hero-body .subtitle {
    font-size: 0.85rem;
  }
  
  .box {
    padding: 0.875rem;
    border-radius: 10px;
  }
  
  .button {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
  
  .button .icon {
    margin-right: 0.25rem;
  }
  
  .modal-card-head,
  .modal-card-body,
  .modal-card-foot {
    padding: 1rem;
  }
  
  .modal-card-title {
    font-size: 1.1rem;
  }
  
  .field .label {
    font-size: 0.85rem;
  }
  
  /* MODIFICADO: Ajuste móvil para inputs */
  .control .input,
  .control .textarea,
  .control .select select {
    padding: 0.5rem 0.75rem 0.5rem 2.5rem; /* Menos padding en móviles */
    font-size: 0.9rem;
  }
  
  .control.has-icons-left .input {
    padding-left: 2.8rem;
  }
  
  .control.has-icons-left .icon.is-left {
    left: 0.6rem;
  }
  
  .control .select select {
    padding-left: 2.5rem;
    padding-right: 2rem;
    background-position: right 0.6rem center;
  }
  
  .box .title {
    font-size: 1.75rem;
  }
  
  .box .heading {
    font-size: 0.85rem;
  }
  
  .has-text-centered .mt-3 {
    font-size: 0.9rem;
  }
  
  .notification.is-info.is-light p {
    font-size: 0.85rem;
  }
  
  .buttons.are-small .button {
    flex: 1 0 100%;
    margin-bottom: 0.5rem;
    justify-content: center;
  }
}

/* For tablets in landscape */
@media (min-width: 769px) and (max-width: 1024px) and (orientation: landscape) {
  .columns {
    display: flex;
    flex-wrap: wrap;
  }
  
  .column.is-3 {
    width: 50%;
  }
  
  .column.is-6 {
    width: 50%;
  }
  
  .buttons.are-small .button {
    flex: none;
    margin-bottom: 0;
  }
}

/* MODIFICADO: For very large screens */
@media (min-width: 1400px) {
  .container {
    max-width: 1400px;
    margin: -2rem auto;
    padding: 2rem;
  }
  
  .hero.is-primary.is-bold {
    padding: 3rem;
  }
  
  .hero-body .title {
    font-size: 2.25rem;
  }
  
  .hero-body .subtitle {
    font-size: 1.25rem;
  }
  
  .box {
    padding: 2rem;
    margin-bottom: 2rem;
  }
  
  /* MODIFICADO: Más espacio en pantallas grandes */
  .control .input,
  .control .textarea,
  .control .select select {
    padding-left: 3.5rem;
    font-size: 1rem;
  }
  
  .control.has-icons-left .input {
    padding-left: 4rem;
  }
  
  .control.has-icons-left .icon.is-left {
    left: 1.2rem;
    font-size: 1.3rem;
  }
}
</style>