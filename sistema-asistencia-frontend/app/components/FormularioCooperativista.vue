<template>
  <div class="form-container">
    <form @submit.prevent="submitForm" novalidate>
      <!-- Información Básica -->
      <div class="section-title">Información Personal</div>

      <div class="columns is-multiline">
        <!-- Nombres: ocupa fila completa -->
        <div class="column is-12">
          <div class="field">
            <label class="label">Nombres *</label>
            <div class="control">
              <input
                v-model="formData.nombres"
                class="input"
                type="text"
                required
                placeholder="NOMBRE COMPLETO"
                aria-label="Nombres"
                maxlength="120"
              />
            </div>
          </div>
        </div>

        <!-- Dos inputs por fila a partir de aquí -->
        <div class="column is-half">
          <div class="field">
            <label class="label">Apellido Paterno *</label>
            <div class="control">
              <input
                v-model="formData.apellido_paterno"
                class="input"
                type="text"
                required
                placeholder="APELLIDO PATERNO"
                aria-label="Apellido paterno"
                maxlength="80"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Apellido Materno</label>
            <div class="control">
              <input
                v-model="formData.apellido_materno"
                class="input"
                type="text"
                placeholder="APELLIDO MATERNO"
                aria-label="Apellido materno"
                maxlength="80"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">CI</label>
            <div class="control">
              <input
                v-model="formData.ci"
                class="input"
                type="text"
                placeholder="CI"
                aria-label="Cédula de identidad"
                inputmode="numeric"
                maxlength="12"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Expedido</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="formData.ci_expedido" aria-label="Departamento expedición">
                  <option value="">-</option>
                  <option value="LP">LP - LA PAZ</option>
                  <option value="OR">OR - ORURO</option>
                  <option value="CB">CB - COCHABAMBA</option>
                  <option value="SC">SC - SANTA CRUZ</option>
                  <option value="PT">PT - POTOSÍ</option>
                  <option value="TJ">TJ - TARIJA</option>
                  <option value="CH">CH - CHUQUISACA</option>
                  <option value="BN">BN - BENI</option>
                  <option value="PD">PD - PANDO</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Fecha Nacimiento</label>
            <div class="control">
              <input
                v-model="formData.fecha_nacimiento"
                class="input"
                type="date"
                aria-label="Fecha de nacimiento"
                :max="maxDate"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input
                v-model="formData.email"
                class="input"
                type="email"
                placeholder="CORREO@EJEMPLO.COM"
                aria-label="Correo electrónico"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Documentos -->
      <div class="section-title">Documentos</div>

      <div class="columns is-multiline">
        <div class="column is-half">
          <div class="field">
            <label class="label">Foto de CI</label>
            <div class="file-upload-zone" :class="{ 'has-preview': formData.ci_foto_url || ciPreviewUrl }">
              <div v-if="formData.ci_foto_url || ciPreviewUrl" class="preview-container">
                <img :src="ciPreviewUrl || formData.ci_foto_url" alt="CI" class="preview-image" />
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
                <i class="mdi mdi-camera upload-icon"></i>
                <button
                  type="button"
                  class="button is-success"
                  @click="$refs.ciFileInput.click()"
                >
                  <i class="mdi mdi-upload"></i>
                  <span>Seleccionar Imagen</span>
                </button>
                <p class="help">JPG, PNG, WEBP (máx 10MB)</p>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Documento ABC</label>
            <div class="file-upload-zone" :class="{ 'has-preview': formData.documento_abc_url || abcPreviewUrl }">
              <div v-if="formData.documento_abc_url || abcPreviewUrl" class="preview-container">
                <div class="document-preview">
                  <i class="mdi mdi-file-document-outline document-icon"></i>
                  <a :href="abcPreviewUrl || formData.documento_abc_url" target="_blank" class="document-link">
                    Ver Documento
                  </a>
                </div>
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
                <i class="mdi mdi-file-document upload-icon"></i>
                <button
                  type="button"
                  class="button is-success"
                  @click="$refs.abcFileInput.click()"
                >
                  <i class="mdi mdi-upload"></i>
                  <span>Seleccionar Archivo</span>
                </button>
                <p class="help">PDF o Imagen (máx 20MB)</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Información Laboral -->
      <div class="section-title">Información Laboral</div>

      <div class="columns is-multiline">
        <div class="column is-half">
          <div class="field">
            <label class="label">Sección</label>
            <div class="control">
              <input
                v-model="formData.seccion"
                class="input"
                type="text"
                placeholder="NOMBRE DE SECCION"
                list="secciones-list"
                aria-label="Sección"
              />
              <datalist id="secciones-list">
                <option v-for="seccion in seccionesDisponibles" :key="seccion" :value="seccion" />
              </datalist>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Cuadrilla</label>
            <div class="control">
              <input
                v-model="formData.cuadrilla"
                class="input"
                type="text"
                placeholder="NOMBRE DE CUADRILLA"
                list="cuadrillas-list"
                aria-label="Cuadrilla"
              />
              <datalist id="cuadrillas-list">
                <option v-for="cuadrilla in cuadrillasDisponibles" :key="cuadrilla" :value="cuadrilla" />
              </datalist>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Jefe de Cuadrilla</label>
            <div class="control">
              <input
                v-model="formData.jefe_cuadrilla"
                class="input"
                type="text"
                placeholder="JEFE DE CUADRILLA"
                list="cargos-cuadrilla-list"
                aria-label="Jefe de cuadrilla"
              />
              <datalist id="cargos-cuadrilla-list">
                <option value="JEFE DE CUADRILLA" />
                <option value="SUB JEFE DE CUADRILLA" />
                <option value="TESORERO DE CUADRILLA" />
              </datalist>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Delegado de Sección</label>
            <div class="control">
              <label class="checkbox delegado-checkbox">
                <input type="checkbox" v-model="esDelegado" />
                Es Delegado de Sección
              </label>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Ocupación</label>
            <div class="control">
              <input
                v-model="formData.ocupacion"
                class="input"
                type="text"
                placeholder="OCUPACIÓN (EJ: PERFORISTA)"
                list="ocupaciones-list"
                aria-label="Ocupación"
              />
              <datalist id="ocupaciones-list">
                <option v-for="ocupacion in ocupacionesDisponibles" :key="ocupacion" :value="ocupacion" />
              </datalist>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Código Asegurado</label>
            <div class="control">
              <input
                v-model="formData.codigo_asegurado"
                class="input"
                type="text"
                placeholder="CÓDIGO ASEGURADO"
                aria-label="Código asegurado"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">CUA</label>
            <div class="control">
              <input
                v-model="formData.cua"
                class="input"
                type="text"
                placeholder="CUA"
                aria-label="CUA"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Estado Asegurado</label>
            <div class="control">
              <input
                v-model="formData.estado_asegurado"
                class="input"
                type="text"
                placeholder="ESTADO ASEGURADO (EJ: ACTIVO)"
                list="estados-asegurado-list"
                aria-label="Estado asegurado"
              />
              <datalist id="estados-asegurado-list">
                <option v-for="estado in estadosAseguradoDisponibles" :key="estado" :value="estado" />
              </datalist>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Fecha Ingreso</label>
            <div class="control">
              <input
                v-model="formData.fecha_ingreso"
                class="input"
                type="date"
                aria-label="Fecha de ingreso"
                :max="today"
              />
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="field">
            <label class="label">Estado</label>
            <div class="control">
              <label class="checkbox activo-checkbox">
                <input type="checkbox" v-model="formData.is_active" />
                Cooperativista Activo
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
                placeholder="DESCRIBIR MOTIVO DE BAJA"
                aria-label="Motivo de baja"
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
                aria-label="Fecha de baja"
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
          {{ isEdit ? 'ACTUALIZAR' : 'CREAR' }} COOPERATIVISTA
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  cooperativista: { type: Object, default: null }
})

