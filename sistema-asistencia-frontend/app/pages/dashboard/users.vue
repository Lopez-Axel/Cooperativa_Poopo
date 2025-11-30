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
/* ====================================
   BASE
   ==================================== */
.users-page {
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: -2rem -1.5rem;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%) !important;
  color: #333333 !important;
}

/* Específico para modales */
.modal-card,
.modal-card-head,
.modal-card-body,
.modal-card-foot {
  background-color: #ffffff !important;
  color: #1a4d1a !important;
}

/* ====================================
   HEADER
   ==================================== */
.page-header {
  background: #c5e4c6;
  border-radius: 16px;
  padding: 2rem 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
  border: 2px solid #4caf50;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-text .title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-text .title i {
  font-size: 2.5rem;
}

.header-text .subtitle {
  color: #666;
  margin: 0;
  font-weight: 500;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  border: none;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
  border-radius: 10px;
}

.button.is-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

/* ====================================
   FILTERS
   ==================================== */
.filters-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  border: 2px solid #e0e0e0;
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
  color: #4caf50;
  font-size: 1.25rem;
  z-index: 1;
}

.search-box .input {
  padding-left: 3rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: #f5f5f5;
  color: #333;
  width: 100%;
}

.search-box .input::placeholder {
  color: #999;
}

.search-box .input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
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
  color: #2e7d32;
  font-size: 0.875rem;
}

.filter-btn {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.875rem;
  color: #666;
}

.filter-btn:hover {
  border-color: #4caf50;
  color: #2e7d32;
  background: #e8f5e9;
}

.filter-btn.active {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  border-color: #ffd700;
  color: #1a4d1a;
  font-weight: 700;
}

.button.is-light {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.button.is-light:hover {
  background: #f5f5f5;
  color: #2e7d32;
  border-color: #4caf50;
}

/* ====================================
   LOADING
   ==================================== */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.loader {
  margin: 0 auto 1rem;
  border: 4px solid #f5f5f5;
  border-top: 4px solid #4caf50;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ====================================
   TABLE
   ==================================== */
.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
  border: 2px solid #e0e0e0;
}

.table {
  margin: 0;
  background: transparent;
  width: 100%;
}

.table thead {
  background: #f5f5f5;
}

.table thead th {
  color: #2e7d32;
  font-weight: 800;
  padding: 1rem;
  border: none;
  text-transform: uppercase;
  font-size: 0.85rem;
  text-align: left;
}

.table tbody tr {
  transition: background 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.table tbody tr:hover {
  background: #f5f5f5;
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
  color: #333;
  border: none;
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
  background: linear-gradient(135deg, #4caf50, #2e7d32);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.875rem;
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
}

.tag.is-primary {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
}

.tag.is-success {
  background: #4caf50;
  color: white;
}

.tag.is-danger {
  background: #f44336;
  color: white;
}

.tag.is-light {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #e0e0e0;
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
}

.button.is-info {
  background: #4caf50;
  color: white;
}

.button.is-info:hover {
  background: #66bb6a;
  transform: scale(1.1);
}

.button.is-danger {
  background: #f44336;
  color: white;
}

.button.is-danger:hover:not(:disabled) {
  background: #ef5350;
  transform: scale(1.1);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty-state {
  padding: 3rem !important;
  color: #999;
}

.empty-state i {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  color: #4caf50;
}

/* ====================================
   PAGINATION
   ==================================== */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
}

.pagination-info {
  font-weight: 800;
  color: #2e7d32;
}

.pagination-container .button {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-container .button:hover:not(:disabled) {
  background: #e8f5e9;
  color: #2e7d32;
  border-color: #4caf50;
}

.pagination-container .button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ====================================
   MODAL
   ==================================== */
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
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}

.modal-card {
  position: relative;
  max-height: calc(100vh - 40px);
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
  overflow: hidden;
  background: white;
  border: 2px solid #e0e0e0;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}



.modal-card-head {
  background: #f5f5f5;
  border-bottom: 2px solid #e0e0e0;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-card-title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 1.25rem;
}

.delete {
  background: #e0e0e0;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete::before, .delete::after {
  background: #666;
  content: '';
  height: 2px;
  left: 25%;
  position: absolute;
  top: 50%;
  width: 50%;
}

.delete::before {
  transform: translateY(-50%) rotate(45deg);
}

.delete::after {
  transform: translateY(-50%) rotate(-45deg);
}

.delete:hover {
  background: #f44336;
}

.delete:hover::before, .delete:hover::after {
  background: white;
}

.modal-card-body {
  padding: 2rem;
  overflow-y: auto;
  flex-grow: 1;
}

.modal-card-foot {
  background: #f5f5f5;
  border-top: 2px solid #e0e0e0;
  padding: 1.5rem;
  gap: 0.75rem;
  display: flex;
  justify-content: flex-end;
}

.field {
  margin-bottom: 1.25rem;
}

.label {
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: block;
}

.control {
  position: relative;
}

.input {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.75rem;
  padding-left: 2.75rem;
  transition: all 0.3s ease;
  background: #f5f5f5;
  color: #333;
  width: 100%;
}

.input::placeholder {
  color: #999;
}

.input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
  outline: none;
}

.icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #4caf50;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #2e7d32;
}

.checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
  accent-color: #4caf50;
}

.notification.is-danger {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #ef5350;
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

/* ====================================
   RESPONSIVE
   ==================================== */
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
  
  .modal {
    padding: 10px;
  }
  
  .modal-card {
    max-width: 100%;
  }
  
  .modal-card-foot {
    flex-direction: column;
  }
  
  .modal-card-foot .button {
    width: 100%;
    justify-content: center;
  }
}
</style>