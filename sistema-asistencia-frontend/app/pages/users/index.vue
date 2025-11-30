<template>
  <div class="users-page">
    
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="title is-2">
            <i class="mdi mdi-account-group"></i>
            Gestión de Usuarios
          </h1>
          <p class="subtitle">Administra los usuarios del sistema</p>
        </div>
        <button 
          v-if="authStore.isSuperuser"
          class="button is-primary"
          @click="openCreateModal"
        >
          <i class="mdi mdi-plus"></i>
          <span>Nuevo Usuario</span>
        </button>
      </div>
    </div>
    
    <!-- Filters Section -->
    <div class="filters-section">
      <div class="search-box">
        <i class="mdi mdi-magnify"></i>
        <input 
          v-model="searchQuery"
          type="text" 
          class="input"
          placeholder="Buscar por nombre, usuario o email..."
          @input="handleSearch"
        >
      </div>
      
      <div class="filter-buttons">
        <div class="filter-group">
          <span class="filter-label">Estado:</span>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_active === null }"
            @click="setActiveFilter(null)"
          >
            Todos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_active === true }"
            @click="setActiveFilter(true)"
          >
            Activos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_active === false }"
            @click="setActiveFilter(false)"
          >
            Inactivos
          </button>
        </div>
        
        <div class="filter-group">
          <span class="filter-label">Rol:</span>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_superuser === null }"
            @click="setSuperuserFilter(null)"
          >
            Todos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_superuser === true }"
            @click="setSuperuserFilter(true)"
          >
            Superadmin
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': usersStore.filters.is_superuser === false }"
            @click="setSuperuserFilter(false)"
          >
            Usuario
          </button>
        </div>
        
        <button 
          class="button is-light is-small"
          @click="resetFilters"
          v-if="hasActiveFilters"
        >
          <i class="mdi mdi-filter-remove"></i>
          Limpiar
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="usersStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando usuarios...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="usersStore.error" class="notification is-danger">
      <i class="mdi mdi-alert-circle"></i>
      {{ usersStore.error }}
    </div>
    
    <!-- Users Table -->
    <div v-else class="table-container">
      <table class="table is-fullwidth is-hoverable">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Último Acceso</th>
            <th v-if="authStore.isSuperuser" class="has-text-centered">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="usersStore.users.length === 0">
            <td colspan="7" class="has-text-centered empty-state">
              <i class="mdi mdi-account-off"></i>
              <p>No se encontraron usuarios</p>
            </td>
          </tr>
          <tr v-for="user in usersStore.users" :key="user.id">
            <td>
              <div class="user-info">
                <div class="user-avatar">
                  {{ getInitials(user.username) }}
                </div>
                <strong>{{ user.username }}</strong>
              </div>
            </td>
            <td>{{ user.full_name || '-' }}</td>
            <td>{{ user.email || '-' }}</td>
            <td>
              <span class="tag" :class="user.is_superuser ? 'is-primary' : 'is-light'">
                <i class="mdi" :class="user.is_superuser ? 'mdi-shield-crown' : 'mdi-account'"></i>
                {{ user.is_superuser ? 'Superadmin' : 'Usuario' }}
              </span>
            </td>
            <td>
              <span class="tag" :class="user.is_active ? 'is-success' : 'is-danger'">
                {{ user.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>{{ formatDate(user.last_login) }}</td>
            <td v-if="authStore.isSuperuser" class="has-text-centered">
              <div class="action-buttons">
                <button 
                  class="button is-small is-info"
                  @click="openEditModal(user)"
                  title="Editar usuario"
                >
                  <i class="mdi mdi-pencil"></i>
                </button>
                <button 
                  class="button is-small is-danger"
                  @click="confirmDelete(user)"
                  title="Eliminar usuario"
                  :disabled="user.id === authStore.user.id"
                >
                  <i class="mdi mdi-delete"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination -->
    <div class="pagination-container" v-if="usersStore.users.length > 0">
      <button 
        class="button"
        :disabled="!usersStore.hasPrevPage"
        @click="prevPage"
      >
        <i class="mdi mdi-chevron-left"></i>
        Anterior
      </button>
      <span class="pagination-info">
        Página {{ usersStore.currentPage }}
      </span>
      <button 
        class="button"
        :disabled="!usersStore.hasNextPage"
        @click="nextPage"
      >
        Siguiente
        <i class="mdi mdi-chevron-right"></i>
      </button>
    </div>
    
    <!-- Modal: Create/Edit User -->
    <div class="modal" :class="{ 'is-active': showModal }">
      <div class="modal-background" @click="closeModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi" :class="isEditMode ? 'mdi-pencil' : 'mdi-account-plus'"></i>
            {{ isEditMode ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </p>
          <button class="delete" @click="closeModal"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Usuario *</label>
            <div class="control has-icons-left">
              <input 
                v-model="formData.username"
                class="input"
                type="text"
                placeholder="nombre_usuario"
                :disabled="isEditMode"
              >
              <span class="icon is-left">
                <i class="mdi mdi-account"></i>
              </span>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Nombre Completo</label>
            <div class="control has-icons-left">
              <input 
                v-model="formData.full_name"
                class="input"
                type="text"
                placeholder="Juan Pérez"
              >
              <span class="icon is-left">
                <i class="mdi mdi-card-account-details"></i>
              </span>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left">
              <input 
                v-model="formData.email"
                class="input"
                type="email"
                placeholder="email@ejemplo.com"
              >
              <span class="icon is-left">
                <i class="mdi mdi-email"></i>
              </span>
            </div>
          </div>
          
          <div class="field" v-if="!isEditMode">
            <label class="label">Contraseña *</label>
            <div class="control has-icons-left">
              <input 
                v-model="formData.password"
                class="input"
                type="password"
                placeholder="••••••••"
              >
              <span class="icon is-left">
                <i class="mdi mdi-lock"></i>
              </span>
            </div>
          </div>
          
          <div class="field" v-if="isEditMode">
            <label class="label">Nueva Contraseña (dejar vacío para no cambiar)</label>
            <div class="control has-icons-left">
              <input 
                v-model="formData.password"
                class="input"
                type="password"
                placeholder="••••••••"
              >
              <span class="icon is-left">
                <i class="mdi mdi-lock-reset"></i>
              </span>
            </div>
          </div>
          
          <div class="field">
            <label class="checkbox-label">
              <input 
                v-model="formData.is_active"
                type="checkbox"
                class="checkbox"
              >
              Usuario Activo
            </label>
          </div>
          
          <div class="field">
            <label class="checkbox-label">
              <input 
                v-model="formData.is_superuser"
                type="checkbox"
                class="checkbox"
              >
              Superadministrador
            </label>
          </div>
          
          <div v-if="modalError" class="notification is-danger is-light">
            <i class="mdi mdi-alert-circle"></i>
            {{ modalError }}
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary"
            @click="saveUser"
            :disabled="!isFormValid || modalLoading"
            :class="{ 'is-loading': modalLoading }"
          >
            <i class="mdi mdi-content-save"></i>
            {{ isEditMode ? 'Guardar Cambios' : 'Crear Usuario' }}
          </button>
          <button class="button" @click="closeModal">
            Cancelar
          </button>
        </footer>
      </div>
    </div>
    
    <!-- Modal: Confirm Delete -->
    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="closeDeleteModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi mdi-delete-alert"></i>
            Confirmar Eliminación
          </p>
          <button class="delete" @click="closeDeleteModal"></button>
        </header>
        <section class="modal-card-body">
          <p class="has-text-centered">
            ¿Estás seguro de que deseas eliminar al usuario <strong>{{ userToDelete?.username }}</strong>?
          </p>
          <p class="has-text-centered has-text-danger">
            Esta acción no se puede deshacer.
          </p>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-danger"
            @click="deleteUser"
            :disabled="deleteLoading"
            :class="{ 'is-loading': deleteLoading }"
          >
            <i class="mdi mdi-delete"></i>
            Eliminar
          </button>
          <button class="button" @click="closeDeleteModal">
            Cancelar
          </button>
        </footer>
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
const usersStore = useUsersStore()

// State
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditMode = ref(false)
const modalLoading = ref(false)
const deleteLoading = ref(false)
const modalError = ref(null)
const searchQuery = ref('')
const userToDelete = ref(null)

const formData = ref({
  username: '',
  full_name: '',
  email: '',
  password: '',
  is_active: true,
  is_superuser: false
})

const editingUserId = ref(null)

// Computed
const isFormValid = computed(() => {
  if (isEditMode.value) {
    return formData.value.username.trim() !== ''
  }
  return formData.value.username.trim() !== '' && formData.value.password.trim() !== ''
})

const hasActiveFilters = computed(() => {
  return usersStore.filters.search !== '' ||
         usersStore.filters.is_active !== null ||
         usersStore.filters.is_superuser !== null
})

// Methods
const openCreateModal = () => {
  isEditMode.value = false
  editingUserId.value = null
  formData.value = {
    username: '',
    full_name: '',
    email: '',
    password: '',
    is_active: true,
    is_superuser: false
  }
  modalError.value = null
  showModal.value = true
}

const openEditModal = (user) => {
  isEditMode.value = true
  editingUserId.value = user.id
  formData.value = {
    username: user.username,
    full_name: user.full_name || '',
    email: user.email || '',
    password: '',
    is_active: user.is_active,
    is_superuser: user.is_superuser
  }
  modalError.value = null
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  modalError.value = null
  modalLoading.value = false
}

const saveUser = async () => {
  modalLoading.value = true
  modalError.value = null
  
  const userData = { ...formData.value }
  
  // Si es edición y no hay nueva contraseña, eliminar el campo
  if (isEditMode.value && !userData.password) {
    delete userData.password
  }
  
  let result
  if (isEditMode.value) {
    result = await usersStore.updateUser(editingUserId.value, userData)
  } else {
    result = await usersStore.createUser(userData)
  }
  
  modalLoading.value = false
  
  if (result.success) {
    closeModal()
  } else {
    modalError.value = result.error
  }
}

const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  userToDelete.value = null
  deleteLoading.value = false
}

const deleteUser = async () => {
  deleteLoading.value = true
  const result = await usersStore.deleteUser(userToDelete.value.id)
  deleteLoading.value = false
  
  if (result.success) {
    closeDeleteModal()
  } else {
    alert(result.error)
  }
}

let searchTimeout
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    usersStore.setSearch(searchQuery.value)
    usersStore.fetchUsers()
  }, 500)
}

