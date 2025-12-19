<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal is-active">
      <div class="modal-background" @click="cerrar"></div>
      <div class="modal-card" style="max-width: 800px;">
        <header class="modal-card-head">
          <p class="modal-card-title">
            <i class="mdi mdi-information"></i>
            Detalles de Sección
          </p>
          <button class="delete" @click="cerrar"></button>
        </header>
        <section class="modal-card-body" v-if="detalles">
          <div class="detail-section">
            <h3 class="detail-title">Información General</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Nombre:</span>
                <span class="detail-value">{{ detalles.nombre }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Descripción:</span>
                <span class="detail-value">{{ detalles.descripcion || 'Sin descripción' }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="detalles.delegado">
            <h3 class="detail-title">Delegado de Sección</h3>
            <div class="delegado-card">
              <i class="mdi mdi-account-star delegado-icon"></i>
              <div class="delegado-info">
                <strong>{{ detalles.delegado.nombres }} {{ detalles.delegado.apellido_paterno }} {{ detalles.delegado.apellido_materno || '' }}</strong>
                <span v-if="detalles.delegado.ci" class="delegado-ci">CI: {{ detalles.delegado.ci }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h3 class="detail-title">Estadísticas</h3>
            <div class="stats-grid">
              <div class="stat-card">
                <i class="mdi mdi-folder-multiple stat-icon"></i>
                <div class="stat-info">
                  <span class="stat-value">{{ detalles.total_cuadrillas }}</span>
                  <span class="stat-label">Cuadrillas</span>
                </div>
              </div>
              <div class="stat-card">
                <i class="mdi mdi-account-group stat-icon"></i>
                <div class="stat-info">
                  <span class="stat-value">{{ detalles.total_cooperativistas }}</span>
                  <span class="stat-label">Cooperativistas</span>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="detalles.cuadrillas.length > 0">
            <h3 class="detail-title">Cuadrillas</h3>
            <div class="cuadrillas-list">
              <div 
                v-for="cuadrilla in detalles.cuadrillas" 
                :key="cuadrilla.id"
                class="cuadrilla-item"
              >
                <div class="cuadrilla-name">
                  <i class="mdi mdi-folder"></i>
                  {{ cuadrilla.nombre }}
                </div>
                <div class="cuadrilla-count">
                  <i class="mdi mdi-account-multiple"></i>
                  {{ cuadrilla.total_cooperativistas }} miembros
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state-small">
            <i class="mdi mdi-folder-open"></i>
            <p>No hay cuadrillas en esta sección</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" @click="cerrar">Cerrar</button>
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
  detalles: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const cerrar = () => {
  emit('close')
}

// Prevenir scroll del body cuando el modal está abierto
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
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

.button {
  background: rgba(255, 255, 255, 0.1);
  color: #c8e6c9;
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.button:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-title {
  color: #ffd700;
  font-weight: 800;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.detail-grid {
  display: grid;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  color: #90a4ae;
  font-size: 0.85rem;
  font-weight: 600;
}

.detail-value {
  color: #e0f2f1;
  font-size: 1rem;
  font-weight: 500;
}

.delegado-card {
  background: rgba(33, 150, 243, 0.2);
  border: 1px solid rgba(33, 150, 243, 0.4);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.delegado-icon {
  font-size: 2.5rem;
  color: #64b5f6;
}

.delegado-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.delegado-info strong {
  color: #e0f2f1;
  font-size: 1.1rem;
}

.delegado-ci {
  color: #90a4ae;
  font-size: 0.9rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
  color: #ffd700;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: 900;
}

.stat-label {
  color: #c8e6c9;
  font-size: 0.85rem;
  font-weight: 600;
}

.cuadrillas-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cuadrilla-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.cuadrilla-item:hover {
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.4);
}

.cuadrilla-name {
  color: #e0f2f1;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cuadrilla-name i {
  color: #ffd700;
}

.cuadrilla-count {
  color: #90a4ae;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.empty-state-small {
  text-align: center;
  padding: 2rem;
  color: #90a4ae;
}

.empty-state-small i {
  font-size: 3rem;
  color: rgba(255, 215, 0, 0.3);
  margin-bottom: 0.5rem;
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