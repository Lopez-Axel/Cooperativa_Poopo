<template>
  <nav class="navbar dashboard-navbar" role="navigation" aria-label="main navigation">
    <div class="container is-fluid">
      
      <!-- Brand -->
      <div class="navbar-brand">
        <NuxtLink to="/" class="navbar-item brand-item">
          <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." style="max-height: 60px; border-radius: 50%;">
          <div class="brand-text">
            <span class="brand-title">Cooperativa Poopó</span>
            <span class="brand-subtitle">Sistema de Gestión</span>
          </div>
        </NuxtLink>
        
        <a 
          role="button" 
          class="navbar-burger" 
          :class="{ 'is-active': isMenuOpen }"
          @click.stop="toggleMenu"
          aria-label="menu"
          aria-expanded="false"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      
      <!-- Menu -->
      <div ref="navRef" class="navbar-menu" :class="{ 'is-active': isMenuOpen }">
        
        <!-- Navigation Links -->
        <div class="navbar-start">
          
          <NuxtLink to="/dashboard" class="navbar-item nav-link">
            <span class="icon">
              <i class="mdi mdi-view-dashboard"></i>
            </span>
            <span>Inicio</span>
          </NuxtLink>
          
          <NuxtLink to="/cooperativistas" class="navbar-item nav-link">
            <span class="icon">
              <i class="mdi mdi-account-group"></i>
            </span>
            <span>Cooperativistas</span>
          </NuxtLink>
          
          <NuxtLink to="/dashboard/asistencias" class="navbar-item nav-link">
            <span class="icon">
              <i class="mdi mdi-clipboard-check"></i>
            </span>
            <span>Asistencias</span>
          </NuxtLink>
          
          <NuxtLink to="/dashboard/dispositivos" class="navbar-item nav-link">
            <span class="icon">
              <i class="mdi mdi-cellphone-link"></i>
            </span>
            <span>Dispositivos</span>
          </NuxtLink>
          
          <!-- Solo para superadmin: se renderiza solo en cliente para evitar mismatch SSR -->
          <ClientOnly>
            <NuxtLink 
              v-if="authStore.isSuperuser" 
              to="/dashboard/users" 
              class="navbar-item nav-link"
            >
              <span class="icon">
                <i class="mdi mdi-shield-account"></i>
              </span>
              <span>Usuarios</span>
            </NuxtLink>
          </ClientOnly>
          
        </div>
        
        <!-- User Menu -->
        <div class="navbar-end">
          <!-- User menu completo envuelto en ClientOnly para que no exista en SSR -->
          <ClientOnly>
            <div ref="dropdownRef" class="navbar-item has-dropdown" :class="{ 'is-active': isUserMenuOpen }">
              <a class="navbar-link user-link" @click.stop="toggleUserMenu">
                <span class="icon">
                  <i class="mdi mdi-account-circle"></i>
                </span>
                <span>{{ authDisplayName }}</span>
              </a>
              
              <div class="navbar-dropdown is-right">
                
                <!-- User Info -->
                <div class="navbar-item user-info">
                  <div class="content">
                    <p class="is-size-7 has-text-weight-semibold mb-1">
                      <span class="icon-text">
                        <span class="icon">
                          <i class="mdi mdi-account"></i>
                        </span>
                        <span>{{ authStore.username }}</span>
                      </span>
                    </p>
                    <p v-if="authStore.isSuperuser" class="is-size-7">
                      <span class="tag is-success is-light">
                        <span class="icon">
                          <i class="mdi mdi-shield-crown"></i>
                        </span>
                        <span>Superadministrador</span>
                      </span>
                    </p>
                  </div>
                </div>
                
                <hr class="navbar-divider">
                              
                <!-- Logout Button -->
                <div class="navbar-item">
                  <button class="button is-warning is-size-7" @click="handleLogout">
                    <span class="icon">
                      <i class="mdi mdi-logout"></i>
                    </span>
                    <span>Cerrar Sesión</span>
                  </button>
                </div>
                
              </div>
            </div>
          </ClientOnly>
        </div>
                
      </div>
      
    </div>
  </nav>