const setActiveFilter = (value) => {
  usersStore.setActiveFilter(value)
  usersStore.fetchUsers()
}

const setSuperuserFilter = (value) => {
  usersStore.setSuperuserFilter(value)
  usersStore.fetchUsers()
}

const resetFilters = () => {
  searchQuery.value = ''
  usersStore.resetFilters()
  usersStore.fetchUsers()
}

const nextPage = () => {
  usersStore.nextPage()
  usersStore.fetchUsers()
}

const prevPage = () => {
  usersStore.prevPage()
  usersStore.fetchUsers()
}

const getInitials = (username) => {
  return username.substring(0, 2).toUpperCase()
}

const formatDate = (date) => {
  if (!date) return 'Nunca'
  return new Date(date).toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  usersStore.fetchUsers()
})

useHead({
  title: 'Gestión de Usuarios'
})
</script>

<style scoped>
.users-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(135deg, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

/* Header */
.page-header {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border-radius: 16px;
  padding: 2rem 2.5rem;
  margin-bottom: 2rem;
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

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.header-text .title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
}

.header-text .title i {
  font-size: 2.5rem;
}

.header-text .subtitle {
  color: #a5d6a7;
  margin: 0;
  font-weight: 500;
  font-size: 1.1rem;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border: none;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4), 0 0 40px rgba(255, 152, 0, 0.2);
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.button.is-primary:hover {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 30px rgba(255, 215, 0, 0.6), 0 0 60px rgba(255, 152, 0, 0.4);
}

/* Filters */
.filters-section {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
}

.search-box {
  position: relative;
  margin-bottom: 1rem;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
  font-size: 1.25rem;
  z-index: 1;
}

.search-box .input {
  padding-left: 3rem;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  width: 100%;
  box-sizing: border-box;
}

.search-box .input::placeholder {
  color: #90a4ae;
}

.search-box .input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.filter-buttons {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.filter-label {
  font-weight: 700;
  color: #c8e6c9;
  font-size: 0.875rem;
}

.filter-btn {
  background: rgba(15, 31, 15, 0.7);
  border: 2px solid rgba(158, 157, 36, 0.4);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.875rem;
  color: #a5d6a7;
}

.filter-btn:hover {
  border-color: #ffd700;
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.filter-btn.active {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  border-color: #ffd700;
  color: #0d1b0d;
  font-weight: 700;
}

.button.is-light {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.button.is-light:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #c8e6c9;
}

.loader {
  margin: 0 auto 1rem;
  border: 4px solid rgba(15, 31, 15, 0.7);
  border-top: 4px solid #ffd700;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-100px) rotate(360deg);
  }
}

/* Table */
.table-container {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.8), rgba(15, 31, 15, 0.8));
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
  border: 2px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24) 1;
}

