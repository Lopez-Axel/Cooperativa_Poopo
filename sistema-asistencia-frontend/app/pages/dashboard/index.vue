<template>
  <div class="dashboard-page">
    
    <!-- Welcome Section -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1 class="title is-1">
            Bienvenido, {{ userName }}
          </h1>
          <p class="subtitle is-4">Sistema de Gestión - Cooperativa Minera Poopó R.L.</p>
        </div>
        <div class="date-time-box">
          <p class="current-date">{{ currentDate }}</p>
          <p class="current-time">{{ currentTime }}</p>
        </div>
      </div>
    </div>
    
    <!-- Main Stats -->
    <div class="main-stats">
      
      <div class="stat-box">
        <div class="stat-icon">
          <i class="mdi mdi-account-group"></i>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.cooperativistas }}</div>
          <div class="stat-title">Total Cooperativistas</div>
          <div class="stat-footer">Registrados en el sistema</div>
        </div>
      </div>
      
      <div class="stat-box">
        <div class="stat-icon">
          <i class="mdi mdi-calendar-check"></i>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.asistenciasMes }}</div>
          <div class="stat-title">Asistencias del Mes</div>
          <div class="stat-footer">{{ currentMonth }}</div>
        </div>
      </div>
      
      <div class="stat-box">
        <div class="stat-icon">
          <i class="mdi mdi-cellphone-link"></i>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.dispositivosActivos }}</div>
          <div class="stat-title">Dispositivos Activos</div>
          <div class="stat-footer">Registrados y verificados</div>
        </div>
      </div>
      
    </div>
    
    <!-- Secondary Stats Grid -->
    <div class="secondary-stats">
      
      <div class="info-card">
        <div class="info-icon">
          <i class="mdi mdi-account-check"></i>
        </div>
        <div class="info-content">
          <div class="info-value">{{ stats.pendientes }}</div>
          <div class="info-label">Pendientes de Marcar</div>
        </div>
      </div>
      
      <div class="info-card">
        <div class="info-icon">
          <i class="mdi mdi-shield-check"></i>
        </div>
        <div class="info-content">
          <div class="info-value">{{ stats.seccionesActivas }}</div>
          <div class="info-label">Secciones Activas</div>
        </div>
      </div>
      
      <div class="info-card">
        <div class="info-icon">
          <i class="mdi mdi-chart-line"></i>
        </div>
        <div class="info-content">
          <div class="info-value">{{ stats.cobertura }}%</div>
          <div class="info-label">Cobertura del Mes</div>
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
.dashboard-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
}

.welcome-section {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  border-radius: 16px;
  padding: 3rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 20px rgba(3, 135, 48, 0.25);
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.welcome-text {
  flex: 1;
}

.welcome-text .title {
  color: #feea01;
  margin-bottom: 0.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-text .subtitle {
  color: white;
  margin: 0;
  font-weight: 500;
}

.date-time-box {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.5rem 2rem;
  text-align: center;
  border: 2px solid rgba(254, 234, 1, 0.3);
}

.current-date {
  color: white;
  font-size: 1rem;
  font-weight: 600;
  text-transform: capitalize;
  margin-bottom: 0.5rem;
}

.current-time {
  color: white;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.main-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-box {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-left: 4px solid #feea01;
}

.stat-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-box.featured {
  background: linear-gradient(135deg, #feea01 0%, #ffd700 100%);
  border-left: 4px solid #038730;
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  background: #038730;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  flex-shrink: 0;
}

.stat-box.featured .stat-icon {
  background: #038730;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #038730;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-title {
  font-weight: 700;
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.stat-footer {
  color: #666;
  font-size: 0.875rem;
}

.secondary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
  border-top: 3px solid #feea01;
}

.info-card:hover {
  transform: scale(1.03);
}

.info-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: white;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-value {
  font-size: 2rem;
  font-weight: 800;
  color: #038730;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.info-label {
  font-size: 0.875rem;
  color: #666;
  font-weight: 600;
}

@media screen and (max-width: 1023px) {
  .main-stats {
    grid-template-columns: 1fr;
  }
  
  .secondary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .date-time-box {
    width: 100%;
  }
}

@media screen and (max-width: 768px) {
  .dashboard-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .welcome-section {
    padding: 2rem 1.5rem;
  }
  
  .welcome-text .title {
    font-size: 1.75rem;
  }
  
  .secondary-stats {
    grid-template-columns: 1fr;
  }
  
  .stat-box {
    padding: 1.5rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
}
</style>