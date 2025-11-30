<template>
  <div class="index_public_container">
    <!-- Navbar -->
    <nav class="index_public_navbar" role="navigation" aria-label="main navigation">
      <div class="index_public_navbar_container">
        <div class="index_public_navbar_brand">
          <a class="index_public_navbar_item" href="/">
            <img src="/logo.jfif" alt="Cooperativa Minera Poopó R.L." class="index_public_logo">
            <span class="index_public_brand_text">COOPERATIVA MINERA POOPÓ R.L.</span>
          </a>

          <a role="button" 
             class="index_public_navbar_burger" 
             :class="{ 'is-active': menuActive }"
             @click="menuActive = !menuActive"
             aria-label="menu" 
             aria-expanded="false">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div class="index_public_navbar_menu" :class="{ 'is-active': menuActive }">
          <div class="index_public_navbar_start">
            <a class="index_public_nav_link" href="#inicio">
              <span class="icon"><i class="mdi mdi-home"></i></span>
              <span>Inicio</span>
            </a>
            <a class="index_public_nav_link" href="#nosotros">
              <span class="icon"><i class="mdi mdi-information"></i></span>
              <span>Nosotros</span>
            </a>
            <a class="index_public_nav_link" href="#servicios">
              <span class="icon"><i class="mdi mdi-cog"></i></span>
              <span>Servicios</span>
            </a>
            <a class="index_public_nav_link" href="#galeria">
              <span class="icon"><i class="mdi mdi-image-multiple"></i></span>
              <span>Galería</span>
            </a>
          </div>

          <div class="index_public_navbar_end">
            <div class="index_public_navbar_item">
              <div class="index_public_buttons">
                <NuxtLink to="/login" class="index_public_login_btn">
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
    <section class="index_public_hero" id="inicio">
      <div class="index_public_hero_body">
        <div class="index_public_carousel">
          <div 
            v-for="(slide, index) in slides" 
            :key="index"
            class="index_public_carousel_item"
            :class="{ 'is-active': currentSlide === index }">
            <img :src="slide.image" :alt="slide.title" class="index_public_carousel_image">
            <div class="index_public_hero_overlay">
              <div class="index_public_carousel_content">
                <h1 class="index_public_carousel_title index_public_slide_in_left">
                  {{ slide.title }}
                </h1>
                <p class="index_public_carousel_subtitle index_public_slide_in_right">
                  {{ slide.subtitle }}
                </p>
              </div>
            </div>
          </div>

          <!-- Controles del carrusel -->
          <div class="index_public_carousel_controls">
            <button @click="prevSlide" aria-label="Anterior" class="index_public_carousel_btn">
              <span class="icon is-large"><i class="mdi mdi-chevron-left mdi-24px"></i></span>
            </button>
            <button @click="nextSlide" aria-label="Siguiente" class="index_public_carousel_btn">
              <span class="icon is-large"><i class="mdi mdi-chevron-right mdi-24px"></i></span>
            </button>
          </div>

          <!-- Indicadores -->
          <div class="index_public_carousel_indicators">
            <button 
              v-for="(slide, index) in slides" 
              :key="index"
              :class="{ 'is-active': currentSlide === index }"
              @click="goToSlide(index)"
              class="index_public_indicator"
              :aria-label="`Ir a slide ${index + 1}`">
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección Nosotros -->
    <section class="index_public_section" id="nosotros">
      <div class="index_public_container_content">
        <h2 class="index_public_section_title index_public_fade_in">
          <span class="icon-text">
            <span class="icon index_public_title_icon"><i class="mdi mdi-history mdi-36px"></i></span>
            <span>Nuestra Historia</span>
          </span>
        </h2>
        <div class="index_public_columns index_public_is_vcentered">
          <div class="index_public_column index_public_fade_in">
            <p class="index_public_text_large">
              Desde el <strong class="index_public_highlight">26 de Diciembre de 1953</strong>, la Cooperativa Minera Poopó R.L. 
              ha sido un pilar fundamental en la industria minera de Bolivia.
            </p>
            <p class="index_public_text_medium">
              Con más de 70 años de experiencia, nos dedicamos a la extracción responsable de minerales, 
              generando empleo y desarrollo para nuestras comunidades. Somos una cooperativa comprometida 
              con el bienestar de nuestros socios y el desarrollo sostenible de la región.
            </p>
            <div class="index_public_info_list">
              <div class="index_public_info_item">
                <i class="mdi mdi-calendar-check index_public_info_icon"></i>
                <div>
                  <strong>Fundada:</strong>
                  <span>26 de Diciembre de 1953</span>
                </div>
              </div>
              <div class="index_public_info_item">
                <i class="mdi mdi-map-marker index_public_info_icon"></i>
                <div>
                  <strong>Ubicación:</strong>
                  <span>Poopó, Oruro - Bolivia</span>
                </div>
              </div>
              <div class="index_public_info_item">
                <i class="mdi mdi-pickaxe index_public_info_icon"></i>
                <div>
                  <strong>Actividad:</strong>
                  <span>Minería responsable y sostenible</span>
                </div>
              </div>
              <div class="index_public_info_item">
                <i class="mdi mdi-account-group index_public_info_icon"></i>
                <div>
                  <strong>Socios:</strong>
                  <span>Más de 500 cooperativistas activos</span>
                </div>
              </div>
            </div>
          </div>
          <div class="index_public_column index_public_fade_in">
            <figure class="index_public_image_wrapper">
              <img src="https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800" 
                   alt="Minería" 
                   class="index_public_rounded_image">
            </figure>
          </div>
        </div>
      </div>
    </section>

    <!-- Estadísticas -->
    <section class="index_public_section index_public_bg_alt">
      <div class="index_public_container_content">
        <h2 class="index_public_section_title">Nuestros Números</h2>
        <div class="index_public_stats_grid">
          <div class="index_public_stat_card index_public_fade_in index_public_stat_blue">
            <div class="index_public_stat_icon">
              <i class="mdi mdi-calendar mdi-48px"></i>
            </div>
            <div class="index_public_stat_number">70+</div>
            <div class="index_public_stat_label">Años de Historia</div>
          </div>
          <div class="index_public_stat_card index_public_fade_in index_public_stat_green" style="animation-delay: 0.1s;">
            <div class="index_public_stat_icon">
              <i class="mdi mdi-account-group mdi-48px"></i>
            </div>
            <div class="index_public_stat_number">500+</div>
            <div class="index_public_stat_label">Cooperativistas</div>
          </div>
          <div class="index_public_stat_card index_public_fade_in index_public_stat_orange" style="animation-delay: 0.2s;">
            <div class="index_public_stat_icon">
              <i class="mdi mdi-chart-line mdi-48px"></i>
            </div>
            <div class="index_public_stat_number">100%</div>
            <div class="index_public_stat_label">Compromiso</div>
          </div>
          <div class="index_public_stat_card index_public_fade_in index_public_stat_purple" style="animation-delay: 0.3s;">
            <div class="index_public_stat_icon">
              <i class="mdi mdi-shield-check mdi-48px"></i>
            </div>
            <div class="index_public_stat_number">24/7</div>
            <div class="index_public_stat_label">Operación</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Misión y Visión -->
    <section class="index_public_section">
      <div class="index_public_container_content">
        <h2 class="index_public_section_title">Misión y Visión</h2>
        <div class="index_public_mission_vision">
          <div class="index_public_mv_card index_public_mv_mission">
            <div class="index_public_mv_header">
              <div class="index_public_mv_icon_wrapper">
                <i class="mdi mdi-target mdi-48px"></i>
              </div>
              <h3 class="index_public_mv_title">Misión</h3>
            </div>
            <p class="index_public_mv_text">
              Ser una cooperativa minera líder en Bolivia, comprometida con la extracción responsable y sostenible 
              de minerales, generando valor económico para nuestros socios y contribuyendo al desarrollo social 
              de nuestras comunidades. Promovemos prácticas seguras, tecnología moderna y respeto absoluto por 
              el medio ambiente, manteniendo los más altos estándares de calidad y ética profesional.
            </p>
          </div>
          <div class="index_public_mv_card index_public_mv_vision">
            <div class="index_public_mv_header">
              <div class="index_public_mv_icon_wrapper">
                <i class="mdi mdi-eye mdi-48px"></i>
              </div>
              <h3 class="index_public_mv_title">Visión</h3>
            </div>
            <p class="index_public_mv_text">
              Consolidarnos como la cooperativa minera más respetada y eficiente de la región, reconocida por 
              nuestra innovación tecnológica, compromiso social y responsabilidad ambiental. Aspiramos a ser un 
              modelo de gestión cooperativa que inspire a futuras generaciones, manteniendo viva la tradición 
              minera boliviana mientras construimos un futuro sostenible para todos nuestros cooperativistas.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Servicios -->
    <section class="index_public_section index_public_bg_alt" id="servicios">
      <div class="index_public_container_content">
        <h2 class="index_public_section_title">Nuestros Servicios</h2>
        <div class="index_public_services_grid">
          <div class="index_public_service_card index_public_fade_in index_public_service_yellow">
            <div class="index_public_service_icon">
              <i class="mdi mdi-hammer-screwdriver mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Extracción Minera</h3>
            <p class="index_public_service_text">Extracción responsable y sostenible de minerales con tecnología de punta y respeto al medio ambiente.</p>
          </div>
          <div class="index_public_service_card index_public_fade_in index_public_service_blue" style="animation-delay: 0.1s;">
            <div class="index_public_service_icon">
              <i class="mdi mdi-school mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Capacitación</h3>
            <p class="index_public_service_text">Programas de formación continua para nuestros cooperativistas en seguridad y técnicas modernas.</p>
          </div>
          <div class="index_public_service_card index_public_fade_in index_public_service_green" style="animation-delay: 0.2s;">
            <div class="index_public_service_icon">
              <i class="mdi mdi-handshake mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Apoyo Social</h3>
            <p class="index_public_service_text">Comprometidos con el bienestar de nuestros socios y el desarrollo de la comunidad.</p>
          </div>
          <div class="index_public_service_card index_public_fade_in index_public_service_teal" style="animation-delay: 0.3s;">
            <div class="index_public_service_icon">
              <i class="mdi mdi-leaf mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Medio Ambiente</h3>
            <p class="index_public_service_text">Prácticas mineras responsables que minimizan el impacto ambiental y promueven la sostenibilidad.</p>
          </div>
          <div class="index_public_service_card index_public_fade_in index_public_service_red" style="animation-delay: 0.4s;">
            <div class="index_public_service_icon">
              <i class="mdi mdi-shield-check mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Seguridad</h3>
            <p class="index_public_service_text">Protocolos de seguridad rigurosos para garantizar la integridad de nuestros cooperativistas.</p>
          </div>
          <div class="index_public_service_card index_public_fade_in index_public_service_purple" style="animation-delay: 0.5s;">
            <div class="index_public_service_icon">
              <i class="mdi mdi-cog mdi-48px"></i>
            </div>
            <h3 class="index_public_service_title">Tecnología</h3>
            <p class="index_public_service_text">Implementación de sistemas modernos de gestión y control para optimizar operaciones.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Galería -->
    <section class="index_public_section" id="galeria">
      <div class="index_public_container_content">
        <h2 class="index_public_section_title">
          <span class="icon-text">
            <span class="icon index_public_title_icon"><i class="mdi mdi-image-multiple mdi-36px"></i></span>
            <span>Galería</span>
          </span>
        </h2>
        <div class="index_public_gallery_grid">
          <div 
            v-for="(image, index) in galleryImages" 
            :key="index"
            class="index_public_gallery_item index_public_fade_in"
            :style="{ animationDelay: `${index * 0.1}s` }">
            <img :src="image.url" :alt="image.title" class="index_public_gallery_image">
            <div class="index_public_gallery_overlay">
              <div class="index_public_gallery_title">{{ image.title }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="index_public_cta">
      <div class="index_public_cta_background"></div>
      <div class="index_public_cta_content">
        <h2 class="index_public_cta_title index_public_fade_in">¿Eres Cooperativista?</h2>
        <p class="index_public_cta_subtitle index_public_fade_in">
          Accede al sistema de gestión para consultar tu información, dispositivos y más.
        </p>
        <NuxtLink to="/login" class="index_public_cta_btn index_public_fade_in">
          <span class="icon"><i class="mdi mdi-login"></i></span>
          <span>Iniciar Sesión Ahora</span>
        </NuxtLink>
      </div>
    </section>

    <!-- Footer -->
    <footer class="index_public_footer">
      <div class="index_public_footer_container">
        <div class="index_public_footer_grid">
          <div class="index_public_footer_column">
            <img src="/logo.jfif" alt="Logo" class="index_public_footer_logo">
            <h3 class="index_public_footer_title">Cooperativa Minera Poopó R.L.</h3>
            <p class="index_public_footer_text">
              Fundada el 26 de Diciembre de 1953<br>
              Más de 70 años de historia y compromiso con Bolivia.
            </p>
          </div>
          <div class="index_public_footer_column">
            <h3 class="index_public_footer_title">Contacto</h3>
            <div class="index_public_footer_links">
              <a href="#" class="index_public_footer_link">
                <span class="icon"><i class="mdi mdi-map-marker"></i></span>
                <span>Poopó, Oruro - Bolivia</span>
              </a>
              <a href="tel:+59121234567" class="index_public_footer_link">
                <span class="icon"><i class="mdi mdi-phone"></i></span>
                <span>+591 (2) 123-4567</span>
              </a>
              <a href="mailto:info@cooperativapoopo.bo" class="index_public_footer_link">
                <span class="icon"><i class="mdi mdi-email"></i></span>
                <span>info@cooperativapoopo.bo</span>
              </a>
            </div>
          </div>
          <div class="index_public_footer_column">
            <h3 class="index_public_footer_title">Enlaces Rápidos</h3>
            <div class="index_public_footer_links">
              <a href="#nosotros" class="index_public_footer_link">Nosotros</a>
              <a href="#servicios" class="index_public_footer_link">Servicios</a>
              <a href="#galeria" class="index_public_footer_link">Galería</a>
              <NuxtLink to="/login" class="index_public_footer_link">Iniciar Sesión</NuxtLink>
            </div>
          </div>
          <div class="index_public_footer_column">
            <h3 class="index_public_footer_title">Horarios</h3>
            <p class="index_public_footer_text">
              <strong>Operación Minera:</strong><br>
              24 horas, 7 días a la semana<br><br>
              <strong>Oficinas Administrativas:</strong><br>
              Lunes a Viernes: 8:00 - 18:00<br>
              Sábados: 8:00 - 13:00
            </p>
          </div>
        </div>
        <hr class="index_public_footer_divider">
        <div class="index_public_footer_bottom">
          <p class="index_public_footer_copyright">
            <strong>© 2025 Cooperativa Minera Poopó R.L.</strong> - Todos los derechos reservados.
          </p>
          <p class="index_public_footer_dedication">
            Este sistema no se hubiera podido realizar sin la gestión y el compromiso 
            de la Directiva 2025 de la Cooperativa Minera Poopó R.L.
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

// Imágenes de la galería
const galleryImages = ref([
  {
    url: 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=600',
    title: 'Instalaciones Mineras'
  },
  {
    url: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600',
    title: 'Equipo de Trabajo'
  },
  {
    url: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600',
    title: 'Operaciones Diarias'
  },
  {
    url: 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600',
    title: 'Extracción Responsable'
  },
  {
    url: 'https://images.unsplash.com/photo-1590845947670-c009801ffa74?w=600',
    title: 'Tecnología Avanzada'
  },
  {
    url: 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600',
    title: 'Seguridad Primero'
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
  title: 'Inicio - Cooperativa Minera Poopó R.L.',
  meta: [
    { name: 'description', content: 'Cooperativa Minera Poopó R.L. - Fundada el 26 de Diciembre de 1953. Más de 70 años de historia en la industria minera boliviana.' }
  ]
})
</script>

<style scoped>
/* ====================================
   BASE Y VARIABLES
   ==================================== */
.index_public_container {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(to bottom, #f8fdf8 0%, #ffffff 100%);
  color: #1a4d1a;
  min-height: 100vh;
}

/* ====================================
   NAVBAR
   ==================================== */
.index_public_navbar {
  background: white;
  box-shadow: 0 2px 15px rgba(46, 125, 50, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 2px solid #4caf50;
}

.index_public_navbar_container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.index_public_navbar_brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
}

.index_public_logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid #ffd700;
  transition: transform 0.3s;
}

.index_public_logo:hover {
  transform: scale(1.1);
}

.index_public_brand_text {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.index_public_navbar_burger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
}

.index_public_navbar_burger span {
  display: block;
  width: 25px;
  height: 3px;
  background: #2e7d32;
  margin: 5px 0;
  border-radius: 3px;
}

.index_public_navbar_menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.index_public_navbar_start {
  display: flex;
  gap: 1.5rem;
}

.index_public_nav_link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2e7d32;
  text-decoration: none;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s;
}

.index_public_nav_link:hover {
  background: #e8f5e9;
  color: #1b5e20;
}

.index_public_login_btn {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s;
}

.index_public_login_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

/* ====================================
   HERO / CAROUSEL
   ==================================== */
.index_public_carousel {
  position: relative;
  height: 600px;
  overflow: hidden;
}

.index_public_carousel_item {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1s;
}

.index_public_carousel_item.is-active {
  opacity: 1;
}

.index_public_carousel_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.8);
}

