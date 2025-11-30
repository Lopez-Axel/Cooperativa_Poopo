<template>
  <div class="devices-page">
    
    <!-- Header -->
    <div class="level mb-5">
      <div class="level-left">
        <div class="level-item">
          <div>
            <h1 class="title is-3">Gestión de Dispositivos</h1>
            <p class="subtitle is-6">Administración de dispositivos móviles por cuadrilla</p>
          </div>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button class="button is-primary" @click="mostrarModalGenerar = true">
            <span class="icon">
              <i class="mdi mdi-plus"></i>
            </span>
            <span>Generar API Keys</span>
          </button>
        </div>
        <div class="level-item">
          <button class="button is-info" @click="cargarEstadisticas">
            <span class="icon">
              <i class="mdi mdi-refresh"></i>
            </span>
            <span>Actualizar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="columns mb-5">
      <div class="column">
        <div class="box has-background-primary-light">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <p class="heading">Total Generados</p>
                  <p class="title">{{ devicesStore.totalDevices }}</p>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <span class="icon is-large has-text-primary">
                  <i class="mdi mdi-cellphone-link mdi-48px"></i>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="column">
        <div class="box has-background-success-light">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <p class="heading">Activados</p>
                  <p class="title">{{ devicesStore.totalActivados }}</p>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <span class="icon is-large has-text-success">
                  <i class="mdi mdi-check-circle mdi-48px"></i>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="column">
        <div class="box has-background-warning-light">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <p class="heading">Pendientes</p>
                  <p class="title">{{ devicesStore.totalPendientes }}</p>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <span class="icon is-large has-text-warning">
                  <i class="mdi mdi-clock-outline mdi-48px"></i>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="column">
        <div class="box has-background-info-light">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <p class="heading">% Activación</p>
                  <p class="title">{{ devicesStore.porcentajeActivacion }}%</p>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <span class="icon is-large has-text-info">
                  <i class="mdi mdi-chart-line mdi-48px"></i>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="box mb-4">
      <div class="columns">
        <div class="column">
          <div class="field">
            <label class="label">Cuadrilla</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="filtros.cuadrilla" @change="aplicarFiltros">
                  <option :value="null">Todas las cuadrillas</option>
                  <option v-for="cuadrilla in cooperativistasStore.cuadrillas" :key="cuadrilla" :value="cuadrilla">
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
    <div v-if="activationStats" class="box mb-5">
      <h2 class="title is-5 mb-4">Estadísticas por Cuadrilla</h2>
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
                <button class="button is-small is-info" @click="exportarCuadrilla(stat.cuadrilla)">
                  <span class="icon is-small">
                    <i class="mdi mdi-download"></i>
                  </span>
                  <span>Exportar</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Lista de Dispositivos -->
    <div class="box">
      <h2 class="title is-5 mb-4">Dispositivos Registrados</h2>
      
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
              <th>API Key</th>
              <th>Estado</th>
              <th>Dispositivo</th>
              <th>Fecha Activación</th>
              <th class="has-text-centered">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="device in devicesStore.devicesFiltrados" :key="device.id">
              <td>
                <strong>{{ obtenerNombreCooperativista(device.cooperativista_id) }}</strong>
              </td>
              <td>{{ obtenerCuadrillaCooperativista(device.cooperativista_id) }}</td>
              <td>
                <code class="is-size-7">{{ device.api_key }}</code>
                <button class="button is-small is-ghost" @click="copiarApiKey(device.api_key)">
                  <span class="icon is-small">
                    <i class="mdi mdi-content-copy"></i>
                  </span>
                </button>
              </td>
              <td>
                <span v-if="device.is_blocked" class="tag is-danger">
                  <span class="icon is-small">
                    <i class="mdi mdi-lock"></i>
                  </span>
                  <span>Bloqueado</span>
                </span>
                <span v-else-if="device.is_activated" class="tag is-success">
                  <span class="icon is-small">
                    <i class="mdi mdi-check-circle"></i>
                  </span>
                  <span>Activado</span>
                </span>
                <span v-else class="tag is-warning">
                  <span class="icon is-small">
                    <i class="mdi mdi-clock-outline"></i>
                  </span>
                  <span>Pendiente</span>
                </span>
              </td>
              <td>
                <span v-if="device.device_id" class="is-size-7">
                  {{ device.device_name || 'Sin nombre' }}<br>
                  <span class="has-text-grey">{{ device.device_model || '' }}</span>
                </span>
                <span v-else class="has-text-grey-light">No activado</span>
              </td>
              <td>
                <span v-if="device.activated_at" class="is-size-7">
                  {{ formatearFecha(device.activated_at) }}
                </span>
                <span v-else class="has-text-grey-light">-</span>
              </td>
              <td class="has-text-centered">
                <div class="buttons is-centered">
                  <button 
                    v-if="!device.is_blocked" 
                    class="button is-small is-danger is-light"
                    @click="bloquearDispositivo(device)"
                  >
                    <span class="icon is-small">
                      <i class="mdi mdi-lock"></i>
                    </span>
                  </button>
                  <button 
                    v-else 
                    class="button is-small is-success is-light"
                    @click="desbloquearDispositivo(device.id)"
                  >
                    <span class="icon is-small">
                      <i class="mdi mdi-lock-open"></i>
                    </span>
                  </button>
                  <button 
                    class="button is-small is-danger"
                    @click="confirmarEliminar(device)"
                  >
                    <span class="icon is-small">
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

    <!-- Modal Generar API Keys -->
    <div class="modal" :class="{ 'is-active': mostrarModalGenerar }">
      <div class="modal-background" @click="cerrarModalGenerar"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Generar API Keys por Lote</p>
          <button class="delete" @click="cerrarModalGenerar"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Seleccionar por Cuadrilla</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formGenerar.cuadrilla">
                  <option :value="null">-- Seleccionar Cuadrilla --</option>
                  <option v-for="cuadrilla in cooperativistasStore.cuadrillas" :key="cuadrilla" :value="cuadrilla">
                    {{ cuadrilla }}
                  </option>
                </select>
              </div>
            </div>
            <p class="help">Generará API Keys para todos los cooperativistas de esta cuadrilla</p>
          </div>

          <div class="field">
            <label class="label">Seleccionar por Sección</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formGenerar.seccion">
                  <option :value="null">-- Seleccionar Sección --</option>
                  <option v-for="seccion in cooperativistasStore.secciones" :key="seccion" :value="seccion">
                    Sección {{ seccion }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="checkbox">
                <input type="checkbox" v-model="formGenerar.regenerate">
                Regenerar API Keys existentes
              </label>
            </div>
            <p class="help has-text-danger">
              Si está marcado, revocará los dispositivos existentes y generará nuevos
            </p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary" 
            @click="generarLote"
            :disabled="!formGenerar.cuadrilla && !formGenerar.seccion"
            :class="{ 'is-loading': devicesStore.loading }"
          >
            Generar API Keys
          </button>
          <button class="button" @click="cerrarModalGenerar">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal Resultado Generación -->
    <div class="modal" :class="{ 'is-active': mostrarResultado }">
      <div class="modal-background" @click="cerrarResultado"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Resultado de Generación</p>
          <button class="delete" @click="cerrarResultado"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="resultadoGeneracion">
            <div class="notification is-success is-light">
              <strong>✓ {{ resultadoGeneracion.total_created }}</strong> API Keys generadas exitosamente
            </div>
            
            <div v-if="resultadoGeneracion.total_skipped > 0" class="notification is-warning is-light">
              <strong>⚠ {{ resultadoGeneracion.total_skipped }}</strong> cooperativistas omitidos (ya tenían dispositivo)
            </div>

            <div v-if="resultadoGeneracion.devices && resultadoGeneracion.devices.length > 0">
              <h3 class="title is-6 mt-4 mb-3">API Keys Generadas:</h3>
              <div class="table-container">
                <table class="table is-fullwidth is-striped is-narrow">
                  <thead>
                    <tr>
                      <th>Código</th>
                      <th>Nombre</th>
                      <th>API Key</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="device in resultadoGeneracion.devices" :key="device.cooperativista_id">
                      <td>{{ device.codigo_unico }}</td>
                      <td>{{ device.nombre_completo }}</td>
                      <td>
                        <code class="is-size-7">{{ device.api_key }}</code>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-primary" @click="cerrarResultado">Cerrar</button>
        </footer>
      </div>
    </div>

    <!-- Modal Exportar Cuadrilla -->
    <div class="modal" :class="{ 'is-active': mostrarModalExport }">
      <div class="modal-background" @click="cerrarModalExport"></div>
      <div class="modal-card" style="width: 90%;">
        <header class="modal-card-head">
          <p class="modal-card-title">Exportar Cuadrilla - {{ cuadrillaExport }}</p>
          <button class="delete" @click="cerrarModalExport"></button>
        </header>
        <section class="modal-card-body">
          <div v-if="exportData">
            <div class="notification is-info is-light mb-4">
              <strong>{{ exportData.total }}</strong> dispositivos pendientes de activación en esta cuadrilla
            </div>
            
            <div class="table-container">
              <table class="table is-fullwidth is-striped is-hoverable is-narrow">
                <thead>
                  <tr>
                    <th>Nombre Completo</th>
                    <th>CI</th>
                    <th>API Key</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="device in exportData.devices" :key="device.codigo_unico">
                    <td>{{ device.nombre_completo }}</td>
                    <td>{{ device.ci }}</td>
                    <td><code class="is-size-7">{{ device.api_key }}</code></td>
                    <td>
                      <span class="tag is-warning">{{ device.estado }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="notification is-warning-light mt-4">
              <p class="has-text-weight-bold mb-2">Instrucciones para distribución:</p>
              <ol class="ml-4">
                <li>Imprima o copie esta lista para distribuir</li>
                <li>Cada cooperativista debe instalar la app móvil</li>
                <li>Ingresar su API Key en la app</li>
                <li>El sistema vinculará automáticamente su dispositivo</li>
              </ol>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-info" @click="imprimirExport">
            <span class="icon">
              <i class="mdi mdi-printer"></i>
            </span>
            <span>Imprimir</span>
          </button>
          <button class="button" @click="cerrarModalExport">Cerrar</button>
        </footer>
      </div>
    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard'
})

