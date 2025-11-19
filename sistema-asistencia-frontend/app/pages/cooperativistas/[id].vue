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
  background: white;
}

.breadcrumb-nav {
  margin-bottom: 2rem;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #038730;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.breadcrumb-link:hover {
  color: #026d27;
  transform: translateX(-4px);
}

.loading-container {
  text-align: center;
  padding: 4rem 2rem;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #038730;
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

.detalle-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.credencial-cooperativista {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 3px solid #e9ecef;
  position: relative;
}

.credencial-cooperativista.is-jefe {
  border: 4px solid #feea01;
  box-shadow: 0 8px 32px rgba(254, 234, 1, 0.3);
}

.credencial-header {
  position: relative;
  height: 180px;
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  overflow: hidden;
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(254, 234, 1, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(254, 234, 1, 0.1) 0%, transparent 50%);
}

.logo-section {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: #feea01;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2.5rem;
  color: #038730;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.cooperativa-nombre {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.fundacion {
  color: #feea01;
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
}

.avatar-section {
  position: relative;
  text-align: center;
  margin-top: -60px;
  padding: 0 2rem 1rem;
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  background: white;
  border: 5px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 4rem;
  color: #038730;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 2;
}

.status-indicator {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.85rem;
  background: #e9ecef;
  color: #666;
}

.status-indicator.active {
  background: #feea01;
  color: #038730;
}

.info-principal {
  text-align: center;
  padding: 1rem 2rem 1.5rem;
  border-bottom: 3px solid #feea01;
}

.nombre-completo {
  color: #038730;
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.codigo-principal {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  color: #feea01;
  font-size: 1.25rem;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  display: inline-block;
  letter-spacing: 1px;
}

.cargo-especial {
  background: #feea01;
  color: #038730;
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
  box-shadow: 0 4px 12px rgba(254, 234, 1, 0.3);
}

.cargo-especial i {
  font-size: 1.5rem;
}

.seccion-datos {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e9ecef;
}

.seccion-datos:last-of-type {
  border-bottom: none;
}

.seccion-titulo {
  color: #038730;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.seccion-titulo i {
  font-size: 1.5rem;
  color: #feea01;
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
  color: #038730;
  font-weight: 700;
}

.credencial-footer {
  background: #f8f9fa;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  border: 2px solid #e9ecef;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #666;
}

.acciones-panel {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid #e9ecef;
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.panel-titulo {
  color: #038730;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #feea01;
}

.action-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  margin-bottom: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  background: white;
  color: #333;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-button i {
  font-size: 1.5rem;
}

.action-button.editar:hover {
  border-color: #038730;
  background: #f0f9f4;
  color: #038730;
}

.action-button.dispositivos:hover {
  border-color: #0066cc;
  background: #f0f7ff;
  color: #0066cc;
}

.action-button.asistencias:hover {
  border-color: #feea01;
  background: #fffef0;
  color: #038730;
}

.action-button.desactivar:hover {
  border-color: #ff9800;
  background: #fff8f0;
  color: #ff9800;
}

.action-button.activar:hover {
  border-color: #4caf50;
  background: #f0fff0;
  color: #4caf50;
}

.action-button.eliminar:hover {
  border-color: #f44336;
  background: #fff0f0;
  color: #f44336;
}

.action-button.imprimir:hover {
  border-color: #9c27b0;
  background: #f8f0ff;
  color: #9c27b0;
}

.modal-card-head {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
}

.modal-card-title {
  color: #feea01;
  font-weight: 700;
}

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
}
</style>