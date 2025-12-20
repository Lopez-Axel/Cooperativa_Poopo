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
          <div class="stat-number">{{ Object.keys(cooperativistasPorSeccion).length }}</div>
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
    <div v-if="cooperativistasStore.loading || seccionesStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando secciones...</p>
    </div>

    <!-- Lista de Secciones -->
    <div v-else class="secciones-container">
      <div 
        v-for="grupo in seccionesOrdenadas" 
        :key="grupo.seccion.id"
        class="seccion-card"
      >
        <div class="seccion-header">
          <div class="seccion-info">
            <h2 class="seccion-titulo">
              <i class="mdi mdi-office-building"></i>
              {{ grupo.seccion.nombre }}
            </h2>
            <span class="seccion-count">
              {{ grupo.cooperativistas.length }} cooperativistas
            </span>
          </div>
          <button 
            class="toggle-button"
            @click="toggleSeccion(grupo.seccion.id)"
          >
            <i class="mdi" :class="seccionesExpandidas[grupo.seccion.id] ? 'mdi-chevron-up' : 'mdi-chevron-down'"></i>
          </button>
        </div>

        <transition name="slide">
          <div v-show="seccionesExpandidas[grupo.seccion.id]" class="seccion-content">
            
            <!-- Estadísticas de la Sección -->
            <div class="seccion-stats">
              <div class="mini-stat">
                <i class="mdi mdi-account-group"></i>
                <span>{{ cuadrillasEnSeccion(grupo.seccion.id) }} Cuadrillas</span>
              </div>
              <div class="mini-stat">
                <i class="mdi mdi-star"></i>
                <span>{{ jefesEnSeccion(grupo.cooperativistas) }} Jefes/Tesoreros</span>
              </div>
            </div>

            <!-- Lista de Cooperativistas -->
            <div class="cooperativistas-list">
              <div 
                v-for="coop in grupo.cooperativistas" 
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
                        {{ obtenerNombreCuadrilla(coop) }}
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
    <div v-if="!cooperativistasStore.loading && !seccionesStore.loading && Object.keys(cooperativistasPorSeccion).length === 0" class="empty-state">
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

const cooperativistasStore = useCooperativistasStore()
const cuadrillasStore = useCuadrillasStore()
const seccionesStore = useSeccionesStore()
const router = useRouter()

const seccionesExpandidas = ref({})

onMounted(async () => {
  // Cargar todos los datos necesarios
  await Promise.all([
    cooperativistasStore.cooperativistas.length === 0 ? cooperativistasStore.cargarCooperativistas() : Promise.resolve(),
    cuadrillasStore.cuadrillas.length === 0 ? cuadrillasStore.fetchCuadrillas() : Promise.resolve(),
    seccionesStore.secciones.length === 0 ? seccionesStore.fetchSecciones() : Promise.resolve()
  ])
  
  // Expandir todas las secciones por defecto
  Object.keys(cooperativistasPorSeccion.value).forEach(seccionId => {
    seccionesExpandidas.value[seccionId] = true
  })
})

// Usar el getter del store que ya maneja las relaciones correctamente
const cooperativistasPorSeccion = computed(() => cooperativistasStore.cooperativistasPorSeccion)

// Ordenar las secciones alfabéticamente
const seccionesOrdenadas = computed(() => {
  return Object.values(cooperativistasPorSeccion.value)
    .filter(grupo => grupo.seccion) // Solo incluir grupos con sección válida
    .sort((a, b) => a.seccion.nombre.localeCompare(b.seccion.nombre))
})

const totalCooperativistas = computed(() => {
  return Object.values(cooperativistasPorSeccion.value)
    .reduce((total, grupo) => total + grupo.cooperativistas.length, 0)
})

// Contar cuadrillas únicas en una sección
const cuadrillasEnSeccion = (seccionId) => {
  const cuadrillasIds = new Set()
  
  cooperativistasStore.cooperativistas
    .filter(c => c.is_active && c.id_cuadrilla)
    .forEach(c => {
      const cuadrilla = cuadrillasStore.cuadrillas.find(cu => cu.id === c.id_cuadrilla)
      if (cuadrilla && cuadrilla.id_seccion === seccionId) {
        cuadrillasIds.add(cuadrilla.id)
      }
    })
  
  return cuadrillasIds.size
}

const jefesEnSeccion = (cooperativistas) => {
  return cooperativistas.filter(c => esJefeOTesorero(c)).length
}

const toggleSeccion = (seccionId) => {
  seccionesExpandidas.value[seccionId] = !seccionesExpandidas.value[seccionId]
}

const esJefeOTesorero = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  return rol.includes('jefe') || rol.includes('tesorero')
}

const obtenerCargo = (coop) => {
  const rol = coop.rol_cuadrilla ? coop.rol_cuadrilla.toLowerCase() : ''
  
  if (rol.includes('sub')) {
    return 'SUB JEFE'
  }
  if (rol.includes('jefe')) {
    return 'JEFE'
  }
  if (rol.includes('tesorero')) {
    return 'TESORERO'
  }
  return ''
}

const obtenerNombreCuadrilla = (coop) => {
  if (!coop.id_cuadrilla) return 'Sin Cuadrilla'
  const cuadrilla = cuadrillasStore.cuadrillas.find(c => c.id === coop.id_cuadrilla)
  return cuadrilla ? cuadrilla.nombre : 'Sin Cuadrilla'
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
  animation: float 15s infinite linear;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.2);
}

.stat-card i {
  font-size: 3rem;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  flex-shrink: 0;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

.stat-number {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 0.25rem;
  text-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.stat-label {
  color: #a5d6a7;
  font-size: 0.95rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1.5rem;
}

.loader {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 215, 0, 0.2);
  border-top-color: #ffd700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-container p {
  color: #a5d6a7;
  font-size: 1.1rem;
  font-weight: 600;
}

.secciones-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.seccion-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
  transition: all 0.3s ease;
}

.seccion-card:hover {
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.2);
}

.seccion-header {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid rgba(255, 215, 0, 0.2);
}

.seccion-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.seccion-titulo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
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
  font-size: 1.75rem;
}

.seccion-count {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #0d1b0d;
  padding: 0.5rem 1rem;
  border-radius: 8px;
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

@keyframes float {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>