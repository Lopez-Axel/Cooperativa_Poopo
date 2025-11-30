<template>
  <footer class="footer dashboard-footer">
    <div class="container">
      <div class="footer-content">
        
        <!-- Info Section -->
        <div class="footer-section">
          <div class="footer-info">
            
            <div class="info-item">
              <div class="logo-container">
                <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." class="footer-logo">
                <div class="logo-shine"></div>
              </div>
              <div class="info-text">
                <p class="company-name">Cooperativa Minera Poopó R.L.</p>
                <p class="company-desc">Fundada el 26 de diciembre de 1953</p>
              </div>
            </div>
            
            <div class="info-item">
              <span class="info-icon">
                <i class="mdi mdi-application-cog"></i>
              </span>
              <div class="info-text">
                <p class="system-name">Sistema de Gestión v1.0.0</p>
                <p class="system-desc">Gestión Digital de Asistencia</p>
              </div>
            </div>
            
            <div class="info-item">
              <span class="info-icon">
                <i class="mdi mdi-account-group"></i>
              </span>
              <div class="info-text">
                <p class="directorio-name">Directorio 2025</p>
                <p class="directorio-desc">Al servicio de nuestros cooperativistas</p>
              </div>
            </div>
            
          </div>
        </div>
        
        <!-- Divider -->
        <div class="footer-divider-container">
          <div class="footer-divider"></div>
        </div>
        
        <!-- Copyright -->
        <div class="footer-copyright">
          <p class="copyright-text">
            <span class="copyright-icon">
              <i class="mdi mdi-copyright"></i>
            </span>
            <span>{{ currentYear }} Cooperativa Minera Poopó R.L. - Todos los derechos reservados</span>
          </p>
          <div class="footer-glow"></div>
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
  background: #1a4d1a;
  padding: 2rem 1.5rem 1rem;
  margin-top: auto;
  border-top: 3px solid #ffd700;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-info {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: space-around;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 250px;
  padding: 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* Logo */
.logo-container {
  position: relative;
  width: 50px;
  height: 50px;
  flex-shrink: 0;
}

.footer-logo {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #ffd700;
}

/* Icon */
.info-icon {
  font-size: 2rem;
  color: #ffd700;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-text {
  flex: 1;
}

.company-name,
.system-name,
.directorio-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: #ffd700;
  margin-bottom: 0.25rem;
}

.company-desc,
.system-desc,
.directorio-desc {
  font-size: 0.8rem;
  color: #a5d6a7;
  margin: 0;
}

/* Divider */
.footer-divider-container {
  margin: 1.5rem 0;
}

.footer-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #ffd700, transparent);
}

/* Copyright */
.footer-copyright {
  text-align: center;
  padding: 1rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
}

.copyright-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #c8e6c9;
  font-weight: 600;
  margin: 0;
}

.copyright-icon {
  color: #ffd700;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .footer-info {
    flex-direction: column;
    gap: 1rem;
  }
  
  .info-item {
    min-width: 100%;
  }
  
  .dashboard-footer {
    padding: 1.5rem 1rem 1rem;
  }
  
  .copyright-text {
    flex-direction: column;
    gap: 0.25rem;
  }
}

@media screen and (max-width: 480px) {
  .info-item {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
}
</style>