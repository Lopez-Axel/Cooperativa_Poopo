<template>
  <div class="cuadrillas-page">
    
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Cooperativistas por Cuadrilla</h1>
        <p class="page-subtitle">Vista organizada por cuadrillas de trabajo</p>
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
        <i class="mdi mdi-account-group"></i>
        <div>
          <div class="stat-number">{{ store.cuadrillas.length }}</div>
          <div class="stat-label">Cuadrillas Activas</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="mdi mdi-account-multiple"></i>
        <div>
          <div class="stat-number">{{ totalCooperativistas }}</div>
          <div class="stat-label">Total Cooperativistas</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="mdi mdi-star"></i>
        <div>
          <div class="stat-number">{{ store.jefesYTesoreros.length }}</div>
          <div class="stat-label">Jefes y Tesoreros</div>
        </div>
      </div>
    </div>

    <!-- Filtro por Sección -->
    <div class="filtro-section">
      <label class="label">Filtrar por Sección:</label>
      <div class="select is-medium">
        <select v-model="seccionSeleccionada">
          <option :value="null">Todas las Secciones</option>
          <option v-for="seccion in store.secciones" :key="seccion" :value="seccion">
            Sección {{ seccion }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando cuadrillas...</p>
    </div>

    <!-- Lista de Cuadrillas -->
    <div v-else class="cuadrillas-grid">
      <div 
        v-for="cuadrilla in cuadrillasFiltradas" 
        :key="cuadrilla"
        class="cuadrilla-card"
      >
        <div class="cuadrilla-header">
          <div class="cuadrilla-icon">
            <i class="mdi mdi-account-group"></i>
          </div>
          <div class="cuadrilla-info">
            <h2 class="cuadrilla-nombre">{{ cuadrilla }}</h2>
            <div class="cuadrilla-meta">
              <span class="meta-item">
                <i class="mdi mdi-account-multiple"></i>
                {{ cooperativistasPorCuadrilla[cuadrilla].length }} miembros
              </span>
              <span class="meta-item" v-if="obtenerSeccionesCuadrilla(cuadrilla).length > 0">
                <i class="mdi mdi-office-building"></i>
                Sección {{ obtenerSeccionesCuadrilla(cuadrilla).join(', ') }}
              </span>
            </div>
          </div>
        </div>

        <!-- Jefe de Cuadrilla destacado -->
        <div v-if="obtenerJefeCuadrilla(cuadrilla)" class="jefe-destacado">
          <div class="jefe-avatar">
            <i class="mdi mdi-star"></i>
          </div>
          <div class="jefe-info">
            <div class="jefe-cargo">JEFE DE CUADRILLA</div>
            <div class="jefe-nombre">{{ obtenerJefeCuadrilla(cuadrilla).nombres }} {{ obtenerJefeCuadrilla(cuadrilla).apellido_paterno }}</div>
            <div class="jefe-codigo">{{ obtenerJefeCuadrilla(cuadrilla).codigo_unico }}</div>
          </div>
          <button 
            class="button is-small is-warning" 
            @click="verDetalle(obtenerJefeCuadrilla(cuadrilla).id)"
          >
            <i class="mdi mdi-eye"></i>
          </button>
        </div>

        <!-- Tesorero de Cuadrilla destacado -->
        <div v-if="obtenerTesoreroCuadrilla(cuadrilla)" class="jefe-destacado tesorero">
          <div class="jefe-avatar">
            <i class="mdi mdi-cash-multiple"></i>
          </div>
          <div class="jefe-info">
            <div class="jefe-cargo">TESORERO DE CUADRILLA</div>
            <div class="jefe-nombre">{{ obtenerTesoreroCuadrilla(cuadrilla).nombres }} {{ obtenerTesoreroCuadrilla(cuadrilla).apellido_paterno }}</div>
            <div class="jefe-codigo">{{ obtenerTesoreroCuadrilla(cuadrilla).codigo_unico }}</div>
          </div>
          <button 
            class="button is-small is-warning" 
            @click="verDetalle(obtenerTesoreroCuadrilla(cuadrilla).id)"
          >
            <i class="mdi mdi-eye"></i>
          </button>
        </div>

        <!-- Lista de Miembros -->
        <div class="miembros-section">
          <h3 class="miembros-titulo">
            <i class="mdi mdi-account-multiple"></i>
            Miembros de la Cuadrilla
          </h3>
          <div class="miembros-list">
            <div 
              v-for="coop in cooperativistasPorCuadrilla[cuadrilla]" 
              :key="coop.id"
              class="miembro-item"
              @click="verDetalle(coop.id)"
            >
              <div class="miembro-avatar">
                {{ coop.nombres.charAt(0) }}{{ coop.apellido_paterno.charAt(0) }}
              </div>
              <div class="miembro-info">
                <div class="miembro-nombre">
                  {{ coop.nombres }} {{ coop.apellido_paterno }} {{ coop.apellido_materno }}
                </div>
                <div class="miembro-detalles">
                  <span class="codigo-badge">{{ coop.codigo_unico }}</span>
                  <span v-if="coop.ocupacion" class="ocupacion-text">
                    <i class="mdi mdi-briefcase"></i>
                    {{ coop.ocupacion }}
                  </span>
                </div>
              </div>
              <button class="button is-small is-ghost">
                <i class="mdi mdi-chevron-right"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Stats de la Cuadrilla -->
        <div class="cuadrilla-stats">
          <div class="stat-item">
            <i class="mdi mdi-account-check"></i>
            <span>{{ cooperativistasPorCuadrilla[cuadrilla].filter(c => c.is_active).length }} Activos</span>
          </div>
          <div class="stat-item">
            <i class="mdi mdi-briefcase"></i>
            <span>{{ obtenerOcupacionesUnicas(cuadrilla) }} Ocupaciones</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!store.loading && cuadrillasFiltradas.length === 0" class="empty-state">
      <i class="mdi mdi-account-group-outline"></i>
      <h3>No hay cuadrillas registradas</h3>
      <p>{{ seccionSeleccionada ? 'No se encontraron cuadrillas en la sección seleccionada' : 'No se encontraron cooperativistas con cuadrillas asignadas' }}</p>
    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard'
})

