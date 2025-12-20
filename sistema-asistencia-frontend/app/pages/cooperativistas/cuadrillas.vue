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
          <div class="stat-number">{{ Object.keys(cooperativistasPorCuadrilla).length }}</div>
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
          <div class="stat-number">{{ cooperativistasStore.jefesYTesoreros.length }}</div>
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
          <option v-for="seccion in seccionesStore.secciones.filter(s => s.is_active)" :key="seccion.id" :value="seccion.id">
            {{ seccion.nombre }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="cooperativistasStore.loading || cuadrillasStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando cuadrillas...</p>
    </div>

    <!-- Lista de Cuadrillas -->
    <div v-else class="cuadrillas-grid">
      <div 
        v-for="grupo in cuadrillasOrdenadas" 
        :key="grupo.cuadrilla.id"
        class="cuadrilla-card"
      >
        <div class="cuadrilla-header">
          <div class="cuadrilla-icon">
            <i class="mdi mdi-account-group"></i>
          </div>
          <div class="cuadrilla-info">
            <h2 class="cuadrilla-nombre">{{ grupo.cuadrilla.nombre }}</h2>
            <div class="cuadrilla-meta">
              <span class="meta-item">
                <i class="mdi mdi-account-multiple"></i>
                {{ grupo.cooperativistas.length }} miembros
              </span>
              <span class="meta-item" v-if="obtenerSeccionCuadrilla(grupo.cuadrilla)">
                <i class="mdi mdi-office-building"></i>
                {{ obtenerSeccionCuadrilla(grupo.cuadrilla).nombre }}
              </span>
            </div>
          </div>
        </div>

        <!-- Jefe de Cuadrilla destacado -->
        <div v-if="obtenerJefeCuadrilla(grupo.cooperativistas)" class="jefe-destacado">
          <div class="jefe-avatar">
            <i class="mdi mdi-star"></i>
          </div>
          <div class="jefe-info">
            <div class="jefe-cargo">JEFE DE CUADRILLA</div>
            <div class="jefe-nombre">
              {{ obtenerJefeCuadrilla(grupo.cooperativistas).nombres }} 
              {{ obtenerJefeCuadrilla(grupo.cooperativistas).apellido_paterno }}
            </div>
            <div class="jefe-codigo">{{ obtenerJefeCuadrilla(grupo.cooperativistas).qr_code }}</div>
          </div>
          <button 
            class="button is-small is-warning" 
            @click="verDetalle(obtenerJefeCuadrilla(grupo.cooperativistas).id)"
          >
            <i class="mdi mdi-eye"></i>
          </button>
        </div>

        <!-- Tesorero de Cuadrilla destacado -->
        <div v-if="obtenerTesoreroCuadrilla(grupo.cooperativistas)" class="jefe-destacado tesorero">
          <div class="jefe-avatar">
            <i class="mdi mdi-cash-multiple"></i>
          </div>
          <div class="jefe-info">
            <div class="jefe-cargo">TESORERO DE CUADRILLA</div>
            <div class="jefe-nombre">
              {{ obtenerTesoreroCuadrilla(grupo.cooperativistas).nombres }} 
              {{ obtenerTesoreroCuadrilla(grupo.cooperativistas).apellido_paterno }}
            </div>
            <div class="jefe-codigo">{{ obtenerTesoreroCuadrilla(grupo.cooperativistas).qr_code }}</div>
          </div>
          <button 
            class="button is-small is-warning" 
            @click="verDetalle(obtenerTesoreroCuadrilla(grupo.cooperativistas).id)"
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
              v-for="coop in grupo.cooperativistas" 
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
                  <span class="codigo-badge">{{ coop.qr_code }}</span>
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
            <span>{{ grupo.cooperativistas.filter(c => c.is_active).length }} Activos</span>
          </div>
          <div class="stat-item">
            <i class="mdi mdi-briefcase"></i>
            <span>{{ obtenerOcupacionesUnicas(grupo.cooperativistas) }} Ocupaciones</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!cooperativistasStore.loading && !cuadrillasStore.loading && cuadrillasOrdenadas.length === 0" class="empty-state">
      <i class="mdi mdi-account-group-outline"></i>
      <h3>No hay cuadrillas registradas</h3>
      <p>{{ seccionSeleccionada ? 'No se encontraron cuadrillas en la sección seleccionada' : 'No se encontraron cooperativistas con cuadrillas asignadas' }}</p>
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

const seccionSeleccionada = ref(null)

onMounted(async () => {
  // Cargar todos los datos necesarios
  await Promise.all([
    cooperativistasStore.cooperativistas.length === 0 ? cooperativistasStore.cargarCooperativistas() : Promise.resolve(),
    cuadrillasStore.cuadrillas.length === 0 ? cuadrillasStore.fetchCuadrillas() : Promise.resolve(),
    seccionesStore.secciones.length === 0 ? seccionesStore.fetchSecciones() : Promise.resolve()
  ])
})

// Usar el getter del store que ya maneja las relaciones correctamente
const cooperativistasPorCuadrilla = computed(() => cooperativistasStore.cooperativistasPorCuadrilla)

// Filtrar y ordenar cuadrillas
const cuadrillasOrdenadas = computed(() => {
  let grupos = Object.values(cooperativistasPorCuadrilla.value)
    .filter(grupo => grupo.cuadrilla) // Solo incluir grupos con cuadrilla válida
  
  // Filtrar por sección si está seleccionada
  if (seccionSeleccionada.value !== null) {
    grupos = grupos.filter(grupo => {
      return grupo.cuadrilla.id_seccion === seccionSeleccionada.value
    })
  }
  
  // Ordenar alfabéticamente por nombre de cuadrilla
  return grupos.sort((a, b) => a.cuadrilla.nombre.localeCompare(b.cuadrilla.nombre))
})

const totalCooperativistas = computed(() => {
  return Object.values(cooperativistasPorCuadrilla.value)
    .reduce((total, grupo) => total + grupo.cooperativistas.length, 0)
})

const obtenerSeccionCuadrilla = (cuadrilla) => {
  if (!cuadrilla.id_seccion) return null
  return seccionesStore.secciones.find(s => s.id === cuadrilla.id_seccion)
}

const obtenerJefeCuadrilla = (cooperativistas) => {
  return cooperativistas.find(c => {
    const rol = c.rol_cuadrilla ? c.rol_cuadrilla.toLowerCase() : ''
    return rol.includes('jefe') && !rol.includes('tesorero')
  })
}

const obtenerTesoreroCuadrilla = (cooperativistas) => {
  return cooperativistas.find(c => {
    const rol = c.rol_cuadrilla ? c.rol_cuadrilla.toLowerCase() : ''
    return rol.includes('tesorero')
  })
}

const obtenerOcupacionesUnicas = (cooperativistas) => {
  const ocupaciones = new Set(cooperativistas.map(c => c.ocupacion).filter(Boolean))
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
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.page-header {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 16px;
  padding: 2.5rem;
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
  position: relative;
  z-index: 1;
}

.header-content .page-subtitle {
  color: #a5d6a7;
  font-size: 1.1rem;
  margin: 0;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.header-actions .button.is-light {
  background: rgba(255, 255, 255, 0.95);
  color: #0d1b0d;
  font-weight: 700;
  border: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
  position: relative;
  z-index: 1;
}

.header-actions .button.is-light:hover {
  background: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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

.filtro-section {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid rgba(255, 215, 0, 0.2);
}

.filtro-section .label {
  color: #ffd700;
  font-weight: 700;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select.is-medium {
  width: 100%;
}

.select.is-medium select {
  background: rgba(15, 31, 15, 0.8);
  color: #e0f2f1;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
}

.select.is-medium select:hover {
  border-color: #ffd700;
  background: rgba(15, 31, 15, 0.9);
}

.select.is-medium select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
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

.cuadrillas-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.cuadrilla-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
  transition: all 0.3s ease;
  animation: cardSlideIn 0.5s ease-out;
}

.cuadrilla-card:hover {
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.2);
  transform: translateY(-4px);
}

.cuadrilla-header {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.2);
}

.cuadrilla-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #0d1b0d;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

.cuadrilla-info {
  flex: 1;
}

.cuadrilla-nombre {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.35rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.cuadrilla-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-item {
  color: #a5d6a7;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-item i {
  color: #ffd700;
  font-size: 1rem;
}

.jefe-destacado {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(158, 157, 36, 0.1));
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.jefe-destacado.tesorero {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.15), rgba(76, 175, 80, 0.1));
}

.jefe-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #0d1b0d;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);
}

