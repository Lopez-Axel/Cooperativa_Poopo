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
          <div class="index_home-info-value">{{ stats.cuadrillasActivas }}</div>
          <div class="index_home-info-label">Cuadrillas Activas</div>
        </div>
      </div>

      
    </div>
    
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const authStore = useAuthStore()
const cooperativistasStore = useCooperativistasStore()
const userName = computed(() => authStore.fullName || authStore.username || 'Usuario')

const stats = ref({
  cooperativistas: cooperativistasStore.listaCooperativistas.length || 0,
  asistenciasMes: 0,
  dispositivosActivos: 0,
  pendientes: 0,
  seccionesActivas: cooperativistasStore.secciones.length || 0,
  cuadrillasActivas: cooperativistasStore.cuadrillas.length || 0,
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
.index_home-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.index_home-welcome-section {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 16px;
  padding: 3rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 30px rgba(76, 175, 80, 0.2), 0 0 60px rgba(255, 215, 0, 0.1);
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-welcome-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  animation: index_home-float 20s infinite linear;
}

.index_home-welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.index_home-welcome-text {
  flex: 1;
}

.index_home-welcome-text .index_home-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 900;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
}

.index_home-welcome-text .index_home-subtitle {
  color: #a5d6a7;
  margin: 0;
  font-weight: 500;
  font-size: 1.25rem;
}

.index_home-date-time-box {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  backdrop-filter: blur(15px);
  border-radius: 12px;
  padding: 1.5rem 2rem;
  text-align: center;
  border: 2px solid rgba(255, 215, 0, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  min-width: 200px;
}

.index_home-current-date {
  color: #c8e6c9;
  font-size: 1rem;
  font-weight: 600;
  text-transform: capitalize;
  margin-bottom: 0.5rem;
}

.index_home-current-time {
  color: #ffd700;
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.index_home-main-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.index_home-stat-box {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border: 2px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-stat-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.index_home-stat-box:hover::before {
  left: 100%;
}

.index_home-stat-box:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 40px rgba(158, 157, 36, 0.4), 0 0 60px rgba(255, 215, 0, 0.2);
}

.index_home-stat-icon {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #0d1b0d;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.index_home-stat-box:hover .index_home-stat-icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.index_home-stat-info {
  flex: 1;
}

.index_home-stat-number {
  font-size: 3rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.index_home-stat-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: #e0f2f1;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.index_home-stat-footer {
  color: #a5d6a7;
  font-size: 0.9rem;
  font-weight: 500;
}

.index_home-secondary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.index_home-info-card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.7));
  border-radius: 14px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(135deg, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
}

.index_home-info-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #ffd700, #9e9d24);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.index_home-info-card:hover::after {
  transform: scaleX(1);
}

.index_home-info-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 8px 30px rgba(158, 157, 36, 0.3);
}

.index_home-info-icon {
  width: 70px;
  height: 70px;
  border-radius: 14px;
  background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #e0f2f1;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
  transition: all 0.3s ease;
}

.index_home-info-card:hover .index_home-info-icon {
  transform: scale(1.1);
  background: linear-gradient(135deg, #9e9d24 0%, #cddc39 100%);
  color: #0d1b0d;
}

.index_home-info-content {
  flex: 1;
}

.index_home-info-value {
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #9e9d24, #cddc39);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 15px rgba(158, 157, 36, 0.3);
}

.index_home-info-label {
  font-size: 0.95rem;
  color: #c8e6c9;
  font-weight: 600;
  letter-spacing: 0.3px;
}

@keyframes index_home-float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-100px) rotate(360deg);
  }
}

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
    padding: 2rem 1.5rem;
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
    font-size: 2.5rem;
  }
  
  .index_home-info-card {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
  }
  
  .index_home-info-value {
    font-size: 2rem;
  }
}
</style>