const devicesStore = useDevicesStore()
const cooperativistasStore = useCooperativistasStore()

const mostrarModalGenerar = ref(false)
const mostrarResultado = ref(false)
const mostrarModalExport = ref(false)
const resultadoGeneracion = ref(null)
const activationStats = ref(null)
const exportData = ref(null)
const cuadrillaExport = ref('')

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

const bloquearDispositivo = async (device) => {
  const motivo = prompt('Ingrese el motivo del bloqueo:')
  if (!motivo) return
  
  try {
    await devicesStore.blockDevice(device.id, motivo)
    alert('Dispositivo bloqueado exitosamente')
  } catch (error) {
    alert('Error al bloquear dispositivo: ' + error.message)
  }
}

const desbloquearDispositivo = async (deviceId) => {
  if (!confirm('¿Está seguro de desbloquear este dispositivo?')) return
  
  try {
    await devicesStore.unblockDevice(deviceId)
    alert('Dispositivo desbloqueado exitosamente')
  } catch (error) {
    alert('Error al desbloquear dispositivo: ' + error.message)
  }
}

const confirmarEliminar = async (device) => {
  if (!confirm(`¿Eliminar dispositivo de ${obtenerNombreCooperativista(device.cooperativista_id)}?`)) return
  
  try {
    await devicesStore.deleteDevice(device.id)
    alert('Dispositivo eliminado exitosamente')
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
  title: 'Gestión de Dispositivos - Admin'
})
</script>

