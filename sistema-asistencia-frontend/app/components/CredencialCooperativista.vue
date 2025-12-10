<template>
  <div>
    <button class="button is-primary" @click="generarCredenciales">
      <i class="mdi mdi-card-account-details"></i>
      <span>Generar Credenciales PNG</span>
    </button>

    <div class="credencial-oculta">
      <!-- FRENTE -->
      <div ref="credencialFrenteRef" class="credencial-impresion">
        <div class="cara-frente">
          <!-- Decoraciones -->
          <div class="circulo-decorativo circulo-1"></div>
          <div class="circulo-decorativo circulo-2"></div>
          <div class="circulo-decorativo circulo-3"></div>
          
          <div class="puntos-decorativos puntos-top">
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
          </div>
          
          <div class="puntos-decorativos puntos-bottom">
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
          </div>

          <!-- Logo empresa -->
          <div class="logo-container">
            <img src="/logo.jfif" alt="Logo" class="logo-frente" />
          </div>

          <!-- Foto circular -->
          <div class="foto-circular-container">
            <div class="foto-circular">
              <img 
                v-if="cooperativista.ci_foto_url" 
                :src="cooperativista.ci_foto_url" 
                alt="Foto"
              />
              <div v-else class="foto-placeholder">
                <i class="mdi mdi-account"></i>
              </div>
            </div>
          </div>

          <!-- Información -->
          <div class="info-frente">
            <h2 class="nombre-principal">
              {{ cooperativista.nombres }}<br>
              {{ cooperativista.apellido_paterno }}<br>
              {{ cooperativista.apellido_materno }}
            </h2>
            <p class="cargo-frente">{{ cooperativista.ocupacion || 'Cooperativista' }}</p>
          </div>

          <!-- Footer con CI -->
          <div class="footer-info-frente">
            <p class="ci-info">CI: {{ cooperativista.ci || 'N/A' }} {{ cooperativista.ci_expedido || '' }}</p>
          </div>
        </div>
      </div>

      <!-- REVERSO -->
      <div ref="credencialReversoRef" class="credencial-impresion">
        <div class="cara-reverso">
          <!-- Decoraciones -->
          <div class="lineas-decorativas">
            <div class="linea linea-1"></div>
            <div class="linea linea-2"></div>
            <div class="linea linea-3"></div>
          </div>

          <div class="puntos-decorativos puntos-reverso-top">
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
          </div>

          <div class="puntos-decorativos puntos-reverso-bottom">
            <div class="punto"></div>
            <div class="punto"></div>
            <div class="punto"></div>
          </div>

          <!-- Logo -->
          <div class="logo-reverso-container">
            <img src="/logo.jfif" alt="Logo" class="logo-reverso" />
          </div>

          <!-- QR Code -->
          <div class="qr-container-reverso">
            <div class="qr-wrapper">
              <QRCodeVue3
                :value="qrData"
                :width="200"
                :height="200"
                :margin="2"
                :dots-options="{ type: 'square', color: '#1a2e1a' }"
                :background-options="{ color: '#ffffff' }"
              />
            </div>
          </div>

          <!-- Información laboral -->
          <div class="info-reverso">
            <h3 class="titulo-cooperativa">COOPERATIVA MINERA POOPÓ R.L.</h3>
            <div class="datos-laborales">
              <p><strong>Sección:</strong> {{ cooperativista.seccion || 'N/A' }}</p>
              <p><strong>Cuadrilla:</strong> {{ cooperativista.cuadrilla || 'N/A' }}</p>
              <p v-if="cooperativista.jefe_cuadrilla"><strong>Jefe:</strong> {{ cooperativista.jefe_cuadrilla }}</p>
            </div>
          </div>

          <!-- Footer contacto -->
          <div class="footer-reverso">
            <p class="contacto-info">www.cooperativapoopo.com</p>
            <p class="contacto-info">contacto@cooperativapoopo.com</p>
            <p class="fecha-reverso">Emisión: {{ fechaEmision }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import QRCodeVue3 from 'qrcode-vue3'
import html2canvas from 'html2canvas'

const props = defineProps({
  cooperativista: { type: Object, required: true }
})

const credencialFrenteRef = ref(null)
const credencialReversoRef = ref(null)

const qrData = computed(() => {
  return `${props.cooperativista.nombres} ${props.cooperativista.apellido_paterno} ${props.cooperativista.apellido_materno}|${props.cooperativista.seccion || 'Sin sección'}|${props.cooperativista.cuadrilla || 'Sin cuadrilla'}`
})

const fechaEmision = computed(() => {
  return new Date().toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
})

const generarCredenciales = async () => {
  try {
    const contenedorOculto = document.querySelector('.credencial-oculta')
    
    // Mostrar temporalmente para captura
    contenedorOculto.style.position = 'fixed'
    contenedorOculto.style.left = '0'
    contenedorOculto.style.top = '0'
    contenedorOculto.style.zIndex = '9999'
    
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Generar FRENTE
    const canvasFrente = await html2canvas(credencialFrenteRef.value, {
      scale: 3.5,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#6B5FB5',
      logging: false,
      imageTimeout: 0,
      width: 1011,
      height: 638
    })

    const imgFrente = canvasFrente.toDataURL('image/png')
    const linkFrente = document.createElement('a')
    linkFrente.download = `frente_${props.cooperativista.nombres}_${props.cooperativista.apellido_paterno}.png`
    linkFrente.href = imgFrente
    linkFrente.click()

    await new Promise(resolve => setTimeout(resolve, 500))

    // Generar REVERSO
    const canvasReverso = await html2canvas(credencialReversoRef.value, {
      scale: 3.5,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#2B2654',
      logging: false,
      imageTimeout: 0,
      width: 1011,
      height: 638
    })

    const imgReverso = canvasReverso.toDataURL('image/png')
    const linkReverso = document.createElement('a')
    linkReverso.download = `reverso_${props.cooperativista.nombres}_${props.cooperativista.apellido_paterno}.png`
    linkReverso.href = imgReverso
    linkReverso.click()

    // Ocultar nuevamente
    contenedorOculto.style.position = 'absolute'
    contenedorOculto.style.left = '-9999px'
    contenedorOculto.style.top = '-9999px'
    contenedorOculto.style.zIndex = '-1'

    alert('Credenciales generadas correctamente')
  } catch (error) {
    console.error('Error generando credenciales:', error)
    alert('Error al generar las credenciales')
  }
}
</script>

<style scoped>
.credencial-oculta {
  position: absolute;
  left: -9999px;
  top: -9999px;
}

.credencial-impresion {
  width: 1011px;
  height: 638px;
  margin-bottom: 30px;
}

/* FRENTE */
.cara-frente {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #7B6FBD 0%, #6B5FB5 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Arial', 'Helvetica', sans-serif;
}

.circulo-decorativo {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circulo-1 {
  width: 350px;
  height: 350px;
  top: -100px;
  left: -80px;
}

.circulo-2 {
  width: 250px;
  height: 250px;
  bottom: -80px;
  right: -60px;
}

.circulo-3 {
  width: 180px;
  height: 180px;
  top: 50%;
  right: 50px;
  background: rgba(255, 255, 255, 0.08);
}

.puntos-decorativos {
  position: absolute;
  display: grid;
  gap: 12px;
}

.puntos-top {
  top: 30px;
  right: 40px;
  grid-template-columns: repeat(3, 1fr);
}

.puntos-bottom {
  bottom: 40px;
  left: 40px;
  grid-template-columns: repeat(2, 1fr);
}

.punto {
  width: 10px;
  height: 10px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
}

.logo-container {
  position: absolute;
  top: 30px;
  left: 40px;
  z-index: 10;
}

.logo-frente {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #FFD700;
  background: white;
}

.foto-circular-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 5;
}

.foto-circular {
  width: 280px;
  height: 280px;
  border-radius: 50%;
  overflow: hidden;
  border: 8px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  background: #e0e0e0;
}

.foto-circular img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.foto-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e0e0e0;
}

