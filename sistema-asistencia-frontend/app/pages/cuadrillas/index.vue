<template>
  <div class="cuadrillas-page">
    
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="title is-2">
            <i class="mdi mdi-folder-multiple"></i>
            Gestión de Cuadrillas
          </h1>
          <p class="subtitle">Administra las cuadrillas organizadas por sección</p>
        </div>
        <div class="header-buttons">
          <button 
            class="button is-warning"
            @click="generarReportePDF"
            :disabled="generandoPDF || cuadrillasStore.cuadrillasFiltradas.length === 0"
            :class="{ 'is-loading': generandoPDF }"
          >
            <i class="mdi mdi-file-pdf-box"></i>
            <span>Generar PDF</span>
          </button>
          <button 
            class="button is-primary"
            @click="openCreateModal"
          >
            <i class="mdi mdi-plus"></i>
            <span>Nueva Cuadrilla</span>
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
          placeholder="Buscar por nombre de cuadrilla..."
          @input="handleSearch"
        >
      </div>
      
      <div class="filter-buttons">
        <div class="filter-group">
          <span class="filter-label">Estado:</span>
          <button 
            class="filter-btn"
            :class="{ 'active': cuadrillasStore.filters.is_active === null }"
            @click="setActiveFilter(null)"
          >
            Todos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': cuadrillasStore.filters.is_active === true }"
            @click="setActiveFilter(true)"
          >
            Activos
          </button>
          <button 
            class="filter-btn"
            :class="{ 'active': cuadrillasStore.filters.is_active === false }"
            @click="setActiveFilter(false)"
          >
            Inactivos
          </button>
        </div>

        <div class="filter-group">
          <span class="filter-label">Sección:</span>
          <div class="control has-icons-left">
            <div class="select">
              <select 
                :value="cuadrillasStore.filters.seccion_id" 
                @change="setSeccionFilter($event.target.value === '' ? null : parseInt($event.target.value))"
              >
                <option value="">Todas las secciones</option>
                <option 
                  v-for="seccion in seccionesActivas" 
                  :key="seccion.id"
                  :value="seccion.id"
                >
                  {{ seccion.nombre }}
                </option>
              </select>
            </div>
            <span class="icon is-left">
              <i class="mdi mdi-sitemap"></i>
            </span>
          </div>
        </div>
        
        <button 
          class="button is-light is-small"
          @click="resetFilters"
          v-if="cuadrillasStore.hasActiveFilters"
        >
          <i class="mdi mdi-filter-remove"></i>
          Limpiar
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="cuadrillasStore.loading" class="loading-container">
      <div class="loader"></div>
      <p>Cargando cuadrillas...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="cuadrillasStore.error" class="notification is-danger">
      <i class="mdi mdi-alert-circle"></i>
      {{ cuadrillasStore.error }}
    </div>
    
    <!-- Cuadrillas agrupadas por sección -->
    <div v-else>
      <div 
        v-for="grupo in gruposFiltrados" 
        :key="grupo.seccion.id"
        class="seccion-grupo"
      >
        <div class="seccion-header">
          <h2 class="seccion-titulo">
            <i class="mdi mdi-sitemap"></i>
            {{ grupo.seccion.nombre }}
          </h2>
          <span class="seccion-count">
            {{ grupo.cuadrillas.length }} cuadrilla{{ grupo.cuadrillas.length !== 1 ? 's' : '' }}
          </span>
        </div>

        <div class="table-container">
          <table class="table is-fullwidth is-hoverable">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Estado</th>
                <th class="has-text-centered">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="grupo.cuadrillas.length === 0">
                <td colspan="4" class="has-text-centered empty-state-small">
                  <i class="mdi mdi-folder-open"></i>
                  <p>No hay cuadrillas en esta sección</p>
                </td>
              </tr>
              <tr v-for="cuadrilla in grupo.cuadrillas" :key="cuadrilla.id">
                <td>
                  <strong>{{ cuadrilla.nombre }}</strong>
                </td>
                <td>
                  <span class="tag" :class="cuadrilla.is_active ? 'is-success' : 'is-danger'">
                    {{ cuadrilla.is_active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="has-text-centered">
                  <div class="action-buttons">
                    <button 
                      class="button is-small is-link"
                      @click="openViewModal(cuadrilla.id)"
                      title="Ver detalles"
                    >
                      <i class="mdi mdi-eye"></i>
                    </button>
                    <button 
                      class="button is-small is-warning"
                      @click="generarReporteIndividual(cuadrilla.id)"
                      title="Generar PDF"
                      :disabled="generandoPDFIndividual === cuadrilla.id"
                      :class="{ 'is-loading': generandoPDFIndividual === cuadrilla.id }"
                    >
                      <i class="mdi mdi-file-pdf-box"></i>
                    </button>
                    <button 
                      class="button is-small is-info"
                      @click="openEditModal(cuadrilla)"
                      title="Editar cuadrilla"
                    >
                      <i class="mdi mdi-pencil"></i>
                    </button>
                    <button 
                      v-if="cuadrilla.is_active"
                      class="button is-small is-danger"
                      @click="confirmDelete(cuadrilla)"
                      title="Desactivar cuadrilla"
                    >
                      <i class="mdi mdi-delete"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Estado vacío global -->
      <div v-if="gruposFiltrados.length === 0" class="empty-state">
        <i class="mdi mdi-folder-open"></i>
        <p>No se encontraron cuadrillas</p>
      </div>
    </div>
    
    <!-- Componentes de Modales -->
    <ModalVerDetalles
      :is-open="modalVerAbierto"
      :detalles="cuadrillaDetalles"
      @close="closeViewModal"
    />

    <ModalFormulario
      :is-open="modalFormAbierto"
      :es-edicion="esEdicion"
      :datos-iniciales="datosFormulario"
      :secciones="seccionesActivas"
      :cargando="cuadrillasStore.loading"
      @close="closeFormModal"
      @guardar="handleGuardar"
    />

    <ModalConfirmarEliminacion
      :is-open="modalEliminarAbierto"
      :cuadrilla="cuadrillaParaEliminar"
      :cargando="cuadrillasStore.loading"
      @close="closeDeleteModal"
      @confirmar="handleEliminar"
    />
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCuadrillasStore } from '~/stores/cuadrillas'
import ModalVerDetalles from '~/components/cuadrillas/ModalVerDetalles.vue'
import ModalFormulario from '~/components/cuadrillas/ModalFormulario.vue'
import ModalConfirmarEliminacion from '~/components/cuadrillas/ModalConfirmarEliminacion.vue'
import { generarReporteCuadrillas, generarReporteCuadrillaPorSeccion, generarReporteIndividualCuadrilla } from '~/utils/reporteCuadrillas'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const cuadrillasStore = useCuadrillasStore()

// Estados de modales
const modalVerAbierto = ref(false)
const modalFormAbierto = ref(false)
const modalEliminarAbierto = ref(false)

const esEdicion = ref(false)
const cuadrillaDetalles = ref(null)
const cuadrillaParaEliminar = ref(null)
const cuadrillaEditando = ref(null)
const datosFormulario = ref({
  nombre: '',
  id_seccion: null
})

const searchQuery = ref('')
const generandoPDF = ref(false)
const generandoPDFIndividual = ref(null) // Para tracking de cuál PDF se está generando


onMounted(async () => {
  await cuadrillasStore.fetchSecciones()
  await cuadrillasStore.fetchCuadrillas()
})

const seccionesActivas = computed(() => {
  return cuadrillasStore.secciones.filter(s => s.is_active)
})

const gruposFiltrados = computed(() => {
  const grupos = cuadrillasStore.cuadrillasAgrupadasPorSeccion
  const cuadrillasFiltradas = cuadrillasStore.cuadrillasFiltradas
  
  return grupos
    .map(grupo => ({
      seccion: grupo.seccion,
      cuadrillas: grupo.cuadrillas.filter(c => 
        cuadrillasFiltradas.some(cf => cf.id === c.id)
      )
    }))
    .filter(grupo => grupo.cuadrillas.length > 0)
})

const handleSearch = () => {
  cuadrillasStore.setSearchQuery(searchQuery.value)
}

const setActiveFilter = (value) => {
  cuadrillasStore.setActiveFilter(value)
}

const setSeccionFilter = (value) => {
  cuadrillasStore.setSeccionFilter(value)
}

const resetFilters = () => {
  searchQuery.value = ''
  cuadrillasStore.resetFilters()
}

// Generar reporte PDF
const generarReportePDF = async () => {
  generandoPDF.value = true
  
  try {
    // Obtener detalles de todas las cuadrillas filtradas
    const cuadrillasFiltradas = cuadrillasStore.cuadrillasFiltradas
    const detallesPromesas = cuadrillasFiltradas.map(c => 
      cuadrillasStore.getCuadrillaDetails(c.id)
    )
    
    const cuadrillasConDetalles = await Promise.all(detallesPromesas)
    
    // Si hay filtro de sección, usar nombre específico
    if (cuadrillasStore.filters.seccion_id) {
      const seccion = cuadrillasStore.secciones.find(
        s => s.id === cuadrillasStore.filters.seccion_id
      )
      await generarReporteCuadrillaPorSeccion(seccion.nombre, cuadrillasConDetalles)
    } else {
      await generarReporteCuadrillas(cuadrillasConDetalles)
    }
  } catch (error) {
    console.error('Error al generar PDF:', error)
    alert('Error al generar el reporte PDF')
  } finally {
    generandoPDF.value = false
  }
}

// Modal Ver Detalles
const openViewModal = async (cuadrillaId) => {
  try {
    cuadrillaDetalles.value = await cuadrillasStore.getCuadrillaDetails(cuadrillaId)
    modalVerAbierto.value = true
  } catch (error) {
    console.error('Error al cargar detalles:', error)
  }
}

const closeViewModal = () => {
  modalVerAbierto.value = false
  cuadrillaDetalles.value = null
}

// Modal Formulario
const openCreateModal = () => {
  esEdicion.value = false
  cuadrillaEditando.value = null
  datosFormulario.value = {
    nombre: '',
    id_seccion: null
  }
  modalFormAbierto.value = true
}

const openEditModal = (cuadrilla) => {
  esEdicion.value = true
  cuadrillaEditando.value = cuadrilla
  datosFormulario.value = {
    nombre: cuadrilla.nombre,
    id_seccion: cuadrilla.id_seccion
  }
  modalFormAbierto.value = true
}

const closeFormModal = () => {
  modalFormAbierto.value = false
  datosFormulario.value = {
    nombre: '',
    id_seccion: null
  }
}

const handleGuardar = async (datos) => {
  try {
    if (esEdicion.value) {
      await cuadrillasStore.updateCuadrilla(cuadrillaEditando.value.id, datos)
    } else {
      await cuadrillasStore.createCuadrilla(datos)
    }
    
    closeFormModal()
    await cuadrillasStore.fetchCuadrillas()
  } catch (error) {
    console.error('Error:', error)
  }
}

// Modal Eliminar
const confirmDelete = (cuadrilla) => {
  cuadrillaParaEliminar.value = cuadrilla
  modalEliminarAbierto.value = true
}

const closeDeleteModal = () => {
  modalEliminarAbierto.value = false
  cuadrillaParaEliminar.value = null
}

const handleEliminar = async () => {
  try {
    await cuadrillasStore.deleteCuadrilla(cuadrillaParaEliminar.value.id)
    closeDeleteModal()
    await cuadrillasStore.fetchCuadrillas()
  } catch (error) {
    console.error('Error:', error)
  }
}

const generarReporteIndividual = async (cuadrillaId) => {
  generandoPDFIndividual.value = cuadrillaId
  
  try {
    const detalle = await cuadrillasStore.getCuadrillaDetails(cuadrillaId)
    await generarReporteIndividualCuadrilla(detalle)
  } catch (error) {
    console.error('Error al generar PDF individual:', error)
    alert('Error al generar el reporte PDF')
  } finally {
    generandoPDFIndividual.value = null
  }
}
</script>

<style scoped>
.cuadrillas-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a1f0a 0%, #0d1b0d 50%, #1a2e1a 100%);
  padding: 2rem;
  color: #e0f2f1;
  margin: -1.5rem;
}