.index_public_hero_overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(232,245,233,0.85));
  display: flex;
  align-items: center;
  justify-content: center;
}

.index_public_carousel_content {
  text-align: center;
  padding: 2rem;
  max-width: 900px;
}

.index_public_carousel_title {
  font-size: 3.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.index_public_carousel_subtitle {
  font-size: 1.5rem;
  color: #1a4d1a;
  font-weight: 500;
}

.index_public_carousel_controls {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 2rem;
  transform: translateY(-50%);
}

.index_public_carousel_btn {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #4caf50;
  color: #2e7d32;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.index_public_carousel_btn:hover {
  background: #4caf50;
  color: white;
  transform: scale(1.1);
}

.index_public_carousel_indicators {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.75rem;
}

.index_public_indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(46, 125, 50, 0.4);
  border: 2px solid #4caf50;
  cursor: pointer;
  transition: all 0.3s;
  padding: 0;
}

.index_public_indicator.is-active {
  background: #4caf50;
  width: 40px;
  border-radius: 6px;
}

/* ====================================
   SECTIONS
   ==================================== */
.index_public_section {
  padding: 5rem 2rem;
}

.index_public_bg_alt {
  background: linear-gradient(135deg, #f1f8f4, #ffffff);
}

.index_public_container_content {
  max-width: 1280px;
  margin: 0 auto;
}

.index_public_section_title {
  font-size: 2.5rem;
  font-weight: 900;
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  padding-bottom: 1rem;
}

.index_public_section_title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, #2e7d32, #ffd700);
  border-radius: 2px;
}

