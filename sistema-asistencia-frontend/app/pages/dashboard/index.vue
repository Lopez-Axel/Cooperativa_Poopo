<template>
  <div class="index_home-page">
    
    <!-- Welcome Section -->
    <div class="index_home-welcome-section">
      <div class="index_home-welcome-content">
        <div class="index_home-welcome-text">
          <h1 class="index_home-title is-size-2">
            Bienvenido, {{ userName }}
          </h1>
          <p class="index_home-subtitle is-4">Sistema de Gestión - Cooperativa Minera Poopó R.L.</p>
        </div>
        <div class="index_home-date-time-box">
          <p class="index_home-current-date">{{ currentDate }}</p>
          <p class="index_home-current-time">{{ currentTime }}</p>
        </div>
      </div>
    </div>
    
    <!-- Main Stats -->
    <div class="index_home-main-stats">
      
      <div class="index_home-stat-box">
        <div class="index_home-stat-icon">
          <i class="mdi mdi-account-group"></i>
        </div>
        <div class="index_home-stat-info">
          <div class="index_home-stat-number">{{ stats.cooperativistas }}</div>
          <div class="index_home-stat-title">Total Cooperativistas</div>
          <div class="index_home-stat-footer">Registrados en el sistema</div>
        </div>
      </div>
      
      <div class="index_home-stat-box">
        <div class="index_home-stat-icon">
          <i class="mdi mdi-calendar-check"></i>
        </div>
        <div class="index_home-stat-info">
          <div class="index_home-stat-number">{{ stats.asistenciasMes }}</div>
          <div class="index_home-stat-title">Asistencias del Mes</div>
          <div class="index_home-stat-footer">{{ currentMonth }}</div>
        </div>
      </div>
      
      <div class="index_home-stat-box">
        <div class="index_home-stat-icon">
          <i class="mdi mdi-cellphone-link"></i>
        </div>
        <div class="index_home-stat-info">
          <div class="index_home-stat-number">{{ stats.dispositivosActivos }}</div>
          <div class="index_home-stat-title">Dispositivos Activos</div>
          <div class="index_home-stat-footer">Registrados y verificados</div>
        </div>
      </div>
      
    </div>
    
    <!-- Secondary Stats Grid -->
    <div class="index_home-secondary-stats">
      
      <div class="index_home-info-card">
        <div class="index_home-info-icon">
          <i class="mdi mdi-account-check"></i>
        </div>
        <div class="index_home-info-content">
          <div class="index_home-info-value">{{ stats.pendientes }}</div>
          <div class="index_home-info-label">Pendientes de Marcar</div>
        </div>
      </div>
      
      <div class="index_home-info-card">
        <div class="index_home-info-icon">
          <i class="mdi mdi-shield-check"></i>
        </div>
        <div class="index_home-info-content">
          <div class="index_home-info-value">{{ stats.seccionesActivas }}</div>
          <div class="index_home-info-label">Secciones Activas</div>
        </div>
      </div>
      
      <div class="index_home-info-card">
        <div class="index_home-info-icon">
          <i class="mdi mdi-chart-line"></i>
        </div>
        <div class="index_home-info-content">
          <div class="index_home-info-value">{{ stats.cobertura }}%</div>
          <div class="index_home-info-label">Cobertura del Mes</div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard'
})

const authStore = useAuthStore()
const userName = computed(() => authStore.fullName || authStore.username || 'Usuario')

const stats = ref({
  cooperativistas: 895,
  asistenciasMes: 0,
  dispositivosActivos: 0,
  pendientes: 0,
  seccionesActivas: 30,
  cobertura: 0
})

const currentTime = ref('')
const currentDate = ref('')
const currentMonth = ref('')

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('es-BO', { 
    hour: '2-digit', 
    minute: '2-digit'
  })
  currentDate.value = now.toLocaleDateString('es-BO', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
  currentMonth.value = now.toLocaleDateString('es-BO', {
    month: 'long',
    year: 'numeric'
  })
}

onMounted(() => {
  updateTime()
  const interval = setInterval(updateTime, 60000)
  
  onUnmounted(() => {
    clearInterval(interval)
  })
})

useHead({
  title: 'Panel Principal - Dashboard'
})
</script>

<style scoped>
/* ====================================
   BASE
   ==================================== */
.index_home-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%);
}

/* ====================================
   WELCOME SECTION
   ==================================== */
.index_home-welcome-section {
  background: #c5e4c6;
  border-radius: 16px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
  border: 2px solid #4caf50;
}

.index_home-welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.index_home-welcome-text {
  flex: 1;
}

.index_home-welcome-text .index_home-title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 900;
}

.index_home-welcome-text .index_home-subtitle {
  color: #2e7d32;
  margin: 0;
  font-weight: 500;
}

.index_home-date-time-box {
  background: linear-gradient(135deg, #e8f5e9, #f1f8f4);
  border-radius: 12px;
  padding: 1.5rem 2rem;
  text-align: center;
  border: 2px solid #4caf50;
  min-width: 200px;
}

.index_home-current-date {
  color: #2e7d32;
  font-size: 1rem;
  font-weight: 600;
  text-transform: capitalize;
  margin-bottom: 0.5rem;
}

.index_home-current-time {
  color: #ff9800;
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
}

/* ====================================
   MAIN STATS
   ==================================== */
.index_home-main-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.index_home-stat-box {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border: 2px solid #e0e0e0;
}

.index_home-stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(46, 125, 50, 0.15);
  border-color: #4caf50;
}

.index_home-stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  flex-shrink: 0;
  transition: transform 0.3s;
}

.index_home-stat-box:hover .index_home-stat-icon {
  transform: scale(1.1);
}

.index_home-stat-info {
  flex: 1;
}

.index_home-stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #2e7d32;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.index_home-stat-title {
  font-weight: 700;
  font-size: 1rem;
  color: #1a4d1a;
  margin-bottom: 0.3rem;
}

.index_home-stat-footer {
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
}

/* ====================================
   SECONDARY STATS
   ==================================== */
.index_home-secondary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.index_home-info-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
}

.index_home-info-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.12);
  border-color: #4caf50;
}

.index_home-info-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4caf50, #2e7d32);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: white;
  flex-shrink: 0;
  transition: transform 0.3s;
}

.index_home-info-card:hover .index_home-info-icon {
  transform: scale(1.1);
}

.index_home-info-content {
  flex: 1;
}

.index_home-info-value {
  font-size: 2rem;
  font-weight: 900;
  color: #2e7d32;
  line-height: 1;
  margin-bottom: 0.3rem;
}

.index_home-info-label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

/* ====================================
   RESPONSIVE
   ==================================== */
@media screen and (max-width: 1023px) {
  .index_home-main-stats {
    grid-template-columns: 1fr;
  }
  
  .index_home-secondary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .index_home-welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .index_home-date-time-box {
    width: 100%;
  }
}

@media screen and (max-width: 768px) {
  .index_home-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .index_home-welcome-section {
    padding: 1.5rem;
  }
  
  .index_home-secondary-stats {
    grid-template-columns: 1fr;
  }
  
  .index_home-stat-box {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
  }
  
  .index_home-stat-number {
    font-size: 2rem;
  }
  
  .index_home-info-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>