.foto-placeholder i {
  font-size: 120px;
  color: #9e9e9e;
}

.info-frente {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  z-index: 10;
  width: 90%;
}

.nombre-principal {
  font-size: 42px;
  font-weight: 900;
  color: white;
  text-transform: uppercase;
  margin: 0 0 15px 0;
  line-height: 1.1;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
  letter-spacing: 1px;
}

.cargo-frente {
  font-size: 26px;
  color: white;
  font-weight: 600;
  margin: 0;
  text-transform: capitalize;
  opacity: 0.95;
}

.footer-info-frente {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.7);
  padding: 12px 40px;
  border-radius: 30px;
  z-index: 10;
}

.ci-info {
  font-size: 20px;
  color: white;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}

/* REVERSO */
.cara-reverso {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #2B2654 0%, #1F1A3D 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Arial', 'Helvetica', sans-serif;
}

.lineas-decorativas {
  position: absolute;
  top: 0;
  right: 0;
  width: 40%;
  height: 100%;
}

.linea {
  position: absolute;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  transform: skewX(-20deg);
}

.linea-1 {
  width: 80px;
  right: 0;
}

.linea-2 {
  width: 60px;
  right: 100px;
}

.linea-3 {
  width: 40px;
  right: 180px;
}

.puntos-reverso-top {
  top: 35px;
  left: 40px;
  grid-template-columns: repeat(5, 1fr);
}

.puntos-reverso-bottom {
  bottom: 35px;
  right: 45px;
  grid-template-columns: repeat(3, 1fr);
}

.logo-reverso-container {
  position: absolute;
  top: 35px;
  right: 45px;
  z-index: 10;
}

.logo-reverso {
  width: 70px;
  height: 70px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #FFD700;
  background: white;
}

.qr-container-reverso {
  position: absolute;
  top: 50%;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
}

.qr-wrapper {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
}

.info-reverso {
  position: absolute;
  top: 140px;
  left: 50px;
  width: 450px;
  z-index: 10;
}

.titulo-cooperativa {
  font-size: 32px;
  font-weight: 900;
  color: #FFD700;
  margin: 0 0 30px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  line-height: 1.2;
}

.datos-laborales {
  background: rgba(255, 255, 255, 0.1);
  padding: 25px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.datos-laborales p {
  font-size: 22px;
  color: white;
  margin: 0 0 15px 0;
  line-height: 1.4;
}

.datos-laborales strong {
  color: #FFD700;
  font-weight: 700;
}

.footer-reverso {
  position: absolute;
  bottom: 30px;
  left: 50px;
  z-index: 10;
}

.contacto-info {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 8px 0;
  font-weight: 600;
}

.fecha-reverso {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  margin: 15px 0 0 0;
  font-weight: 600;
}
</style>