/* ====================================
   COLUMNS / GRID
   ==================================== */
.index_public_columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.index_public_text_large {
  font-size: 1.3rem;
  color: #2e7d32;
  line-height: 1.8;
  margin-bottom: 1rem;
  font-weight: 500;
}

.index_public_highlight {
  color: #ffd700;
  font-weight: 800;
}

.index_public_text_medium {
  color: #1a4d1a;
  line-height: 1.8;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.index_public_info_list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.index_public_info_item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  border-left: 4px solid #4caf50;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
}

.index_public_info_item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
}

.index_public_info_icon {
  font-size: 1.5rem;
  color: #4caf50;
}

.index_public_info_item strong {
  color: #2e7d32;
  font-weight: 700;
}

.index_public_rounded_image {
  width: 100%;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(46, 125, 50, 0.2);
  transition: transform 0.3s;
}

.index_public_rounded_image:hover {
  transform: scale(1.03);
}

/* ====================================
   STATS
   ==================================== */
.index_public_stats_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.index_public_stat_card {
  background: white;
  border: 2px solid;
  border-radius: 15px;
  padding: 2.5rem 2rem;
  text-align: center;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.index_public_stat_card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.index_public_stat_blue {
  border-color: #2e7d32;
}

.index_public_stat_green {
  border-color: #4caf50;
}

.index_public_stat_orange {
  border-color: #ff9800;
}

.index_public_stat_purple {
  border-color: #9e9d24;
}

.index_public_stat_icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.index_public_stat_blue .index_public_stat_icon {
  color: #2e7d32;
}

.index_public_stat_green .index_public_stat_icon {
  color: #4caf50;
}

.index_public_stat_orange .index_public_stat_icon {
  color: #ff9800;
}

.index_public_stat_purple .index_public_stat_icon {
  color: #9e9d24;
}

.index_public_stat_number {
  font-size: 3rem;
  font-weight: 900;
  color: #1a4d1a;
  margin-bottom: 0.5rem;
}

.index_public_stat_label {
  font-size: 1.1rem;
  color: #2e7d32;
  font-weight: 600;
}

/* ====================================
   MISSION & VISION
   ==================================== */
.index_public_mission_vision {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.index_public_mv_card {
  background: white;
  border: 2px solid;
  border-radius: 15px;
  padding: 2.5rem;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.index_public_mv_card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.index_public_mv_mission {
  border-color: #ffd700;
}

.index_public_mv_vision {
  border-color: #4caf50;
}

.index_public_mv_header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.index_public_mv_icon_wrapper {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.index_public_mv_mission .index_public_mv_icon_wrapper {
  background: rgba(255, 215, 0, 0.2);
  color: #ff9800;
}

.index_public_mv_vision .index_public_mv_icon_wrapper {
  background: rgba(76, 175, 80, 0.2);
  color: #2e7d32;
}

.index_public_mv_title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1a4d1a;
}

.index_public_mv_text {
  color: #2e7d32;
  line-height: 1.8;
  font-size: 1.05rem;
}

/* ====================================
   SERVICES
   ==================================== */
.index_public_services_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.index_public_service_card {
  background: white;
  border: 2px solid;
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.index_public_service_card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.index_public_service_yellow {
  border-color: #ffc107;
}

.index_public_service_blue {
  border-color: #2e7d32;
}

.index_public_service_green {
  border-color: #4caf50;
}

.index_public_service_teal {
  border-color: #9e9d24;
}

.index_public_service_red {
  border-color: #ff9800;
}

.index_public_service_purple {
  border-color: #689f38;
}

.index_public_service_icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.index_public_service_yellow .index_public_service_icon {
  color: #ffc107;
}

.index_public_service_blue .index_public_service_icon {
  color: #2e7d32;
}

.index_public_service_green .index_public_service_icon {
  color: #4caf50;
}

.index_public_service_teal .index_public_service_icon {
  color: #9e9d24;
}

.index_public_service_red .index_public_service_icon {
  color: #ff9800;
}

.index_public_service_purple .index_public_service_icon {
  color: #689f38;
}

.index_public_service_title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a4d1a;
}

.index_public_service_text {
  color: #2e7d32;
  line-height: 1.7;
}

/* ====================================
   GALLERY
   ==================================== */
.index_public_gallery_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.index_public_gallery_item {
  position: relative;
  height: 280px;
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.index_public_gallery_item:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.index_public_gallery_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.index_public_gallery_item:hover .index_public_gallery_image {
  transform: scale(1.1);
}

.index_public_gallery_overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(255,255,255,0.95), transparent);
  padding: 1.5rem;
  transform: translateY(100%);
  transition: transform 0.3s;
}

.index_public_gallery_item:hover .index_public_gallery_overlay {
  transform: translateY(0);
}

.index_public_gallery_title {
  color: #2e7d32;
  font-weight: 800;
  font-size: 1.2rem;
}

/* ====================================
   CALL TO ACTION
   ==================================== */
.index_public_cta {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  padding: 5rem 2rem;
  text-align: center;
}

.index_public_cta_content {
  max-width: 800px;
  margin: 0 auto;
}

.index_public_cta_title {
  font-size: 3rem;
  font-weight: 900;
  background: linear-gradient(135deg, #2e7d32, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.index_public_cta_subtitle {
  font-size: 1.3rem;
  color: #1a4d1a;
  margin-bottom: 2rem;
}

.index_public_cta_btn {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  color: #1a4d1a;
  padding: 1rem 3rem;
  border-radius: 12px;
  border: none;
  font-size: 1.2rem;
  font-weight: 800;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s;
  text-decoration: none;
  box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
}

.index_public_cta_btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.5);
}

/* ====================================
   FOOTER
   ==================================== */
.index_public_footer {
  background: linear-gradient(135deg, #1a4d1a, #2e7d32);
  border-top: 3px solid #ffd700;
  padding: 3rem 2rem 2rem;
  color: white;
}

.index_public_footer_container {
  max-width: 1280px;
  margin: 0 auto;
}

.index_public_footer_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.index_public_footer_logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid #ffd700;
  margin-bottom: 1rem;
}

.index_public_footer_title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 1rem;
}

