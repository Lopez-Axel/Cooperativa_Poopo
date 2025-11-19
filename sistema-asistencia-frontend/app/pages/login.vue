<template>
  <div class="login-page">
    <div class="login-container">
      
      <!-- Left Side - Login Form -->
      <div class="login-left">
        
        <!-- Logo y Header -->
        <div class="login-header">
          <div class="logo-wrapper">
            <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." class="logo-image">
          </div>
          <h1 class="title is-3">Cooperativa Minera Poopó R.L.</h1>
          <p class="subtitle is-6">Sistema de Gestión de Asistencia</p>
        </div>
        
        <!-- Login Card -->
        <div class="login-form">
          
          <!-- Error Message -->
          <div v-if="error" class="notification is-danger is-light mb-4">
            <button class="delete" @click="error = null"></button>
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-alert-circle"></i>
              </span>
              <span>{{ error }}</span>
            </span>
          </div>
          
          <!-- Login Form -->
          <form @submit.prevent="handleLogin">
            
            <!-- Username Field -->
            <div class="field">
              <label class="label">Usuario</label>
              <div class="control has-icons-left">
                <input 
                  v-model="username" 
                  class="input is-medium" 
                  type="text" 
                  placeholder="Ingrese su usuario"
                  required
                  :disabled="loading"
                  autocomplete="username"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-account-outline"></i>
                </span>
              </div>
            </div>
            
            <!-- Password Field -->
            <div class="field">
              <label class="label">Contraseña</label>
              <div class="control has-icons-left">
                <input 
                  v-model="password" 
                  class="input is-medium" 
                  type="password" 
                  placeholder="Ingrese su contraseña"
                  required
                  :disabled="loading"
                  autocomplete="current-password"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-lock-outline"></i>
                </span>
              </div>
            </div>
            
            <!-- Submit Button -->
            <div class="field mt-5">
              <div class="control">
                <button 
                  type="submit" 
                  class="button is-primary is-medium is-fullwidth"
                  :class="{ 'is-loading': loading }"
                  :disabled="loading"
                >
                  <span class="icon">
                    <i class="mdi mdi-login"></i>
                  </span>
                  <span>Iniciar Sesión</span>
                </button>
              </div>
            </div>
            
          </form>
        </div>
        
        <!-- Footer Info -->
        <div class="login-footer">
          <p class="has-text-grey is-size-7">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-shield-check"></i>
              </span>
              <span>Fundada el 26 de Diciembre de 1953</span>
            </span>
          </p>
          <p class="has-text-grey is-size-7 mt-2">
            © {{ currentYear }} Cooperativa Minera Poopó R.L.
          </p>
        </div>
        
      </div>
      
      <!-- Right Side - Image -->
      <div class="login-right">
        <div class="image-overlay">
          <div class="overlay-content">
            <h2 class="title is-2 has-text-white">Bienvenido</h2>
            <p class="subtitle is-5 has-text-white">Sistema de Gestión Cooperativa</p>
            <div class="decorative-line"></div>
            <p class="has-text-white mt-4">Gestiona asistencias, dispositivos y cooperativistas de manera eficiente</p>
          </div>
        </div>
        <img src="https://images.unsplash.com/photo-1580651315530-69c8e0026377?q=80&w=2000" alt="Minería" class="background-image">
      </div>
      
    </div>
  </div>
</template>

<script setup>
const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)
const currentYear = new Date().getFullYear()

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})

const handleLogin = async () => {
  loading.value = true
  error.value = null
  
  const result = await authStore.login(username.value, password.value)
  
  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error
  }
  
  loading.value = false
}

useHead({
  title: 'Iniciar Sesión - Cooperativa Minera Poopó R.L.'
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  min-height: 600px;
}

.login-left {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-wrapper {
  display: inline-block;
  margin-bottom: 1.5rem;
}

.logo-image {
  max-height: 100px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-header .title {
  color: #038730;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.login-header .subtitle {
  color: #666;
  margin: 0;
}

.login-form {
  margin-bottom: 2rem;
}

.login-footer {
  text-align: center;
  margin-top: auto;
}

.login-right {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.9) 0%, rgba(2, 109, 39, 0.85) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.overlay-content {
  text-align: center;
  padding: 2rem;
}

.overlay-content .title {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 1rem;
}

.overlay-content .subtitle {
  margin-bottom: 1.5rem;
  opacity: 0.95;
}

.decorative-line {
  width: 80px;
  height: 4px;
  background: #feea01;
  margin: 0 auto;
  border-radius: 2px;
}

.label {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.input {
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.input:focus {
  border-color: #038730;
  box-shadow: 0 0 0 0.125em rgba(3, 135, 48, 0.25);
}

.button.is-primary {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.button.is-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(3, 135, 48, 0.3);
}

.button.is-primary:active:not(:disabled) {
  transform: translateY(0);
}

@media screen and (max-width: 1023px) {
  .login-container {
    grid-template-columns: 1fr;
    max-width: 500px;
  }
  
  .login-right {
    display: none;
  }
  
  .login-left {
    padding: 2rem;
  }
}

@media screen and (max-width: 768px) {
  .login-page {
    padding: 1rem;
  }
  
  .login-left {
    padding: 1.5rem;
  }
  
  .logo-image {
    max-height: 80px;
  }
  
  .login-header .title {
    font-size: 1.5rem;
  }
}
</style>