<template>
  <div class="container">
    <div class="box">
      <h1 class="title">Gestión de Períodos de Asistencia</h1>
      <p class="subtitle">Crear y administrar períodos mensuales de asistencia</p>
    </div>

    <div v-if="periodStore.error" class="notification is-danger">
      <button class="delete" @click="periodStore.error = null"></button>
      {{ periodStore.error }}
    </div>

    <div class="box">
      <button class="button is-primary" @click="showCreateModal = true">
        <span class="icon">
          <i class="mdi mdi-plus"></i>
        </span>
        <span>Crear Nuevo Período</span>
      </button>
    </div>

    <div class="box">
      <div class="columns">
        <div class="column is-3">
          <div class="field">
            <label class="label">Mes</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filters.mes">
                  <option :value="undefined">Todos los meses</option>
                  <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">Año</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filters.anio">
                  <option :value="undefined">Todos los años</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">Estado</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filters.is_open">
                  <option :value="undefined">Todos</option>
                  <option :value="true">Abiertos</option>
                  <option :value="false">Cerrados</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-3">
          <div class="field">
            <label class="label">&nbsp;</label>
            <div class="control">
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
    </div>

    <div class="box">
      <div v-if="periodStore.loading" class="has-text-centered">
        <p>Cargando períodos...</p>
      </div>

      <div v-else-if="periodStore.periods.length === 0" class="has-text-centered">
        <p>No hay períodos registrados</p>
      </div>

      <table v-else class="table is-fullwidth is-striped">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Fecha</th>
            <th>Horario</th>
            <th>Duración</th>
            <th>Estado</th>
            <th>Estadísticas</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(period, index) in periodStore.periods" :key="period.id">
            <td>
              <strong>{{ period.nombre }}</strong>
              <br>
              <small>{{ period.descripcion }}</small>
            </td>
            <td>{{ formatDate(period.fecha_asistencia) }}</td>
            <td>{{ period.hora_inicio.substring(0, 5) }} - {{ period.hora_fin.substring(0, 5) }}</td>
            <td class="has-text-centered">
              <div v-if="!period.is_open" class="dropdown is-hoverable">
                <div class="dropdown-trigger">
                  <button class="button is-small is-light">
                    <span>{{ calculateDuration(period.hora_inicio, period.hora_fin) }}</span>
                    <span class="icon is-small">
                      <i class="mdi mdi-chevron-down"></i>
                    </span>
                  </button>
                </div>
                <div class="dropdown-menu">
                  <div class="dropdown-content">
                    <a 
                      v-for="shortcut in periodStore.durationShortcuts" 
                      :key="shortcut.label"
                      class="dropdown-item"
                      @click="extendDuration(period.id, shortcut.minutes)"
                    >
                      {{ shortcut.label }}
                    </a>
                  </div>
                </div>
              </div>
              <span v-else class="tag is-light">
                {{ calculateDuration(period.hora_inicio, period.hora_fin) }}
              </span>
            </td>
            <td>
              <span v-if="period.is_open && periodStore.isOpenOutOfTime(period)" class="tag is-warning">
                <span class="icon">
                  <i class="mdi mdi-alert"></i>
                </span>
                <span>Abierto fuera de tiempo</span>
              </span>
              <span v-else-if="period.is_open" class="tag is-success">
                <span class="icon">
                  <i class="mdi mdi-circle"></i>
                </span>
                <span>Abierto</span>
              </span>
              <span v-else-if="periodStore.getPeriodStatus(period) === 'programado'" class="tag is-info">
                <span class="icon">
                  <i class="mdi mdi-clock-outline"></i>
                </span>
                <span>Programado</span>
              </span>
              <span v-else-if="periodStore.getPeriodStatus(period) === 'en_curso'" class="tag is-primary">
                <span class="icon">
                  <i class="mdi mdi-clock"></i>
                </span>
                <span>En Curso</span>
              </span>
              <span v-else-if="periodStore.getPeriodStatus(period) === 'finalizado'" class="tag is-dark">
                <span class="icon">
                  <i class="mdi mdi-check"></i>
                </span>
                <span>Finalizado</span>
              </span>
              <span v-else class="tag is-danger">
                <span class="icon">
                  <i class="mdi mdi-cancel"></i>
                </span>
                <span>Inactivo</span>
              </span>
            </td>
            <td>
              <small>
                {{ period.total_marked }} / {{ period.total_expected }}
                <span v-if="period.total_expected > 0">
                  ({{ Math.round((period.total_marked / period.total_expected) * 100) }}%)
                </span>
              </small>
            </td>
            <td>
              <div class="buttons are-small">
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
                  class="button is-info"
                  @click="viewStats(period.id)"
                  title="Estadísticas"
                >
                  <span class="icon">
                    <i class="mdi mdi-chart-bar"></i>
                  </span>
                </button>
                
                <button 
                  v-if="!period.is_open && period.is_active" 
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
                  @click="confirmDelete(period.id)"
                  :disabled="periodStore.loading || period.is_open"
                  title="Eliminar"
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

    <div class="modal" :class="{ 'is-active': showCreateModal || showEditModal }">
      <div class="modal-background" @click="closeModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ showEditModal ? 'Editar Período' : 'Crear Nuevo Período' }}</p>
          <button class="delete" @click="closeModal"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nombre</label>
            <div class="control">
              <input class="input" type="text" v-model="formData.nombre" placeholder="Ej: Primera Quincena Enero 2025">
            </div>
          </div>

          <div class="field">
            <label class="label">Descripción</label>
            <div class="control">
              <textarea class="textarea" v-model="formData.descripcion" rows="2"></textarea>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <div class="field">
                <label class="label">Mes</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="formData.mes">
                      <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            <div class="column">
              <div class="field">
                <label class="label">Año</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="formData.anio">
                      <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Fecha de Asistencia</label>
            <div class="control">
              <input 
                class="input" 
                type="date" 
                v-model="formData.fecha_asistencia"
                :min="minDate"
              >
            </div>
            <p v-if="formData.fecha_asistencia && isDateInPast" class="help is-danger">
              La fecha no puede ser anterior al día actual
            </p>
          </div>

          <div class="columns">
            <div class="column">
              <div class="field">
                <label class="label">Hora Inicio</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="time" 
                    v-model="formData.hora_inicio"
                    :min="isToday ? minTime : '00:00'"
                  >
                </div>
              </div>
            </div>
            <div class="column">
              <div class="field">
                <label class="label">Hora Fin</label>
                <div class="control">
                  <input class="input" type="time" v-model="formData.hora_fin">
                </div>
              </div>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="checkbox">
                <input type="checkbox" v-model="formData.is_active">
                Período Activo
              </label>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="savePeriod" 
            :disabled="!canSavePeriod || periodStore.loading"
          >
            {{ showEditModal ? 'Actualizar' : 'Crear' }}
          </button>
          <button class="button" @click="closeModal">Cancelar</button>
        </footer>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showStatsModal }">
      <div class="modal-background" @click="showStatsModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Estadísticas del Período</p>
          <button class="delete" @click="showStatsModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="!periodStore.periodStats">
            <p>Cargando estadísticas...</p>
          </div>
          <div v-else>
            <table class="table is-fullwidth">
              <tbody>
                <tr>
                  <th>Nombre:</th>
                  <td>{{ periodStore.periodStats.nombre }}</td>
                </tr>
                <tr>
                  <th>Fecha:</th>
                  <td>{{ formatDate(periodStore.periodStats.fecha_asistencia) }}</td>
                </tr>
                <tr>
                  <th>Total Esperado:</th>
                  <td><strong>{{ periodStore.periodStats.total_expected }}</strong></td>
                </tr>
                <tr>
                  <th>Total Marcado:</th>
                  <td><strong>{{ periodStore.periodStats.total_marked }}</strong></td>
                </tr>
                <tr>
                  <th>Pendientes:</th>
                  <td><strong>{{ periodStore.periodStats.pendientes }}</strong></td>
                </tr>
                <tr>
                  <th>Porcentaje:</th>
                  <td><strong>{{ periodStore.periodStats.porcentaje_asistencia }}%</strong></td>
                </tr>
                <tr>
                  <th>Estado:</th>
                  <td>
                    <span v-if="periodStore.periodStats.is_open" class="tag is-success">Abierto</span>
                    <span v-else class="tag is-warning">Cerrado</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="showStatsModal = false">Cerrar</button>
        </footer>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="showDeleteModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Eliminación</p>
          <button class="delete" @click="showDeleteModal = false"></button>
        </header>
        <section class="modal-card-body">
          <p>¿Está seguro que desea eliminar este período?</p>
          <p class="has-text-danger mt-2">
            <strong>Nota:</strong> Solo se pueden eliminar períodos sin asistencias registradas.
          </p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="deletePeriod" :disabled="periodStore.loading">
            Eliminar
          </button>
          <button class="button" @click="showDeleteModal = false">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAttendancePeriodStore } from '~/stores/attendancePeriod'