.index_public_footer_text {
  color: #e8f5e9;
  line-height: 1.7;
}

.index_public_footer_links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.index_public_footer_link {
  color: #c8e6c9;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.index_public_footer_link:hover {
  color: #ffd700;
  transform: translateX(5px);
}

.index_public_footer_divider {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, transparent, #ffd700, transparent);
  margin: 2rem 0;
}

.index_public_footer_bottom {
  text-align: center;
  color: #e8f5e9;
}

.index_public_footer_copyright {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.index_public_footer_dedication {
  color: #ffd700;
  font-style: italic;
  font-weight: 600;
}

/* ====================================
   ANIMATIONS
   ==================================== */
.index_public_fade_in {
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ====================================
   RESPONSIVE
   ==================================== */
@media (max-width: 1024px) {
  .index_public_columns,
  .index_public_mission_vision {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .index_public_navbar_burger {
    display: block;
  }

  .index_public_navbar_menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    padding: 1rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  .index_public_navbar_menu.is-active {
    display: block;
  }

  .index_public_navbar_start {
    flex-direction: column;
    width: 100%;
  }

  .index_public_nav_link,
  .index_public_login_btn {
    width: 100%;
    justify-content: center;
  }

  .index_public_carousel {
    height: 450px;
  }

  .index_public_carousel_title {
    font-size: 2rem;
  }

  .index_public_section_title {
    font-size: 2rem;
  }

  .index_public_services_grid,
  .index_public_gallery_grid {
    grid-template-columns: 1fr;
  }
}

/* ====================================
   UTILITY CLASSES
   ==================================== */
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.icon-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>