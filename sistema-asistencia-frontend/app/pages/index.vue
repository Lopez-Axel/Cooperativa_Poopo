<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." style="max-height: 60px; border-radius: 50%;">
            <span class="ml-3 has-text-white has-text-weight-bold is-size-5">COOPERATIVA MINERA POOPÓ R.L.</span>
          </a>

          <a role="button" 
             class="navbar-burger" 
             :class="{ 'is-active': menuActive }"
             @click="menuActive = !menuActive"
             aria-label="menu" 
             aria-expanded="false">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div class="navbar-menu" :class="{ 'is-active': menuActive }">
          <div class="navbar-start">
            <a class="navbar-item has-text-white has-text-weight-bold" href="#inicio">
              <span class="icon"><i class="mdi mdi-home"></i></span>
              <span>Inicio</span>
            </a>
            <a class="navbar-item has-text-white has-text-weight-bold" href="#nosotros">
              <span class="icon"><i class="mdi mdi-information"></i></span>
              <span>Nosotros</span>
            </a>
            <a class="navbar-item has-text-white has-text-weight-bold" href="#servicios">
              <span class="icon"><i class="mdi mdi-cog"></i></span>
              <span>Servicios</span>
            </a>
          </div>

          <div class="navbar-end">
            <div class="navbar-item">
              <div class="buttons">
                <NuxtLink to="/login" class="button is-warning">
                  <span class="icon"><i class="mdi mdi-login"></i></span>
                  <span>Iniciar Sesión</span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section con Carrusel -->
    <section class="hero is-large" id="inicio">
      <div class="hero-body p-0">
        <div class="carousel">
          <div 
            v-for="(slide, index) in slides" 
            :key="index"
            class="carousel-item"
            :class="{ 'is-active': currentSlide === index }">
            <img :src="slide.image" :alt="slide.title">
            <div class="hero-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center;">
              <div class="container has-text-centered">
                <h1 class="title is-1 has-text-white slide-in-left" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
                  {{ slide.title }}
                </h1>
                <p class="subtitle is-4 has-text-white slide-in-right" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
                  {{ slide.subtitle }}
                </p>
              </div>
            </div>
          </div>

          <!-- Controles del carrusel -->
          <div class="carousel-controls">
            <button @click="prevSlide" aria-label="Anterior">
              <span class="icon is-large"><i class="mdi mdi-chevron-left mdi-24px"></i></span>
            </button>
            <button @click="nextSlide" aria-label="Siguiente">
              <span class="icon is-large"><i class="mdi mdi-chevron-right mdi-24px"></i></span>
            </button>
          </div>

          <!-- Indicadores -->
          <div class="carousel-indicators">
            <button 
              v-for="(slide, index) in slides" 
              :key="index"
              :class="{ 'is-active': currentSlide === index }"
              @click="goToSlide(index)"
              :aria-label="`Ir a slide ${index + 1}`">
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección Nosotros -->
    <section class="section" id="nosotros">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-6 fade-in">
            <h2 class="title is-2 text-primary">
              <span class="icon-text">
                <span class="icon has-text-primary"><i class="mdi mdi-history mdi-36px"></i></span>
                <span>Nuestra Historia</span>
              </span>
            </h2>
            <p class="is-size-5 mb-4">
              Desde el <strong>26 de Diciembre de 1953</strong>, la Cooperativa Minera Poopó R.L. 
              ha sido un pilar fundamental en la industria minera de Bolivia.
            </p>
            <p class="is-size-6 mb-4">
              Con más de 70 años de experiencia, nos dedicamos a la extracción responsable de minerales, 
              generando empleo y desarrollo para nuestras comunidades. Somos una cooperativa comprometida 
              con el bienestar de nuestros socios y el desarrollo sostenible de la región.
            </p>
            <div class="content">
              <ul>
                <li><strong>Fundada:</strong> 26 de Diciembre de 1953</li>
                <li><strong>Ubicación:</strong> Poopó, Oruro - Bolivia</li>
                <li><strong>Actividad:</strong> Minería responsable y sostenible</li>
                <li><strong>Socios:</strong> Más de 500 cooperativistas activos</li>
              </ul>
            </div>
          </div>
          <div class="column is-6 fade-in">
            <figure class="image">
              <img src="https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800" 
                   alt="Minería" 
                   style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
            </figure>
          </div>
        </div>
      </div>
    </section>

    <!-- Estadísticas -->
    <section class="section bg-primary-light">
      <div class="container">
        <h2 class="title is-2 has-text-centered text-primary mb-6">Nuestros Números</h2>
        <div class="columns">
          <div class="column">
            <div class="card stat-card fade-in">
              <div class="stat-icon text-primary">
                <i class="mdi mdi-calendar"></i>
              </div>
              <div class="stat-number">70+</div>
              <div class="stat-label">Años de Historia</div>
            </div>
          </div>
          <div class="column">
            <div class="card stat-card fade-in" style="animation-delay: 0.1s;">
              <div class="stat-icon text-primary">
                <i class="mdi mdi-account-group"></i>
              </div>
              <div class="stat-number">500+</div>
              <div class="stat-label">Cooperativistas</div>
            </div>
          </div>
          <div class="column">
            <div class="card stat-card fade-in" style="animation-delay: 0.2s;">
              <div class="stat-icon text-primary">
                <i class="mdi mdi-chart-line"></i>
              </div>
              <div class="stat-number">100%</div>
              <div class="stat-label">Compromiso</div>
            </div>
          </div>
          <div class="column">
            <div class="card stat-card fade-in" style="animation-delay: 0.3s;">
              <div class="stat-icon text-primary">
                <i class="mdi mdi-shield-check"></i>
              </div>
              <div class="stat-number">24/7</div>
              <div class="stat-label">Operación</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Servicios -->
    <section class="section" id="servicios">
      <div class="container">
        <h2 class="title is-2 has-text-centered text-primary mb-6">Nuestros Servicios</h2>
        <div class="columns is-multiline">
          <div class="column is-4">
            <div class="card fade-in">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-hammer-screwdriver"></i>
                </span>
                <h3 class="title is-4 mt-4">Extracción Minera</h3>
                <p>Extracción responsable y sostenible de minerales con tecnología de punta y respeto al medio ambiente.</p>
              </div>
            </div>
          </div>
          <div class="column is-4">
            <div class="card fade-in" style="animation-delay: 0.1s;">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-school"></i>
                </span>
                <h3 class="title is-4 mt-4">Capacitación</h3>
                <p>Programas de formación continua para nuestros cooperativistas en seguridad y técnicas modernas.</p>
              </div>
            </div>
          </div>
          <div class="column is-4">
            <div class="card fade-in" style="animation-delay: 0.2s;">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-handshake"></i>
                </span>
                <h3 class="title is-4 mt-4">Apoyo Social</h3>
                <p>Comprometidos con el bienestar de nuestros socios y el desarrollo de la comunidad.</p>
              </div>
            </div>
          </div>
          <div class="column is-4">
            <div class="card fade-in" style="animation-delay: 0.3s;">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-leaf"></i>
                </span>
                <h3 class="title is-4 mt-4">Medio Ambiente</h3>
                <p>Prácticas mineras responsables que minimizan el impacto ambiental y promueven la sostenibilidad.</p>
              </div>
            </div>
          </div>
          <div class="column is-4">
            <div class="card fade-in" style="animation-delay: 0.4s;">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-shield-check"></i>
                </span>
                <h3 class="title is-4 mt-4">Seguridad</h3>
                <p>Protocolos de seguridad rigurosos para garantizar la integridad de nuestros cooperativistas.</p>
              </div>
            </div>
          </div>
          <div class="column is-4">
            <div class="card fade-in" style="animation-delay: 0.5s;">
              <div class="card-content has-text-centered">
                <span class="icon has-text-primary" style="font-size: 4rem;">
                  <i class="mdi mdi-cog"></i>
                </span>
                <h3 class="title is-4 mt-4">Tecnología</h3>
                <p>Implementación de sistemas modernos de gestión y control para optimizar operaciones.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="hero is-medium is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title is-2 has-text-white fade-in">¿Eres Cooperativista?</h2>
          <p class="subtitle is-4 has-text-white mb-5 fade-in">
            Accede al sistema de gestión para consultar tu información, dispositivos y más.
          </p>
          <NuxtLink to="/login" class="button is-warning is-large fade-in">
            <span class="icon"><i class="mdi mdi-login"></i></span>
            <span>Iniciar Sesión Ahora</span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="columns">
          <div class="column is-4">
            <div class="content">
              <img src="/logo.jfif" alt="Logo" style="max-width: 100px; border-radius: 50%; margin-bottom: 1rem;">
              <h3 class="title is-5 has-text-white">Cooperativa Minera Poopó R.L.</h3>
              <p>
                Fundada el 26 de Diciembre de 1953<br>
                Más de 70 años de historia y compromiso con Bolivia.
              </p>
            </div>
          </div>
          <div class="column is-4">
            <h3 class="title is-5 has-text-white">Contacto</h3>
            <div class="content">
              <p>
                <span class="icon-text">
                  <span class="icon"><i class="mdi mdi-map-marker"></i></span>
                  <span>Poopó, Oruro - Bolivia</span>
                </span>
              </p>
              <p>
                <span class="icon-text">
                  <span class="icon"><i class="mdi mdi-phone"></i></span>
                  <span>+591 (2) 123-4567</span>
                </span>
              </p>
              <p>
                <span class="icon-text">
                  <span class="icon"><i class="mdi mdi-email"></i></span>
                  <span>info@cooperativapoopo.bo</span>
                </span>
              </p>
            </div>
          </div>
          <div class="column is-4">
            <h3 class="title is-5 has-text-white">Enlaces Rápidos</h3>
            <div class="content">
              <ul>
                <li><a href="#nosotros">Nosotros</a></li>
                <li><a href="#servicios">Servicios</a></li>
                <li><NuxtLink to="/login">Iniciar Sesión</NuxtLink></li>
              </ul>
            </div>
          </div>
        </div>
        <hr style="background-color: rgba(255,255,255,0.2);">
        <div class="content has-text-centered">
          <p>
            <strong class="has-text-white">© 2025 Cooperativa Minera Poopó R.L.</strong><br>
            Todos los derechos reservados.<br>
            <em class="has-text-warning">
              Este sistema no se hubiera podido realizar sin la gestión y el compromiso 
              de la Directiva 2025 de la Cooperativa Minera Poopó R.L.
            </em>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Estado del menú móvil
