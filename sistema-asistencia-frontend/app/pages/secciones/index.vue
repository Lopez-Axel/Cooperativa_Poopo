<template>
  <div class="secciones-page">
    
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="title is-2">
            <i class="mdi mdi-sitemap"></i>
            Gestión de Secciones
          </h1>
          <p class="subtitle">Administra las secciones de la cooperativa</p>
        </div>
        <div class="header-actions">
          <button 
            class="button is-warning"
            @click="generarReporteGlobal"
            :disabled="generandoPDF"
            title="Generar reporte PDF de todas las secciones"
          >
            <i class="mdi mdi-file-pdf-box"></i>
            <span>{{ generandoPDF ? 'Generando PDF...' : 'Generar PDF Global' }}</span>
          </button>
          <button 
            class="button is-primary"
            @click="openCreateModal"
          >
            <i class="mdi mdi-plus"></i>
            <span>Nueva Sección</span>
          </button>
        </div>
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
          placeholder="Buscar por nombre..."
          @input="handleSearch"
        >
      </div>
      
      <div class="filter-buttons">
        <div class="filter-group">
          <span class="filter-label">Estado:</span>
          <button 
            class="filter-btn"
            :class="{ 'active': seccionesStore.filters.is_active === null }"
            @click="setActiveFilter(null)"
          >
            Todos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': seccionesStore.filters.is_active === true }"
            @click="setActiveFilter(true)"
          >
            Activos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': seccionesStore.filters.is_active === false }"
            @click="setActiveFilter(false)"
          >
            Inactivos
          </button>
        </div>
        
        <button 
          class="button is-light is-small"
          @click="resetFilters"
          v-if="seccionesStore.hasActiveFilters"
        >
          <i class="mdi mdi-filter-remove"></i>
          Limpiar
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="seccionesStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando secciones...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="seccionesStore.error" class="notification is-danger">
      <i class="mdi mdi-alert-circle"></i>
      {{ seccionesStore.error }}
    </div>
    
    <!-- Secciones Table -->
    <div v-else class="table-container">
      <table class="table is-fullwidth is-hoverable">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Delegado</th>
            <th>Estado</th>
            <th class="has-text-centered">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="seccionesStore.seccionesFiltradas.length === 0">
            <td colspan="5" class="has-text-centered empty-state">
              <i class="mdi mdi-folder-open"></i>
              <p>No se encontraron secciones</p>
            </td>
          </tr>
          <tr v-for="seccion in seccionesStore.seccionesFiltradas" :key="seccion.id">
            <td>
              <strong>{{ seccion.nombre }}</strong>
            </td>
            <td>{{ seccion.descripcion || '-' }}</td>
            <td>
              <span 
                v-if="seccion.id_delegado" 
                class="tag is-info is-light"
              >
                <i class="mdi mdi-account-star"></i>
                Asignado
              </span>
              <span v-else class="tag is-warning is-light">
                <i class="mdi mdi-account-off"></i>
                Sin asignar
              </span>
            </td>
            <td>
              <span class="tag" :class="seccion.is_active ? 'is-success' : 'is-danger'">
                {{ seccion.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="has-text-centered">
              <div class="action-buttons">
                <button 
                  class="button is-small is-link"
                  @click="openViewModal(seccion.id)"
                  title="Ver detalles"
                >
                  <i class="mdi mdi-eye"></i>
                </button>
                <button 
                  class="button is-small is-warning"
                  @click="generarReporteIndividual(seccion.id)"
                  :disabled="generandoPDF"
                  title="Generar PDF de esta sección"
                >
                  <i class="mdi mdi-file-pdf-box"></i>
                </button>
                <button 
                  class="button is-small is-info"
                  @click="openEditModal(seccion)"
                  title="Editar sección"
                >
                  <i class="mdi mdi-pencil"></i>
                </button>
                <button 
                  v-if="seccion.is_active"
                  class="button is-small is-danger"
                  @click="confirmDelete(seccion)"
                  title="Desactivar sección"
                >
                  <i class="mdi mdi-delete"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Modals -->
    <ModalVerDetalles
    :is-open="modalVerAbierto"
    :detalles="seccionDetalles"
    @close="closeViewModal"
    />

    <ModalFormulario
    :is-open="modalFormAbierto"
    :es-edicion="esEdicion"
    :datos-iniciales="datosFormulario"
    :cooperativistas="cooperativistasActivos"
    :cargando="seccionesStore.loading"
    @close="closeFormModal"
    @guardar="handleGuardar"
    />

    <ModalConfirmarEliminacion
    :is-open="modalEliminarAbierto"
    :seccion="seccionParaEliminar"
    :cargando="seccionesStore.loading"
    @close="closeDeleteModal"
    @confirmar="handleEliminar"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSeccionesStore } from '~/stores/secciones'
import { useAuthStore } from '~/stores/auth'
import { useCuadrillasStore } from '~/stores/cuadrillas'
import { useCooperativistasStore } from '~/stores/cooperativistas'
import ModalVerDetalles from '~/components/secciones/ModalVerDetalles.vue'
import ModalFormulario from '~/components/secciones/ModalFormulario.vue'
import ModalConfirmarEliminacion from '~/components/secciones/ModalConfirmarEliminacion.vue'
import { generarReporteSecciones, generarReporteIndividualSeccion } from '~/utils/reporteSecciones'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const seccionesStore = useSeccionesStore()
const authStore = useAuthStore()
const cuadrillasStore = useCuadrillasStore()
const cooperativistasStore = useCooperativistasStore()

// Estados de modales
const modalVerAbierto = ref(false)
const modalFormAbierto = ref(false)
const modalEliminarAbierto = ref(false)

const esEdicion = ref(false)
const seccionDetalles = ref(null)
const seccionParaEliminar = ref(null)
const datosFormulario = ref({
  nombre: '',
  descripcion: '',
  id_delegado: null
})

const searchQuery = ref('')
const cooperativistasActivos = ref([])
const generandoPDF = ref(false)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    await authStore.initFromStorage()
  }
  await seccionesStore.fetchSecciones()
  await cuadrillasStore.fetchCuadrillas()
  await cooperativistasStore.cargarCooperativistas()
  cooperativistasActivos.value = await seccionesStore.fetchCooperativistasActivos()
})

