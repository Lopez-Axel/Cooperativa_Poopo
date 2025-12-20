<template>
  <div class="cooperativistas-page">
    
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Gestión de Cooperativistas</h1>
        <p class="page-subtitle">Cooperativa Minera Poopó R.L.</p>
      </div>
      <div class="header-actions">
        <NuxtLink to="/cooperativistas/secciones" class="button is-light quick-link">
          <i class="mdi mdi-office-building"></i>
          <span>Ver por Secciones</span>
        </NuxtLink>
        <NuxtLink to="/cooperativistas/cuadrillas" class="button is-light quick-link">
          <i class="mdi mdi-account-group"></i>
          <span>Ver por Cuadrillas</span>
        </NuxtLink>
        <button class="button is-warning" @click="mostrarFormularioCrear = true">
          <i class="mdi mdi-plus-circle"></i>
          <span>Nuevo Cooperativista</span>
        </button>
      </div>
    </div>

    <!-- Filtros Section -->
    <div class="filtros-section">
      <div class="filtros-grid">
        
        <!-- Búsqueda general -->
        <div class="field">
          <label class="label">Buscar</label>
          <div class="control has-icons-left">
            <input 
              class="input" 
              type="text" 
              placeholder="Buscar por nombre, CI, QR..."
              v-model="filtros.search"
            />
            <span class="icon is-left">
              <i class="mdi mdi-magnify"></i>
            </span>
          </div>
        </div>

        <!-- Filtro por Sección -->
        <div class="field">
          <label class="label">Sección</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.id_seccion">
              <option :value="null">Todas las Secciones</option>
              <option v-for="seccion in seccionesStore.secciones" :key="seccion.id" :value="seccion.id">
                {{ seccion.nombre }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filtro por Cuadrilla -->
        <div class="field">
          <label class="label">Cuadrilla</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.id_cuadrilla">
              <option :value="null">Todas las Cuadrillas</option>
              <option v-for="cuadrilla in cuadrillasDisponibles" :key="cuadrilla.id" :value="cuadrilla.id">
                {{ cuadrilla.nombre }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filtro por Estado -->
        <div class="field">
          <label class="label">Estado</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.is_active">
              <option :value="true">Activos</option>
              <option :value="false">Inactivos</option>
              <option :value="null">Todos</option>
            </select>
          </div>
        </div>

        <!-- Filtro por Ocupación -->
        <div class="field">
          <label class="label">Ocupación</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.ocupacion">
              <option :value="null">Todas las Ocupaciones</option>
              <option v-for="ocupacion in ocupacionesDisponibles" :key="ocupacion" :value="ocupacion">
                {{ ocupacion }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filtro por Estado Asegurado -->
        <div class="field">
          <label class="label">Estado Asegurado</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.estado_asegurado">
              <option :value="null">Todos los Estados</option>
              <option v-for="estado in estadosAseguradoDisponibles" :key="estado" :value="estado">
                {{ estado }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filtro Fecha Ingreso Desde -->
        <div class="field">
          <label class="label">Ingreso Desde</label>
          <div class="control">
            <input 
              class="input" 
              type="date" 
              v-model="filtros.fecha_ingreso_desde"
            />
          </div>
        </div>

        <!-- Filtro Fecha Ingreso Hasta -->
        <div class="field">
          <label class="label">Ingreso Hasta</label>
          <div class="control">
            <input 
              class="input" 
              type="date" 
              v-model="filtros.fecha_ingreso_hasta"
            />
          </div>
        </div>

      </div>
      
      <div class="filtros-actions">
        <div class="filtros-especiales">
          <button 
            class="button" 
            :class="{ 'is-warning': filtros.solo_cargos_especiales }"
            @click="filtros.solo_cargos_especiales = !filtros.solo_cargos_especiales"
          >
            <i class="mdi mdi-star-circle"></i>
            <span>{{ filtros.solo_cargos_especiales ? 'Mostrar Todos' : 'Solo Cargos Especiales' }}</span>
          </button>
        </div>
        <button class="button is-light" @click="limpiarFiltros()">
          <i class="mdi mdi-filter-remove"></i>
          <span>Limpiar Filtros</span>
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-bar">
      <div class="stat-item">
        <span class="stat-label">Total:</span>
        <span class="stat-value">{{ cooperativistasFiltrados.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Secciones:</span>
        <span class="stat-value">{{ seccionesStore.secciones.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Cuadrillas:</span>
        <span class="stat-value">{{ cuadrillasStore.cuadrillas.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Jefes:</span>
        <span class="stat-value">{{ contarPorCargo('jefe') }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Sub Jefes:</span>
        <span class="stat-value">{{ contarPorCargo('sub') }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Tesoreros:</span>
        <span class="stat-value">{{ contarPorCargo('tesorero') }}</span>
      </div>
    </div>

    <!-- Lista de Cooperativistas -->
    <div class="cooperativistas-grid" v-if="!store.loading">
      <div 
        v-for="coop in cooperativistasFiltrados" 
        :key="coop.id"
        class="cooperativista-card"
        :class="[obtenerClasesCargo(coop), { 'is-inactive': !coop.is_active }]"
      >
        <div class="card-header-custom">
          <div class="status-badge" :class="{ 'active': coop.is_active }">
            {{ coop.is_active ? 'ACTIVO' : 'INACTIVO' }}
          </div>
        </div>
        
        <div class="card-body">
          <h3 class="cooperativista-nombre">
            {{ coop.nombres }} {{ coop.apellido_paterno }} {{ coop.apellido_materno }}
          </h3>
          
          <div class="cooperativista-info">
            <div class="info-row">
              <i class="mdi mdi-card-account-details"></i>
              <span>{{ coop.ci || 'Sin CI' }} {{ coop.ci_expedido ? `- ${coop.ci_expedido}` : '' }}</span>
            </div>
                        
            <div class="info-row">
              <i class="mdi mdi-office-building"></i>
              <span>{{ getSeccionName(coop.id_cuadrilla) }}</span>
            </div>
            
            <div class="info-row">
              <i class="mdi mdi-account-group"></i>
              <span>{{ getCuadrillaName(coop.id_cuadrilla) }}</span>
            </div>
            
            <div class="info-row-rol" v-if="coop.rol_cuadrilla">
              <i class="mdi mdi-star-circle"></i>
              <span>{{ coop.rol_cuadrilla }}</span>
            </div>

            <div class="info-row" v-if="coop.ocupacion">
              <i class="mdi mdi-briefcase"></i>
              <span>{{ coop.ocupacion }}</span>
            </div>

            <div class="info-row" v-if="coop.estado_asegurado">
              <i class="mdi mdi-shield-check"></i>
              <span>{{ coop.estado_asegurado }}</span>
            </div>

            <div class="info-row" v-if="coop.fecha_ingreso">
              <i class="mdi mdi-calendar"></i>
              <span>{{ formatearFecha(coop.fecha_ingreso) }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer-custom">
          <button 
            class="button is-small action-btn" 
            :class="coop.is_active ? 'is-warning' : 'is-success'"
            @click.stop="toggleActivacion(coop)"
            :title="coop.is_active ? 'Desactivar' : 'Activar'"
          >
            <i class="mdi" :class="coop.is_active ? 'mdi-cancel' : 'mdi-check-circle'"></i>
            <span>{{ coop.is_active ? 'Desactivar' : 'Activar' }}</span>
          </button>
          <button 
            class="button is-small is-info action-btn" 
            @click.stop="verDetalle(coop.id)"
            title="Ver Detalles"
          >
            <i class="mdi mdi-eye"></i>
            <span>Detalles</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando cooperativistas...</p>
    </div>

    <!-- Empty State -->
    <div v-if="!store.loading && cooperativistasFiltrados.length === 0" class="empty-state">
      <i class="mdi mdi-account-search"></i>
      <h3>No se encontraron cooperativistas</h3>
      <p>Intenta ajustar los filtros de búsqueda</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCooperativistasStore } from '~/stores/cooperativistas'
import { useCuadrillasStore } from '~/stores/cuadrillas'
import { useSeccionesStore } from '~/stores/secciones'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const store = useCooperativistasStore()
const cuadrillasStore = useCuadrillasStore()
const seccionesStore = useSeccionesStore()
const router = useRouter()

const cooperativistaAEliminar = ref(null)

// Filtros locales
const filtros = ref({
  search: '',
  id_seccion: null,
  id_cuadrilla: null,
  is_active: true,
  ocupacion: null,
  estado_asegurado: null,
  fecha_ingreso_desde: null,
  fecha_ingreso_hasta: null,
  solo_cargos_especiales: false
})

onMounted(async () => {
  // Cargar datos necesarios
  await Promise.all([
    store.cooperativistas.length === 0 ? store.cargarCooperativistas() : Promise.resolve(),
    cuadrillasStore.cuadrillas.length === 0 ? cuadrillasStore.fetchCuadrillas() : Promise.resolve(),
    seccionesStore.secciones.length === 0 ? seccionesStore.fetchSecciones() : Promise.resolve()
  ])
})

// Helper functions para obtener nombres
const getCuadrillaName = (id_cuadrilla) => {
  if (!id_cuadrilla) return 'Sin Cuadrilla'
  const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === id_cuadrilla)
  return cuadrilla ? cuadrilla.nombre : 'N/A'
}

const getSeccionName = (id_cuadrilla) => {
  if (!id_cuadrilla) return 'Sin Sección'
  const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === id_cuadrilla)
  if (!cuadrilla || !cuadrilla.id_seccion) return 'N/A'
  
  const seccion = seccionesStore.secciones.find(s => s.id === cuadrilla.id_seccion)
  return seccion ? seccion.nombre : 'N/A'
}

// Computed para cuadrillas disponibles según filtro de sección
const cuadrillasDisponibles = computed(() => {
  if (filtros.value.id_seccion !== null) {
    return cuadrillasStore.cuadrillas.filter(c => c.id_seccion === filtros.value.id_seccion)
  }
  return cuadrillasStore.cuadrillas
})

// Computed para ocupaciones únicas
const ocupacionesDisponibles = computed(() => {
  const ocupaciones = new Set(
    store.cooperativistas
      .filter(c => c.ocupacion)
      .map(c => c.ocupacion)
  )
  return Array.from(ocupaciones).sort()
})

// Computed para estados de asegurado únicos
const estadosAseguradoDisponibles = computed(() => {
  const estados = new Set(
    store.cooperativistas
      .filter(c => c.estado_asegurado)
      .map(c => c.estado_asegurado)
  )
  return Array.from(estados).sort()
})

// Filtrado completo de cooperativistas
const cooperativistasFiltrados = computed(() => {
  let resultado = store.cooperativistas
  // Filtrar por estado activo
  if (filtros.value.is_active !== null) {
    resultado = resultado.filter(c => c.is_active === filtros.value.is_active)
  }

  // Filtrar por sección (a través de cuadrilla)
  if (filtros.value.id_seccion !== null) {
    resultado = resultado.filter(c => {
      if (!c.id_cuadrilla) return false
      const cuadrilla = cuadrillasStore.cuadrillas.find(cu => cu.id === c.id_cuadrilla)
      return cuadrilla?.id_seccion === filtros.value.id_seccion
    })
  }

  // Filtrar por cuadrilla
  if (filtros.value.id_cuadrilla) {
    resultado = resultado.filter(c => c.id_cuadrilla === filtros.value.id_cuadrilla)
  }

  // Filtrar por ocupación
  if (filtros.value.ocupacion) {
    resultado = resultado.filter(c => c.ocupacion === filtros.value.ocupacion)
  }

  // Filtrar por estado asegurado
  if (filtros.value.estado_asegurado) {
    resultado = resultado.filter(c => c.estado_asegurado === filtros.value.estado_asegurado)
  }

  // Filtrar por rango de fecha de ingreso
  if (filtros.value.fecha_ingreso_desde) {
    const fechaDesde = new Date(filtros.value.fecha_ingreso_desde)
    resultado = resultado.filter(c => {
      if (!c.fecha_ingreso) return false
      const fechaIngreso = new Date(c.fecha_ingreso)
      return fechaIngreso >= fechaDesde
    })
  }

  if (filtros.value.fecha_ingreso_hasta) {
    const fechaHasta = new Date(filtros.value.fecha_ingreso_hasta)
    resultado = resultado.filter(c => {
      if (!c.fecha_ingreso) return false
      const fechaIngreso = new Date(c.fecha_ingreso)
      return fechaIngreso <= fechaHasta
    })
  }

  // Filtrar por búsqueda
  if (filtros.value.search) {
    const searchLower = filtros.value.search.toLowerCase()
    resultado = resultado.filter(c => {
      const nombreCompleto = `${c.nombres} ${c.apellido_paterno} ${c.apellido_materno}`.toLowerCase()
      const ci = c.ci ? c.ci.toLowerCase() : ''
      const qr = c.qr_code ? c.qr_code.toLowerCase() : ''
      return nombreCompleto.includes(searchLower) || ci.includes(searchLower) || qr.includes(searchLower)
    })
  }

  // Filtrar solo cargos especiales
  if (filtros.value.solo_cargos_especiales) {
    resultado = resultado.filter(c => {
      const rol = c.rol_cuadrilla ? c.rol_cuadrilla.toLowerCase() : ''
      return rol.includes('jefe') || rol.includes('tesorero') || rol.includes('delegado')
    })
  }

  return resultado
})

// Funciones para identificar cargos específicos
const esCargoEspecial = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  return rol.includes('jefe') || rol.includes('tesorero') || rol.includes('delegado')
}

const esJefeCuadrilla = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  return rol.includes('jefe') && !rol.includes('sub') && !rol.includes('tesorero')
}

const esSubJefeCuadrilla = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  return rol.includes('sub') && rol.includes('jefe')
}

const esTesoreroCuadrilla = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  return rol.includes('tesorero')
}

// Obtener clases CSS según los cargos
const obtenerClasesCargo = (coop) => {
  const clases = []
  
  if (esJefeCuadrilla(coop)) clases.push('is-jefe')
  else if (esSubJefeCuadrilla(coop)) clases.push('is-sub-jefe')
  else if (esTesoreroCuadrilla(coop)) clases.push('is-tesorero')
  
  return clases.join(' ')
}

// Contar cooperativistas por cargo
const contarPorCargo = (cargo) => {
  return cooperativistasFiltrados.value.filter(c => {
    if (cargo === 'jefe') return esJefeCuadrilla(c)
    if (cargo === 'sub') return esSubJefeCuadrilla(c)
    if (cargo === 'tesorero') return esTesoreroCuadrilla(c)
    return false
  }).length
}

const formatearFecha = (fecha) => {
  if (!fecha) return ''
  return new Date(fecha).toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const limpiarFiltros = () => {
  filtros.value = {
    search: '',
    id_seccion: null,
    id_cuadrilla: null,
    is_active: true,
    ocupacion: null,
    estado_asegurado: null,
    fecha_ingreso_desde: null,
    fecha_ingreso_hasta: null,
    solo_cargos_especiales: false
  }
}

const verDetalle = (id) => {
  router.push(`/cooperativistas/${id}`)
}

const toggleActivacion = async (coop) => {
  try {
    await store.toggleActivacion(coop.id, !coop.is_active)
  } catch (error) {
    alert('Error al cambiar estado: ' + error.message)
  }
}

useHead({
  title: 'Cooperativistas - Sistema de Gestión'
})
</script>
<style scoped>
.cooperativistas-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(135deg, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.page-header {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  animation: float 20s infinite linear;
}

.header-content .page-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
}

.header-content .page-subtitle {
  color: #a5d6a7;
  font-size: 1.1rem;
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.header-actions .quick-link {
  background: rgba(255, 255, 255, 0.95);
  color: #0d1b0d;
  font-weight: 700;
  border: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.header-actions .quick-link:hover {
  background: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.header-actions .button.is-warning {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  font-weight: 800;
  border: none;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.header-actions .button.is-warning:hover {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.filtros-section {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.field .label {
  color: #ffd700;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.2);
}

.control.has-icons-left .input {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  transition: all 0.3s ease;
}

.control.has-icons-left .input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
}

.control.has-icons-left .input::placeholder {
  color: #90a4ae;
}

.icon.is-left {
  color: #9e9d24;
}

.select.is-fullwidth select {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  transition: all 0.3s ease;
}

.select.is-fullwidth select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
}

.filtros-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.filtros-especiales .button {
  font-weight: 700;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 215, 0, 0.4);
  background: rgba(15, 31, 15, 0.7);
  color: #a5d6a7;
}

.filtros-especiales .button.is-warning {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  border-color: #ffd700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

.filtros-especiales .button.is-warning:hover {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%);
  border-color: #ffd700;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5);
}

.filtros-especiales .button:not(.is-warning):hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: #ffd700;
}

.filtros-actions .button.is-light {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.filtros-actions .button.is-light:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.stats-bar {
  display: flex;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  color: #c8e6c9;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-value {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  font-size: 1.4rem;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.cooperativistas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}

.cooperativista-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 16px;
  border: 2px solid rgba(255, 215, 0, 0.2);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.cooperativista-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.cooperativista-card:hover::before {
  left: 100%;
}

.cooperativista-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(158, 157, 36, 0.3), 0 0 60px rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.5);
}

/* Estilos diferenciados por cargo */
.cooperativista-card.is-jefe {
  border: 3px solid #ffd700;
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.4);
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.9), rgba(26, 46, 26, 0.9));
}

.cooperativista-card.is-sub-jefe {
  border: 3px solid #ff9800;
  box-shadow: 0 6px 25px rgba(255, 152, 0, 0.4);
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(26, 46, 26, 0.9));
}

.cooperativista-card.is-tesorero {
  border: 3px solid #2196f3;
  box-shadow: 0 6px 25px rgba(33, 150, 243, 0.4);
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(26, 46, 26, 0.9));
}

.cooperativista-card.is-delegado {
  border: 3px solid #9c27b0;
  box-shadow: 0 6px 25px rgba(156, 39, 176, 0.4);
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.1), rgba(26, 46, 26, 0.9));
}

.card-header-custom {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.status-badge {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 800;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.status-badge.active {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  border-color: #ffd700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

.card-body {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.cooperativista-nombre {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.3;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.2);
}

.cooperativista-info {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  flex: 1;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  color: #e0f2f1;
  font-size: 0.9rem;
  font-weight: 500;
}

.info-row i {
  color: #9e9d24;
  font-size: 1.2rem;
  width: 22px;
  text-align: center;
  flex-shrink: 0;
  text-shadow: 0 0 8px rgba(158, 157, 36, 0.4);
}

.info-row-rol {
  display: flex;
  align-items: center;
  gap: 0.65rem;

  padding: 0.45rem 0.65rem;
  margin: 0.25rem 0;

  border: 1px solid rgba(224, 242, 241, 0.35);
  border-radius: 6px;

  background-color: rgba(224, 242, 241, 0.08);

  color: #e0f2f1;
  font-size: 0.9rem;
  font-weight: 500;
}


.badges-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.badge-cargo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-weight: 800;
  font-size: 0.8rem;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.badge-cargo:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.badge-cargo i {
  font-size: 1.1rem;
}

.badge-cargo.jefe {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
}

.badge-cargo.sub-jefe {
  background: linear-gradient(135deg, #ff9800 0%, #ff6f00 100%);
  color: white;
}

.badge-cargo.tesorero {
  background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
  color: white;
}

.badge-cargo.delegado {
  background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
  color: white;
}

.card-footer-custom {
  padding: 0.75rem 1.25rem;
  background: rgba(15, 31, 15, 0.9);
  display: flex;
  gap: 0.5rem;
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  margin-top: auto;
}

.card-footer-custom .button {
  flex: 1;
  font-size: 0.875rem;
  height: 2.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.card-footer-custom .button.is-ghost {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.card-footer-custom .button.is-ghost:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: #ffd700;
  transform: translateY(-1px);
}

.card-footer-custom .button.is-ghost.is-danger {
  background: rgba(244, 67, 54, 0.1);
  color: #ffcdd2;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.card-footer-custom .button.is-ghost.is-danger:hover {
  background: rgba(244, 67, 54, 0.2);
  color: #ff5252;
  border-color: #f44336;
}

.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #c8e6c9;
}

.loader {
  border: 4px solid rgba(15, 31, 15, 0.7);
  border-top: 4px solid #ffd700;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-100px) rotate(360deg);
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #90a4ae;
}

.empty-state i {
  font-size: 5rem;
  color: #9e9d24;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(158, 157, 36, 0.4);
}

.empty-state h3 {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #a5d6a7;
  font-size: 1rem;
}

/* Modal Styles */
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
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
  background: rgba(10, 26, 10, 0.9);
  backdrop-filter: blur(5px);
  z-index: -1;
}

.modal-card {
  position: relative;
  max-height: calc(100vh - 40px);
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.95));
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
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

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  margin: 0;
  font-size: 1.25rem;
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

.modal-card-foot .button {
  font-weight: 700;
  transition: all 0.3s ease;
}

.modal-card-foot .button.is-danger {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.modal-card-foot .button.is-danger:hover {
  background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.5);
}

.modal-card-foot .button:not(.is-danger) {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.modal-card-foot .button:not(.is-danger):hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

/* Responsive */
@media screen and (max-width: 1200px) {
  .filtros-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media screen and (max-width: 1023px) {
  .filtros-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .header-actions .button {
    flex: 1;
    min-width: 150px;
  }
}

@media screen and (max-width: 768px) {
  .cooperativistas-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .filtros-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-bar {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .cooperativistas-grid {
    grid-template-columns: 1fr;
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

/* Animación de entrada para modales */
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


/* Estilos específicos para inputs de fecha */
.input[type="date"] {
  background: rgba(15, 31, 15, 0.7) !important;
  border: 2px solid rgba(255, 215, 0, 0.3) !important;
  border-radius: 8px !important;
  color: #e0f2f1 !important;
  padding: 0.75rem !important;
  font-family: inherit !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  position: relative !important;
}

.input[type="date"]:focus {
  border-color: #ffd700 !important;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25) !important;
  background: rgba(26, 46, 26, 0.9) !important;
  outline: none !important;
}

.input[type="date"]:hover {
  border-color: rgba(255, 215, 0, 0.5) !important;
  background: rgba(26, 46, 26, 0.8) !important;
}

/* Estilos para el calendario nativo (Webkit/Blink) */
.input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(0.8) sepia(1) saturate(5) hue-rotate(10deg) !important;
  cursor: pointer !important;
  padding: 0.25rem !important;
  border-radius: 4px !important;
  background: rgba(255, 215, 0, 0.1) !important;
}

.input[type="date"]::-webkit-calendar-picker-indicator:hover {
  background: rgba(255, 215, 0, 0.2) !important;
}

/* Estilos para el texto del placeholder */
.input[type="date"]::placeholder {
  color: #90a4ae !important;
}

/* Estilos para Firefox */
.input[type="date"]::-moz-placeholder {
  color: #90a4ae !important;
}

/* Estilos para el texto seleccionado en el input */
.input[type="date"]::-webkit-datetime-edit {
  color: #e0f2f1 !important;
}

.input[type="date"]::-webkit-datetime-edit-fields-wrapper {
  background: transparent !important;
}

.input[type="date"]::-webkit-datetime-edit-text {
  color: #ffd700 !important;
  padding: 0 0.2em !important;
}

.input[type="date"]::-webkit-datetime-edit-month-field,
.input[type="date"]::-webkit-datetime-edit-day-field,
.input[type="date"]::-webkit-datetime-edit-year-field {
  color: #e0f2f1 !important;
}

/* Estilos para el dropdown del calendario (cuando se abre) */
.input[type="date"]::-webkit-calendar-picker-indicator:active {
  background: rgba(255, 215, 0, 0.3) !important;
}

/* Variante con icono personalizado si es necesario */
.date-input-wrapper {
  position: relative !important;
}

.date-input-wrapper::after {
  content: '📅' !important;
  position: absolute !important;
  right: 0.75rem !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  color: #9e9d24 !important;
  pointer-events: none !important;
  font-size: 1.1rem !important;
}

/* Para inputs dentro de grupos con iconos */
.control.has-icons-left .input[type="date"] {
  padding-left: 2.75rem !important;
}

/* Estilos responsivos */
@media screen and (max-width: 768px) {
  .input[type="date"] {
    font-size: 16px !important; /* Previene zoom en iOS */
    padding: 0.875rem !important;
  }
}

/* Estados de validación */
.input[type="date"]:valid {
  border-color: rgba(255, 215, 0, 0.5) !important;
}

.input[type="date"]:invalid {
  border-color: rgba(244, 67, 54, 0.5) !important;
}

/* Estilos para el calendario modal (mejora la apariencia) */
.input[type="date"]:focus::-webkit-calendar-picker-indicator {
  background: rgba(255, 215, 0, 0.2) !important;
}

/* Estilos para los botones de acción en las cartas */
.card-footer-custom {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, rgba(15, 31, 15, 0.8), rgba(10, 26, 10, 0.8));
  border-top: 1px solid rgba(255, 215, 0, 0.2);
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border-radius: 6px;
}

.action-btn i {
  font-size: 1rem;
}

.action-btn span {
  font-size: 0.75rem;
}

.action-btn.is-warning {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  border-color: #ff9800;
  color: white;
}

.action-btn.is-warning:hover {
  background: linear-gradient(135deg, #f57c00, #e65100);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.4);
}

.action-btn.is-success {
  background: linear-gradient(135deg, #4caf50, #388e3c);
  border-color: #4caf50;
  color: white;
}

.action-btn.is-success:hover {
  background: linear-gradient(135deg, #388e3c, #2e7d32);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.action-btn.is-info {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  border-color: #2196f3;
  color: white;
}

.action-btn.is-info:hover {
  background: linear-gradient(135deg, #1976d2, #1565c0);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
}

.action-btn.is-danger {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  border-color: #f44336;
  color: white;
}

.action-btn.is-danger:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

/* Carta inactiva tiene opacidad reducida */
.cooperativista-card.is-inactive {
  opacity: 0.7;
}

.cooperativista-card.is-inactive .card-body {
  filter: grayscale(0.3);
}

/* Responsive para botones en móvil */
@media screen and (max-width: 768px) {
  .card-footer-custom {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .action-btn span {
    font-size: 0.875rem;
  }
}
</style>