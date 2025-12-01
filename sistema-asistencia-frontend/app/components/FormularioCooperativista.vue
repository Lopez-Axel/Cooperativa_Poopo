<!-- components/FormularioCooperativista.vue -->
<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      
      <!-- Información Básica -->
      <div class="section-title">Información Personal</div>
      
      <div class="columns">
        <div class="column">
          <div class="field">
            <label class="label">Apellido Paterno *</label>
            <div class="control">
              <input 
                v-model="formData.apellido_paterno" 
                class="input" 
                type="text" 
                required
              />
            </div>
          </div>
        </div>
        
        <div class="column">
          <div class="field">
            <label class="label">Apellido Materno</label>
            <div class="control">
              <input 
                v-model="formData.apellido_materno" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column">
          <div class="field">
            <label class="label">Nombres *</label>
            <div class="control">
              <input 
                v-model="formData.nombres" 
                class="input" 
                type="text" 
                required
              />
            </div>
          </div>
        </div>
      </div>
      
      <div class="columns">
        <div class="column is-4">
          <div class="field">
            <label class="label">CI</label>
            <div class="control">
              <input 
                v-model="formData.ci" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-2">
          <div class="field">
            <label class="label">Expedido</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formData.ci_expedido">
                  <option value="">-</option>
                  <option value="LP">LP</option>
                  <option value="OR">OR</option>
                  <option value="CB">CB</option>
                  <option value="SC">SC</option>
                  <option value="PT">PT</option>
                  <option value="TJ">TJ</option>
                  <option value="CH">CH</option>
                  <option value="BN">BN</option>
                  <option value="PD">PD</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <div class="column is-3">
          <div class="field">
            <label class="label">Fecha Nacimiento</label>
            <div class="control">
              <input 
                v-model="formData.fecha_nacimiento" 
                class="input" 
                type="date"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-3">
          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input 
                v-model="formData.email" 
                class="input" 
                type="email"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Documentos -->
      <div class="section-title">Documentos</div>
      
      <div class="columns">
        <div class="column">
          <div class="field">
            <label class="label">Foto de CI</label>
            <div class="file-upload-zone">
              <div v-if="formData.ci_foto_url" class="preview-container">
                <img :src="formData.ci_foto_url" alt="CI" class="preview-image" />
                <button 
                  type="button" 
                  class="button is-danger is-small delete-btn"
                  @click="eliminarCIFoto"
                >
                  <i class="mdi mdi-delete"></i> Eliminar
                </button>
              </div>
              <div v-else class="upload-box">
                <input 
                  ref="ciFileInput"
                  type="file" 
                  accept="image/jpeg,image/jpg,image/png,image/webp"
                  @change="handleCIFileChange"
                  style="display: none"
                />
                <button 
                  type="button" 
                  class="button is-light"
                  @click="$refs.ciFileInput.click()"
                >
                  <i class="mdi mdi-upload"></i> Seleccionar Imagen
                </button>
                <p class="help">JPG, PNG, WEBP (máx 10MB)</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="column">
          <div class="field">
            <label class="label">Documento ABC</label>
            <div class="file-upload-zone">
              <div v-if="formData.documento_abc_url" class="preview-container">
                <a :href="formData.documento_abc_url" target="_blank" class="document-link">
                  <i class="mdi mdi-file-document"></i> Ver documento
                </a>
                <button 
                  type="button" 
                  class="button is-danger is-small delete-btn"
                  @click="eliminarDocumentoABC"
                >
                  <i class="mdi mdi-delete"></i> Eliminar
                </button>
              </div>
              <div v-else class="upload-box">
                <input 
                  ref="abcFileInput"
                  type="file" 
                  accept="application/pdf,image/jpeg,image/jpg,image/png"
                  @change="handleABCFileChange"
                  style="display: none"
                />
                <button 
                  type="button" 
                  class="button is-light"
                  @click="$refs.abcFileInput.click()"
                >
                  <i class="mdi mdi-upload"></i> Seleccionar Archivo
                </button>
                <p class="help">PDF o Imagen (máx 20MB)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Información Laboral -->
      <div class="section-title">Información Laboral</div>
      
      <div class="columns">
        <div class="column is-3">
          <div class="field">
            <label class="label">Sección</label>
            <div class="control">
              <input 
                v-model="formData.seccion" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-3">
          <div class="field">
            <label class="label">Cuadrilla</label>
            <div class="control">
              <input 
                v-model="formData.cuadrilla" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-3">
          <div class="field">
            <label class="label">Jefe de Cuadrilla</label>
            <div class="control">
              <input 
                v-model="formData.jefe_cuadrilla" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-3">
          <div class="field">
            <label class="label">Delegado Sección</label>
            <div class="control">
              <input 
                v-model="formData.delegado_seccion" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
      </div>
      
      <div class="columns">
        <div class="column is-4">
          <div class="field">
            <label class="label">Ocupación</label>
            <div class="control">
              <input 
                v-model="formData.ocupacion" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-4">
          <div class="field">
            <label class="label">Código Asegurado</label>
            <div class="control">
              <input 
                v-model="formData.codigo_asegurado" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-4">
          <div class="field">
            <label class="label">CUA</label>
            <div class="control">
              <input 
                v-model="formData.cua" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
      </div>
      
      <div class="columns">
        <div class="column is-4">
          <div class="field">
            <label class="label">Estado Asegurado</label>
            <div class="control">
              <input 
                v-model="formData.estado_asegurado" 
                class="input" 
                type="text"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-4">
          <div class="field">
            <label class="label">Fecha Ingreso</label>
            <div class="control">
              <input 
                v-model="formData.fecha_ingreso" 
                class="input" 
                type="date"
              />
            </div>
          </div>
        </div>
        
        <div class="column is-4">
          <div class="field">
            <label class="label">Estado</label>
            <div class="control">
              <label class="checkbox">
                <input type="checkbox" v-model="formData.is_active" />
                Activo
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="!formData.is_active" class="columns">
        <div class="column is-8">
          <div class="field">
            <label class="label">Motivo de Baja</label>
            <div class="control">
              <textarea 
                v-model="formData.motivo_baja" 
                class="textarea" 
                rows="2"
              ></textarea>
            </div>
          </div>
        </div>
        
        <div class="column is-4">
          <div class="field">
            <label class="label">Fecha de Baja</label>
            <div class="control">
              <input 
                v-model="formData.fecha_baja" 
                class="input" 
                type="date"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Botones -->
      <div class="buttons-container">
        <button 
          type="button" 
          class="button is-light" 
          @click="$emit('cancel')"
          :disabled="loading"
        >
          Cancelar
        </button>
        <button 
          type="submit" 
          class="button is-primary" 
          :class="{ 'is-loading': loading }"
          :disabled="loading"
        >
          {{ isEdit ? 'Actualizar' : 'Crear' }} Cooperativista
        </button>
      </div>
      
    </form>
  </div>