import dayjs from 'dayjs'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const router = useRouter()
const periodStore = useAttendancePeriodStore()

const showCreateModal = ref(false)
const showEditModal = ref(false)
const showStatsModal = ref(false)
const showDeleteModal = ref(false)
const periodToDelete = ref(null)
const editingPeriodId = ref(null)

const filters = ref({
  mes: null,
  anio: new Date().getFullYear(),
  is_open: undefined
})

const formData = ref({
  nombre: '',
  descripcion: '',
  mes: new Date().getMonth() + 1,
  anio: new Date().getFullYear(),
  fecha_asistencia: '',
  hora_inicio: '07:00',
  hora_fin: '19:00',
  is_active: true
})

const years = computed(() => {
  const currentYear = new Date().getFullYear()
  return [currentYear - 1, currentYear, currentYear + 1]
})

// minDate usando dayjs (fecha local, evita el salto por UTC)
const minDate = computed(() => dayjs().format('YYYY-MM-DD'))

console.log(minDate.value)

// minTime en formato HH:mm usando dayjs
const minTime = computed(() => dayjs().format('HH:mm'))

// bandera si la fecha seleccionada es hoy (comparación en zona local)
const isToday = computed(() => {
  if (!formData.value.fecha_asistencia) return false
  return dayjs(formData.value.fecha_asistencia).isSame(dayjs(), 'day')
})

