<template>
  <div class="devices-page">
    
    <!-- Header -->
    <div class="page-header">
      <h1 class="title is-2">Gestión de Dispositivos</h1>
      <p class="subtitle is-5">Administración de dispositivos móviles por cuadrilla</p>
      <div class="header-actions">
        <button class="button is-primary is-medium" @click="mostrarModalGenerar = true">
          <span class="icon">
            <i class="mdi mdi-plus"></i>
          </span>
          <span>Generar Códigos</span>
        </button>
        <button class="button is-light is-medium" @click="cargarEstadisticas">
          <span class="icon">
            <i class="mdi mdi-refresh"></i>
          </span>
          <span>Actualizar</span>
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-box primary">
        <div class="stat-icon">
          <i class="mdi mdi-cellphone-link"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ devicesStore.totalDevices }}</p>
          <p class="stat-label">Total Generados</p>
        </div>
      </div>

      <div class="stat-box success">
        <div class="stat-icon">
          <i class="mdi mdi-check-circle"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ devicesStore.totalActivados }}</p>
          <p class="stat-label">Activados</p>
        </div>
      </div>

      <div class="stat-box warning">
        <div class="stat-icon">
          <i class="mdi mdi-clock-outline"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ devicesStore.totalPendientes }}</p>
          <p class="stat-label">Pendientes</p>
        </div>
      </div>

      <div class="stat-box info">
        <div class="stat-icon">
          <i class="mdi mdi-chart-line"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ devicesStore.porcentajeActivacion }}%</p>
          <p class="stat-label">% Activación</p>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="box filters-box">
      <div class="columns">
        <div class="column">
          <div class="field">
            <label class="label">Cuadrilla</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filtros.cuadrilla" @change="aplicarFiltros">
                  <option :value="null">Todas las cuadrillas</option>
                  <option v-for="cuadrilla in cuadrillasDisponibles" :key="cuadrilla" :value="cuadrilla">
                    {{ cuadrilla }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="field">
            <label class="label">Estado</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filtros.is_activated" @change="aplicarFiltros">
                  <option :value="null">Todos</option>
                  <option :value="true">Activados</option>
                  <option :value="false">Pendientes</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="field">
            <label class="label">Bloqueados</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filtros.is_blocked" @change="aplicarFiltros">
                  <option :value="null">Todos</option>
                  <option :value="false">No bloqueados</option>
                  <option :value="true">Bloqueados</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-narrow">
          <div class="field">
            <label class="label">&nbsp;</label>
            <div class="control">
              <button class="button" @click="limpiarFiltros">
                <span class="icon">
                  <i class="mdi mdi-filter-remove"></i>
                </span>
                <span>Limpiar</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Estadísticas por Cuadrilla -->
    <div v-if="activationStats" class="box content-box">
      <h2 class="box-title">
        <i class="mdi mdi-chart-bar"></i>
        Estadísticas por Cuadrilla
      </h2>
      <div class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>Cuadrilla</th>
              <th class="has-text-centered">Total</th>
              <th class="has-text-centered">Activados</th>
              <th class="has-text-centered">Pendientes</th>
              <th class="has-text-centered">% Activación</th>
              <th class="has-text-centered">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stat in activationStats.by_cuadrilla" :key="stat.cuadrilla">
              <td><strong>{{ stat.cuadrilla }}</strong></td>
              <td class="has-text-centered">{{ stat.total }}</td>
              <td class="has-text-centered">
                <span class="tag is-success">{{ stat.activated }}</span>
              </td>
              <td class="has-text-centered">
                <span class="tag is-warning">{{ stat.pending }}</span>
              </td>
              <td class="has-text-centered">
                <progress 
                  class="progress is-small" 
                  :class="stat.percentage > 75 ? 'is-success' : stat.percentage > 50 ? 'is-warning' : 'is-danger'"
                  :value="stat.percentage" 
                  max="100"
                >
                  {{ stat.percentage }}%
                </progress>
                <span class="is-size-7">{{ stat.percentage }}%</span>
              </td>
              <td class="has-text-centered">
                <button class="button is-small is-primary" @click="exportarCuadrilla(stat.cuadrilla)">
                  <span class="icon is-small">
                    <i class="mdi mdi-download"></i>
                  </span>
                  <span>Ver Códigos</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Lista de Dispositivos -->
    <div class="box content-box">
      <h2 class="box-title">
        <i class="mdi mdi-cellphone-link"></i>
        Dispositivos Registrados
      </h2>
      
      <div v-if="devicesStore.loading" class="has-text-centered py-6">
        <span class="icon is-large">
          <i class="mdi mdi-loading mdi-spin mdi-48px"></i>
        </span>
        <p class="mt-3">Cargando dispositivos...</p>
      </div>

      <div v-else-if="devicesStore.devicesFiltrados.length === 0" class="has-text-centered py-6">
        <span class="icon is-large has-text-grey-light">
          <i class="mdi mdi-cellphone-off mdi-48px"></i>
        </span>
        <p class="mt-3 has-text-grey">No hay dispositivos registrados</p>
      </div>

      <div v-else class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>Cooperativista</th>
              <th>Cuadrilla</th>
              <th>Estado</th>
              <th>Dispositivo</th>
              <th>Registrado</th>
              <th>Última Actividad</th>
              <th class="has-text-centered">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="device in devicesStore.devicesFiltrados" :key="device.id">
              <td><strong>{{ obtenerNombreCooperativista(device.cooperativista_id) }}</strong></td>
              <td>{{ obtenerCuadrillaCooperativista(device.cooperativista_id) }}</td>
              <td>
                <span v-if="device.is_blocked" class="tag is-danger">
                  <i class="mdi mdi-block-helper"></i> Bloqueado
                </span>
                <span v-else-if="device.is_active" class="tag is-success">
                  <i class="mdi mdi-check-circle"></i> Activado
                </span>
                <span v-else class="tag is-warning">
                  <i class="mdi mdi-clock-outline"></i> Pendiente
                </span>
              </td>
              <td>
                <div v-if="device.device_name">
                  <div><i class="mdi mdi-cellphone"></i> {{ device.device_name }}</div>
                  <div v-if="device.device_model" class="is-size-7 has-text-grey">{{ device.device_model }}</div>
                </div>
                <span v-else class="has-text-grey">Sin activar</span>
              </td>
              <td>{{ formatearFecha(device.registered_at) }}</td>
              <td>{{ formatearFecha(device.last_seen) }}</td>
              <td class="has-text-centered">
                <div class="buttons is-centered">
                  <button 
                    v-if="!device.is_blocked" 
                    class="button is-small is-danger is-light"
                    @click="bloquearDispositivo(device)"
                    title="Bloquear"
                  >
                    <i class="mdi mdi-block-helper"></i>
                  </button>
                  <button 
                    v-else
                    class="button is-small is-success is-light"
                    @click="desbloquearDispositivo(device.id)"
                    title="Desbloquear"
                  >
                    <i class="mdi mdi-check-circle"></i>
                  </button>
                  <button 
                    class="button is-small is-danger is-outlined"
                    @click="confirmarEliminar(device)"
                    title="Eliminar"
                  >
                    <i class="mdi mdi-delete"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Generar -->
    <div class="modal" :class="{ 'is-active': mostrarModalGenerar }">
      <div class="modal-background" @click="cerrarModalGenerar"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Generar Códigos de Activación</p>
          <button class="delete" @click="cerrarModalGenerar"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Cuadrilla *</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formGenerar.cuadrilla" required>
                  <option :value="null">Seleccione una cuadrilla</option>
                  <option v-for="cuadrilla in cuadrillasDisponibles" :key="cuadrilla" :value="cuadrilla">
                    {{ cuadrilla }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Sección (opcional)</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formGenerar.seccion">
                  <option :value="null">Todas las secciones</option>
                  <option v-for="seccion in seccionesDisponibles" :key="seccion" :value="seccion">
                    {{ seccion }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="checkbox">
              <input type="checkbox" v-model="formGenerar.regenerate" />
              Regenerar códigos existentes
            </label>
            <p class="help">Si está marcado, se generarán nuevos códigos aunque ya existan</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="cerrarModalGenerar">Cancelar</button>
          <button class="button is-primary" @click="generarLote" :disabled="!formGenerar.cuadrilla">
            Generar
          </button>
        </footer>
      </div>
    </div>

    <!-- Modal Resultado -->
    <div class="modal" :class="{ 'is-active': mostrarResultado }">
      <div class="modal-background" @click="cerrarResultado"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Códigos Generados</p>
          <button class="delete" @click="cerrarResultado"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="resultadoGeneracion" class="notification is-success is-light">
            <p class="has-text-weight-bold mb-2">
              ✓ Se generaron <strong>{{ resultadoGeneracion.created }}</strong> códigos nuevos
            </p>
            <p v-if="resultadoGeneracion.skipped > 0">
              ⚠️ Se omitieron <strong>{{ resultadoGeneracion.skipped }}</strong> cooperativistas que ya tenían código
            </p>
            <p class="mt-3">
              Total procesados: <strong>{{ resultadoGeneracion.total }}</strong>
            </p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-primary" @click="cerrarResultado">Aceptar</button>
        </footer>
      </div>
    </div>

    <!-- Modal Export Cuadrilla -->
    <div class="modal modal-export" :class="{ 'is-active': mostrarModalExport }">
      <div class="modal-background" @click="cerrarModalExport"></div>
      <div class="modal-card modal-large">
        <header class="modal-card-head">
          <p class="modal-card-title">Códigos de Activación: {{ cuadrillaExport }}</p>
          <button class="delete" @click="cerrarModalExport"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="exportData">
            <div class="notification is-info is-light mb-4">
              <strong>{{ exportData.total }}</strong> dispositivos pendientes en esta cuadrilla
            </div>
            
            <div class="table-container">
              <table class="table is-fullwidth is-striped is-hoverable is-narrow">
                <thead>
                  <tr>
                    <th>Nombre Completo</th>
                    <th>CI</th>
                    <th>API Key</th>
                    <th>Estado</th>
                    <th class="has-text-centered">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="device in exportData.devices" :key="device.id">
                    <td><strong>{{ device.nombre_completo }}</strong></td>
                    <td>{{ device.ci }}</td>
                    <td>
                      <code class="is-size-7">{{ device.api_key }}</code>
                      <button 
                        class="button is-small is-ghost ml-2" 
                        @click="copiarApiKey(device.api_key)"
                        title="Copiar"
                      >
                        <i class="mdi mdi-content-copy"></i>
                      </button>
                    </td>
                    <td>
                      <span class="tag is-warning">{{ device.estado }}</span>
                    </td>
                    <td class="has-text-centered">
                      <button 
                        class="button is-small is-primary"
                        @click="mostrarQRGrande(device)"
                      >
                        <i class="mdi mdi-qrcode"></i> Ver QR
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="notification is-warning-light mt-4 no-print">
              <p class="has-text-weight-bold mb-2">📱 Instrucciones:</p>
              <ol class="ml-4">
                <li>Imprima o use "Ver QR" para cada cooperativista</li>
                <li>Escanear el QR en la app móvil</li>
                <li>O ingresar manualmente la API Key</li>
                <li>El sistema vinculará automáticamente el dispositivo</li>
              </ol>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot no-print">
          <button class="button is-primary" @click="imprimirExport">
            <span class="icon"><i class="mdi mdi-printer"></i></span>
            <span>Imprimir</span>
          </button>
          <button class="button" @click="cerrarModalExport">Cerrar</button>
        </footer>
      </div>
    </div>

    <!-- Modal QR Grande -->
    <div class="modal modal-qr" :class="{ 'is-active': mostrarModalQR }">
      <div class="modal-background" @click="cerrarModalQR"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Código QR de Activación</p>
          <button class="delete" @click="cerrarModalQR"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="deviceQRSeleccionado" class="qr-modal-content">
            <div class="cooperativista-info">
              <h3 class="title is-4">{{ deviceQRSeleccionado.nombre_completo }}</h3>
              <p class="subtitle is-6">CI: {{ deviceQRSeleccionado.ci }}</p>
            </div>
            
            <div class="qr-display">
              <QRCodeVue3
                :value="deviceQRSeleccionado.api_key"
                :width="300"
                :height="300"
                :margin="2"
                :corner-square-options="{ type: 'square', color: '#038730' }"
                :corner-dot-options="{ type: 'square', color: '#feea01' }"
                :dots-options="{ type: 'square', color: '#1a2e1a' }"
                :background-options="{ color: '#ffffff' }"
              />
            </div>

            <div class="api-key-display">
              <label class="label">API Key:</label>
              <div class="api-key-box">
                <code>{{ deviceQRSeleccionado.api_key }}</code>
                <button 
                  class="button is-primary"
                  @click="copiarApiKey(deviceQRSeleccionado.api_key)"
                >
                  <span class="icon"><i class="mdi mdi-content-copy"></i></span>
                  <span>Copiar</span>
                </button>
              </div>
            </div>

            <div class="notification is-info is-light mt-4">
              <p><strong>Instrucciones:</strong></p>
              <ol class="ml-4">
                <li>Abrir la aplicación móvil</li>
                <li>Escanear este código QR</li>
                <li>O copiar la API Key manualmente</li>
              </ol>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="cerrarModalQR">Cerrar</button>
        </footer>
      </div>
    </div>

  </div>
</template>

<script setup>
import QRCodeVue3 from 'qrcode-vue3'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const devicesStore = useDevicesStore()
const cooperativistasStore = useCooperativistasStore()

const mostrarModalGenerar = ref(false)
const mostrarResultado = ref(false)
const mostrarModalExport = ref(false)
const mostrarModalQR = ref(false)
const resultadoGeneracion = ref(null)
const activationStats = ref(null)
const exportData = ref(null)
const cuadrillaExport = ref('')
const deviceQRSeleccionado = ref(null)

const filtros = ref({
  cuadrilla: null,
  is_activated: null,
  is_blocked: null
})

const formGenerar = ref({
  cuadrilla: null,
  seccion: null,
  regenerate: false
})

// Fix: Snapshots para evitar problemas de reactividad
const cuadrillasDisponibles = computed(() => {
  return JSON.parse(JSON.stringify(cooperativistasStore.cuadrillas || []))
})

const seccionesDisponibles = computed(() => {
  return JSON.parse(JSON.stringify(cooperativistasStore.secciones || []))
})

onMounted(async () => {
  await cooperativistasStore.cargarCooperativistas()
  await cargarEstadisticas()
})

const cargarEstadisticas = async () => {
  try {
    await devicesStore.fetchDevices({ limit: 500 })
    activationStats.value = await devicesStore.fetchActivationStats()
  } catch (error) {
    console.error('Error cargando estadísticas:', error)
  }
}

const aplicarFiltros = () => {
  devicesStore.setFilters(filtros.value)
}

const limpiarFiltros = () => {
  filtros.value = {
    cuadrilla: null,
    is_activated: null,
    is_blocked: null
  }
  devicesStore.limpiarFiltros()
}

const generarLote = async () => {
  try {
    const batchData = {
      cuadrilla: formGenerar.value.cuadrilla,
      seccion: formGenerar.value.seccion,
      regenerate: formGenerar.value.regenerate
    }
    
    resultadoGeneracion.value = await devicesStore.generateBatch(batchData)
    mostrarModalGenerar.value = false
    mostrarResultado.value = true
    
    await cargarEstadisticas()
  } catch (error) {
    alert('Error al generar API Keys: ' + error.message)
  }
}

const exportarCuadrilla = async (cuadrilla) => {
  try {
    cuadrillaExport.value = cuadrilla
    exportData.value = await devicesStore.exportCuadrilla(cuadrilla)
    mostrarModalExport.value = true
  } catch (error) {
    alert('Error al exportar cuadrilla: ' + error.message)
  }
}

const mostrarQRGrande = (device) => {
  deviceQRSeleccionado.value = device
  mostrarModalQR.value = true
}

const cerrarModalQR = () => {
  mostrarModalQR.value = false
  deviceQRSeleccionado.value = null
}

const bloquearDispositivo = async (device) => {
  const motivo = prompt('Ingrese el motivo del bloqueo:')
  if (!motivo) return
  
  try {
    await devicesStore.blockDevice(device.id, motivo)
    alert('Dispositivo bloqueado exitosamente')
    await cargarEstadisticas()
  } catch (error) {
    alert('Error al bloquear dispositivo: ' + error.message)
  }
}

const desbloquearDispositivo = async (deviceId) => {
  if (!confirm('¿Está seguro de desbloquear este dispositivo?')) return
  
  try {
    await devicesStore.unblockDevice(deviceId)
    alert('Dispositivo desbloqueado exitosamente')
    await cargarEstadisticas()
  } catch (error) {
    alert('Error al desbloquear dispositivo: ' + error.message)
  }
}

const confirmarEliminar = async (device) => {
  if (!confirm(`¿Eliminar dispositivo de ${obtenerNombreCooperativista(device.cooperativista_id)}?`)) return
  
  try {
    await devicesStore.deleteDevice(device.id)
    alert('Dispositivo eliminado exitosamente')
    await cargarEstadisticas()
  } catch (error) {
    alert('Error al eliminar dispositivo: ' + error.message)
  }
}

const copiarApiKey = async (apiKey) => {
  try {
    await navigator.clipboard.writeText(apiKey)
    alert('API Key copiada al portapapeles')
  } catch (error) {
    console.error('Error copiando:', error)
  }
}

const imprimirExport = () => {
  window.print()
}

const cerrarModalGenerar = () => {
  mostrarModalGenerar.value = false
  formGenerar.value = {
    cuadrilla: null,
    seccion: null,
    regenerate: false
  }
}

const cerrarResultado = () => {
  mostrarResultado.value = false
  resultadoGeneracion.value = null
}

const cerrarModalExport = () => {
  mostrarModalExport.value = false
  exportData.value = null
}

const obtenerNombreCooperativista = (id) => {
  const coop = cooperativistasStore.cooperativistas.find(c => c.id === id)
  return coop ? `${coop.nombres} ${coop.apellido_paterno} ${coop.apellido_materno || ''}`.trim() : 'Desconocido'
}

const obtenerCuadrillaCooperativista = (id) => {
  const coop = cooperativistasStore.cooperativistas.find(c => c.id === id)
  return coop?.cuadrilla || '-'
}

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleString('es-BO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

useHead({
  title: 'Gestión de Dispositivos'
})
</script>

<style scoped>
.devices-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(135deg, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

/* Header */
.page-header {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.1), rgba(26, 46, 26, 0.1));
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 2px solid rgba(254, 234, 1, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header .title {
  color: #feea01;
  margin-bottom: 0.5rem;
}

.page-header .subtitle {
  color: #a5d6a7;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border: 2px solid rgba(254, 234, 1, 0.2);
  transition: transform 0.3s ease;
}

.stat-box:hover {
  transform: translateY(-4px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
}

.stat-box.primary .stat-icon {
  background: linear-gradient(135deg, #038730, #026d27);
  color: #feea01;
}

.stat-box.success .stat-icon {
  background: linear-gradient(135deg, #4caf50, #2e7d32);
  color: white;
}

.stat-box.warning .stat-icon {
  background: linear-gradient(135deg, #feea01, #ffd700);
  color: #0a1a0a;
}

.stat-box.info .stat-icon {
  background: linear-gradient(135deg, #BBC863, #9e9d24);
  color: white;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #feea01;
  line-height: 1;
}

.stat-label {
  color: #a5d6a7;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

/* Boxes */
.box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 2px solid rgba(254, 234, 1, 0.2);
}

.box-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #feea01;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(254, 234, 1, 0.3);
}

/* Modal QR */
.qr-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.cooperativista-info {
  text-align: center;
}

.cooperativista-info .title {
  color: #feea01;
  margin-bottom: 0.5rem;
}

.cooperativista-info .subtitle {
  color: #a5d6a7;
}

.qr-display {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.api-key-display {
  width: 100%;
}

.api-key-display .label {
  color: #a5d6a7;
  font-weight: 700;
}

.api-key-box {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: 8px;
  border: 2px solid rgba(254, 234, 1, 0.3);
}

.api-key-box code {
  flex: 1;
  color: #e0f2f1;
  font-size: 0.875rem;
  word-break: break-all;
}

/* Modal Styles */
.modal-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.95));
}

.modal-card-head {
  background: linear-gradient(135deg, #038730, #026d27);
  border-bottom: 2px solid #feea01;
}

.modal-card-title {
  color: #feea01;
  font-weight: 700;
}

.modal-card-body {
  color: #e0f2f1;
}

.modal-card-foot {
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(254, 234, 1, 0.2);
}

.modal-large .modal-card {
  width: 90%;
  max-width: 1200px;
}

@media print {
  .no-print {
    display: none !important;
  }
}

@media screen and (max-width: 1023px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media screen and (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>