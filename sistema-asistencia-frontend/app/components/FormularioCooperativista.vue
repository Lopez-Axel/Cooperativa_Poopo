<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal is-active">
      <div class="modal-background" @click="cerrar"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi" :class="esEdicion ? 'mdi-pencil' : 'mdi-plus'"></i>
            {{ esEdicion ? 'Editar Cooperativista' : 'Nuevo Cooperativista' }}
          </p>
          <button class="delete" @click="cerrar"></button>
        </header>
        
        <section class="modal-card-body">
          <!-- DATOS PERSONALES -->
          <div class="seccion-formulario">
            <h3 class="seccion-titulo">
              <i class="mdi mdi-account-circle"></i>
              Datos Personales
            </h3>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Nombres *</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.nombres"
                      class="input"
                      type="text"
                      placeholder="Ej: Juan Carlos"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-account"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Apellido Paterno *</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.apellido_paterno"
                      class="input"
                      type="text"
                      placeholder="Ej: Pérez"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-account"></i>
                    </span>
                  </div>
                </div>
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">Apellido Materno</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.apellido_materno"
                      class="input"
                      type="text"
                      placeholder="Ej: González"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-account"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">CI</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.ci"
                      class="input"
                      type="text"
                      placeholder="Ej: 12345678"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-card-account-details"></i>
                    </span>
                  </div>
                </div>
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">Expedido en</label>
                  <div class="control has-icons-left">
                    <div class="select is-fullwidth">
                      <select v-model="formulario.ci_expedido">
                        <option :value="null">SELECCIONE</option>
                        <option value="LP">LA PAZ</option>
                        <option value="OR">ORURO</option>
                        <option value="PT">POTOSI</option>
                        <option value="CB">COCHABAMBA</option>
                        <option value="SC">SANTA CRUZ</option>
                        <option value="CH">CHUQUISACA</option>
                        <option value="TJ">TARIJA</option>
                        <option value="BE">BENI</option>
                        <option value="PD">PANDO</option>
                      </select>
                    </div>
                    <span class="icon is-left">
                      <i class="mdi mdi-map-marker"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Fecha de Nacimiento</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.fecha_nacimiento"
                      class="input"
                      type="date"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-calendar"></i>
                    </span>
                  </div>
                </div>
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">Teléfono</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.telefono"
                      class="input"
                      type="tel"
                      placeholder="Ej: 71234567"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-phone"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Email</label>
              <div class="control has-icons-left">
                <input 
                  v-model="formulario.email"
                  class="input"
                  type="email"
                  placeholder="ejemplo@correo.com"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-email"></i>
                </span>
              </div>
            </div>
          </div>

          <!-- DATOS LABORALES -->
          <div class="seccion-formulario">
            <h3 class="seccion-titulo">
              <i class="mdi mdi-briefcase"></i>
              Información Laboral
            </h3>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Sección *</label>
                  <div class="control has-icons-left">
                    <div class="select is-fullwidth">
                      <select v-model="seccionSeleccionada" @change="onSeccionChange">
                        <option :value="null">Seleccione una sección</option>
                        <option 
                          v-for="seccion in secciones" 
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
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">Cuadrilla *</label>
                  <div class="control has-icons-left">
                    <div class="select is-fullwidth">
                      <select 
                        v-model="formulario.id_cuadrilla"
                        :disabled="!seccionSeleccionada"
                      >
                        <option :value="null">Seleccione una cuadrilla</option>
                        <option 
                          v-for="cuadrilla in cuadrillasFiltradas" 
                          :key="cuadrilla.id"
                          :value="cuadrilla.id"
                        >
                          {{ cuadrilla.nombre }}
                        </option>
                      </select>
                    </div>
                    <span class="icon is-left">
                      <i class="mdi mdi-account-group"></i>
                    </span>
                  </div>
                  <p v-if="!seccionSeleccionada" class="help">Primero seleccione una sección</p>
                </div>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Rol en Cuadrilla</label>
                  <div class="control has-icons-left">
                    <div class="select is-fullwidth">
                      <select v-model="formulario.rol_cuadrilla">
                        <option :value="null">Sin rol especial</option>
                        <option value="JEFE DE CUADRILLA">JEFE DE CUADRILLA</option>
                        <option value="SUB JEFE DE CUADRILLA">SUB JEFE DE CUADRILLA</option>
                        <option value="TESORERO DE CUADRILLA">TESORERO DE CUADRILLA</option>
                      </select>
                    </div>
                    <span class="icon is-left">
                      <i class="mdi mdi-star"></i>
                    </span>
                  </div>
                </div>
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">Ocupación</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.ocupacion"
                      class="input"
                      type="text"
                      placeholder="Ej: Minero, Perforista"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-hammer-wrench"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Fecha de Ingreso</label>
              <div class="control has-icons-left">
                <input 
                  v-model="formulario.fecha_ingreso"
                  class="input"
                  type="date"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-calendar-check"></i>
                </span>
              </div>
            </div>
          </div>

          <!-- INFORMACIÓN DE SEGURO -->
          <div class="seccion-formulario">
            <h3 class="seccion-titulo">
              <i class="mdi mdi-shield-check"></i>
              Información de Seguro
            </h3>

            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Código Asegurado</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.codigo_asegurado"
                      class="input"
                      type="text"
                      placeholder="Código de asegurado"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-identifier"></i>
                    </span>
                  </div>
                </div>
              </div>

              <div class="column">
                <div class="field">
                  <label class="label">CUA</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="formulario.cua"
                      class="input"
                      type="text"
                      placeholder="Código Único de Asegurado"
                    >
                    <span class="icon is-left">
                      <i class="mdi mdi-card-text"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Estado Asegurado</label>
              <div class="control has-icons-left">
                <div class="select is-fullwidth">
                  <select v-model="formulario.estado_asegurado">
                    <option :value="null">Seleccione</option>
                    <option value="Activo">Activo</option>
                    <option value="Inactivo">Inactivo</option>
                    <option value="Suspendido">Suspendido</option>
                    <option value="En trámite">En trámite</option>
                  </select>
                </div>
                <span class="icon is-left">
                  <i class="mdi mdi-shield-account"></i>
                </span>
              </div>
            </div>
          </div>

          <!-- DOCUMENTOS -->
          <div class="seccion-formulario">
            <h3 class="seccion-titulo">
              <i class="mdi mdi-file-document"></i>
              URLs de Documentos
            </h3>

            <div class="field">
              <label class="label">URL Foto CI</label>
              <div class="control has-icons-left">
                <input 
                  v-model="formulario.ci_foto_url"
                  class="input"
                  type="url"
                  placeholder="https://ejemplo.com/foto.jpg"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-image"></i>
                </span>
              </div>
              <p class="help">URL de la imagen de la cédula de identidad</p>
            </div>

            <div class="field">
              <label class="label">URL Documento ABC</label>
              <div class="control has-icons-left">
                <input 
                  v-model="formulario.documento_abc_url"
                  class="input"
                  type="url"
                  placeholder="https://ejemplo.com/documento.pdf"
                >
                <span class="icon is-left">
                  <i class="mdi mdi-file-pdf-box"></i>
                </span>
              </div>
              <p class="help">URL del documento ABC</p>
            </div>
          </div>

          <!-- ESTADO -->
          <div class="seccion-formulario">
            <div class="field">
              <label class="checkbox-container">
                <input 
                  v-model="formulario.is_active"
                  type="checkbox"
                >
                <span class="checkmark"></span>
                <span class="checkbox-label">Cooperativista Activo</span>
              </label>
            </div>
          </div>
        </section>

        <footer class="modal-card-foot">
          <button 
            class="button is-primary"
            @click="guardar"
            :disabled="!formularioValido"
            :class="{ 'is-loading': cargando }"
          >
            <i class="mdi mdi-check"></i>
            {{ esEdicion ? 'Actualizar' : 'Crear' }}
          </button>
          <button class="button" @click="cerrar">
            <i class="mdi mdi-close"></i>
            Cancelar
          </button>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  esEdicion: {
    type: Boolean,
    default: false
  },
  datosIniciales: {
    type: Object,
    default: () => ({
      nombres: '',
      apellido_paterno: '',
      apellido_materno: '',
      ci: '',
      ci_expedido: null,
      ci_foto_url: '',
      fecha_nacimiento: '',
      email: '',
      telefono: '',
      id_cuadrilla: null,
      rol_cuadrilla: null,
      ocupacion: '',
      fecha_ingreso: '',
      codigo_asegurado: '',
      cua: '',
      estado_asegurado: null,
      documento_abc_url: '',
      is_active: true
    })
  },
  secciones: {
    type: Array,
    default: () => []
  },
  cuadrillas: {
    type: Array,
    default: () => []
  },
  cargando: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'guardar'])