// si la fecha seleccionada está en el pasado (comparación por día, zona local)
const isDateInPast = computed(() => {
  if (!formData.value.fecha_asistencia) return false
  return dayjs(formData.value.fecha_asistencia).isBefore(dayjs(), 'day')
})

// si la hora de inicio ya pasó (solo relevante si la fecha es hoy)
const isTimeInPast = computed(() => {
  if (!isToday.value || !formData.value.hora_inicio) return false
  // dayjs acepta 'YYYY-MM-DDTHH:mm' como local
  const selectedDateTime = dayjs(`${formData.value.fecha_asistencia}T${formData.value.hora_inicio}`)
  return selectedDateTime.isBefore(dayjs())
})

const canSavePeriod = computed(() => {
  return !!formData.value.nombre &&
         !!formData.value.fecha_asistencia &&
         !!formData.value.hora_inicio &&
         !!formData.value.hora_fin &&
         !isDateInPast.value &&
         !isTimeInPast.value
})

const getMonthName = (month) => {
  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ]
  return months[month - 1]
}

const formatDate = (dateString) => {
  // dateString esperado en 'YYYY-MM-DD'
  const date = dayjs(`${dateString}T00:00:00`)
  return date.locale('es').format('dddd, D [de] MMMM [de] YYYY')
}

const calculateDuration = (startTime, endTime) => {
  if (!startTime || !endTime) return ''
  const start = dayjs(`2000-01-01T${startTime}`)
  let end = dayjs(`2000-01-01T${endTime}`)

  // si end es antes que start (p. ej. pasa la medianoche), asumir que termina al día siguiente
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
    await periodStore.fetchPeriods(filters.value)
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

const viewStats = async (periodId) => {
  try {
    await periodStore.fetchPeriodStats(periodId)
    showStatsModal.value = true
  } catch (error) {
    console.error('Error al obtener estadísticas:', error)
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
    hora_fin: period.hora_fin ? period.hora_fin.substring(0, 5) : '19:00',
    is_active: period.is_active
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
      hora_fin: formData.value.hora_fin + ':00',
      is_active: formData.value.is_active
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

const confirmDelete = (periodId) => {
  periodToDelete.value = periodId
  showDeleteModal.value = true
}

const deletePeriod = async () => {
  try {
    await periodStore.deletePeriod(periodToDelete.value)
    showDeleteModal.value = false
    periodToDelete.value = null
    await loadPeriods()
  } catch (error) {
    console.error('Error al eliminar período:', error)
  }
}

const extendDuration = async (periodId, additionalMinutes) => {
  try {
    await periodStore.extendPeriodDuration(periodId, additionalMinutes)
    await loadPeriods()
  } catch (error) {
    console.error('Error al extender duración:', error)
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
    hora_fin: '19:00',
    is_active: true
  }
}

onMounted(() => {
  loadPeriods()
})

useHead({
  title: 'Gestión de Períodos de Asistencia'
})
</script>