const handleSearch = () => {
  seccionesStore.setSearchQuery(searchQuery.value)
}

const setActiveFilter = (value) => {
  seccionesStore.setActiveFilter(value)
}

const resetFilters = () => {
  searchQuery.value = ''
  seccionesStore.resetFilters()
}

// Función para cargar detalles completos de una sección con cuadrillas y cooperativistas
const cargarDetallesCompletos = async (seccionId) => {
  try {
    const detalles = await seccionesStore.getSeccionDetails(seccionId)
    
    // Obtener cuadrillas de esta sección
    const cuadrillasDeLaSeccion = cuadrillasStore.cuadrillas.filter(
      c => c.id_seccion === seccionId && c.is_active
    )
    
    // Para cada cuadrilla, obtener sus cooperativistas
    const cuadrillasConCooperativistas = cuadrillasDeLaSeccion.map(cuadrilla => {
      const cooperativistasDeCuadrilla = cooperativistasStore.cooperativistas.filter(
        coop => coop.id_cuadrilla === cuadrilla.id && coop.is_active
      )
      
      return {
        ...cuadrilla,
        cooperativistas: cooperativistasDeCuadrilla
      }
    })
    
    return {
      ...detalles,
      cuadrillas: cuadrillasConCooperativistas,
      total_cuadrillas: cuadrillasConCooperativistas.length,
      total_cooperativistas: cuadrillasConCooperativistas.reduce(
        (sum, c) => sum + c.cooperativistas.length, 0
      )
    }
  } catch (error) {
    console.error('Error cargando detalles completos:', error)
    throw error
  }
}

// Generar reporte global de todas las secciones
const generarReporteGlobal = async () => {
  generandoPDF.value = true
  try {
    // Obtener todas las secciones activas
    const seccionesActivas = seccionesStore.secciones.filter(s => s.is_active)
    
    // Cargar detalles completos de cada sección
    const seccionesConDetalles = await Promise.all(
      seccionesActivas.map(async (seccion) => {
        return await cargarDetallesCompletos(seccion.id)
      })
    )
    
    // Generar el PDF
    await generarReporteSecciones(seccionesConDetalles)
  } catch (error) {
    console.error('Error generando reporte global:', error)
    alert('Error al generar el reporte PDF. Por favor, intente nuevamente.')
  } finally {
    generandoPDF.value = false
  }
}

// Generar reporte individual de una sección
const generarReporteIndividual = async (seccionId) => {
  generandoPDF.value = true
  try {
    const detallesCompletos = await cargarDetallesCompletos(seccionId)
    await generarReporteIndividualSeccion(detallesCompletos)
  } catch (error) {
    console.error('Error generando reporte individual:', error)
    alert('Error al generar el reporte PDF. Por favor, intente nuevamente.')
  } finally {
    generandoPDF.value = false
  }
}

// Modal Ver Detalles
const openViewModal = async (seccionId) => {
  try {
    seccionDetalles.value = await seccionesStore.getSeccionDetails(seccionId)
    modalVerAbierto.value = true
  } catch (error) {
    console.error('Error al cargar detalles:', error)
  }
}

const closeViewModal = () => {
  modalVerAbierto.value = false
  seccionDetalles.value = null
}

// Modal Formulario
const openCreateModal = () => {
  esEdicion.value = false
  datosFormulario.value = {
    nombre: '',
    descripcion: '',
    id_delegado: null
  }
  modalFormAbierto.value = true
}

const openEditModal = (seccion) => {
  esEdicion.value = true
  datosFormulario.value = {
    nombre: seccion.nombre,
    descripcion: seccion.descripcion || '',
    id_delegado: seccion.id_delegado
  }
  modalFormAbierto.value = true
}

const closeFormModal = () => {
  modalFormAbierto.value = false
  datosFormulario.value = {
    nombre: '',
    descripcion: '',
    id_delegado: null
  }
}

