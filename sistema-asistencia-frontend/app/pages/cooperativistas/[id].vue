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
  layout: 'dashboard',
  middleware: 'auth'
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
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.breadcrumb-nav {
  margin-bottom: 2rem;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(158, 157, 36, 0.3));
  color: #ffd700;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: 2px solid rgba(255, 215, 0, 0.4);
}

.breadcrumb-link:hover {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(158, 157, 36, 0.4));
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #a5d6a7;
}

.loader {
  border: 4px solid rgba(255, 215, 0, 0.2);
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

.detalle-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.credencial-cooperativista {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4), 0 0 60px rgba(255, 215, 0, 0.1);
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
}

.credencial-cooperativista.is-jefe {
  border: 4px solid #ffd700;
  box-shadow: 0 8px 40px rgba(255, 215, 0, 0.4), 0 0 80px rgba(255, 215, 0, 0.2);
}

.credencial-header {
  position: relative;
  height: 180px;
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  overflow: hidden;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
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
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2.5rem;
  color: #0d1b0d;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5);
}

.cooperativa-nombre {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.fundacion {
  color: #a5d6a7;
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
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border: 5px solid #0d1b0d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 4rem;
  color: #0d1b0d;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5);
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
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.4);
}

.status-indicator.active {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #0d1b0d;
}

.info-principal {
  text-align: center;
  padding: 1rem 2rem 1.5rem;
  border-bottom: 3px solid #ffd700;
}

.nombre-completo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.75rem;
  font-weight: 900;
  margin-bottom: 0.75rem;
  line-height: 1.3;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.codigo-principal {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  font-size: 1.25rem;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  display: inline-block;
  letter-spacing: 1px;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

.cargo-especial {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  color: #0d1b0d;
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
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.cargo-especial i {
  font-size: 1.5rem;
}

.seccion-datos {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.seccion-datos:last-of-type {
  border-bottom: none;
}

.seccion-titulo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.seccion-titulo i {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  color: #a5d6a7;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dato-valor {
  color: #e0f2f1;
  font-size: 1rem;
  font-weight: 600;
}

.dato-valor.ocupacion {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.credencial-footer {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 215, 0, 0.2);
}

.fecha-emision {
  color: #a5d6a7;
  font-size: 0.875rem;
  margin: 0;
}

.qr-placeholder {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border: 2px solid rgba(255, 215, 0, 0.4);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #ffd700;
}

.acciones-panel {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 16px;
  padding: 1.5rem;
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  height: fit-content;
  position: sticky;
  top: 2rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.panel-titulo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #ffd700;
}

.action-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  margin-bottom: 0.75rem;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  color: #e0f2f1;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.action-button:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
}

.action-button i {
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.action-button:hover i {
  transform: scale(1.2);
}

.action-button.editar:hover {
  border-color: #ffd700;
  color: #ffd700;
}

.action-button.dispositivos:hover {
  border-color: #4caf50;
  color: #4caf50;
}

.action-button.asistencias:hover {
  border-color: #ff9800;
  color: #ff9800;
}

.action-button.desactivar:hover {
  border-color: #ff5722;
  color: #ff5722;
}

.action-button.activar:hover {
  border-color: #4caf50;
  color: #4caf50;
}

.action-button.eliminar:hover {
  border-color: #f44336;
  color: #f44336;
}

.action-button.imprimir:hover {
  border-color: #9c27b0;
  color: #9c27b0;
}

/* Modal Styles */
.modal-card-head {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 100%);
  border-bottom: 2px solid #ffd700;
}

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
}

.modal-card-body {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  color: #e0f2f1;
}

.modal-card-foot {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-top: 1px solid rgba(255, 215, 0, 0.3);
}

.button.is-danger {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  font-weight: 600;
}

.button.is-danger:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.button {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(158, 157, 36, 0.3));
  border: 2px solid rgba(255, 215, 0, 0.4);
  color: #ffd700;
  font-weight: 600;
  transition: all 0.3s ease;
}

.button:hover {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(158, 157, 36, 0.4));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
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
  
  .credencial-header {
    height: 150px;
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
}
</style>