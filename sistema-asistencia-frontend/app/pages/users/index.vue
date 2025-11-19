<template>
  <div class="user-management">
    <!-- Header Section -->
    <section class="hero is-small" style="background: linear-gradient(135deg, #F0E491 0%, #BBC863 100%);">
      <div class="hero-body">
        <div class="container">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <h1 class="title is-2 has-text-dark">
                    <span class="icon-text">
                      <span class="icon has-text-dark">
                        <i class="mdi mdi-account-group mdi-36px"></i>
                      </span>
                      <span>Gestión de Usuarios</span>
                    </span>
                  </h1>
                  <p class="subtitle is-5 has-text-dark">
                    Administra los usuarios del sistema de la cooperativa
                  </p>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item" v-if="userStore.isCurrentUserSuperuser">
                <NuxtLink to="/users/new" class="button is-primary is-medium">
                  <span class="icon">
                    <i class="mdi mdi-account-plus"></i>
                  </span>
                  <span>Nuevo Usuario</span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filters Section -->
    <section class="section py-4" style="background: rgba(240, 228, 145, 0.1);">
      <div class="container">
        <div class="box" style="backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.9);">
          <div class="columns is-vcentered">
            <div class="column is-4">
              <div class="field">
                <label class="label has-text-dark">Buscar usuarios</label>
                <div class="control has-icons-left">
                  <input
                    v-model="searchQuery"
                    @input="handleSearch"
                    class="input"
                    type="text"
                    placeholder="Buscar por username, nombre o email..."
                  >
                  <span class="icon is-left">
                    <i class="mdi mdi-magnify"></i>
                  </span>
                </div>
              </div>
            </div>
            <div class="column is-3">
              <div class="field">
                <label class="label has-text-dark">Estado</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="filters.is_active" @change="applyFilters">
                      <option :value="null">Todos</option>
                      <option :value="true">Activos</option>
                      <option :value="false">Inactivos</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            <div class="column is-3">
              <div class="field">
                <label class="label has-text-dark">Tipo de usuario</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="filters.is_superuser" @change="applyFilters">
                      <option :value="null">Todos</option>
                      <option :value="true">Superadmin</option>
                      <option :value="false">Usuario básico</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            <div class="column is-2">
              <div class="field">
                <label class="label">&nbsp;</label>
                <div class="control">
                  <button @click="clearFilters" class="button is-light is-fullwidth">
                    <span class="icon">
                      <i class="mdi mdi-filter-remove"></i>
                    </span>
                    <span>Limpiar</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="section py-4">
      <div class="container">
        <div class="columns">
          <div class="column is-3">
            <div class="card" style="border-left: 4px solid #F0E491;">
              <div class="card-content">
                <div class="level">
                  <div class="level-left">
                    <div>
                      <p class="heading">Total de usuarios</p>
                      <p class="title is-3">{{ userStore.userStats.total }}</p>
                    </div>
                  </div>
                  <div class="level-right">
                    <span class="icon has-text-grey-light is-large">
                      <i class="mdi mdi-account-group mdi-48px"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-3">
            <div class="card" style="border-left: 4px solid #BBC863;">
              <div class="card-content">
                <div class="level">
                  <div class="level-left">
                    <div>
                      <p class="heading">Usuarios activos</p>
                      <p class="title is-3 has-text-success">{{ userStore.userStats.active }}</p>
                    </div>
                  </div>
                  <div class="level-right">
                    <span class="icon has-text-success is-large">
                      <i class="mdi mdi-account-check mdi-48px"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-3">
            <div class="card" style="border-left: 4px solid #658C58;">
              <div class="card-content">
                <div class="level">
                  <div class="level-left">
                    <div>
                      <p class="heading">Superadmins</p>
                      <p class="title is-3 has-text-warning">{{ userStore.userStats.superusers }}</p>
                    </div>
                  </div>
                  <div class="level-right">
                    <span class="icon has-text-warning is-large">
                      <i class="mdi mdi-account-star mdi-48px"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-3">
            <div class="card" style="border-left: 4px solid #31694E;">
              <div class="card-content">
                <div class="level">
                  <div class="level-left">
                    <div>
                      <p class="heading">Usuarios básicos</p>
                      <p class="title is-3 has-text-info">{{ userStore.userStats.basicUsers }}</p>
                    </div>
                  </div>
                  <div class="level-right">
                    <span class="icon has-text-info is-large">
                      <i class="mdi mdi-account mdi-48px"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Table Section -->
    <section class="section">
      <div class="container">
        <div class="box" style="backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.95);">
          <!-- Loading State -->
          <div v-if="userStore.loading" class="has-text-centered py-6">
            <div class="is-flex is-justify-content-center is-align-items-center">
              <div class="loader mr-3"></div>
              <span class="is-size-5">Cargando usuarios...</span>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="userStore.error" class="notification is-danger">
            <button @click="userStore.clearError" class="delete"></button>
            <strong>Error:</strong> {{ userStore.error }}
          </div>

          <!-- Data Table -->
          <div v-else>
            <div class="table-container">
              <table class="table is-fullwidth is-striped is-hoverable">
                <thead>
                  <tr style="background: linear-gradient(45deg, #F0E491, #BBC863);">
                    <th class="has-text-dark">Usuario</th>
                    <th class="has-text-dark">Email</th>
                    <th class="has-text-dark">Tipo</th>
                    <th class="has-text-dark">Estado</th>
                    <th class="has-text-dark">Último acceso</th>
                    <th class="has-text-dark">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredUsers.length === 0">
                    <td colspan="6" class="has-text-centered py-6">
                      <span class="icon is-large has-text-grey-light">
                        <i class="mdi mdi-account-search mdi-48px"></i>
                      </span>
                      <br>
                      <span class="is-size-5 has-text-grey">No se encontraron usuarios</span>
                    </td>
                  </tr>
                  <tr v-for="user in filteredUsers" :key="user.id">
                    <!-- Usuario Info -->
                    <td>
                      <div class="media">
                        <div class="media-left">
                          <span class="icon is-large" :class="{
                            'has-text-warning': user.is_superuser,
                            'has-text-info': !user.is_superuser
                          }">
                            <i class="mdi" :class="{
                              'mdi-account-star mdi-36px': user.is_superuser,
                              'mdi-account mdi-36px': !user.is_superuser
                            }"></i>
                          </span>
                        </div>
                        <div class="media-content">
                          <p class="is-size-6 has-text-weight-semibold">{{ user.username }}</p>
                          <p class="is-size-7 has-text-grey" v-if="user.full_name">{{ user.full_name }}</p>
                        </div>
                      </div>
                    </td>

                    <!-- Email -->
                    <td>
                      <span v-if="user.email" class="is-size-6">{{ user.email }}</span>
                      <span v-else class="has-text-grey-light is-italic">Sin email</span>
                    </td>

                    <!-- Tipo -->
                    <td>
                      <span class="tag" :class="{
                        'is-warning': user.is_superuser,
                        'is-info': !user.is_superuser
                      }">
                        <span class="icon">
                          <i class="mdi" :class="{
                            'mdi-star': user.is_superuser,
                            'mdi-account': !user.is_superuser
                          }"></i>
                        </span>
                        <span>{{ user.is_superuser ? 'Superadmin' : 'Usuario básico' }}</span>
                      </span>
                    </td>

                    <!-- Estado -->
                    <td>
                      <span class="tag" :class="{
                        'is-success': user.is_active,
                        'is-danger': !user.is_active
                      }">
                        <span class="icon">
                          <i class="mdi" :class="{
                            'mdi-check': user.is_active,
                            'mdi-close': !user.is_active
                          }"></i>
                        </span>
                        <span>{{ user.is_active ? 'Activo' : 'Inactivo' }}</span>
                      </span>
                    </td>

                    <!-- Último acceso -->
                    <td>
                      <span v-if="user.last_login" class="is-size-7">
                        {{ formatDateTime(user.last_login) }}
                      </span>
                      <span v-else class="has-text-grey-light is-italic">Nunca</span>
                    </td>

                    <!-- Acciones -->
                    <td>
                      <div class="buttons are-small">
                        <NuxtLink 
                          :to="`/users/edit/${user.id}`" 
                          class="button is-info"
                          v-if="userStore.isCurrentUserSuperuser || userStore.currentUser?.id === user.id">
                          <span class="icon">
                            <i class="mdi mdi-pencil"></i>
                          </span>
                          <span>Editar</span>
                        </NuxtLink>
                        
                        <button 
                          @click="confirmDelete(user)"
                          class="button is-danger"
                          v-if="userStore.isCurrentUserSuperuser && user.id !== userStore.currentUser?.id">
                          <span class="icon">
                            <i class="mdi mdi-delete"></i>
                          </span>
                          <span>Eliminar</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Delete Confirmation Modal -->
    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="showDeleteModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head" style="background: #F0E491;">
          <p class="modal-card-title has-text-dark">
            <span class="icon-text">
              <span class="icon">
                <i class="mdi mdi-alert-circle"></i>
              </span>
              <span>Confirmar eliminación</span>
            </span>
          </p>
          <button @click="showDeleteModal = false" class="delete" aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          <div class="content">
            <p class="is-size-5">
              ¿Estás seguro de que deseas eliminar al usuario 
              <strong>{{ userToDelete?.username }}</strong>?
            </p>
            <div class="notification is-warning is-light">
              <span class="icon">
                <i class="mdi mdi-alert"></i>
              </span>
              Esta acción no se puede deshacer.
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button @click="handleDelete" :disabled="userStore.loading" class="button is-danger">
            <span class="icon" v-if="userStore.loading">
              <div class="loader"></div>
            </span>
            <span class="icon" v-else>
              <i class="mdi mdi-delete"></i>
            </span>
            <span>Eliminar</span>
          </button>
          <button @click="showDeleteModal = false" class="button">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '~/stores/users'
