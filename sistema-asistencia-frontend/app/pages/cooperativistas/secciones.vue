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
  layout: 'dashboard'
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
  background: white;
}

.page-header {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(3, 135, 48, 0.2);
}

.header-content .page-title {
  color: #feea01;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.header-content .page-subtitle {
  color: white;
  font-size: 1.1rem;
  margin: 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #feea01 0%, #ffd700 100%);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card i {
  font-size: 3rem;
  color: #038730;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #038730;
  line-height: 1;
}

.stat-label {
  font-size: 0.95rem;
  color: #026d27;
  font-weight: 600;
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

.secciones-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.seccion-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.seccion-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.seccion-header {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.seccion-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.seccion-titulo {
  color: #feea01;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.seccion-titulo i {
  font-size: 2rem;
}

.seccion-count {
  background: rgba(254, 234, 1, 0.2);
  color: #feea01;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
}

.toggle-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
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
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.toggle-button i {
  font-size: 1.5rem;
}

.seccion-content {
  padding: 1.5rem;
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
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.mini-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #038730;
  font-weight: 600;
}

.mini-stat i {
  font-size: 1.5rem;
  color: #feea01;
}

.cooperativistas-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cooperativista-item {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.cooperativista-item:hover {
  border-color: #feea01;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.cooperativista-item.is-jefe {
  border-color: #feea01;
  background: linear-gradient(to right, #fffef0 0%, white 100%);
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
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  color: #feea01;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
}

.item-nombre {
  color: #038730;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.item-detalles {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.detalle-badge {
  background: #038730;
  color: #feea01;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 700;
  font-size: 0.85rem;
}

.detalle-text {
  color: #666;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.detalle-text i {
  color: #038730;
}

.item-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cargo-badge {
  background: #feea01;
  color: #038730;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 800;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cargo-badge i {
  font-size: 1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.empty-state i {
  font-size: 5rem;
  color: #ccc;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #038730;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
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
}
</style>