.jefe-destacado.tesorero .jefe-avatar {
  background: linear-gradient(135deg, #2e7d32, #4caf50);
  color: #e0f2f1;
}

.jefe-info {
  flex: 1;
}

.jefe-cargo {
  color: #ffd700;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.jefe-destacado.tesorero .jefe-cargo {
  color: #4caf50;
}

.jefe-nombre {
  color: #e0f2f1;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.jefe-codigo {
  color: #a5d6a7;
  font-size: 0.85rem;
  font-weight: 600;
}

.button.is-small.is-warning {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
  border: none;
  border-radius: 6px;
  font-weight: 700;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.button.is-small.is-warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5);
}

.miembros-section {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.miembros-titulo {
  color: #ffd700;
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
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 10px;
  padding: 0.875rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.miembro-item:hover {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  border-color: #ffd700;
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
}

.miembro-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  color: #0d1b0d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.9rem;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

.miembro-info {
  flex: 1;
}

.miembro-nombre {
  color: #e0f2f1;
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
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #0d1b0d;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 800;
}

.ocupacion-text {
  color: #a5d6a7;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.ocupacion-text i {
  color: #ffd700;
}

.button.is-small.is-ghost {
  background: transparent;
  border: 1px solid rgba(255, 215, 0, 0.4);
  color: #ffd700;
  transition: all 0.3s ease;
}

.button.is-small.is-ghost:hover {
  background: rgba(255, 215, 0, 0.1);
  border-color: #ffd700;
}

.cuadrilla-stats {
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a5d6a7;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-item i {
  color: #ffd700;
  font-size: 1.25rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #a5d6a7;
}

.empty-state i {
  font-size: 5rem;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.empty-state h3 {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

@keyframes float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-100px) rotate(360deg);
  }
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
  
  .cuadrillas-grid {
    grid-template-columns: 1fr;
  }
}
</style>