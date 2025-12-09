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

.page-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  animation: header-float 20s infinite linear;
  z-index: 0;
}

.title.is-2 {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 800;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
  font-size: 2rem;
  position: relative;
  z-index: 1;
}

.subtitle.is-5 {
  color: #a5d6a7;
  margin-bottom: 1.5rem;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.header-actions {
  display: flex;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

/* Buttons */
.button {
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid transparent;
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

.button.is-danger.is-light {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.05));
  border-color: rgba(244, 67, 54, 0.3);
  color: #ff5252;
}

.button.is-danger.is-light:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(211, 47, 47, 0.1));
  border-color: #f44336;
  color: #ffebee;
}

.button.is-success.is-light {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(46, 125, 50, 0.05));
  border-color: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.button.is-success.is-light:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(46, 125, 50, 0.1));
  border-color: #4caf50;
  color: #e0f2f1;
}

.button.is-danger.is-outlined {
  background: transparent;
  border-color: #f44336;
  color: #f44336;
}

.button.is-danger.is-outlined:hover:not(:disabled) {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: #ffebee;
  transform: translateY(-3px);
}

.button.is-ghost {
  background: transparent;
  border: none;
  color: #a5d6a7;
  padding: 0.25rem;
}

.button.is-ghost:hover {
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  border: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.stat-box.primary {
  border-image: linear-gradient(135deg, #ffd700, #ff9800) 1;
}

.stat-box.success {
  border-image: linear-gradient(135deg, #4caf50, #388e3c) 1;
}

.stat-box.warning {
  border-image: linear-gradient(135deg, #ff9800, #f57c00) 1;
}

.stat-box.info {
  border-image: linear-gradient(135deg, #2196f3, #1976d2) 1;
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
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #0d1b0d;
}

.stat-box.success .stat-icon {
  background: linear-gradient(135deg, #4caf50, #388e3c);
  color: #e0f2f1;
}

.stat-box.warning .stat-icon {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: #fff3e0;
}

.stat-box.info .stat-icon {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: #e3f2fd;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-box.primary .stat-value {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-box.success .stat-value {
  background: linear-gradient(135deg, #4caf50, #388e3c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-box.warning .stat-value {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-box.info .stat-value {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  color: #a5d6a7;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Boxes */
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

.box-title {
  color: #ffd700;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* MODIFICADO: Form elements con más padding */
.field .label {
  color: #e0f2f1;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  letter-spacing: 0.3px;
}

.control .select select {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  backdrop-filter: blur(10px);
  border: 2px solid rgba(46, 125, 50, 0.5);
  border-radius: 10px;
  color: #c8e6c9;
  font-weight: 500;
  padding: 0.625rem 0.875rem 0.625rem 3rem; /* MODIFICADO: Más padding izquierdo */
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 100%;
  font-size: 0.95rem;
  height: 2.75rem;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffd700'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.875rem center;
  background-size: 16px 16px;
  padding-right: 2.5rem;
}

.control .select select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2), 0 4px 15px rgba(255, 215, 0, 0.3);
  outline: none;
  transform: translateY(-2px);
}

.control .select select option {
  background: #0f1f0f;
  color: #c8e6c9;
  padding: 0.5rem;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #c8e6c9;
  font-weight: 500;
  cursor: pointer;
}

.checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #ffd700;
  cursor: pointer;
}

.help {
  color: #a5d6a7;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  font-weight: 500;
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

.table.is-narrow td {
  padding: 0.5rem 0.75rem;
}

/* Tags */
.tag {
  border-radius: 8px;
  font-weight: 600;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.tag.is-danger {
  background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
  border-color: #d32f2f;
  color: #ffebee;
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
  background: linear-gradient(135deg, #ff9800, #ffa726);
}

.progress.is-danger::-webkit-progress-value {
  background: linear-gradient(135deg, #f44336, #ef5350);
}

/* Modal */
.modal-card {
  background: linear-gradient(135deg, #0f1f0f 0%, #0a1a0a 100%);
  border-radius: 16px;
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  overflow: hidden;
}

.modal-large {
  max-width: 900px;
}

.modal-card-head {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%);
  border-bottom: 2px solid rgba(255, 215, 0, 0.4);
  padding: 1.5rem;
}

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  font-size: 1.25rem;
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

/* Notifications */
.notification {
  border-radius: 10px;
  border: 2px solid transparent;
}

.notification.is-success.is-light {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(46, 125, 50, 0.1));
  border-color: rgba(76, 175, 80, 0.3);
  color: #c8e6c9;
}

.notification.is-info.is-light {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(25, 118, 210, 0.1));
  border-color: rgba(33, 150, 243, 0.3);
  color: #bbdefb;
}

.notification.is-warning-light {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(245, 124, 0, 0.05));
  border-color: rgba(255, 152, 0, 0.3);
  color: #ffcc80;
}

/* QR Modal */
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
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.25rem;
}

.cooperativista-info .subtitle {
  color: #a5d6a7;
}

.qr-display {
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 3px solid #ffd700;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.api-key-display {
  width: 100%;
}

.api-key-display .label {
  color: #e0f2f1;
  margin-bottom: 0.5rem;
}

.api-key-box {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: rgba(15, 31, 15, 0.8);
  border: 2px solid rgba(46, 125, 50, 0.5);
  border-radius: 10px;
  padding: 1rem;
}

.api-key-box code {
  flex: 1;
  color: #ffd700;
  font-weight: 600;
  font-size: 0.9rem;
  word-break: break-all;
}

/* Loading states */
.has-text-centered.py-6 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.icon.is-large .mdi-spin {
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
}

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
  
  .modal-export .modal-card {
    box-shadow: none;
    border: 2px solid #333;
    page-break-inside: avoid;
  }
  
  body {
    background: white;
  }
  
  .devices-page {
    background: white;
    padding: 0;
    margin: 0;
  }
}

/* Animations */
@keyframes header-float {
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

/* MODIFICADO: Responsive Design */
@media screen and (max-width: 1024px) {
  .devices-page {
    padding: 1.5rem;
    margin: -1.5rem -1rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .title.is-2 {
    font-size: 1.75rem;
  }
  
  .subtitle.is-5 {
    font-size: 1rem;
  }
  
  .control .select select {
    padding-left: 2.8rem; /* Ajuste responsive */
    font-size: 0.9rem;
  }
  
  .stat-value {
    font-size: 2rem;
  }
}

@media screen and (max-width: 768px) {
  .devices-page {
    padding: 1rem;
    margin: -1rem -0.75rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    padding: 1.25rem;
    text-align: center;
  }
  
  .header-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .button.is-medium {
    width: 100%;
  }
  
  .columns {
    flex-direction: column;
  }
  
  .column.is-narrow {
    width: 100%;
  }
  
  .box {
    padding: 1rem;
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
  
  .control .select select {
    padding-left: 2.5rem; /* Menos padding en móviles */
    padding-right: 2rem;
  }
  
  .buttons.is-centered {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .buttons.is-centered .button {
    flex: 1;
    min-width: 45px;
  }
}

@media screen and (max-width: 480px) {
  .devices-page {
    padding: 0.75rem;
    margin: -0.75rem -0.5rem;
  }
  
  .page-header {
    padding: 1rem;
  }
  
  .title.is-2 {
    font-size: 1.5rem;
  }
  
  .subtitle.is-5 {
    font-size: 0.9rem;
  }
  
  .stat-box {
    padding: 1rem;
    gap: 1rem;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.75rem;
  }
  
  .stat-value {
    font-size: 1.75rem;
  }
  
  .stat-label {
    font-size: 0.85rem;
  }
  
  .box-title {
    font-size: 1.1rem;
  }
  
  .control .select select {
    padding-left: 2.2rem; /* Menos padding en móviles pequeños */
    padding-right: 1.75rem;
    font-size: 0.9rem;
    height: 2.5rem;
  }
  
  .field .label {
    font-size: 0.85rem;
  }
  
  .buttons.is-centered .button {
    flex: 1 0 100%;
    margin-bottom: 0.5rem;
  }
  
  .api-key-box {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .api-key-box code {
    text-align: center;
  }
}

/* For tablets in landscape */
@media (min-width: 769px) and (max-width: 1024px) and (orientation: landscape) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .columns {
    display: flex;
    flex-wrap: wrap;
  }
  
  .column {
    width: 50% !important;
  }
}

/* For very large screens */
@media (min-width: 1400px) {
  .devices-page {
    max-width: 1400px;
    margin: -2rem auto;
    padding: 2rem;
  }
  
  .page-header {
    padding: 3rem;
  }
  
  .title.is-2 {
    font-size: 2.5rem;
  }
  
  .subtitle.is-5 {
    font-size: 1.25rem;
  }
  
  .stats-grid {
    gap: 2rem;
  }
  
  .stat-box {
    padding: 2rem;
  }
  
  .stat-value {
    font-size: 2.5rem;
  }
  
  .control .select select {
    padding-left: 3.5rem; /* Más padding en pantallas grandes */
    font-size: 1rem;
    height: 3rem;
  }
}
</style>