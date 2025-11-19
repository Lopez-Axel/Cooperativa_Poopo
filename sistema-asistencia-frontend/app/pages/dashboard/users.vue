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
}

/* Header */
.page-header {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  border-radius: 16px;
  padding: 2rem 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(3, 135, 48, 0.25);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-text .title {
  color: #feea01;
  margin-bottom: 0.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-text .title i {
  font-size: 2.5rem;
}

.header-text .subtitle {
  color: white;
  margin: 0;
  font-weight: 500;
}

.button.is-primary {
  background: #feea01;
  color: #038730;
  border: none;
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.button.is-primary:hover {
  background: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(254, 234, 1, 0.4);
}

/* Filters */
.filters-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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
  color: #999;
  font-size: 1.25rem;
}

.search-box .input {
  padding-left: 3rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box .input:focus {
  border-color: #038730;
  box-shadow: 0 0 0 0.125em rgba(3, 135, 48, 0.25);
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
  font-weight: 600;
  color: #666;
  font-size: 0.875rem;
}

.filter-btn {
  background: white;
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
  border-color: #038730;
  color: #038730;
}

.filter-btn.active {
  background: #038730;
  border-color: #038730;
  color: white;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
}

.loader {
  margin: 0 auto 1rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #038730;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Table */
.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
}

.table {
  margin: 0;
}

.table thead {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
}

.table thead th {
  color: white;
  font-weight: 700;
  padding: 1rem;
  border: none;
}

.table tbody tr {
  transition: background 0.2s ease;
}

.table tbody tr:hover {
  background: #f8f9fa;
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
  border-bottom: 1px solid #f0f0f0;
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
  background: linear-gradient(135deg, #038730, #026d27);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 600;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
}

.tag.is-primary {
  background: #038730;
  color: white;
}

.tag.is-success {
  background: #48c774;
  color: white;
}

.tag.is-danger {
  background: #f14668;
  color: white;
}

.tag.is-light {
  background: #f5f5f5;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.action-buttons .button {
  padding: 0.5rem;
  border-radius: 6px;
}

.button.is-info {
  background: #3298dc;
  color: white;
  border: none;
}

.button.is-info:hover {
  background: #2793da;
}

.button.is-danger {
  background: #f14668;
  color: white;
  border: none;
}

.button.is-danger:hover:not(:disabled) {
  background: #ef2e55;
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
  font-weight: 700;
  color: #038730;
}

/* Modal */
.modal-card {
  border-radius: 12px;
  overflow: hidden;
  max-width: 600px;
}

.modal-card-head {
  background: linear-gradient(135deg, #038730 0%, #026d27 100%);
  border: none;
  padding: 1.5rem;
}

.modal-card-title {
  color: #feea01;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-card-title i {
  font-size: 1.5rem;
}

.modal-card-body {
  padding: 2rem;
}

.field {
  margin-bottom: 1.25rem;
}

.label {
  color: #333;
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
}

.input:focus {
  border-color: #038730;
  box-shadow: 0 0 0 0.125em rgba(3, 135, 48, 0.25);
}

.icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #666;
}

.checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.modal-card-foot {
  background: #f8f9fa;
  border: none;
  padding: 1.5rem;
  gap: 0.75rem;
}

.modal-card-foot .button.is-primary {
  background: #038730;
  color: white;
  border: none;
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-card-foot .button.is-primary:hover:not(:disabled) {
  background: #026d27;
}

.notification.is-danger.is-light {
  background: #fee;
  color: #c00;
  border-left: 4px solid #f14668;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
}
</style>