<style scoped>
/* ====================================
   BASE - FORZAR MODO CLARO
   ==================================== */
:root {
  color-scheme: light;
}

.devices-page {
  padding: 2rem;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%) !important;
  color: #333333 !important;
  min-height: 100vh;
}

/* Forzar colores claros en todos los elementos */
.devices-page * {
  background-color: inherit !important;
  color: inherit !important;
}

/* ====================================
   HEADER Y TÍTULOS
   ==================================== */
.title {
  color: #2e7d32 !important;
  font-weight: 800 !important;
}

.subtitle {
  color: #666666 !important;
}

/* ====================================
   BOXES Y TARJETAS
   ==================================== */
.box {
  background: #ffffff !important;
  border: 2px solid #e0e0e0 !important;
  border-radius: 12px !important;
  box-shadow: 0 3px 10px rgba(46, 125, 50, 0.1) !important;
  color: #333333 !important;
}

/* Cards de estadísticas con fondos claros */
.box.has-background-primary-light {
  background: linear-gradient(135deg, #e8f5e9, #ffffff) !important;
  border-color: #4caf50 !important;
}

.box.has-background-success-light {
  background: linear-gradient(135deg, #e8f5e9, #ffffff) !important;
  border-color: #4caf50 !important;
}

.box.has-background-warning-light {
  background: linear-gradient(135deg, #fff3e0, #ffffff) !important;
  border-color: #ff9800 !important;
}

.box.has-background-info-light {
  background: linear-gradient(135deg, #e3f2fd, #ffffff) !important;
  border-color: #2196f3 !important;
}

/* ====================================
   BOTONES
   ==================================== */
.button.is-primary {
  background: linear-gradient(135deg, #ffd700, #ff9800) !important;
  color: #1a4d1a !important;
  border: none !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
}

.button.is-info {
  background: #4caf50 !important;
  color: white !important;
  border: none !important;
}

.button.is-success {
  background: #4caf50 !important;
  color: white !important;
  border: none !important;
}

.button.is-warning {
  background: #ff9800 !important;
  color: white !important;
  border: none !important;
}

.button.is-danger {
  background: #f44336 !important;
  color: white !important;
  border: none !important;
}

.button.is-light {
  background: #f5f5f5 !important;
  color: #333333 !important;
  border: 2px solid #e0e0e0 !important;
}

.button.is-ghost {
  background: transparent !important;
  border: none !important;
  color: #666666 !important;
}

/* ====================================
   FORMULARIOS Y FILTROS
   ==================================== */
.input, .textarea, .select select {
  background: #ffffff !important;
  color: #333333 !important;
  border: 2px solid #e0e0e0 !important;
  border-radius: 8px !important;
}

.input:focus, .textarea:focus, .select select:focus {
  border-color: #4caf50 !important;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25) !important;
  background: #ffffff !important;
  color: #333333 !important;
}

.label {
  color: #2e7d32 !important;
  font-weight: 600 !important;
}

.help {
  color: #666666 !important;
}

.checkbox input[type="checkbox"] {
  accent-color: #4caf50 !important;
}

/* ====================================
   TABLAS
   ==================================== */
.table {
  background: #ffffff !important;
  color: #333333 !important;
  border-radius: 8px;
  overflow: hidden;
}

.table thead th {
  background: #f5f5f5 !important;
  color: #2e7d32 !important;
  font-weight: 800 !important;
  border-color: #e0e0e0 !important;
}

.table tbody tr {
  background: #ffffff !important;
  color: #333333 !important;
}

.table tbody tr:hover {
  background: #f5f5f5 !important;
}

.table tbody td {
  border-color: #e0e0e0 !important;
  color: #333333 !important;
}

.table.is-striped tbody tr:nth-child(even) {
  background: #fafafa !important;
}

.table.is-striped tbody tr:nth-child(even):hover {
  background: #f0f0f0 !important;
}

/* ====================================
   TAGS
   ==================================== */
.tag {
  font-weight: 600 !important;
}

.tag.is-success {
  background: #4caf50 !important;
  color: white !important;
}

.tag.is-warning {
  background: #ff9800 !important;
  color: white !important;
}

.tag.is-danger {
  background: #f44336 !important;
  color: white !important;
}

.tag.is-info {
  background: #2196f3 !important;
  color: white !important;
}

/* ====================================
   PROGRESS BARS
   ==================================== */
.progress {
  background: #f5f5f5 !important;
  border: 1px solid #e0e0e0 !important;
}

.progress::-webkit-progress-bar {
  background: #f5f5f5 !important;
}

.progress::-webkit-progress-value {
  background: #4caf50 !important;
}

.progress.is-success::-webkit-progress-value {
  background: #4caf50 !important;
}

.progress.is-warning::-webkit-progress-value {
  background: #ff9800 !important;
}

.progress.is-danger::-webkit-progress-value {
  background: #f44336 !important;
}

/* ====================================
   MODALES
   ==================================== */
.modal-card {
  background: #ffffff !important;
  color: #333333 !important;
  border-radius: 16px;
  border: 2px solid #e0e0e0 !important;
}

.modal-card-head {
  background: #f5f5f5 !important;
  border-bottom: 2px solid #e0e0e0 !important;
  color: #333333 !important;
}

.modal-card-title {
  color: #2e7d32 !important;
  font-weight: 800 !important;
}

.modal-card-body {
  background: #ffffff !important;
  color: #333333 !important;
}

.modal-card-foot {
  background: #f5f5f5 !important;
  border-top: 1px solid #e0e0e0 !important;
  color: #333333 !important;
}

.modal-background {
  background: rgba(0, 0, 0, 0.7) !important;
}

/* ====================================
   NOTIFICACIONES
   ==================================== */
.notification {
  border: 1px solid !important;
}

.notification.is-success {
  background: #e8f5e9 !important;
  color: #2e7d32 !important;
  border-color: #4caf50 !important;
}

.notification.is-warning {
  background: #fff3e0 !important;
  color: #e65100 !important;
  border-color: #ff9800 !important;
}

.notification.is-info {
  background: #e3f2fd !important;
  color: #1565c0 !important;
  border-color: #2196f3 !important;
}

.notification.is-danger {
  background: #ffebee !important;
  color: #c62828 !important;
  border-color: #f44336 !important;
}

/* ====================================
   CÓDIGO Y TEXTO ESPECIAL
   ==================================== */
code {
  background: #f5f5f5 !important;
  color: #d32f2f !important;
  padding: 0.25rem 0.5rem !important;
  border-radius: 4px !important;
  border: 1px solid #e0e0e0 !important;
  font-family: 'Courier New', monospace !important;
}

.has-text-grey {
  color: #666666 !important;
}

.has-text-grey-light {
  color: #999999 !important;
}

.has-text-danger {
  color: #f44336 !important;
}

.has-text-success {
  color: #4caf50 !important;
}

.has-text-warning {
  color: #ff9800 !important;
}

.has-text-info {
  color: #2196f3 !important;
}

/* ====================================
   ICONOS
   ==================================== */
.icon.has-text-primary {
  color: #2e7d32 !important;
}

.icon.has-text-success {
  color: #4caf50 !important;
}

.icon.has-text-warning {
  color: #ff9800 !important;
}

.icon.has-text-info {
  color: #2196f3 !important;
}

.icon.has-text-danger {
  color: #f44336 !important;
}

.icon.has-text-grey-light {
  color: #999999 !important;
}

/* ====================================
   ANIMACIONES Y TRANSICIONES
   ==================================== */
.button, .box, .table {
  transition: all 0.3s ease;
}

.button:hover {
  transform: translateY(-2px);
}

.box:hover {
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.15) !important;
  border-color: #4caf50 !important;
}

/* ====================================
   RESPONSIVE
   ==================================== */
@media screen and (max-width: 768px) {
  .devices-page {
    padding: 1rem;
  }
  
  .box {
    margin-bottom: 1rem;
  }
  
  .buttons .button {
    margin-bottom: 0.25rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
}

/* ====================================
   ESTILOS DE IMPRESIÓN
   ==================================== */
@media print {
  .modal-card-head,
  .modal-card-foot {
    display: none !important;
  }
  
  .modal-card {
    box-shadow: none !important;
    border: 2px solid #333 !important;
  }
  
  .button {
    display: none !important;
  }
}

/* ====================================
   ESTADOS DE CARGA
   ==================================== */
.mdi-loading.mdi-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>