const emit = defineEmits(['submit', 'cancel', 'guardar'])

const authStore = useAuthStore()
const store = useCooperativistasStore()
const loading = ref(false)
const ciFileInput = ref(null)
const abcFileInput = ref(null)

const isEdit = computed(() => !!props.cooperativista)

const today = new Date().toISOString().split('T')[0]
const maxDate = today

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

// Checkbox para delegado
const esDelegado = ref(false)

// Previews y archivos temporales para cuando se está creando
const ciTempFile = ref(null)
const abcTempFile = ref(null)
const ciPreviewUrl = ref('')
const abcPreviewUrl = ref('')

// Cargar datos si es edición
if (props.cooperativista) {
  Object.assign(formData.value, props.cooperativista)
  esDelegado.value = !!props.cooperativista.delegado_seccion && props.cooperativista.delegado_seccion.toLowerCase().includes('delegado')
}

// --- Datos para datalist ---
const cuadrillasDisponibles = computed(() => store.cuadrillas || [])
const seccionesDisponibles = computed(() => store.secciones || [])
const ocupacionesDisponibles = computed(() => store.ocupaciones || [])
const estadosAseguradoDisponibles = computed(() => {
  const est = new Set((store.cooperativistas || []).filter(c => c.estado_asegurado).map(c => c.estado_asegurado))
  return Array.from(est).sort()
})

const handleCIFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.size > 10 * 1024 * 1024) {
    alert('La imagen es muy pesada (máximo 10MB)')
    return
  }

  // Si estamos editando, subir inmediatamente
  if (isEdit.value) {
    await subirArchivo(file, 'ci-foto')
    return
  }

  // Si es creación: guardar temporalmente para subir después
  ciTempFile.value = file
  try { 
    ciPreviewUrl.value = URL.createObjectURL(file) 
  } catch (e) { 
    ciPreviewUrl.value = '' 
  }
}

const handleABCFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.size > 20 * 1024 * 1024) {
    alert('El archivo es muy pesado (máximo 20MB)')
    return
  }
  
  if (isEdit.value) {
    await subirArchivo(file, 'documento-abc')
    return
  }
  
  abcTempFile.value = file
  try { 
    abcPreviewUrl.value = URL.createObjectURL(file) 
  } catch (e) { 
    abcPreviewUrl.value = '' 
  }
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

const subirArchivosDespuesDeCrear = async (cooperativistaId) => {
  const uploads = []
  
  // Subir CI si existe
  if (ciTempFile.value) {
    const formDataCI = new FormData()
    formDataCI.append('file', ciTempFile.value)
    
    uploads.push(
      $fetch(`${authStore.apiUrl}/api/cooperativistas/${cooperativistaId}/ci-foto`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${authStore.token}` },
        body: formDataCI
      }).catch(err => console.error('Error subiendo CI:', err))
    )
  }
  
  // Subir ABC si existe
  if (abcTempFile.value) {
    const formDataABC = new FormData()
    formDataABC.append('file', abcTempFile.value)
    
    uploads.push(
      $fetch(`${authStore.apiUrl}/api/cooperativistas/${cooperativistaId}/documento-abc`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${authStore.token}` },
        body: formDataABC
      }).catch(err => console.error('Error subiendo ABC:', err))
    )
  }
  
  if (uploads.length > 0) {
    await Promise.all(uploads)
  }
}