.page-header {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.3), rgba(30, 70, 30, 0.3));
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.header-text .title {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.header-text .subtitle {
  color: #c8e6c9;
  font-size: 1rem;
  margin: 0;
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
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
}

.button.is-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
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
  flex-wrap: wrap;
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

.button.is-small.is-warning:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.seccion-grupo {
  margin-bottom: 2rem;
}

.seccion-header {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.4), rgba(30, 70, 30, 0.4));
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px 12px 0 0;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.seccion-titulo {
  color: #ffd700;
  font-size: 1.25rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.seccion-count {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.9rem;
}

.table-container {
  background: rgba(15, 31, 15, 0.6);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-top: none;
  border-radius: 0 0 12px 12px;
  overflow: hidden;
}

.table {
  width: 100%;
  background: transparent;
  color: #e0f2f1;
}

.table thead tr {
  background: linear-gradient(135deg, rgba(3, 135, 48, 0.3), rgba(30, 70, 30, 0.3));
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
  background: rgba(15, 31, 15, 0.6);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
}

.empty-state i {
  font-size: 4rem;
  color: rgba(255, 215, 0, 0.3);
}

.empty-state-small {
  padding: 2rem;
  color: #90a4ae;
  text-align: center;
}

.empty-state-small i {
  font-size: 2rem;
  color: rgba(255, 215, 0, 0.3);
  display: block;
  margin-bottom: 0.5rem;
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

.cooperativistas-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #90a4ae;
  font-size: 0.9rem;
}

.cooperativistas-badge i {
  color: #64b5f6;
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

.header-buttons {
  display: flex;
  gap: 0.75rem;
}

.button.is-warning {
  background: linear-gradient(135deg, #ff9800 0%, #ff6f00 50%, #f57c00 100%);
  color: #fff;
  border: none;
  font-weight: 800;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px rgba(255, 152, 0, 0.4);
  transition: all 0.3s ease;
}

.button.is-warning:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff9800 0%, #ff6f00 60%, #f57c00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 152, 0, 0.6);
}

.button.is-warning:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.filter-group .select {
  position: relative;
}

.filter-group .select select {
  background: rgba(15, 31, 15, 0.7);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #e0f2f1;
  padding: 0.5rem 2.5rem 0.5rem 2.5rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
}

.filter-group .select select:focus {
  border-color: #ffd700;
  outline: none;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
}

.filter-group .select::after {
  border: 2px solid #ffd700;
  border-right: 0;
  border-top: 0;
  content: " ";
  display: block;
  height: 0.5em;
  width: 0.5em;
  pointer-events: none;
  position: absolute;
  top: 50%;
  transform: rotate(-45deg);
  transform-origin: center;
  margin-top: -0.375em;
  right: 1.125em;
  z-index: 4;
}

.filter-group .control {
  position: relative;
}

.filter-group .icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
  pointer-events: none;
  z-index: 1;
}

@media screen and (max-width: 1023px) {
  .cuadrillas-page {
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
}
</style>