</template>

<script setup>
/**
 * Correcciones clave:
 * - Partes dependientes del authStore se renderizan solo en cliente (ClientOnly)
 *   para evitar mismatches SSR <-> CSR.
 * - Uso de refs para nav y dropdown en lugar de document.querySelector.
 * - Listeners globales añadidos/removidos de forma segura.
 */

import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

/* Si estás exportando el store desde ~/stores/auth, podrías importar:
   import { useAuthStore } from '~/stores/auth'
   pero useAuthStore() suele estar disponible globalmente con Pinia + Nuxt.
*/
const authStore = useAuthStore()

// refs para control de UI
const isMenuOpen = ref(false)
const isUserMenuOpen = ref(false)
const navRef = ref(null)
const dropdownRef = ref(null)

// nombre a mostrar (solo se mostrará en cliente por el ClientOnly)
const authDisplayName = computed(() => authStore.fullName || authStore.username || 'Usuario')

const toggleMenu = (e) => {
  if (e && e.stopPropagation) e.stopPropagation()
  isMenuOpen.value = !isMenuOpen.value
}

const toggleUserMenu = (e) => {
  if (e && e.stopPropagation) e.stopPropagation()
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

const handleLogout = async () => {
  closeUserMenu()
  // asumo que authStore.logout() existe y limpia el estado
  await authStore.logout()
  navigateTo('/login')
}

// Listener global para clicks fuera — usa refs si están presentes
const onDocumentClick = (e) => {
  const target = e.target

  // cerrar user menu si el click no está dentro del dropdown
  if (dropdownRef.value && !dropdownRef.value.contains(target)) {
    isUserMenuOpen.value = false
  }

  // cerrar mobile menu si el click no está dentro de la navbar
  if (navRef.value && !navRef.value.contains(target)) {
    isMenuOpen.value = false
  }
}

onMounted(() => {
  // añadir listener solo en cliente
  document.addEventListener('click', onDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<style scoped>

.dashboard-navbar {
  background: #1a4d1a;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
  border-bottom: 3px solid #ffd700;
  min-height: 70px;
}

/* Brand */
.brand-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
}

.brand-title {
  font-weight: 800;
  font-size: 1.1rem;
  color: white;
}

.brand-subtitle {
  font-size: 0.75rem;
  color: #a5d6a7;
  font-weight: 500;
}

/* Navigation Links */
.nav-link {
  color: white;
  font-weight: 600;
  transition: all 0.2s ease;
  border-bottom: 3px solid transparent;
  margin: 0 0.25rem;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #ffd700 !important;
  border-bottom-color: #ffd700;
}

.nav-link.router-link-active {
  background: rgba(255, 215, 0, 0.2) !important;
  color: #ffd700 !important;
  border-bottom-color: #ffd700;
}

.nav-link .icon {
  color: #a5d6a7;
}

.nav-link:hover .icon,
.nav-link.router-link-active .icon {
  color: #ffd700;
}

/* User Link */
.user-link {
  color: white;
  font-weight: 600;
}

.user-link:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #ffd700 !important;
}

/* Dropdown */
.navbar-dropdown {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  margin-top: 0.5rem;
  background: white;
}

.user-info {
  background: #f8fdf8;
  color: #2e7d32;
}

/* Logout Button */
.button.is-warning {
  background: #ffd700;
  color: #1a4d1a;
  font-weight: 600;
  border: none;
  width: 100%;
}

.button.is-warning:hover {
  background: #ffc400;
}

/* Burger Menu */
.navbar-burger {
  color: white;
}

.navbar-burger:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Mobile */
@media screen and (max-width: 1023px) {
  .navbar-menu {
    background: #1a4d1a;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }
  
  .brand-text {
    display: none;
  }
}
</style>