const menuActive = ref(false)

// Slides del carrusel
const slides = ref([
  {
    image: 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=1200',
    title: 'Cooperativa Minera Poopó R.L.',
    subtitle: 'Más de 70 años de historia minera en Bolivia'
  },
  {
    image: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=1200',
    title: 'Tradición y Modernidad',
    subtitle: 'Tecnología de punta para una minería responsable'
  },
  {
    image: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1200',
    title: 'Compromiso con Bolivia',
    subtitle: 'Generando empleo y desarrollo sostenible'
  },
  {
    image: 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=1200',
    title: 'Fundada en 1953',
    subtitle: 'Siete décadas de excelencia en la industria minera'
  }
])

const currentSlide = ref(0)

// Funciones del carrusel
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.value.length
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 ? slides.value.length - 1 : currentSlide.value - 1
}

const goToSlide = (index) => {
  currentSlide.value = index
}

// Auto-play del carrusel
onMounted(() => {
  const interval = setInterval(nextSlide, 5000)
  
  onUnmounted(() => {
    clearInterval(interval)
  })
})

// Meta tags
useHead({
  title: 'Inicio',
  meta: [
    { name: 'description', content: 'Cooperativa Minera Poopó R.L. - Fundada el 26 de Diciembre de 1953. Más de 70 años de historia en la industria minera boliviana.' }
  ]
})
</script>