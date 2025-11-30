<template>
  <div class="container">
    <div class="box" v-if="periodStore.selectedPeriod">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <div>
              <h1 class="title">{{ periodStore.selectedPeriod.nombre }}</h1>
              <p class="subtitle">{{ formatDate(periodStore.selectedPeriod.fecha_asistencia) }}</p>
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

      <div class="columns">
        <div class="column is-6">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control">
              <div class="tags has-addons">
                <span class="tag">Horario</span>
                <span class="tag is-dark">
                  {{ periodStore.selectedPeriod.hora_inicio.substring(0, 5) }} - {{ periodStore.selectedPeriod.hora_fin.substring(0, 5) }}
                </span>
              </div>
            </div>
            <div class="control">
              <div class="tags has-addons">
                <span class="tag">Estado</span>
                <span v-if="periodStore.selectedPeriod.is_open" class="tag is-success">Abierto</span>
                <span v-else class="tag is-dark">Cerrado</span>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-6">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control">
              <div class="tags has-addons">
                <span class="tag">Asistencias</span>
                <span class="tag is-primary">
                  {{ periodStore.selectedPeriod.total_marked }} / {{ periodStore.selectedPeriod.total_expected }}
                </span>
              </div>
            </div>
            <div class="control" v-if="periodStore.selectedPeriod.total_expected > 0">
              <div class="tags has-addons">
                <span class="tag">Porcentaje</span>
                <span class="tag is-info">
                  {{ Math.round((periodStore.selectedPeriod.total_marked / periodStore.selectedPeriod.total_expected) * 100) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="attendanceStore.error || periodStore.error || cooperativistaStore.error" class="notification is-danger">
      <button class="delete" @click="clearErrors"></button>
      {{ attendanceStore.error || periodStore.error || cooperativistaStore.error }}
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
                <i class="mdi mdi-plus"></i>
              </span>
              <span>Agregar Asistencia Manual</span>
            </button>
          </div>
        </div>
      </div>

      <div class="field">
        <label class="label">Buscar por CI</label>
        <div class="control has-icons-left">
          <input 
            class="input" 
            type="text" 
            placeholder="Ingrese CI del cooperativista..." 
            v-model="ciFilter"
          >
          <span class="icon is-small is-left">
            <i class="mdi mdi-magnify"></i>
          </span>
        </div>
      </div>
    </div>

    <div class="box">
      <div v-if="attendanceStore.loading" class="has-text-centered">
        <p>Cargando asistencias...</p>
      </div>

      <div v-else-if="filteredAttendances.length === 0" class="has-text-centered">
        <p>No hay asistencias registradas</p>
      </div>

      <table v-else class="table is-fullwidth is-striped">
        <thead>
          <tr>
            <th>CI</th>
            <th>Cooperativista</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Ubicación GPS</th>
            <th>Distancia</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="attendance in filteredAttendances" :key="attendance.id">
            <td>
              <strong>{{ getCooperativistaById(attendance.cooperativista_id)?.ci || 'N/A' }}</strong>
            </td>
            <td>
              <div>
                <strong>{{ getCooperativistaById(attendance.cooperativista_id)?.nombres || 'Cooperativista no encontrado' }}</strong>
                <br>
                <small>{{ getCooperativistaById(attendance.cooperativista_id)?.apellidos || '' }}</small>
              </div>
            </td>
            <td>{{ formatDate(attendance.fecha) }}</td>
            <td>{{ attendance.hora.substring(0, 5) }}</td>
            <td>
              <small>
                {{ attendance.location_lat.toFixed(6) }}, {{ attendance.location_lon.toFixed(6) }}
              </small>
            </td>
            <td>
              <span v-if="attendance.distance_meters !== null" class="tag is-light">
                {{ attendance.distance_meters }}m
              </span>
              <span v-else class="tag">N/A</span>
            </td>
            <td>
              <span v-if="attendance.is_valid" class="tag is-success">
                <span class="icon">
                  <i class="mdi mdi-check"></i>
                </span>
                <span>Válida</span>
              </span>
              <span v-else class="tag is-warning">
                <span class="icon">
                  <i class="mdi mdi-alert"></i>
                </span>
                <span>Pendiente</span>
              </span>
            </td>
            <td>
              <div class="buttons are-small">
                <button 
                  v-if="attendance.notes"
                  class="button is-info"
                  @click="showNotes(attendance.notes)"
                  title="Ver notas"
                >
                  <span class="icon">
                    <i class="mdi mdi-note-text"></i>
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

    <!-- Modal para agregar asistencia manual -->
    <div class="modal" :class="{ 'is-active': showAddModal }">
      <div class="modal-background" @click="closeAddModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Agregar Asistencia Manual</p>
          <button class="delete" @click="closeAddModal"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">CI del Cooperativista</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                placeholder="Ingrese CI..." 
                v-model="manualForm.ci"
                list="cooperativistas-list"
                @input="onCiInput"
              >
              <datalist id="cooperativistas-list">
                <option v-for="coop in cooperativistaStore.cooperativistas" :key="coop.id" :value="coop.ci">
                  {{ coop.ci }} - {{ coop.nombres }} {{ coop.apellidos }}
                </option>
              </datalist>
            </div>
          </div>

          <div v-if="selectedCooperativista" class="field">
            <label class="label">Cooperativista Seleccionado</label>
            <div class="box has-background-light">
              <p><strong>CI:</strong> {{ selectedCooperativista.ci }}</p>
              <p><strong>Nombre:</strong> {{ selectedCooperativista.nombres }} {{ selectedCooperativista.apellidos }}</p>
            </div>
          </div>

          <div class="field">
            <label class="label">Hora de Registro</label>
            <div class="control">
              <input 
                class="input" 
                type="time" 
                v-model="manualForm.hora"
                required
              >
            </div>
          </div>

          <div class="field">
            <label class="label">Motivo de Asistencia Manual</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="manualForm.motivo" required>
                  <option value="">Seleccione un motivo...</option>
                  <option value="presente_sin_registro">Cooperativista en reunión pero no registró asistencia</option>
                  <option value="retraso_presente">Retraso pero estuvo en la reunión</option>
                  <option value="problema_dispositivo">Problemas con el dispositivo</option>
                  <option value="admin_ingresado">Ingresado por el administrador</option>
                  <option value="justificacion_especial">Justificación especial</option>
                  <option value="otro">Otro motivo</option>
                </select>
              </div>
            </div>
          </div>

          <div v-if="manualForm.motivo === 'otro'" class="field">
            <label class="label">Especificar motivo</label>
            <div class="control">
              <textarea 
                class="textarea" 
                placeholder="Describa el motivo..."
                v-model="manualForm.motivoOtro"
              ></textarea>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="saveManualAttendance"
            :disabled="!canSaveManual || attendanceStore.loading"
          >
            <span v-if="attendanceStore.loading">Guardando...</span>
            <span v-else>Guardar Asistencia</span>
          </button>
          <button class="button" @click="closeAddModal">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal para confirmar eliminación -->
    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="showDeleteModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Eliminación</p>
          <button class="delete" @click="showDeleteModal = false"></button>
        </header>
        <section class="modal-card-body">
          <p>¿Está seguro de que desea eliminar este registro de asistencia?</p>
          <p class="has-text-weight-bold">Esta acción no se puede deshacer.</p>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-danger" 
            @click="deleteAttendance"
            :disabled="attendanceStore.loading"
          >
            <span v-if="attendanceStore.loading">Eliminando...</span>
            <span v-else>Eliminar</span>
          </button>
          <button class="button" @click="showDeleteModal = false">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal para mostrar notas -->
    <div class="modal" :class="{ 'is-active': showNotesModal }">
      <div class="modal-background" @click="showNotesModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Notas del Registro</p>
          <button class="delete" @click="showNotesModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div class="content">
            {{ currentNotes }}
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="showNotesModal = false">Cerrar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import 'dayjs/locale/es'
import { useAttendancePeriodStore } from '~/stores/attendancePeriod'
import { useAttendanceStore } from '~/stores/attendance'
import { useCooperativistasStore } from '~/stores/cooperativistas'

dayjs.locale('es')

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const router = useRouter()
const route = useRoute()
const periodStore = useAttendancePeriodStore()
const attendanceStore = useAttendanceStore()
const cooperativistaStore = useCooperativistasStore()

const periodId = parseInt(route.params.id)

const showAddModal = ref(false)
const showDeleteModal = ref(false)
const showNotesModal = ref(false)
const attendanceToDelete = ref(null)
const currentNotes = ref('')
const ciFilter = ref('')

const manualForm = ref({
  ci: '',
  hora: '',
  motivo: '',
  motivoOtro: ''
})

const selectedCooperativista = ref(null)

const filteredAttendances = computed(() => {
  if (!ciFilter.value) {
    return attendanceStore.attendances
  }
  
  return attendanceStore.attendances.filter(attendance => {
    const cooperativista = getCooperativistaById(attendance.cooperativista_id)
    return cooperativista?.ci?.includes(ciFilter.value) || false
  })
})

const canSaveManual = computed(() => {
  return selectedCooperativista.value && 
         manualForm.value.hora && 
         manualForm.value.motivo &&
         (manualForm.value.motivo !== 'otro' || manualForm.value.motivoOtro)
})

const formatDate = (dateString) => {
  const date = dayjs(`${dateString}T00:00:00`)
  return date.locale('es').format('dddd, D [de] MMMM [de] YYYY')
}

const getCooperativistaById = (id) => {
  return cooperativistaStore.cooperativistas.find(c => c.id === id)
}

const onCiInput = () => {
  const cooperativista = cooperativistaStore.cooperativistas.find(c => c.ci === manualForm.value.ci)
  selectedCooperativista.value = cooperativista || null
}

const loadData = async () => {
  try {
    await Promise.all([
      periodStore.fetchPeriod(periodId),
      attendanceStore.fetchAttendancesByPeriod(periodId),
      cooperativistaStore.cargarCooperativistas()
    ])
  } catch (error) {
    console.error('Error al cargar datos:', error)
  }
}

const clearErrors = () => {
  attendanceStore.error = null
  periodStore.error = null
  cooperativistaStore.error = null
}

const showNotes = (notes) => {
  currentNotes.value = notes
  showNotesModal.value = true
}

const confirmDelete = (attendanceId) => {
  attendanceToDelete.value = attendanceId
  showDeleteModal.value = true
}

const deleteAttendance = async () => {
  try {
    await attendanceStore.deleteAttendance(attendanceToDelete.value)
    showDeleteModal.value = false
    attendanceToDelete.value = null
    await loadData()
  } catch (error) {
    console.error('Error al eliminar asistencia:', error)
  }
}

const saveManualAttendance = async () => {
  if (!selectedCooperativista.value || !periodStore.selectedPeriod) return

  const notes = manualForm.value.motivo === 'otro' 
    ? manualForm.value.motivoOtro 
    : getMotivoDescription(manualForm.value.motivo)

  const attendanceData = {
    cooperativista_id: selectedCooperativista.value.id,
    period_id: periodId,
    device_id: 'ADMIN_MANUAL',
    fecha: periodStore.selectedPeriod.fecha_asistencia,
    hora: manualForm.value.hora + ':00',
    location_lat: -17.9833, // Coordenadas por defecto de Oruro
    location_lon: -67.1167,
    notes: `REGISTRO MANUAL - ${notes}`
  }

  try {
    await attendanceStore.createAttendance(attendanceData)
    closeAddModal()
    await loadData()
  } catch (error) {
    console.error('Error al guardar asistencia manual:', error)
  }
}

const getMotivoDescription = (motivo) => {
  const motivos = {
    'presente_sin_registro': 'Cooperativista en reunión pero no registró asistencia',
    'retraso_presente': 'Retraso pero estuvo en la reunión',
    'problema_dispositivo': 'Problemas con el dispositivo',
    'admin_ingresado': 'Ingresado por el administrador',
    'justificacion_especial': 'Justificación especial'
  }
  return motivos[motivo] || motivo
}

const closeAddModal = () => {
  showAddModal.value = false
  manualForm.value = {
    ci: '',
    hora: '',
    motivo: '',
    motivoOtro: ''
  }
  selectedCooperativista.value = null
}

onMounted(() => {
  loadData()
})

useHead({
  title: 'Detalle de Período de Asistencia'
})
</script>