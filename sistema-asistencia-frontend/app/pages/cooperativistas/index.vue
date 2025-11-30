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
              placeholder="Buscar por nombre, CI..."
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
            <select v-model="filtros.seccion">
              <option :value="null">Todas las Secciones</option>
              <option v-for="seccion in store.secciones" :key="seccion" :value="seccion">
                Sección {{ seccion }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filtro por Cuadrilla -->
        <div class="field">
          <label class="label">Cuadrilla</label>
          <div class="select is-fullwidth">
            <select v-model="filtros.cuadrilla">
              <option :value="null">Todas las Cuadrillas</option>
              <option v-for="cuadrilla in store.cuadrillas" :key="cuadrilla" :value="cuadrilla">
                {{ cuadrilla }}
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
        <span class="stat-value">{{ store.secciones.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Cuadrillas:</span>
        <span class="stat-value">{{ store.cuadrillas.length }}</span>
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
      <div class="stat-item">
        <span class="stat-label">Delegados:</span>
        <span class="stat-value">{{ contarDelegados }}</span>
      </div>
    </div>

    <!-- Lista de Cooperativistas -->
    <div class="cooperativistas-grid" v-if="!store.loading">
      <div 
        v-for="coop in cooperativistasFiltrados" 
        :key="coop.id"
        class="cooperativista-card"
        :class="obtenerClasesCargo(coop)"
        @click="verDetalle(coop.id)"
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
              <span>{{ coop.seccion || 'N/A' }}</span>
            </div>
            
            <div class="info-row">
              <i class="mdi mdi-account-group"></i>
              <span>{{ coop.cuadrilla || 'Sin Cuadrilla' }}</span>
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

            <!-- Badges de Cargos Especiales -->
            <div class="badges-container">
              <div v-if="esDelegadoSeccion(coop)" class="badge-cargo delegado">
                <i class="mdi mdi-account-star"></i>
                <span>DELEGADO DE SECCIÓN</span>
              </div>
              
              <div v-if="esJefeCuadrilla(coop)" class="badge-cargo jefe">
                <i class="mdi mdi-star"></i>
                <span>JEFE DE CUADRILLA</span>
              </div>
              
              <div v-if="esSubJefeCuadrilla(coop)" class="badge-cargo sub-jefe">
                <i class="mdi mdi-star-half-full"></i>
                <span>SUB JEFE DE CUADRILLA</span>
              </div>
              
              <div v-if="esTesoreroCuadrilla(coop)" class="badge-cargo tesorero">
                <i class="mdi mdi-cash-multiple"></i>
                <span>TESORERO DE CUADRILLA</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer-custom">
          <button class="button is-small is-ghost" @click.stop="verDetalle(coop.id)">
            <i class="mdi mdi-eye"></i>
            Ver Detalle
          </button>
          <button class="button is-small is-ghost is-danger" @click.stop="confirmarEliminar(coop)">
            <i class="mdi mdi-delete"></i>
            Eliminar
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

    <!-- Modal de Crear Cooperativista -->
    <div class="modal" :class="{ 'is-active': mostrarFormularioCrear }">
      <div class="modal-background" @click="cerrarFormularioCrear"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Nuevo Cooperativista</p>
          <button class="delete" @click="cerrarFormularioCrear"></button>
        </header>
        <section class="modal-card-body">
          <FormularioCooperativista 
            @guardar="handleGuardar"
            @cancelar="cerrarFormularioCrear"
          />
        </section>
      </div>
    </div>

    <!-- Modal de Confirmación de Eliminación -->
    <div class="modal" :class="{ 'is-active': cooperativistaAEliminar !== null }">
      <div class="modal-background" @click="cancelarEliminar"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Eliminación</p>
          <button class="delete" @click="cancelarEliminar"></button>
        </header>
        <section class="modal-card-body">
          <p v-if="cooperativistaAEliminar">
            ¿Está seguro que desea eliminar al cooperativista 
            <strong>{{ cooperativistaAEliminar.nombres }} {{ cooperativistaAEliminar.apellido_paterno }}</strong>?
          </p>
          <p class="has-text-danger mt-3">Esta acción no se puede deshacer.</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="cancelarEliminar">Cancelar</button>
          <button class="button is-danger" @click="eliminarCooperativista">Eliminar</button>
        </footer>
      </div>
    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard'
})

const store = useCooperativistasStore()
const router = useRouter()

const mostrarFormularioCrear = ref(false)
const cooperativistaAEliminar = ref(null)

// Filtros locales extendidos
const filtros = ref({
  search: '',
  seccion: null,
  cuadrilla: null,
  is_active: true,
  ocupacion: null,
  estado_asegurado: null,
  fecha_ingreso_desde: null,
  fecha_ingreso_hasta: null,
  solo_cargos_especiales: false
})

onMounted(async () => {
  if (store.cooperativistas.length === 0) {
    await store.cargarCooperativistas()
  }
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

  // Filtrar por sección
  if (filtros.value.seccion !== null) {
    resultado = resultado.filter(c => c.seccion === filtros.value.seccion)
  }

  // Filtrar por cuadrilla
  if (filtros.value.cuadrilla) {
    resultado = resultado.filter(c => c.cuadrilla === filtros.value.cuadrilla)
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
      return nombreCompleto.includes(searchLower) || ci.includes(searchLower)
    })
  }

  // Filtrar solo cargos especiales
  if (filtros.value.solo_cargos_especiales) {
    resultado = resultado.filter(c => {
      return esDelegadoSeccion(c) || esJefeCuadrilla(c) || 
             esSubJefeCuadrilla(c) || esTesoreroCuadrilla(c)
    })
  }

  return resultado
})