const eliminarCIFoto = async () => {
  // Si hay preview temporal, eliminar localmente
  if (ciTempFile.value && !isEdit.value) {
    ciTempFile.value = null
    if (ciPreviewUrl.value) { 
      URL.revokeObjectURL(ciPreviewUrl.value)
      ciPreviewUrl.value = '' 
    }
    return
  }

  if (!isEdit.value) return
  if (!confirm('¿Eliminar la foto de CI?')) return
  
  loading.value = true
  
  try {
    await $fetch(
      `${authStore.apiUrl}/api/cooperativistas/${props.cooperativista.id}/ci-foto`,
      {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${authStore.token}` }
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
  if (abcTempFile.value && !isEdit.value) {
    abcTempFile.value = null
    if (abcPreviewUrl.value) { 
      URL.revokeObjectURL(abcPreviewUrl.value)
      abcPreviewUrl.value = '' 
    }
    return
  }

  if (!isEdit.value) return
  if (!confirm('¿Eliminar el documento ABC?')) return
  
  loading.value = true
  
  try {
    await $fetch(
      `${authStore.apiUrl}/api/cooperativistas/${props.cooperativista.id}/documento-abc`,
      {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${authStore.token}` }
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

const submitForm = async () => {
  loading.value = true
  
  try {
    const datos = { ...formData.value }
    
    // Manejar el campo delegado_seccion según el checkbox
    if (esDelegado.value) {
      datos.delegado_seccion = 'DELEGADO'
    } else {
      datos.delegado_seccion = ''
    }
    
    // No enviar URLs de archivos en el payload principal
    delete datos.ci_foto_url
    delete datos.documento_abc_url
    
    // Limpiar valores vacíos
    Object.keys(datos).forEach(key => {
      if (datos[key] === '' || datos[key] === null) {
        delete datos[key]
      }
    })
    
    let cooperativistaCreado
    
    if (isEdit.value) {
      // ACTUALIZAR
      await store.actualizarCooperativista(props.cooperativista.id, datos)
      alert('Cooperativista actualizado exitosamente')
    } else {
      // CREAR
      cooperativistaCreado = await store.crearCooperativista(datos)
      
      // Subir archivos si existen
      if (cooperativistaCreado?.id && (ciTempFile.value || abcTempFile.value)) {
        await subirArchivosDespuesDeCrear(cooperativistaCreado.id)
      }
      
      alert('Cooperativista creado exitosamente')
    }
    
    emit('guardar')
    
  } catch (error) {
    console.error('Error al guardar:', error)
    alert('Error al guardar: ' + (error.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// Limpiar URLs al desmontar
onUnmounted(() => {
  if (ciPreviewUrl.value) URL.revokeObjectURL(ciPreviewUrl.value)
  if (abcPreviewUrl.value) URL.revokeObjectURL(abcPreviewUrl.value)
})
</script>

<style scoped>
.form-container {
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(76, 175, 80, 0.2), 0 0 60px rgba(255, 215, 0, 0.1);
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
  position: relative;
  overflow: hidden;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.form-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
  animation: form-float 20s infinite linear;
  z-index: 0;
}

/* Títulos de sección */
.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.4);
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
}

/* Contenedor de columnas */
.columns.is-multiline {
  margin-top: 0.75rem;
  position: relative;
  z-index: 1;
}

/* Estilos para columnas individuales */
.columns.is-multiline .column {
  padding: 0.5rem;
}

/* Estilos para labels */
.field .label {
  color: #e0f2f1;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  letter-spacing: 0.3px;
  display: block;
}

/* Estilos para inputs y textareas */
.control .input,
.control .textarea,
.control .select select {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  backdrop-filter: blur(10px);
  border: 2px solid rgba(46, 125, 50, 0.5);
  border-radius: 10px;
  color: #c8e6c9;
  font-weight: 500;
  padding: 0.625rem 0.875rem;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 100%;
  font-size: 0.95rem;
  height: auto;
  min-height: 2.75rem;
}

.control .input:focus,
.control .textarea:focus,
.control .select select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2), 0 4px 15px rgba(255, 215, 0, 0.3);
  outline: none;
  transform: translateY(-2px);
}

.control .input::placeholder,
.control .textarea::placeholder {
  color: rgba(165, 214, 167, 0.6);
  font-weight: 500;
  font-size: 0.9rem;
}

/* Estilo específico para el select de expedido */
.control .select {
  width: 100%;
  position: relative;
}

.control .select select {
  height: 2.75rem;
  width: 100%;
  color: #c8e6c9;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9)) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffd700'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E") no-repeat right 0.875rem center/16px 16px;
  cursor: pointer;
  padding-right: 2.5rem;
}

.control .select select:focus {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.95), rgba(15, 31, 15, 0.95)) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffd700'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E") no-repeat right 0.875rem center/16px 16px;
}

.control .select select option {
  background: #0f1f0f;
  color: #c8e6c9;
  padding: 0.5rem;
}

.control .select select option:hover {
  background: #ffd700;
  color: #0d1b0d;
}

/* File Upload Zones - Botones más pequeños y elegantes */
.file-upload-zone {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  border: 2px dashed rgba(255, 215, 0, 0.4);
  border-radius: 12px;
  padding: 1.25rem;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  margin-bottom: 1rem;
}

.file-upload-zone.has-preview {
  border-color: #ffd700;
  border-style: solid;
  background: linear-gradient(135deg, rgba(26, 46, 26, 1), rgba(15, 31, 15, 1));
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.2);
}