const formulario = ref({
  nombres: '',
  apellido_paterno: '',
  apellido_materno: '',
  ci: '',
  ci_expedido: null,
  ci_foto_url: '',
  fecha_nacimiento: '',
  email: '',
  telefono: '',
  id_cuadrilla: null,
  rol_cuadrilla: null,
  ocupacion: '',
  fecha_ingreso: '',
  codigo_asegurado: '',
  cua: '',
  estado_asegurado: null,
  documento_abc_url: '',
  is_active: true
})

const seccionSeleccionada = ref(null)

// Filtrar cuadrillas por sección seleccionada
const cuadrillasFiltradas = computed(() => {
  if (!seccionSeleccionada.value) return []
  return props.cuadrillas.filter(c => c.id_seccion === seccionSeleccionada.value && c.is_active)
})

// Validación del formulario
const formularioValido = computed(() => {
  return formulario.value.nombres.trim() !== '' &&
         formulario.value.apellido_paterno.trim() !== '' &&
         formulario.value.id_cuadrilla !== null
})

// Watch para datos iniciales
watch(() => props.datosIniciales, (nuevosDatos) => {
  formulario.value = { ...nuevosDatos }
  
  // Si es edición, encontrar la sección de la cuadrilla
  if (props.esEdicion && nuevosDatos.id_cuadrilla) {
    const cuadrilla = props.cuadrillas.find(c => c.id === nuevosDatos.id_cuadrilla)
    if (cuadrilla) {
      seccionSeleccionada.value = cuadrilla.id_seccion
    }
  }
}, { immediate: true, deep: true })