const store = useCooperativistasStore()
const router = useRouter()

const seccionSeleccionada = ref(null)

onMounted(async () => {
  if (store.cooperativistas.length === 0) {
    await store.cargarCooperativistas()
  }
})

const cooperativistasPorCuadrilla = computed(() => store.cooperativistasPorCuadrilla)

const cuadrillasFiltradas = computed(() => {
  let cuadrillas = store.cuadrillas
  
  if (seccionSeleccionada.value !== null) {
    cuadrillas = cuadrillas.filter(cuadrilla => {
      const coops = cooperativistasPorCuadrilla.value[cuadrilla] || []
      return coops.some(c => c.seccion === seccionSeleccionada.value)
    })
  }
  
  return cuadrillas.sort()
})

const totalCooperativistas = computed(() => {
  return Object.values(cooperativistasPorCuadrilla.value)
    .reduce((total, coops) => total + coops.length, 0)
})

const obtenerSeccionesCuadrilla = (cuadrilla) => {
  const coops = cooperativistasPorCuadrilla.value[cuadrilla] || []
  const secciones = new Set(coops.map(c => c.seccion).filter(s => s != null))
  return Array.from(secciones).sort((a, b) => a - b)
}

const obtenerJefeCuadrilla = (cuadrilla) => {
  const coops = cooperativistasPorCuadrilla.value[cuadrilla] || []
  return coops.find(c => {
    const ocupacion = c.ocupacion ? c.ocupacion.toLowerCase() : ''
    const jefe = c.jefe_cuadrilla ? c.jefe_cuadrilla.toLowerCase() : ''
    return (ocupacion.includes('jefe') || jefe.includes('jefe')) && 
           !ocupacion.includes('tesorero') && !jefe.includes('tesorero')
  })
}

const obtenerTesoreroCuadrilla = (cuadrilla) => {
  const coops = cooperativistasPorCuadrilla.value[cuadrilla] || []
  return coops.find(c => {
    const ocupacion = c.ocupacion ? c.ocupacion.toLowerCase() : ''
    const jefe = c.jefe_cuadrilla ? c.jefe_cuadrilla.toLowerCase() : ''
    return ocupacion.includes('tesorero') || jefe.includes('tesorero')
  })
}

const obtenerOcupacionesUnicas = (cuadrilla) => {
  const coops = cooperativistasPorCuadrilla.value[cuadrilla] || []
  const ocupaciones = new Set(coops.map(c => c.ocupacion).filter(Boolean))
  return ocupaciones.size
}

const verDetalle = (id) => {
  router.push(`/cooperativistas/${id}`)
}

useHead({
  title: 'Cooperativistas por Cuadrilla'
})
</script>

<style scoped>
.cuadrillas-page {
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
  grid-template-columns: repeat(3, 1fr);
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

.filtro-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid #e9ecef;
}

.filtro-section .label {
  color: #038730;
  font-weight: 700;
  margin-bottom: 0.75rem;
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

.cuadrillas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.cuadrilla-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cuadrilla-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: #feea01;
}

.cuadrilla-header {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cuadrilla-icon {
  width: 60px;
  height: 60px;
  background: #feea01;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #038730;
  flex-shrink: 0;
}

.cuadrilla-info {
  flex: 1;
}

.cuadrilla-nombre {
  color: #feea01;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.cuadrilla-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-item {
  color: white;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-item i {
  font-size: 1rem;
}

.jefe-destacado {
  background: linear-gradient(to right, #feea01, #ffd700);
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.jefe-destacado.tesorero {
  background: linear-gradient(to right, #e3f2fd, #bbdefb);
}

.jefe-avatar {
  width: 50px;
  height: 50px;
  background: #038730;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #feea01;
  flex-shrink: 0;
}

.jefe-destacado.tesorero .jefe-avatar {
  background: #1976d2;
  color: white;
}

.jefe-info {
  flex: 1;
}

.jefe-cargo {
  color: #038730;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.jefe-destacado.tesorero .jefe-cargo {
  color: #1976d2;
}

.jefe-nombre {
  color: #333;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.jefe-codigo {
  color: #666;
  font-size: 0.85rem;
  font-weight: 600;
}

.miembros-section {
  padding: 1.5rem;
  border-bottom: 2px solid #e9ecef;
}

.miembros-titulo {
  color: #038730;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.miembros-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.miembro-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 0.875rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.miembro-item:hover {
  background: white;
  border-color: #feea01;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.miembro-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  color: #feea01;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.miembro-info {
  flex: 1;
}

.miembro-nombre {
  color: #333;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.miembro-detalles {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.codigo-badge {
  background: #038730;
  color: #feea01;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.ocupacion-text {
  color: #666;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.ocupacion-text i {
  color: #038730;
}

.cuadrilla-stats {
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #038730;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-item i {
  color: #feea01;
  font-size: 1.25rem;
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

@media screen and (max-width: 1023px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cuadrillas-grid {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .cuadrillas-page {
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
}
</style>