.file-upload-zone:hover {
  transform: translateY(-4px);
  border-color: #ffd700;
  box-shadow: 0 8px 30px rgba(158, 157, 36, 0.3);
}

.upload-box {
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 2.5rem;
  color: #ffd700;
  margin-bottom: 0;
  display: block;
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

/* Botones más pequeños y compactos */
.button.is-success {
  background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
  border: 2px solid #ffd700;
  color: #e0f2f1;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.625rem 1.25rem;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4),
              0 0 0 6px rgba(26, 46, 26, 0.8);
  position: relative;
  z-index: 2;
  letter-spacing: 0.5px;
  min-width: 200px;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-transform: uppercase;
  height: auto;
}

.button.is-success:hover {
  background: linear-gradient(135deg, #9e9d24 0%, #cddc39 100%);
  border-color: #ffd700;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(158, 157, 36, 0.5),
              0 0 0 6px rgba(26, 46, 26, 0.9);
  color: #0d1b0d;
}

.button.is-success .mdi-upload {
  font-size: 1.1rem;
}

/* Previews */
.preview-container {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  border: 2px solid #ffd700;
  transition: all 0.3s ease;
}

.preview-image:hover {
  transform: scale(1.03);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.4);
}

.document-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(15, 31, 15, 0.8);
  border-radius: 10px;
  border: 2px solid #ffd700;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
  width: 100%;
}

.document-icon {
  font-size: 3rem;
  color: #ffd700;
  text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.document-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 2px solid rgba(255, 215, 0, 0.4);
  background: rgba(15, 31, 15, 0.9);
}

.document-link:hover {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-text-fill-color: #0d1b0d;
  border-color: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.button.is-danger {
  background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
  border: 2px solid #ffd700;
  color: #ffebee;
  font-weight: 600;
  font-size: 0.85rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  position: relative;
  z-index: 2;
  height: auto;
}

.button.is-danger:hover {
  background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
  border-color: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(183, 28, 28, 0.5);
}

/* Checkbox Styling */
.delegado-checkbox,
.activo-checkbox {
  display: flex;
  align-items: center;
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.9), rgba(15, 31, 15, 0.9));
  backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 2px solid rgba(255, 215, 0, 0.4);
  font-weight: 700;
  color: #ffd700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-size: 0.95rem;
  margin-top: 0.5rem;
}

.delegado-checkbox:hover,
.activo-checkbox:hover {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  border-color: #ffd700;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
}

.delegado-checkbox input[type="checkbox"],
.activo-checkbox input[type="checkbox"] {
  margin-right: 0.75rem;
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #ffd700;
}

/* Buttons Container */
.buttons-container {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid rgba(255, 215, 0, 0.3);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.button.is-light {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(158, 157, 36, 0.2));
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 215, 0, 0.4);
  color: #c8e6c9;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-size: 0.95rem;
  min-width: 140px;
}

.button.is-light:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(158, 157, 36, 0.3));
  border-color: #ffd700;
  color: #ffd700;
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(255, 215, 0, 0.3);
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  border: 3px solid #ffd700;
  color: #0d1b0d;
  font-weight: 800;
  padding: 0.75rem 2rem;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4),
              0 0 0 8px rgba(26, 46, 26, 0.9);
  letter-spacing: 1px;
  text-transform: uppercase;
  font-size: 1rem;
  min-width: 220px;
  position: relative;
  z-index: 2;
}

.button.is-primary:hover:not(:disabled) {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5),
              0 0 0 8px rgba(26, 46, 26, 1);
}

