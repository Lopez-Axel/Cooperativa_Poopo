<template>
  <div class="formulario-cooperativista">
    <form @submit.prevent="submitForm">
      
      <div class="form-section">
        <h3 class="section-title">Datos Personales</h3>
        
        <div class="columns is-multiline">
          <div class="column is-12">
            <div class="field">
              <label class="label">CI</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.ci"
                  placeholder="12345678"
                />
              </div>
            </div>
          </div>
          
          <div class="column is-4">
            <div class="field">
              <label class="label">Nombres *</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.nombres"
                  required
                />
              </div>
            </div>
          </div>
          
          <div class="column is-4">
            <div class="field">
              <label class="label">Apellido Paterno *</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.apellido_paterno"
                  required
                />
              </div>
            </div>
          </div>
          
          <div class="column is-4">
            <div class="field">
              <label class="label">Apellido Materno</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.apellido_materno"
                />
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Expedido en</label>
              <div class="select is-fullwidth">
                <select v-model="form.ci_expedido">
                  <option value="">Seleccionar</option>
                  <option value="LP">La Paz</option>
                  <option value="OR">Oruro</option>
                  <option value="CB">Cochabamba</option>
                  <option value="SC">Santa Cruz</option>
                  <option value="PT">Potosí</option>
                  <option value="TJ">Tarija</option>
                  <option value="CH">Chuquisaca</option>
                  <option value="BE">Beni</option>
                  <option value="PD">Pando</option>
                </select>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Fecha de Nacimiento</label>
              <div class="control">
                <input 
                  class="input" 
                  type="date" 
                  v-model="form.fecha_nacimiento"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Información Laboral</h3>
        
        <div class="columns is-multiline">
          <div class="column is-6">
            <div class="field">
              <label class="label">Sección</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.seccion"
                  placeholder="Ej: 1, 2, 3..."
                  list="secciones-list"
                />
                <datalist id="secciones-list">
                  <option v-for="seccion in seccionesDisponibles" :key="seccion" :value="seccion"/>
                </datalist>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Cuadrilla</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.cuadrilla"
                  placeholder="Nombre de la cuadrilla"
                  list="cuadrillas-list"
                />
                <datalist id="cuadrillas-list">
                  <option v-for="cuadrilla in cuadrillasDisponibles" :key="cuadrilla" :value="cuadrilla"/>
                </datalist>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Cargo Especial en Cuadrilla</label>
              <div class="select is-fullwidth">
                <select v-model="form.jefe_cuadrilla">
                  <option value="">Sin cargo especial</option>
                  <option value="JEFE DE CUADRILLA">JEFE DE CUADRILLA</option>
                  <option value="SUB JEFE DE CUADRILLA">SUB JEFE DE CUADRILLA</option>
                  <option value="TESORERO DE CUADRILLA">TESORERO DE CUADRILLA</option>
                </select>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Ocupación</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.ocupacion"
                  placeholder="Ej: PERFORISTA, CARRERO"
                  list="ocupaciones-list"
                />
                <datalist id="ocupaciones-list">
                  <option v-for="ocupacion in ocupacionesDisponibles" :key="ocupacion" :value="ocupacion"/>
                </datalist>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Fecha de Ingreso</label>
              <div class="control">
                <input 
                  class="input" 
                  type="date" 
                  v-model="form.fecha_ingreso"
                />
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Código Asegurado</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.codigo_asegurado"
                />
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="label">Estado Asegurado</label>
              <div class="control">
                <input 
                  class="input" 
                  type="text" 
                  v-model="form.estado_asegurado"
                  placeholder="Ej: ACTIVO, INACTIVO"
                  list="estados-asegurado-list"
                />
                <datalist id="estados-asegurado-list">
                  <option v-for="estado in estadosAseguradoDisponibles" :key="estado" :value="estado"/>
                </datalist>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label class="checkbox checkbox-delegado">
                <input type="checkbox" v-model="esDelegado" />
                <span class="checkbox-label">
                  <i class="mdi mdi-account-star"></i>
                  Es Delegado de Sección
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Estado del Cooperativista</h3>
        
        <div class="columns">
          <div class="column is-12">
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="form.is_active" />
                <span class="checkbox-label">Cooperativista Activo</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="button is-light" @click="$emit('cancelar')">
          Cancelar
        </button>
        <button type="submit" class="button is-warning" :disabled="guardando">
          <span v-if="!guardando">Guardar</span>
          <span v-else>Guardando...</span>
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
const emit = defineEmits(['guardar', 'cancelar'])
const props = defineProps({
  cooperativista: {
    type: Object,
    default: null
  }
})