.table {
  margin: 0;
  background: transparent;
  width: 100%;
  border-collapse: collapse;
}

.table thead {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
}

.table thead th {
  color: #ffd700;
  font-weight: 800;
  padding: 1rem;
  border: none;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
  text-align: left;
}

.table tbody tr {
  transition: background 0.2s ease;
  border-bottom: 1px solid rgba(46, 125, 50, 0.2);
}

.table tbody tr:hover {
  background: rgba(255, 215, 0, 0.05);
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
  color: #e0f2f1;
  border-bottom: 1px solid rgba(46, 125, 50, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  color: #0d1b0d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
  flex-shrink: 0;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 700;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
}

.tag.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
  color: #0d1b0d;
}

.tag.is-success {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  color: white;
}

.tag.is-danger {
  background: linear-gradient(135deg, #f44336 0%, #ef5350 100%);
  color: white;
}

.tag.is-light {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.action-buttons .button {
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.button.is-info {
  background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
  color: white;
  border: none;
}

.button.is-info:hover {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  transform: scale(1.1);
}

.button.is-danger {
  background: linear-gradient(135deg, #f44336 0%, #ef5350 100%);
  color: white;
  border: none;
}

.button.is-danger:hover:not(:disabled) {
  background: linear-gradient(135deg, #ef5350 0%, #e57373 100%);
  transform: scale(1.1);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.empty-state {
  padding: 3rem !important;
  color: #90a4ae;
}

.empty-state i {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  color: #9e9d24;
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
}

.pagination-info {
  font-weight: 800;
  color: #ffd700;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.pagination-container .button {
  background: rgba(15, 31, 15, 0.7);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-container .button:hover:not(:disabled) {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: #ffd700;
}

.pagination-container .button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Modal */
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.modal.is-active {
  display: flex;
}

.modal-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 26, 10, 0.9);
  backdrop-filter: blur(5px);
  z-index: -1;
}

.modal-card {
  position: relative;
  max-height: calc(100vh - 40px);
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.95));
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.modal-card-head {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border: none;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.modal-card-title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  margin: 0;
  font-size: 1.25rem;
}

.modal-card-title i {
  font-size: 1.5rem;
}

.delete {
  background: rgba(255, 215, 0, 0.3);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.delete::before, .delete::after {
  background: #ffd700;
  content: '';
  height: 2px;
  left: 25%;
  position: absolute;
  top: 50%;
  width: 50%;
  transition: all 0.3s ease;
}

.delete::before {
  transform: translateY(-50%) rotate(45deg);
}

.delete::after {
  transform: translateY(-50%) rotate(-45deg);
}

.delete:hover {
  background: rgba(255, 215, 0, 0.5);
  transform: scale(1.1);
}

.delete:hover::before, .delete:hover::after {
  background: #ff6f00;
}

.modal-card-body {
  padding: 2rem;
  overflow-y: auto;
  flex-grow: 1;
  background: transparent;
}

.modal-card-foot {
  background: rgba(15, 31, 15, 0.9);
  border: none;
  padding: 1.5rem;
  gap: 0.75rem;
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
}

.field {
  margin-bottom: 1.25rem;
}

.label {
  color: #e0f2f1;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: block;
}

.control {
  position: relative;
}

.input {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  padding-left: 2.75rem;
  transition: all 0.3s ease;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  width: 100%;
  box-sizing: border-box;
}

.input::placeholder {
  color: #90a4ae;
}

.input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #c8e6c9;
}

.checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
  accent-color: #ffd700;
}

.modal-card-foot .button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border: none;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.modal-card-foot .button.is-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.modal-card-foot .button {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.modal-card-foot .button:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.notification.is-danger.is-light {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(211, 47, 47, 0.2));
  color: #ffcdd2;
  border-left: 4px solid #f44336;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 8px;
}

.notification.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(211, 47, 47, 0.3));
  color: #ffcdd2;
  border: 1px solid rgba(244, 67, 54, 0.5);
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.has-text-centered {
  text-align: center;
}

.has-text-danger {
  color: #f44336 !important;
}

.is-loading {
  position: relative;
  color: transparent !important;
}

.is-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 16px;
  margin: -8px 0 0 -8px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Animación de entrada para modales */
.modal.is-active .modal-card {
  animation: modal-slideIn 0.3s ease-out;
}

@keyframes modal-slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media screen and (max-width: 1023px) {
  .users-page {
    padding: 1rem;
    margin: -1.5rem -1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-text .title {
    font-size: 1.5rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .filter-buttons {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    flex-wrap: wrap;
  }
  
  .modal {
    padding: 10px;
  }
  
  .modal-card {
    max-height: calc(100vh - 20px);
    max-width: 100%;
  }
  
  .modal-card-body {
    padding: 1.5rem;
  }
  
  .modal-card-head {
    padding: 1.25rem;
  }
  
  .modal-card-foot {
    padding: 1.25rem;
    flex-direction: column;
  }
  
  .modal-card-foot .button {
    width: 100%;
    justify-content: center;
  }
}
</style>