// Funciones para identificar cargos específicos
const esDelegadoSeccion = (coop) => {
  const delegado = coop.delegado_seccion ? coop.delegado_seccion.toLowerCase() : ''
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  return delegado.includes('delegado') || ocupacion.includes('delegado')
}

const esJefeCuadrilla = (coop) => {
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  const jefe = coop.jefe_cuadrilla ? coop.jefe_cuadrilla.toLowerCase() : ''
  return (ocupacion.includes('jefe') || jefe.includes('jefe')) && 
         !ocupacion.includes('sub') && !jefe.includes('sub') &&
         !ocupacion.includes('tesorero') && !jefe.includes('tesorero')
}

const esSubJefeCuadrilla = (coop) => {
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  const jefe = coop.jefe_cuadrilla ? coop.jefe_cuadrilla.toLowerCase() : ''
  return (ocupacion.includes('sub jefe') || ocupacion.includes('subjefe') || 
          jefe.includes('sub jefe') || jefe.includes('subjefe') ||
          (ocupacion.includes('sub') && ocupacion.includes('jefe')) ||
          (jefe.includes('sub') && jefe.includes('jefe')))
}

const esTesoreroCuadrilla = (coop) => {
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  const jefe = coop.jefe_cuadrilla ? coop.jefe_cuadrilla.toLowerCase() : ''
  return ocupacion.includes('tesorero') || jefe.includes('tesorero')
}

// Obtener clases CSS según los cargos
const obtenerClasesCargo = (coop) => {
  const clases = []
  
  if (esDelegadoSeccion(coop)) clases.push('is-delegado')
  if (esJefeCuadrilla(coop)) clases.push('is-jefe')
  if (esSubJefeCuadrilla(coop)) clases.push('is-sub-jefe')
  if (esTesoreroCuadrilla(coop)) clases.push('is-tesorero')
  
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

const contarDelegados = computed(() => {
  return cooperativistasFiltrados.value.filter(c => esDelegadoSeccion(c)).length
})

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
    seccion: null,
    cuadrilla: null,
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

const confirmarEliminar = (coop) => {
  cooperativistaAEliminar.value = coop
}

const cancelarEliminar = () => {
  cooperativistaAEliminar.value = null
}

const eliminarCooperativista = async () => {
  if (!cooperativistaAEliminar.value) return
  
  try {
    await store.eliminarCooperativista(cooperativistaAEliminar.value.id)
    cooperativistaAEliminar.value = null
  } catch (error) {
    alert('Error al eliminar cooperativista: ' + error.message)
  }
}

const cerrarFormularioCrear = () => {
  mostrarFormularioCrear.value = false
}

const handleGuardar = async () => {
  cerrarFormularioCrear()
  await store.cargarCooperativistas()
}

useHead({
  title: 'Cooperativistas - Sistema de Gestión'
})
</script>

<style scoped>
/* ====================================
   BASE
   ==================================== */
.cooperativistas-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%);
}