const store = useCooperativistasStore()
const guardando = ref(false)
const esDelegado = ref(false)

const form = ref({
  nombres: '',
  apellido_paterno: '',
  apellido_materno: '',
  ci: '',
  ci_expedido: '',
  fecha_nacimiento: '',
  seccion: '',
  cuadrilla: '',
  jefe_cuadrilla: '',
  ocupacion: '',
  fecha_ingreso: '',
  codigo_asegurado: '',
  estado_asegurado: '',
  is_active: true
})

const cuadrillasDisponibles = computed(() => store.cuadrillas)

const seccionesDisponibles = computed(() => store.secciones)

const ocupacionesDisponibles = computed(() => {
  const ocupaciones = new Set(
    store.cooperativistas
      .filter(c => c.ocupacion)
      .map(c => c.ocupacion)
  )
  return Array.from(ocupaciones).sort()
})

const estadosAseguradoDisponibles = computed(() => {
  const estados = new Set(
    store.cooperativistas
      .filter(c => c.estado_asegurado)
      .map(c => c.estado_asegurado)
  )
  return Array.from(estados).sort()
})

onMounted(() => {
  if (props.cooperativista) {
    Object.assign(form.value, props.cooperativista)
    // Verificar si es delegado
    const delegadoField = props.cooperativista.delegado_seccion || ''
    esDelegado.value = delegadoField.toLowerCase().includes('delegado')
  }
})

const submitForm = async () => {
  guardando.value = true
  
  try {
    const datos = { ...form.value }
    
    // Manejar el campo delegado_seccion según el checkbox
    if (esDelegado.value) {
      datos.delegado_seccion = 'DELEGADO'
    } else {
      datos.delegado_seccion = ''
    }
    
    // Limpiar valores vacíos
    Object.keys(datos).forEach(key => {
      if (datos[key] === '' || datos[key] === null) {
        delete datos[key]
      }
    })
    
    if (props.cooperativista) {
      await store.actualizarCooperativista(props.cooperativista.id, datos)
    } else {
      await store.crearCooperativista(datos)
    }
    
    emit('guardar')
  } catch (error) {
    alert('Error al guardar: ' + error.message)
  } finally {
    guardando.value = false
  }
}
</script>

<style scoped>
/* ====================================
   BASE
   ==================================== */
.formulario-cooperativista {
  padding: 1rem;
}

/* ====================================
   SECCIONES DEL FORMULARIO
   ==================================== */
.form-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  border: 2px solid #e0e0e0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.form-section:hover {
  border-color: #4caf50;
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.12);
}

.section-title {
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #4caf50;
}

/* ====================================
   CAMPOS DEL FORMULARIO
   ==================================== */
.field .label {
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.input, .select select {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  color: #333;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.input::placeholder {
  color: #999;
  opacity: 0.7;
}

.input:focus, .select select:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 0.125em rgba(76, 175, 80, 0.25);
  background: white;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: #4caf50;
}

/* ====================================
   CHECKBOX
   ==================================== */
.checkbox {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 1.25rem;
  background: #f5f5f5;
  border-radius: 10px;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.checkbox:hover {
  border-color: #4caf50;
  background: #e8f5e9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.1);
}

.checkbox input[type="checkbox"] {
  width: 22px;
  height: 22px;
  cursor: pointer;
  accent-color: #4caf50;
}

.checkbox-label {
  color: #2e7d32;
  font-weight: 700;
  font-size: 1rem;
}

.checkbox-delegado {
  height: 100%;
  display: flex;
  align-items: center;
  margin-top: 1.85rem;
}

.checkbox-delegado .checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-delegado .checkbox-label i {
  font-size: 1.5rem;
  color: #ff9800;
}

/* ====================================
   ACCIONES DEL FORMULARIO
   ==================================== */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 2rem;
  margin-top: 1rem;
  border-top: 2px solid #e0e0e0;
}

.form-actions .button {
  min-width: 140px;
  font-weight: 700;
  padding: 0.875rem 2rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.button.is-light {
  background: white;
  border: 2px solid #e0e0e0;
  color: #666;
}

.button.is-light:hover {
  background: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #4caf50;
}

.button.is-warning {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  border: none;
  font-weight: 800;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.button.is-warning:hover {
  background: linear-gradient(135deg, #ff9800, #ffd700);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

.button.is-warning:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* ====================================
   RESPONSIVE
   ==================================== */
@media screen and (max-width: 768px) {
  .formulario-cooperativista {
    padding: 0.5rem;
  }
  
  .form-section {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .button {
    min-width: 100%;
  }
  
  .checkbox-delegado {
    margin-top: 0;
    height: auto;
  }
}
</style>