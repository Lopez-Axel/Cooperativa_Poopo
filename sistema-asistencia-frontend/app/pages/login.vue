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
definePageMeta({
  layout: false
})

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
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 0 60px rgba(255, 215, 0, 0.1);
  min-height: 600px;
  border: 3px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700, #689f38) 1;
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
  border: 3px solid #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5), 0 0 40px rgba(158, 157, 36, 0.3);
  transition: all 0.3s ease;
}

.logo-image:hover {
  transform: rotate(360deg) scale(1.1);
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 0 0 60px rgba(158, 157, 36, 0.5);
}

.login-header .title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 900;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
}

.login-header .subtitle {
  color: #a5d6a7;
  margin: 0;
  font-weight: 500;
}

.login-form {
  margin-bottom: 2rem;
}

.login-footer {
  text-align: center;
  margin-top: auto;
}

.login-footer p {
  color: #90a4ae !important;
}

.login-right {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  filter: brightness(0.6);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(13, 27, 13, 0.9) 0%, 
    rgba(26, 46, 26, 0.85) 25%,
    rgba(30, 70, 30, 0.8) 50%,
    rgba(26, 46, 26, 0.85) 75%,
    rgba(13, 27, 13, 0.9) 100%);
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
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
  margin-bottom: 1rem;
  font-weight: 900;
}

.overlay-content .subtitle {
  color: #e0f2f1;
  margin-bottom: 1.5rem;
  opacity: 0.95;
  font-weight: 500;
}

.decorative-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #ffd700, #9e9d24);
  margin: 0 auto;
  border-radius: 2px;
  box-shadow: 0 0 15px rgba(158, 157, 36, 0.6);
}

.overlay-content p {
  color: #c8e6c9;
  line-height: 1.6;
}

.label {
  color: #e0f2f1;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.input {
  border-radius: 8px;
  border: 2px solid rgba(255, 215, 0, 0.3);
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  transition: all 0.3s ease;
}

.input::placeholder {
  color: #90a4ae;
}

.input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
}

.control.has-icons-left .icon {
  color: #9e9d24;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  border: none;
  border-radius: 8px;
  font-weight: 700;
  transition: all 0.3s ease;
  color: #0d1b0d;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4), 0 0 40px rgba(255, 152, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.button.is-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 30px rgba(255, 215, 0, 0.6), 0 0 60px rgba(255, 152, 0, 0.4);
}

.button.is-primary:active:not(:disabled) {
  transform: translateY(0);
}

.notification.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(211, 47, 47, 0.2));
  border: 1px solid rgba(244, 67, 54, 0.3);
  color: #ffcdd2;
}

.notification.is-danger .delete {
  background: rgba(244, 67, 54, 0.5);
}

.notification.is-danger .delete:hover {
  background: rgba(244, 67, 54, 0.7);
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