.modal-card,
.modal-card-head,
.modal-card-body,
.modal-card-foot {
  background-color: #ffffff !important;
  color: #1a4d1a !important;
}

/* ====================================
   HEADER
   ==================================== */
.page-header {
  background: #c5e4c6;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
  border: 2px solid #4caf50;
}

.header-content .page-title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
}

.header-content .page-subtitle {
  color: #666;
  font-size: 1rem;
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.header-actions .quick-link {
  background: #f5f5f5;
  color: #2e7d32;
  font-weight: 700;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.header-actions .quick-link:hover {
  background: #e8f5e9;
  border-color: #4caf50;
  transform: translateY(-2px);
}

.header-actions .button.is-warning {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  font-weight: 800;
  border: none;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.header-actions .button.is-warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

/* ====================================
   FILTROS
   ==================================== */
.filtros-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid #e0e0e0;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.field .label {
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.control.has-icons-left .input {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f5f5f5;
  color: #333;
  transition: all 0.3s ease;
}

.control.has-icons-left .input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
}

.control.has-icons-left .input::placeholder {
  color: #999;
}

.icon.is-left {
  color: #4caf50;
}

.select.is-fullwidth select {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f5f5f5;
  color: #333;
  transition: all 0.3s ease;
}

.select.is-fullwidth select:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
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
  border: 2px solid #e0e0e0;
  background: #f5f5f5;
  color: #666;
}

.filtros-especiales .button.is-warning {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  border-color: #ffd700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.filtros-especiales .button:not(.is-warning):hover {
  background: #e8f5e9;
  color: #2e7d32;
  border-color: #4caf50;
}

.filtros-actions .button.is-light {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
}

.filtros-actions .button.is-light:hover {
  background: #f5f5f5;
  color: #2e7d32;
  border-color: #4caf50;
}

/* ====================================
   STATS BAR
   ==================================== */
.stats-bar {
  display: flex;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: #c5e4c6;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  border: 2px solid #e0e0e0;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  color: #666;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-value {
  color: #2e7d32;
  font-weight: 900;
  font-size: 1.4rem;
}

/* ====================================
   GRID DE COOPERATIVISTAS
   ==================================== */
.cooperativistas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}

.cooperativista-card {
  background: white;
  border-radius: 16px;
  border: 2px solid #c5e4c6;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}
s
.cooperativista-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(46, 125, 50, 0.15);
  border-color: #4caf50;
}

/* Estilos por cargo */
.cooperativista-card.is-jefe {
  border: 3px solid #ffd700;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
}

.cooperativista-card.is-sub-jefe {
  border: 3px solid #ff9800;
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
}

.cooperativista-card.is-tesorero {
  border: 3px solid #2196f3;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
}

.cooperativista-card.is-delegado {
  border: 3px solid #9c27b0;
  box-shadow: 0 4px 15px rgba(156, 39, 176, 0.2);
}