import { useAuthStore } from '~/stores/auth'

// Meta tags
definePageMeta({
  middleware: ['auth'],
  layout: 'dashboard'
})

useHead({
  title: 'Gestión de Usuarios - Cooperativa Minera Poopó R.L.'
})

// Stores
const userStore = useUserStore()
const authStore = useAuthStore()

// Reactive data
const searchQuery = ref('')
const showDeleteModal = ref(false)
const userToDelete = ref(null)
const searchTimeout = ref(null)

// Filters
const filters = ref({
  is_active: null,
  is_superuser: null
})

// Computed
const filteredUsers = computed(() => userStore.filteredUsers)

// Methods
const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    userStore.updateFilters({ search: searchQuery.value })
  }, 300)
}

const applyFilters = () => {
  userStore.updateFilters(filters.value)
}

const clearFilters = () => {
  searchQuery.value = ''
  filters.value = {
    is_active: null,
    is_superuser: null
  }
  userStore.clearFilters()
}

const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!userToDelete.value) return

  const result = await userStore.deleteUser(userToDelete.value.id)
  
  if (result.success) {
    showDeleteModal.value = false
    userToDelete.value = null
    await useNuxtApp().$toast.success('Usuario eliminado exitosamente')
  } else {
    await useNuxtApp().$toast.error(result.error || 'Error al eliminar usuario')
  }
}

const formatDateTime = (dateTime) => {
  return new Intl.DateTimeFormat('es-BO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(dateTime))
}

// Lifecycle
onMounted(async () => {
  await userStore.fetchCurrentUser()
  await userStore.fetchUsers()
})
</script>

<style scoped>
.user-management {
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(240, 228, 145, 0.1) 0%, rgba(187, 200, 99, 0.1) 100%);
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #F0E491;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.table {
  border-radius: 8px;
  overflow: hidden;
}

.table thead th {
  border: none;
  font-weight: 600;
}

.table tbody tr:hover {
  background-color: rgba(240, 228, 145, 0.1);
}

.buttons .button {
  margin-right: 0.5rem;
}

.modal-card {
  border-radius: 12px;
}
</style>