<template>
  <div class="secciones-page">
    
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Cooperativistas por Sección</h1>
        <p class="page-subtitle">Vista organizada por secciones de trabajo</p>
      </div>
      <div class="header-actions">
        <NuxtLink to="/cooperativistas" class="button is-light">
          <i class="mdi mdi-arrow-left"></i>
          <span>Volver</span>
        </NuxtLink>
      </div>
    </div>

    <!-- Stats Rápidas -->
    <div class="stats-row">
      <div class="stat-card">
        <i class="mdi mdi-office-building"></i>
        <div>
          <div class="stat-number">{{ store.secciones.length }}</div>
          <div class="stat-label">Secciones Activas</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="mdi mdi-account-group"></i>
        <div>
          <div class="stat-number">{{ totalCooperativistas }}</div>
          <div class="stat-label">Total Cooperativistas</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando secciones...</p>
    </div>

    <!-- Lista de Secciones -->
    <div v-else class="secciones-container">
      <div 
        v-for="seccion in seccionesOrdenadas" 
        :key="seccion"
        class="seccion-card"
      >
        <div class="seccion-header">
          <div class="seccion-info">
            <h2 class="seccion-titulo">
              <i class="mdi mdi-office-building"></i>
              Sección {{ seccion }}
            </h2>
            <span class="seccion-count">
              {{ cooperativistasPorSeccion[seccion].length }} cooperativistas
            </span>
          </div>
          <button 
            class="toggle-button"
            @click="toggleSeccion(seccion)"
          >
            <i class="mdi" :class="seccionesExpandidas[seccion] ? 'mdi-chevron-up' : 'mdi-chevron-down'"></i>
          </button>
        </div>

        <transition name="slide">
          <div v-show="seccionesExpandidas[seccion]" class="seccion-content">
            
            <!-- Estadísticas de la Sección -->
            <div class="seccion-stats">
              <div class="mini-stat">
                <i class="mdi mdi-account-group"></i>
                <span>{{ cuadrillasEnSeccion(seccion).length }} Cuadrillas</span>
              </div>
              <div class="mini-stat">
                <i class="mdi mdi-star"></i>
                <span>{{ jefesEnSeccion(seccion) }} Jefes/Tesoreros</span>
              </div>
            </div>

            <!-- Lista de Cooperativistas -->
            <div class="cooperativistas-list">
              <div 
                v-for="coop in cooperativistasPorSeccion[seccion]" 
                :key="coop.id"
                class="cooperativista-item"
                :class="{ 'is-jefe': esJefeOTesorero(coop) }"
                @click="verDetalle(coop.id)"
              >
                <div class="item-left">
                  <div class="item-avatar">
                    <i class="mdi mdi-account"></i>
                  </div>
                  <div class="item-info">
                    <h4 class="item-nombre">
                      {{ coop.nombres }} {{ coop.apellido_paterno }} {{ coop.apellido_materno }}
                    </h4>
                    <div class="item-detalles">
                      <span class="detalle-text">
                        <i class="mdi mdi-account-group"></i>
                        {{ coop.cuadrilla || 'Sin Cuadrilla' }}
                      </span>
                      <span class="detalle-text" v-if="coop.ocupacion">
                        <i class="mdi mdi-briefcase"></i>
                        {{ coop.ocupacion }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="item-right">
                  <span v-if="esJefeOTesorero(coop)" class="cargo-badge">
                    <i class="mdi mdi-star"></i>
                    {{ obtenerCargo(coop) }}
                  </span>
                  <button class="button is-small is-ghost" @click.stop="verDetalle(coop.id)">
                    <i class="mdi mdi-eye"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!store.loading && store.secciones.length === 0" class="empty-state">
      <i class="mdi mdi-office-building-off"></i>
      <h3>No hay secciones registradas</h3>
      <p>No se encontraron cooperativistas con secciones asignadas</p>
    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const store = useCooperativistasStore()
const router = useRouter()

const seccionesExpandidas = ref({})

onMounted(async () => {
  if (store.cooperativistas.length === 0) {
    await store.cargarCooperativistas()
  }
  
  // Expandir todas las secciones por defecto
  store.secciones.forEach(seccion => {
    seccionesExpandidas.value[seccion] = true
  })
})

const cooperativistasPorSeccion = computed(() => store.cooperativistasPorSeccion)

const seccionesOrdenadas = computed(() => {
  return store.secciones.sort((a, b) => a - b)
})

const totalCooperativistas = computed(() => {
  return Object.values(cooperativistasPorSeccion.value)
    .reduce((total, coops) => total + coops.length, 0)
})

const cuadrillasEnSeccion = (seccion) => {
  const coops = cooperativistasPorSeccion.value[seccion] || []
  const cuadrillas = new Set(coops.map(c => c.cuadrilla).filter(Boolean))
  return Array.from(cuadrillas)
}

const jefesEnSeccion = (seccion) => {
  const coops = cooperativistasPorSeccion.value[seccion] || []
  return coops.filter(c => esJefeOTesorero(c)).length
}

const toggleSeccion = (seccion) => {
  seccionesExpandidas.value[seccion] = !seccionesExpandidas.value[seccion]
}

const esJefeOTesorero = (coop) => {
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  const jefe = coop.jefe_cuadrilla ? coop.jefe_cuadrilla.toLowerCase() : ''
  return ocupacion.includes('jefe') || 
         ocupacion.includes('tesorero') ||
         jefe.includes('jefe') || 
         jefe.includes('tesorero')
}

const obtenerCargo = (coop) => {
  const ocupacion = coop.ocupacion ? coop.ocupacion.toLowerCase() : ''
  const jefe = coop.jefe_cuadrilla ? coop.jefe_cuadrilla.toLowerCase() : ''
  
  if (ocupacion.includes('sub') || jefe.includes('sub')) {
    return 'SUB JEFE'
  }
  if (ocupacion.includes('jefe') || jefe.includes('jefe')) {
    return 'JEFE'
  }
  if (ocupacion.includes('tesorero') || jefe.includes('tesorero')) {
    return 'TESORERO'
  }
  return ''
}

const verDetalle = (id) => {
  router.push(`/cooperativistas/${id}`)
}

useHead({
  title: 'Cooperativistas por Sección'
})
</script>

<style scoped>
.secciones-page {
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

.header-actions .button.is-light {
  background: rgba(255, 255, 255, 0.95);
  color: #0d1b0d;
  font-weight: 700;
  border: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.header-actions .button.is-light:hover {
  background: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  transition: all 0.6s ease;
  opacity: 0;
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(158, 157, 36, 0.3);
}

.stat-card i {
  font-size: 3rem;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  flex-shrink: 0;
}

.stat-number {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.stat-label {
  font-size: 0.95rem;
  color: #c8e6c9;
  font-weight: 600;
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

.secciones-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.seccion-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border: 2px solid rgba(255, 215, 0, 0.2);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
}

.seccion-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(158, 157, 36, 0.3), 0 0 60px rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.4);
}

.seccion-header {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  transition: all 0.3s ease;
}

.seccion-header:hover {
  background: linear-gradient(135deg, #1e461e 0%, #0f1f0f 50%, #1a2e1a 100%);
}

.seccion-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.seccion-titulo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.5rem;
  font-weight: 900;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.seccion-titulo i {
  font-size: 2rem;
}

.seccion-count {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 800;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

.toggle-button {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #ffd700;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-button:hover {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.toggle-button i {
  font-size: 1.5rem;
}

.seccion-content {
  padding: 1.5rem;
  background: transparent;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.seccion-stats {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: rgba(15, 31, 15, 0.7);
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.mini-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #c8e6c9;
  font-weight: 600;
}

.mini-stat i {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.cooperativistas-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cooperativista-item {
  background: rgba(15, 31, 15, 0.7);
  border: 2px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.cooperativista-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.cooperativista-item:hover::before {
  left: 100%;
}

.cooperativista-item:hover {
  border-color: rgba(255, 215, 0, 0.5);
  transform: translateX(8px);
  box-shadow: 0 4px 20px rgba(158, 157, 36, 0.3);
}

.cooperativista-item.is-jefe {
  border-color: #ffd700;
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(15, 31, 15, 0.7));
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
}

.item-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.item-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  color: #0d1b0d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.cooperativista-item:hover .item-avatar {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.6);
}

.item-info {
  flex: 1;
}

.item-nombre {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.2);
}

.item-detalles {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.detalle-text {
  color: #a5d6a7;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 500;
}

.detalle-text i {
  color: #9e9d24;
  text-shadow: 0 0 8px rgba(158, 157, 36, 0.4);
}

.item-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cargo-badge {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 900;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.cargo-badge:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.6);
}

.cargo-badge i {
  font-size: 1rem;
}

.button.is-small.is-ghost {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button.is-small.is-ghost:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: #ffd700;
  transform: scale(1.1);
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

@media screen and (max-width: 768px) {
  .secciones-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .seccion-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .cooperativista-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .item-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .seccion-stats {
    flex-direction: column;
    gap: 1rem;
  }
}

/* Animación de entrada para tarjetas */
.seccion-card {
  animation: cardSlideIn 0.5s ease-out;
}

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>