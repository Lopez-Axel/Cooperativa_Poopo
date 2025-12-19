<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal is-active">
      <div class="modal-background" @click="cerrar"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi" :class="esEdicion ? 'mdi-pencil' : 'mdi-plus'"></i>
            {{ esEdicion ? 'Editar Cuadrilla' : 'Nueva Cuadrilla' }}
          </p>
          <button class="delete" @click="cerrar"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nombre *</label>
            <div class="control has-icons-left">
              <input 
                v-model="formulario.nombre"
                class="input"
                type="text"
                placeholder="Ej: Cuadrilla A"
              >
              <span class="icon is-left">
                <i class="mdi mdi-tag"></i>
              </span>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Sección *</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="formulario.id_seccion">
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
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-primary"
            @click="guardar"
            :disabled="!formulario.nombre.trim() || !formulario.id_seccion"
            :class="{ 'is-loading': cargando }"
          >
            <i class="mdi mdi-check"></i>
            {{ esEdicion ? 'Actualizar' : 'Crear' }}
          </button>
          <button class="button" @click="cerrar">Cancelar</button>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

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
      nombre: '',
      id_seccion: null
    })
  },
  secciones: {
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
  nombre: '',
  id_seccion: null
})

watch(() => props.datosIniciales, (nuevosDatos) => {
  formulario.value = { ...nuevosDatos }
}, { immediate: true, deep: true })

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const cerrar = () => {
  emit('close')
}

const guardar = () => {
  emit('guardar', { ...formulario.value })
}
</script>

<style scoped>
/* Usa exactamente los mismos estilos del ModalFormulario de secciones */
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
  max-width: 600px;
  width: 100%;
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

.icon.is-left {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9e9d24;
}

.select {
  width: 100%;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: #ffd700;
  right: 1.125em;
  z-index: 4;
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
</style>