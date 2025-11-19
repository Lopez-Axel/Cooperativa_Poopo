<template>
  <footer class="footer dashboard-footer">
    <div class="container">
      <div class="footer-content">
        
        <!-- Info Section -->
        <div class="footer-section">
          <div class="footer-info">
            
            <div class="info-item">
              <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." style="max-height: 40px; border-radius: 50%;">
              <div class="info-text">
                <p class="has-text-weight-semibold has-text-dark">Cooperativa Minera Poopó R.L.</p>
                <p class="is-size-7 has-text-grey">Fundada el 26 de diciembre de 1953</p>
              </div>
            </div>
            
            <div class="info-item">
              <span class="icon has-text-dark">
                <i class="mdi mdi-application-cog"></i>
              </span>
              <div class="info-text">
                <p class="has-text-weight-semibold has-text-dark">Sistema de Gestión v1.0.0</p>
                <p class="is-size-7 has-text-grey">Gestión Digital de Asistencia</p>
              </div>
            </div>
            
            <div class="info-item">
              <span class="icon has-text-dark">
                <i class="mdi mdi-account-group"></i>
              </span>
              <div class="info-text">
                <p class="has-text-weight-semibold">Directorio 2025</p>
                <p class="is-size-7 has-text-grey">Al servicio de nuestros cooperativistas</p>
              </div>
            </div>
            
          </div>
        </div>
        
        <!-- Divider -->
        <hr class="footer-divider">
        
        <!-- Copyright -->
        <div class="footer-copyright">
          <p class="is-size-7 has-text-grey">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-copyright"></i>
              </span>
              <span>{{ currentYear }} Cooperativa Minera Poopó R.L. - Todos los derechos reservados</span>
            </span>
          </p>
        </div>
        
      </div>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.dashboard-footer {
  background: linear-gradient(135deg, #F0E491 0%, #BBC863 100%);
  padding: 2rem 1.5rem 1.5rem;
  margin-top: auto;
  border-top: 3px solid #658C58;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section {
  margin-bottom: 1rem;
}

.footer-info {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: space-around;
  align-items: flex-start;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  flex: 1;
  min-width: 200px;
}

.info-item .icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.info-text p {
  margin: 0;
  line-height: 1.4;
}

.info-text .has-text-weight-semibold {
  color: #31694E;
  margin-bottom: 0.25rem;
}

.footer-divider {
  background-color: rgba(101, 140, 88, 0.3);
  margin: 1.5rem 0 1rem;
  height: 2px;
}

.footer-copyright {
  text-align: center;
}

.footer-copyright .has-text-grey {
  color: #658C58 !important;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .footer-info {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .info-item {
    min-width: 100%;
  }
  
  .dashboard-footer {
    padding: 1.5rem 1rem 1rem;
  }
}

@media screen and (min-width: 769px) and (max-width: 1023px) {
  .footer-info {
    justify-content: space-between;
  }
  
  .info-item {
    flex: 0 1 calc(50% - 1rem);
  }
}
</style>