.card-header-custom {
  background: #c5e4c6;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

.status-badge {
  background: #e0e0e0;
  color: #666;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 800;
}

.status-badge.active {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
}

.card-body {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.cooperativista-nombre {
  color: #2e7d32;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.3;
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
  color: #333;
  font-size: 0.9rem;
  font-weight: 500;
}

.info-row i {
  color: #4caf50;
  font-size: 1.2rem;
  width: 22px;
  text-align: center;
  flex-shrink: 0;
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
  transition: all 0.3s ease;
}

.badge-cargo:hover {
  transform: scale(1.05);
}

.badge-cargo.jefe {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
}

.badge-cargo.sub-jefe {
  background: linear-gradient(135deg, #ff9800, #ff6f00);
  color: white;
}

.badge-cargo.tesorero {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
}

.badge-cargo.delegado {
  background: linear-gradient(135deg, #9c27b0, #7b1fa2);
  color: white;
}

.card-footer-custom {
  padding: 0.75rem 1.25rem;
  background: #f5f5f5;
  display: flex;
  gap: 0.5rem;
  border-top: 1px solid #e0e0e0;
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
  background: white;
  color: #666;
  border: 1px solid #e0e0e0;
}

.card-footer-custom .button.is-ghost:hover {
  background: #e8f5e9;
  color: #2e7d32;
  border-color: #4caf50;
}

.card-footer-custom .button.is-ghost.is-danger {
  background: white;
  color: #f44336;
  border: 1px solid #ffcdd2;
}

.card-footer-custom .button.is-ghost.is-danger:hover {
  background: #ffebee;
  border-color: #f44336;
}

/* ====================================
   LOADING Y EMPTY STATE
   ==================================== */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.loader {
  border: 4px solid #f5f5f5;
  border-top: 4px solid #4caf50;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
}

.empty-state i {
  font-size: 5rem;
  color: #4caf50;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2e7d32;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #666;
  font-size: 1rem;
}

/* ====================================
   MODAL
   ==================================== */
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
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}

.modal-card {
  position: relative;
  max-height: calc(100vh - 40px);
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
  overflow: hidden;
  background: white;
  border: 2px solid #e0e0e0;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.modal-card-head {
  background: #f5f5f5;
  border-bottom: 2px solid #e0e0e0;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-card-title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  margin: 0;
  font-size: 1.25rem;
}

.delete {
  background: #e0e0e0;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete::before, .delete::after {
  background: #666;
  content: '';
  height: 2px;
  left: 25%;
  position: absolute;
  top: 50%;
  width: 50%;
}

.delete::before {
  transform: translateY(-50%) rotate(45deg);
}

.delete::after {
  transform: translateY(-50%) rotate(-45deg);
}

.delete:hover {
  background: #f44336;
}

.delete:hover::before, .delete:hover::after {
  background: white;
}

.modal-card-body {
  padding: 2rem;
  overflow-y: auto;
  flex-grow: 1;
}

.modal-card-foot {
  background: #f5f5f5;
  border-top: 2px solid #e0e0e0;
  padding: 1.5rem;
  gap: 0.75rem;
  display: flex;
  justify-content: flex-end;
}

.modal-card-foot .button {
  font-weight: 700;
  transition: all 0.3s ease;
}

.modal-card-foot .button.is-danger {
  background: #f44336;
  color: white;
  border: none;
}

.modal-card-foot .button.is-danger:hover {
  background: #d32f2f;
}

.modal-card-foot .button:not(.is-danger) {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
}

.modal-card-foot .button:not(.is-danger):hover {
  background: #f5f5f5;
  border-color: #4caf50;
}

/* ====================================
   INPUTS DE FECHA
   ==================================== */
.input[type="date"] {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  color: #333;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.input[type="date"]:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
  outline: none;
}

.input[type="date"]:hover {
  border-color: #4caf50;
  background: white;
}

.input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(0.5);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
}

.input[type="date"]::-webkit-calendar-picker-indicator:hover {
  background: #e8f5e9;
}

/* ====================================
   RESPONSIVE
   ==================================== */
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
    max-width: 100%;
  }
  
  .modal-card-foot {
    flex-direction: column;
  }
  
  .modal-card-foot .button {
    width: 100%;
    justify-content: center;
  }
}
</style>