<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal is-active">
      <div class="modal-background" @click="cerrar"></div>
      <div class="modal-card" style="max-width: 500px;">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi mdi-alert"></i>
            Confirmar Desactivación
          </p>
          <button class="delete" @click="cerrar"></button>
        </header>
        <section class="modal-card-body">
          <div class="notification is-danger is-light">
            <p>¿Está seguro de desactivar la cuadrilla <strong>"{{ cuadrilla?.nombre }}"</strong>?</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            class="button is-danger"
            @click="confirmar"
            :class="{ 'is-loading': cargando }"
          >
            <i class="mdi mdi-delete"></i>
            Desactivar
          </button>
          <button class="button" @click="cerrar">Cancelar</button>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { watch } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  cuadrilla: {
    type: Object,
    default: null
  },
  cargando: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'confirmar'])

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

const confirmar = () => {
  emit('confirmar')
}
</script>

<style scoped>
/* Usa exactamente los mismos estilos del ModalConfirmarEliminacion de secciones */
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

.button.is-danger {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.5), rgba(211, 47, 47, 0.5));
  color: #ffcdd2;
  border: 1px solid rgba(244, 67, 54, 0.7);
}

.button.is-danger:hover {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.7), rgba(211, 47, 47, 0.7));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.button:not(.is-danger) {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.button:not(.is-danger):hover {
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