const handleGuardar = async (datos) => {
  try {
    if (esEdicion.value) {
      // Necesitamos el ID de la sección que se está editando
      const seccionEditando = seccionesStore.secciones.find(
        s => s.nombre === datosFormulario.value.nombre
      )
      await seccionesStore.updateSeccion(seccionEditando.id, datos)
    } else {
      await seccionesStore.createSeccion(datos)
    }
    
    closeFormModal()
    await seccionesStore.fetchSecciones()
  } catch (error) {
    console.error('Error:', error)
  }
}

// Modal Eliminar
const confirmDelete = (seccion) => {
  seccionParaEliminar.value = seccion
  modalEliminarAbierto.value = true
}

const closeDeleteModal = () => {
  modalEliminarAbierto.value = false
  seccionParaEliminar.value = null
}

const handleEliminar = async () => {
  try {
    await seccionesStore.deleteSeccion(seccionParaEliminar.value.id)
    closeDeleteModal()
    await seccionesStore.fetchSecciones()
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
.secciones-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.2), rgba(30, 70, 30, 0.3));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.header-text .title {
  color: #ffd700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.header-text .title i {
  font-size: 2.5rem;
  color: #038730;
  text-shadow: 0 0 20px rgba(3, 135, 48, 0.6);
}

.header-text .subtitle {
  color: #c8e6c9;
  font-size: 1.1rem;
  margin-bottom: 0;
  font-weight: 500;
}

.button.is-primary,
.button.is-warning {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  border: none;
  color: #0d1b0d;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.button.is-primary:hover:not(:disabled),
.button.is-warning:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.button.is-primary:disabled,
.button.is-warning:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.filters-section {
  background: rgba(15, 31, 15, 0.6);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
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
  background: rgba(26, 46, 26, 0.6);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #e0f2f1;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.search-box .input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.search-box .input::placeholder {
  color: #90a4ae;
}

.filter-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.filter-label {
  color: #c8e6c9;
  font-weight: 700;
  font-size: 0.9rem;
}

.filter-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.9rem;
}

.filter-btn:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: #ffd700;
}

.filter-btn.active {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border-color: #ffd700;
  box-shadow: 0 2px 10px rgba(255, 215, 0, 0.4);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.loader {
  border: 4px solid rgba(255, 215, 0, 0.2);
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

.table-container {
  background: rgba(15, 31, 15, 0.6);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  overflow: hidden;
}

.table {
  width: 100%;
  background: transparent;
  color: #e0f2f1;
}

.table thead tr {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.4), rgba(30, 70, 30, 0.4));
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.table thead th {
  color: #ffd700;
  font-weight: 800;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  padding: 1rem;
  border: none;
}

.table tbody tr {
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
  transition: all 0.3s ease;
}

.table tbody tr:hover {
  background: rgba(255, 215, 0, 0.1);
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
  border: none;
  color: #e0f2f1;
}

.empty-state {
  padding: 4rem 2rem;
  color: #90a4ae;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-state i {
  font-size: 4rem;
  color: rgba(255, 215, 0, 0.3);
}

.tag {
  font-weight: 700;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
}

.tag.is-success {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.3), rgba(56, 142, 60, 0.3));
  color: #c8e6c9;
  border: 1px solid rgba(76, 175, 80, 0.5);
}

.tag.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(211, 47, 47, 0.3));
  color: #ffcdd2;
  border: 1px solid rgba(244, 67, 54, 0.5);
}

.tag.is-info {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.3), rgba(21, 101, 192, 0.3));
  color: #bbdefb;
  border: 1px solid rgba(33, 150, 243, 0.5);
}

.tag.is-warning {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.3), rgba(245, 124, 0, 0.3));
  color: #ffe0b2;
  border: 1px solid rgba(255, 152, 0, 0.5);
}

.tag.is-light {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.button.is-small {
  padding: 0.5rem;
  height: auto;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.button.is-small.is-link {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.3), rgba(21, 101, 192, 0.3));
  color: #bbdefb;
  border-color: rgba(33, 150, 243, 0.5);
}

.button.is-small.is-link:hover {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.5), rgba(21, 101, 192, 0.5));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
}

.button.is-small.is-warning {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.3), rgba(245, 124, 0, 0.3));
  color: #ffe0b2;
  border-color: rgba(255, 152, 0, 0.5);
}

.button.is-small.is-warning:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.5), rgba(245, 124, 0, 0.5));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
}

.button.is-small.is-info {
  background: linear-gradient(135deg, rgba(0, 188, 212, 0.3), rgba(0, 151, 167, 0.3));
  color: #b2ebf2;
  border-color: rgba(0, 188, 212, 0.5);
}

.button.is-small.is-info:hover {
  background: linear-gradient(135deg, rgba(0, 188, 212, 0.5), rgba(0, 151, 167, 0.5));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 188, 212, 0.4);
}

.button.is-small.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(211, 47, 47, 0.3));
  color: #ffcdd2;
  border-color: rgba(244, 67, 54, 0.5);
}

.button.is-small.is-danger:hover {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.5), rgba(211, 47, 47, 0.5));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
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
  .secciones-page {
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

  .header-actions {
    flex-direction: column;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>