</template>

<script setup>
const props = defineProps({
  cooperativista: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const authStore = useAuthStore()
const loading = ref(false)
const ciFileInput = ref(null)
const abcFileInput = ref(null)

const isEdit = computed(() => !!props.cooperativista)

const formData = ref({
  apellido_paterno: '',
  apellido_materno: '',
  nombres: '',
  ci: '',
  ci_expedido: '',
  ci_foto_url: '',
  documento_abc_url: '',
  fecha_nacimiento: '',
  email: '',
  seccion: '',
  cuadrilla: '',
  jefe_cuadrilla: '',
  delegado_seccion: '',
  ocupacion: '',
  codigo_asegurado: '',
  cua: '',
  estado_asegurado: '',
  fecha_ingreso: '',
  is_active: true,
  motivo_baja: '',
  fecha_baja: ''
})

// Cargar datos si es edición
if (props.cooperativista) {
  Object.assign(formData.value, props.cooperativista)
}

const handleCIFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validar tamaño
  if (file.size > 10 * 1024 * 1024) {
    alert('La imagen es muy pesada (máximo 10MB)')
    return
  }
  
  // Si es nuevo cooperativista, esperar a que se cree primero
  if (!isEdit.value) {
    alert('Primero debes crear el cooperativista antes de subir archivos')
    return
  }
  
  await subirArchivo(file, 'ci-foto')
}

const handleABCFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validar tamaño
  if (file.size > 20 * 1024 * 1024) {
    alert('El archivo es muy pesado (máximo 20MB)')
    return
  }
  
  // Si es nuevo cooperativista, esperar a que se cree primero
  if (!isEdit.value) {
    alert('Primero debes crear el cooperativista antes de subir archivos')
    return
  }
  
  await subirArchivo(file, 'documento-abc')
}

const subirArchivo = async (file, tipo) => {
  loading.value = true
  
  try {
    const formDataUpload = new FormData()
    formDataUpload.append('file', file)
    
    const response = await $fetch(
      `${authStore.apiUrl}/api/cooperativistas/${props.cooperativista.id}/${tipo}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        },
        body: formDataUpload
      }
    )
    
    // Actualizar URL en el formulario
    if (tipo === 'ci-foto') {
      formData.value.ci_foto_url = response.url
    } else {
      formData.value.documento_abc_url = response.url
    }
    
    alert('Archivo subido exitosamente')
  } catch (error) {
    console.error('Error subiendo archivo:', error)
    alert('Error al subir archivo: ' + (error.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const eliminarCIFoto = async () => {
  if (!confirm('¿Eliminar la foto de CI?')) return
  
  loading.value = true
  
  try {
    await $fetch(
      `${authStore.apiUrl}/api/cooperativistas/${props.cooperativista.id}/ci-foto`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )
    
    formData.value.ci_foto_url = ''
    alert('Foto eliminada')
  } catch (error) {
    console.error('Error eliminando foto:', error)
    alert('Error al eliminar foto')
  } finally {
    loading.value = false
  }
}

const eliminarDocumentoABC = async () => {
  if (!confirm('¿Eliminar el documento ABC?')) return
  
  loading.value = true
  
  try {
    await $fetch(
      `${authStore.apiUrl}/api/cooperativistas/${props.cooperativista.id}/documento-abc`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )
    
    formData.value.documento_abc_url = ''
    alert('Documento eliminado')
  } catch (error) {
    console.error('Error eliminando documento:', error)
    alert('Error al eliminar documento')
  } finally {
    loading.value = false
  }
}

const submitForm = () => {
  // No enviar las URLs de archivos en el submit principal
  const dataToSubmit = { ...formData.value }
  delete dataToSubmit.ci_foto_url
  delete dataToSubmit.documento_abc_url
  
  emit('submit', dataToSubmit)
}
</script>

<style scoped>
.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #038730;
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #feea01;
}

.file-upload-zone {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 1rem;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-box {
  text-align: center;
}

.preview-container {
  width: 100%;
  text-align: center;
  position: relative;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.document-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #038730;
  margin-bottom: 0.5rem;
}

.delete-btn {
  margin-top: 0.5rem;
}

.buttons-container {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>