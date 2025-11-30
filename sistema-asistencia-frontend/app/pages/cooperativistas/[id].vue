<template>
  <div class="detalle-cooperativista-page">
    
    <!-- Breadcrumb -->
    <nav class="breadcrumb-nav">
      <NuxtLink to="/cooperativistas" class="breadcrumb-link">
        <i class="mdi mdi-arrow-left"></i>
        Volver a Cooperativistas
      </NuxtLink>
    </nav>

    <div v-if="loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando información...</p>
    </div>

    <div v-else-if="cooperativista" class="detalle-container">
      
      <!-- Credencial del Cooperativista -->
      <div class="credencial-cooperativista" :class="{ 'is-jefe': esJefeOTesorero }">
        
        <!-- Header de la Credencial -->
        <div class="credencial-header">
          <div class="header-bg"></div>
          <div class="logo-section">
            <div class="logo-circle">
              <i class="mdi mdi-account"></i>
            </div>
            <h2 class="cooperativa-nombre">Cooperativa Minera Poopó R.L.</h2>
          </div>
        </div>

        <!-- Información Principal -->
        <div class="info-principal">
          <h1 class="nombre-completo">
            {{ cooperativista.nombres }} {{ cooperativista.apellido_paterno }} {{ cooperativista.apellido_materno }}
          </h1>
        </div>

        <!-- Badge de Cargo Especial -->
        <div v-if="esJefeOTesorero" class="cargo-especial">
          <i class="mdi mdi-star"></i>
          <span>{{ obtenerCargo }}</span>
        </div>

        <!-- Datos Personales -->
        <div class="seccion-datos">
          <h3 class="seccion-titulo">
            <i class="mdi mdi-card-account-details"></i>
            Datos Personales
          </h3>
          <div class="datos-grid">
            <div class="dato-item">
              <span class="dato-label">CI:</span>
              <span class="dato-valor">{{ cooperativista.ci || 'No registrado' }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.ci_expedido">
              <span class="dato-label">Expedido:</span>
              <span class="dato-valor">{{ cooperativista.ci_expedido }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.fecha_nacimiento">
              <span class="dato-label">Fecha Nacimiento:</span>
              <span class="dato-valor">{{ formatearFecha(cooperativista.fecha_nacimiento) }}</span>
            </div>
            <div class="dato-item" v-if="edad">
              <span class="dato-label">Edad:</span>
              <span class="dato-valor">{{ edad }} años</span>
            </div>
          </div>
        </div>

        <!-- Información Laboral -->
        <div class="seccion-datos">
          <h3 class="seccion-titulo">
            <i class="mdi mdi-briefcase"></i>
            Información Laboral
          </h3>
          <div class="datos-grid">
            <div class="dato-item">
              <span class="dato-label">Sección:</span>
              <span class="dato-valor">{{ cooperativista.seccion || 'No asignada' }}</span>
            </div>
            <div class="dato-item">
              <span class="dato-label">Cuadrilla:</span>
              <span class="dato-valor">{{ cooperativista.cuadrilla || 'No asignada' }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.jefe_cuadrilla">
              <span class="dato-label">Jefe Cuadrilla:</span>
              <span class="dato-valor">{{ cooperativista.jefe_cuadrilla }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.delegado_seccion">
              <span class="dato-label">Delegado Sección:</span>
              <span class="dato-valor">{{ cooperativista.delegado_seccion }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.ocupacion">
              <span class="dato-label">Ocupación:</span>
              <span class="dato-valor ocupacion">{{ cooperativista.ocupacion }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.fecha_ingreso">
              <span class="dato-label">Fecha Ingreso:</span>
              <span class="dato-valor">{{ formatearFecha(cooperativista.fecha_ingreso) }}</span>
            </div>
          </div>
        </div>

        <!-- Información de Seguro -->
        <div class="seccion-datos" v-if="cooperativista.codigo_asegurado">
          <h3 class="seccion-titulo">
            <i class="mdi mdi-shield-check"></i>
            Información de Seguro
          </h3>
          <div class="datos-grid">
            <div class="dato-item">
              <span class="dato-label">Código Asegurado:</span>
              <span class="dato-valor">{{ cooperativista.codigo_asegurado }}</span>
            </div>
            <div class="dato-item" v-if="cooperativista.estado_asegurado">
              <span class="dato-label">Estado:</span>
              <span class="dato-valor">{{ cooperativista.estado_asegurado }}</span>
            </div>
          </div>
        </div>

        <!-- Footer de Credencial -->
        <div class="credencial-footer">
          <p class="fecha-emision">Fecha de emisión: {{ fechaActual }}</p>
          <div class="qr-placeholder">
            <i class="mdi mdi-qrcode"></i>
          </div>
        </div>

      </div>

      <!-- Panel de Acciones -->
      <div class="acciones-panel">
        <h3 class="panel-titulo">Acciones</h3>
        
        <button class="action-button editar" @click="editarCooperativista">
          <i class="mdi mdi-pencil"></i>
          <span>Editar Información</span>
        </button>

        <button class="action-button dispositivos" @click="verDispositivos">
          <i class="mdi mdi-cellphone-link"></i>
          <span>Ver Dispositivos</span>
        </button>

        <button class="action-button asistencias" @click="verAsistencias">
          <i class="mdi mdi-calendar-check"></i>
          <span>Ver Asistencias</span>
        </button>

        <button class="action-button desactivar" @click="toggleEstado" v-if="cooperativista.is_active">
          <i class="mdi mdi-account-off"></i>
          <span>Desactivar Cooperativista</span>
        </button>

        <button class="action-button activar" @click="toggleEstado" v-else>
          <i class="mdi mdi-account-check"></i>
          <span>Activar Cooperativista</span>
        </button>

        <button class="action-button eliminar" @click="confirmarEliminar">
          <i class="mdi mdi-delete"></i>
          <span>Eliminar Cooperativista</span>
        </button>

        <button class="action-button imprimir" @click="imprimirCredencial">
          <i class="mdi mdi-printer"></i>
          <span>Imprimir Credencial</span>
        </button>
      </div>

    </div>

    <!-- Modal de Confirmación de Eliminación -->
    <div class="modal" :class="{ 'is-active': mostrarConfirmacion }">
      <div class="modal-background" @click="mostrarConfirmacion = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Eliminación</p>
          <button class="delete" @click="mostrarConfirmacion = false"></button>
        </header>
        <section class="modal-card-body">
          <p>¿Está seguro que desea eliminar al cooperativista?</p>
          <p class="has-text-danger mt-3">Esta acción no se puede deshacer.</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="mostrarConfirmacion = false">Cancelar</button>
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

const route = useRoute()
const router = useRouter()
const store = useCooperativistasStore()

const cooperativista = ref(null)
const loading = ref(true)
const mostrarConfirmacion = ref(false)

const cooperativistaId = computed(() => parseInt(route.params.id))

onMounted(async () => {
  try {
    cooperativista.value = await store.obtenerCooperativista(cooperativistaId.value)
  } catch (error) {
    alert('Error al cargar cooperativista: ' + error.message)
    router.push('/cooperativistas')
  } finally {
    loading.value = false
  }
})

const esJefeOTesorero = computed(() => {
  if (!cooperativista.value) return false
  const ocupacion = cooperativista.value.ocupacion ? cooperativista.value.ocupacion.toLowerCase() : ''
  const jefe = cooperativista.value.jefe_cuadrilla ? cooperativista.value.jefe_cuadrilla.toLowerCase() : ''
  return ocupacion.includes('jefe') || 
         ocupacion.includes('tesorero') ||
         jefe.includes('jefe') || 
         jefe.includes('tesorero')
})

const obtenerCargo = computed(() => {
  if (!cooperativista.value) return ''
  const ocupacion = cooperativista.value.ocupacion ? cooperativista.value.ocupacion.toLowerCase() : ''
  const jefe = cooperativista.value.jefe_cuadrilla ? cooperativista.value.jefe_cuadrilla.toLowerCase() : ''
  
  if (ocupacion.includes('sub') || jefe.includes('sub')) {
    return 'SUB JEFE DE CUADRILLA'
  }
  if (ocupacion.includes('jefe') || jefe.includes('jefe')) {
    return 'JEFE DE CUADRILLA'
  }
  if (ocupacion.includes('tesorero') || jefe.includes('tesorero')) {
    return 'TESORERO DE CUADRILLA'
  }
  return ''
})

const edad = computed(() => {
  if (!cooperativista.value?.fecha_nacimiento) return null
  const hoy = new Date()
  const nacimiento = new Date(cooperativista.value.fecha_nacimiento)
  let edad = hoy.getFullYear() - nacimiento.getFullYear()
  const mes = hoy.getMonth() - nacimiento.getMonth()
  if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
    edad--
  }
  return edad
})

const fechaActual = computed(() => {
  return new Date().toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const formatearFecha = (fecha) => {
  if (!fecha) return ''
  return new Date(fecha).toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const editarCooperativista = () => {
  router.push(`/cooperativistas/${cooperativistaId.value}/editar`)
}

const verDispositivos = () => {
  router.push(`/cooperativistas/${cooperativistaId.value}/dispositivos`)
}

const verAsistencias = () => {
  router.push(`/cooperativistas/${cooperativistaId.value}/asistencias`)
}

const toggleEstado = async () => {
  try {
    await store.actualizarCooperativista(cooperativistaId.value, {
      is_active: !cooperativista.value.is_active
    })
    cooperativista.value = await store.obtenerCooperativista(cooperativistaId.value)
  } catch (error) {
    alert('Error al cambiar estado: ' + error.message)
  }
}

const confirmarEliminar = () => {
  mostrarConfirmacion.value = true
}

const eliminarCooperativista = async () => {
  try {
    await store.eliminarCooperativista(cooperativistaId.value)
    router.push('/cooperativistas')
  } catch (error) {
    alert('Error al eliminar: ' + error.message)
  }
}

const imprimirCredencial = () => {
  window.print()
}

useHead({
  title: cooperativista.value ? `${cooperativista.value.nombres} ${cooperativista.value.apellido_paterno}` : 'Cooperativista'
})
</script>

<style scoped>

.detalle-cooperativista-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%);
}

/* Breadcrumb */
.breadcrumb-nav {
  margin-bottom: 2rem;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #f5f5f5;
  color: #2e7d32;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.breadcrumb-link:hover {
  background: #e8f5e9;
  border-color: #4caf50;
  transform: translateX(-4px);
}

/* Loading States */
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

/* Main Container */
.detalle-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

/* Credencial Styles */
.credencial-cooperativista {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.credencial-cooperativista:hover {
  box-shadow: 0 8px 25px rgba(46, 125, 50, 0.15);
  border-color: #4caf50;
}

.credencial-cooperativista.is-jefe {
  border: 3px solid #ffd700;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
}

.credencial-header {
  background: #4caf50;
  padding: 2rem;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #4caf50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cooperativa-nombre {
  color: white;
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0;
}

/* Información Principal */
.info-principal {
  text-align: center;
  padding: 2rem;
  border-bottom: 1px solid #e0e0e0;
}

.nombre-completo {
  color: #2e7d32;
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.cargo-especial {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  padding: 1rem 2rem;
  text-align: center;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin: 0 2rem 1.5rem;
  border-radius: 8px;
}

/* Secciones de Datos */
.seccion-datos {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e0e0e0;
}

.seccion-datos:last-of-type {
  border-bottom: none;
}

.seccion-titulo {
  color: #2e7d32;
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.seccion-titulo i {
  color: #4caf50;
  font-size: 1.5rem;
}

.datos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.dato-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.dato-label {
  color: #666;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dato-valor {
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.dato-valor.ocupacion {
  color: #2e7d32;
  font-weight: 700;
}

/* Credencial Footer */
.credencial-footer {
  background: #f5f5f5;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e0e0e0;
}

.fecha-emision {
  color: #666;
  font-size: 0.875rem;
  margin: 0;
}

.qr-placeholder {
  width: 60px;
  height: 60px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #4caf50;
}

/* Panel de Acciones */
.acciones-panel {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  border: 2px solid #e0e0e0;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.panel-titulo {
  color: #2e7d32;
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #4caf50;
}

.action-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  margin-bottom: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  color: #333;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: #e8f5e9;
  border-color: #4caf50;
  transform: translateX(4px);
}

.action-button i {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.action-button:hover i {
  transform: scale(1.1);
}

/* Colores específicos para cada botón */
.action-button.editar:hover {
  color: #2e7d32;
}

.action-button.dispositivos:hover {
  color: #4caf50;
}

.action-button.asistencias:hover {
  color: #ff9800;
}

.action-button.desactivar:hover {
  color: #ff5722;
}

.action-button.activar:hover {
  color: #4caf50;
}

.action-button.eliminar:hover {
  color: #f44336;
}

.action-button.imprimir:hover {
  color: #9c27b0;
}

/* Modal Styles */
.modal-card-head {
  background: #f5f5f5;
  border-bottom: 2px solid #e0e0e0;
}

.modal-card-title {
  color: #2e7d32;
  font-weight: 800;
}

.modal-card-body {
  background: white;
  color: #333;
}

.modal-card-foot {
  background: #f5f5f5;
  border-top: 1px solid #e0e0e0;
}

.button.is-danger {
  background: #f44336;
  color: white;
  border: none;
  font-weight: 600;
}

.button.is-danger:hover {
  background: #d32f2f;
  transform: translateY(-2px);
}

.button {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  font-weight: 600;
  transition: all 0.3s ease;
}

.button:hover {
  background: #f5f5f5;
  border-color: #4caf50;
  color: #2e7d32;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Print Styles */
@media print {
  .breadcrumb-nav,
  .acciones-panel {
    display: none;
  }
  
  .detalle-container {
    grid-template-columns: 1fr;
  }
  
  .credencial-cooperativista {
    box-shadow: none;
    border: 2px solid #333;
  }
}

/* Responsive */
@media screen and (max-width: 1023px) {
  .detalle-container {
    grid-template-columns: 1fr;
  }
  
  .acciones-panel {
    position: static;
  }
  
  .datos-grid {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .detalle-cooperativista-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .credencial-header {
    padding: 1.5rem;
  }
  
  .logo-circle {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }
  
  .cooperativa-nombre {
    font-size: 1.2rem;
  }
  
  .nombre-completo {
    font-size: 1.4rem;
  }
  
  .seccion-datos {
    padding: 1rem;
  }
  
  .cargo-especial {
    margin: 0 1rem 1rem;
    padding: 0.75rem 1rem;
    font-size: 1rem;
  }
}
</style>