// Bloquear scroll del body cuando el modal está abierto
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const onSeccionChange = () => {
  // Limpiar cuadrilla seleccionada cuando cambia la sección
  formulario.value.id_cuadrilla = null
}

const cerrar = () => {
  emit('close')
  // Resetear sección seleccionada
  seccionSeleccionada.value = null
}

const guardar = () => {
  if (!formularioValido.value) return
  
  // Limpiar campos vacíos (convertir strings vacíos a null)
  const datosLimpios = { ...formulario.value }
  
  Object.keys(datosLimpios).forEach(key => {
    if (datosLimpios[key] === '') {
      datosLimpios[key] = null
    }
  })
  
  emit('guardar', datosLimpios)
}
</script>

<style scoped>
/* Usa los mismos estilos base del ModalFormulario */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
}

.modal-card {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  border: 2px solid rgba(255, 215, 0, 0.4);
  border-radius: 12px;
  max-width: 800px;
  width: 95%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  animation: modal-slideIn 0.3s ease-out;
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
  padding: 1.5rem 2rem;
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

/* Secciones del formulario */
.seccion-formulario {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.seccion-formulario:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.seccion-titulo {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.seccion-titulo i {
  font-size: 1.3rem;
}

.columns {
  display: flex;
  gap: 1rem;
  margin-bottom: 0;
}

.column {
  flex: 1;
}

.field {
  margin-bottom: 1rem;
}

.label {
  color: #e0f2f1;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: block;
  font-size: 0.9rem;
}

.control {
  position: relative;
}

.input, .select select {
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
  background: rgba(15, 31, 15, 0.7);
  color: #e0f2f1;
  width: 100%;
  box-sizing: border-box;
  height: 3rem;
  font-size: 0.95rem;
}

.control.has-icons-left .input,
.control.has-icons-left .select select {
  padding-left: 2.75rem;
}

.input::placeholder {
  color: #90a4ae;
}

.input:focus, .select select:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 0.125em rgba(255, 215, 0, 0.25);
  background: rgba(26, 46, 26, 0.9);
  outline: none;
}

.input:disabled, .select select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(15, 31, 15, 0.5);
}

.icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
  pointer-events: none;
}

.select {
  width: 100%;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: #ffd700;
  right: 1.125em;
  z-index: 4;
}

.help {
  color: #90a4ae;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

/* Checkbox personalizado */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-left: 2rem;
}

.checkbox-container input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 20px;
  width: 20px;
  background: rgba(15, 31, 15, 0.7);
  border: 2px solid rgba(255, 215, 0, 0.4);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.checkbox-container:hover .checkmark {
  border-color: #ffd700;
  background: rgba(26, 46, 26, 0.9);
}

.checkbox-container input:checked ~ .checkmark {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  border-color: #ffd700;
}

.checkmark::after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid #0d1b0d;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container input:checked ~ .checkmark::after {
  display: block;
}

.checkbox-label {
  color: #e0f2f1;
  font-weight: 600;
}

.button {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid transparent;
}

.button.is-primary {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  border: none;
  font-weight: 800;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.button.is-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 60%, #ff6f00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.button.is-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.button:not(.is-primary) {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.button:not(.is-primary):hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

@media screen and (max-width: 768px) {
  .modal-card {
    max-width: 95%;
    margin: 1rem;
  }
  
  .columns {
    flex-direction: column;
    gap: 0;
  }
  
  .modal-card-body {
    padding: 1rem;
  }
}
</style>