.button.is-primary.is-loading {
  background: linear-gradient(135deg, #9e9d24 0%, #ff9800 100%);
}

.help {
  margin-top: 0.75rem;
  font-size: 0.8rem;
  color: #a5d6a7;
  font-weight: 500;
  text-align: center;
  background: rgba(15, 31, 15, 0.8);
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

/* Animations */
@keyframes form-float {
  from {
    transform: translateY(0) rotate(0deg);
  }
  to {
    transform: translateY(-100px) rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .form-container {
    padding: 1.25rem;
    max-width: 95%;
  }
  
  .button.is-success {
    min-width: 180px;
    padding: 0.6rem 1.1rem;
    font-size: 0.85rem;
  }
  
  .button.is-primary {
    min-width: 200px;
    padding: 0.7rem 1.75rem;
  }
  
  .file-upload-zone {
    min-height: 170px;
    padding: 1.1rem;
  }
}

@media (max-width: 768px) {
  .form-container {
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem auto;
  }
  
  .section-title {
    font-size: 1rem;
    margin: 1.25rem 0 0.75rem 0;
  }
  
  .columns.is-multiline .column {
    padding: 0.375rem;
  }
  
  .column.is-half,
  .column.is-12,
  .column.is-8,
  .column.is-4 {
    width: 100% !important;
  }
  
  .file-upload-zone {
    min-height: 160px;
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .button.is-success {
    min-width: 100%;
    max-width: 100%;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    box-shadow: 0 3px 10px rgba(46, 125, 50, 0.4),
                0 0 0 4px rgba(26, 46, 26, 0.8);
  }
  
  .button.is-primary {
    min-width: 100%;
    padding: 0.7rem 1.5rem;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4),
                0 0 0 6px rgba(26, 46, 26, 0.9);
  }
  
  .preview-image {
    max-height: 180px;
  }
  
  .document-icon {
    font-size: 2.5rem;
  }
  
  .upload-icon {
    font-size: 2rem;
  }
  
  .buttons-container {
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 2rem;
  }
  
  .button.is-light,
  .button.is-primary {
    width: 100%;
    min-width: unset;
  }
  
  .control .input,
  .control .textarea,
  .control .select select {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
    min-height: 2.5rem;
  }
  
  .field .label {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .form-container {
    padding: 0.75rem;
    margin: 0.25rem auto;
    border-width: 2px;
  }
  
  .section-title {
    font-size: 0.95rem;
    margin: 1rem 0 0.5rem 0;
  }
  
  .file-upload-zone {
    min-height: 140px;
    padding: 0.75rem;
  }
  
  .button.is-success,
  .button.is-primary {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    border-radius: 8px;
  }
  
  .preview-image {
    max-height: 150px;
  }
  
  .document-icon {
    font-size: 2rem;
  }
  
  .upload-icon {
    font-size: 1.75rem;
  }
  
  .document-link {
    padding: 0.4rem 0.75rem;
    font-size: 0.85rem;
  }
  
  .help {
    font-size: 0.75rem;
    padding: 0.3rem 0.6rem;
  }
  
  .buttons-container {
    margin-top: 1.5rem;
    padding-top: 1rem;
  }
  
  .delegado-checkbox,
  .activo-checkbox {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .delegado-checkbox input[type="checkbox"],
  .activo-checkbox input[type="checkbox"] {
    width: 16px;
    height: 16px;
  }
  
  .control .select select {
    padding-right: 2rem;
    background-size: 12px 12px;
    background-position: right 0.75rem center;
  }
}

/* Para tablets en modo paisaje */
@media (min-width: 769px) and (max-width: 1024px) and (orientation: landscape) {
  .columns.is-multiline {
    display: flex;
    flex-wrap: wrap;
  }
  
  .column.is-half {
    width: 50% !important;
  }
  
  .file-upload-zone {
    min-height: 200px;
  }
}

/* Para pantallas muy grandes */
@media (min-width: 1400px) {
  .form-container {
    max-width: 1300px;
    padding: 2rem;
  }
  
  .button.is-success {
    min-width: 220px;
    padding: 0.75rem 1.5rem;
  }
  
  .button.is-primary {
    min-width: 250px;
    padding: 0.875rem 2.25rem;
  }
}
</style>