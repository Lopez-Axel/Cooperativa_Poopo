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
   VARIABLES Y BASE
   ==================================== */
.index_public_container {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(to bottom, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
  color: #e8f5e9;
  min-height: 100vh;
}

/* ====================================
   HEADER / NAVBAR
   ==================================== */
.index_public_navbar {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1a2e1a 100%);
  box-shadow: 0 4px 30px rgba(76, 175, 80, 0.2), 0 0 60px rgba(255, 215, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 3px solid transparent;
  border-image: linear-gradient(90deg, #2e7d32, #ffd700, #9e9d24, #2e7d32) 1;
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
  justify-content: space-between;
  width: 100%;
}

.index_public_navbar_item {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
}

.index_public_logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5), 0 0 40px rgba(158, 157, 36, 0.3);
  transition: all 0.3s ease;
}

.index_public_logo:hover {
  transform: rotate(360deg) scale(1.1);
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 0 0 60px rgba(158, 157, 36, 0.5);
}

.index_public_brand_text {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffd700 0%, #ffa000 50%, #ff6f00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
  letter-spacing: 0.5px;
}

.index_public_navbar_burger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.index_public_navbar_burger span {
  display: block;
  width: 25px;
  height: 3px;
  background: linear-gradient(90deg, #ffd700, #9e9d24);
  margin: 5px 0;
  transition: all 0.3s ease;
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
  align-items: center;
}

.index_public_nav_link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a5d6a7;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.index_public_nav_link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(158, 157, 36, 0.3), transparent);
  transition: left 0.5s ease;
}

.index_public_nav_link:hover::before {
  left: 100%;
}

.index_public_nav_link:hover {
  background: linear-gradient(135deg, rgba(102, 187, 106, 0.2), rgba(158, 157, 36, 0.2));
  color: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(158, 157, 36, 0.3);
}

.index_public_navbar_end {
  display: flex;
}

.index_public_navbar_item {
  display: flex;
}

.index_public_buttons {
  display: flex;
}

.index_public_login_btn {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  padding: 0.75rem 1.75rem;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.4s ease;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4), 0 0 40px rgba(255, 152, 0, 0.2);
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.index_public_login_btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.index_public_login_btn:hover::before {
  width: 300px;
  height: 300px;
}

.index_public_login_btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 30px rgba(255, 215, 0, 0.6), 0 0 60px rgba(255, 152, 0, 0.4);
}

/* ====================================
   HERO / CAROUSEL
   ==================================== */
.index_public_hero {
  position: relative;
  overflow: hidden;
}

.index_public_hero_body {
  padding: 0;
}

.index_public_carousel {
  position: relative;
  height: 650px;
  overflow: hidden;
}

.index_public_carousel_item {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1.2s ease-in-out;
}

.index_public_carousel_item.is-active {
  opacity: 1;
  z-index: 1;
}

.index_public_carousel_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7);
}

.index_public_hero_overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(13, 27, 13, 0.9) 0%, 
    rgba(26, 46, 26, 0.85) 25%,
    rgba(30, 70, 30, 0.8) 50%,
    rgba(26, 46, 26, 0.85) 75%,
    rgba(13, 27, 13, 0.9) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.index_public_carousel_content {
  text-align: center;
  padding: 2rem;
  max-width: 900px;
}

.index_public_carousel_title {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.5);
  letter-spacing: 1px;
}

.index_public_carousel_subtitle {
  font-size: 1.75rem;
  color: #e0f2f1;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.8), 0 0 40px rgba(158, 157, 36, 0.3);
  font-weight: 500;
  letter-spacing: 0.5px;
}

.index_public_carousel_controls {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 2rem;
  transform: translateY(-50%);
  z-index: 3;
}

.index_public_carousel_btn {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.25), rgba(158, 157, 36, 0.25));
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 215, 0, 0.6);
  color: #ffd700;
  width: 55px;
  height: 55px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.index_public_carousel_btn:hover {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.5), rgba(158, 157, 36, 0.5));
  transform: scale(1.15);
  border-color: #9e9d24;
  box-shadow: 0 6px 30px rgba(158, 157, 36, 0.5);
}

.index_public_carousel_indicators {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.75rem;
  z-index: 3;
}

.index_public_indicator {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  border: 2px solid rgba(255, 215, 0, 0.6);
  cursor: pointer;
  transition: all 0.4s ease;
  padding: 0;
}

.index_public_indicator:hover {
  background: rgba(255, 215, 0, 0.6);
  transform: scale(1.2);
}

.index_public_indicator.is-active {
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  width: 45px;
  border-radius: 8px;
  border-color: #9e9d24;
  box-shadow: 0 0 15px rgba(158, 157, 36, 0.6);
}

/* ====================================
   SECTIONS
   ==================================== */
.index_public_section {
  padding: 6rem 2rem;
  position: relative;
}

.index_public_bg_alt {
  background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 50%, #1e461e 100%);
  position: relative;
}

.index_public_bg_alt::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(158, 157, 36, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.index_public_container_content {
  max-width: 1280px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.index_public_section_title {
  font-size: 3rem;
  font-weight: 900;
  text-align: center;
  margin-bottom: 4rem;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 30%, #9e9d24 60%, #4caf50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 30px rgba(255, 215, 0, 0.4);
  letter-spacing: 1px;
  position: relative;
  display: inline-block;
  width: 100%;
}

.index_public_section_title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, #ffd700, #9e9d24, #4caf50);
  border-radius: 2px;
  box-shadow: 0 0 20px rgba(158, 157, 36, 0.5);
}

.index_public_title_icon {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ====================================
   COLUMNS / GRID
   ==================================== */
.index_public_columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.index_public_column {
  position: relative;
}

.index_public_text_large {
  font-size: 1.4rem;
  color: #c8e6c9;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.index_public_highlight {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-size: 1.5rem;
}

.index_public_text_medium {
  color: #a5d6a7;
  line-height: 1.9;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.index_public_info_list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.index_public_info_item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(30, 70, 30, 0.2));
  border-radius: 12px;
  border-left: 4px solid;
  border-image: linear-gradient(180deg, #ffd700, #9e9d24) 1;
  transition: all 0.3s ease;
}

.index_public_info_item:hover {
  transform: translateX(10px);
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(30, 70, 30, 0.3));
  box-shadow: 0 4px 20px rgba(158, 157, 36, 0.3);
}

.index_public_info_icon {
  font-size: 2rem;
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.index_public_info_item strong {
  color: #ffd700;
  margin-right: 0.5rem;
  font-weight: 700;
}

.index_public_info_item span {
  color: #b0bec5;
}

.index_public_image_wrapper {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
}

.index_public_rounded_image {
  width: 100%;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(158, 157, 36, 0.3), 0 0 100px rgba(255, 215, 0, 0.2);
  border: 3px solid transparent;
  background: linear-gradient(#0a1a0a, #0a1a0a) padding-box,
              linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) border-box;
  transition: all 0.4s ease;
}

.index_public_rounded_image:hover {
  transform: scale(1.05) rotate(2deg);
  box-shadow: 0 25px 80px rgba(158, 157, 36, 0.5), 0 0 120px rgba(255, 215, 0, 0.3);
}

/* ====================================
   STATS
   ==================================== */
.index_public_stats_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2.5rem;
}

.index_public_stat_card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.6), rgba(15, 31, 15, 0.6));
  border: 3px solid;
  border-radius: 24px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.index_public_stat_card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  transform: scale(0);
  transition: transform 0.6s ease;
}

.index_public_stat_card:hover::before {
  transform: scale(1);
}

.index_public_stat_card:hover {
  transform: translateY(-15px) scale(1.05);
}

/* Colores modificados para usar solo verdes y amarillos */
.index_public_stat_blue {
  border-color: #2e7d32;
  box-shadow: 0 10px 40px rgba(46, 125, 50, 0.3);
}

.index_public_stat_blue:hover {
  box-shadow: 0 20px 60px rgba(46, 125, 50, 0.5);
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(15, 31, 15, 0.6));
}

.index_public_stat_green {
  border-color: #4caf50;
  box-shadow: 0 10px 40px rgba(76, 175, 80, 0.3);
}

.index_public_stat_green:hover {
  box-shadow: 0 20px 60px rgba(76, 175, 80, 0.5);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(15, 31, 15, 0.6));
}

.index_public_stat_orange {
  border-color: #ff9800;
  box-shadow: 0 10px 40px rgba(255, 152, 0, 0.3);
}

.index_public_stat_orange:hover {
  box-shadow: 0 20px 60px rgba(255, 152, 0, 0.5);
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.2), rgba(15, 31, 15, 0.6));
}

.index_public_stat_purple {
  border-color: #9e9d24;
  box-shadow: 0 10px 40px rgba(158, 157, 36, 0.3);
}

.index_public_stat_purple:hover {
  box-shadow: 0 20px 60px rgba(158, 157, 36, 0.5);
  background: linear-gradient(135deg, rgba(158, 157, 36, 0.2), rgba(15, 31, 15, 0.6));
}

.index_public_stat_icon {
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
}

.index_public_stat_blue .index_public_stat_icon {
  color: #4caf50;
  filter: drop-shadow(0 0 15px rgba(46, 125, 50, 0.6));
}

.index_public_stat_green .index_public_stat_icon {
  color: #66bb6a;
  filter: drop-shadow(0 0 15px rgba(76, 175, 80, 0.6));
}

.index_public_stat_orange .index_public_stat_icon {
  color: #ffb74d;
  filter: drop-shadow(0 0 15px rgba(255, 152, 0, 0.6));
}

.index_public_stat_purple .index_public_stat_icon {
  color: #cddc39;
  filter: drop-shadow(0 0 15px rgba(158, 157, 36, 0.6));
}

.index_public_stat_number {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.index_public_stat_blue .index_public_stat_number {
  color: #66bb6a;
  text-shadow: 0 4px 30px rgba(46, 125, 50, 0.6);
}

.index_public_stat_green .index_public_stat_number {
  color: #81c784;
  text-shadow: 0 4px 30px rgba(76, 175, 80, 0.6);
}

.index_public_stat_orange .index_public_stat_number {
  color: #ffb74d;
  text-shadow: 0 4px 30px rgba(255, 152, 0, 0.6);
}

.index_public_stat_purple .index_public_stat_number {
  color: #cddc39;
  text-shadow: 0 4px 30px rgba(158, 157, 36, 0.6);
}

.index_public_stat_label {
  font-size: 1.2rem;
  color: #e0f2f1;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

/* ====================================
   MISSION & VISION
   ==================================== */
.index_public_mission_vision {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-top: 3rem;
}

.index_public_mv_card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.7));
  border: 3px solid;
  border-radius: 24px;
  padding: 3rem;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.index_public_mv_card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
  transition: all 0.6s ease;
  opacity: 0;
}

.index_public_mv_card:hover::before {
  opacity: 1;
  transform: scale(1.2);
}

.index_public_mv_mission {
  border-color: #9e9d24;
  box-shadow: 0 15px 50px rgba(158, 157, 36, 0.3);
}

.index_public_mv_mission:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 70px rgba(158, 157, 36, 0.5);
  border-color: #cddc39;
}

.index_public_mv_vision {
  border-color: #2e7d32;
  box-shadow: 0 15px 50px rgba(46, 125, 50, 0.3);
}

.index_public_mv_vision:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 70px rgba(46, 125, 50, 0.5);
  border-color: #4caf50;
}

.index_public_mv_header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.index_public_mv_icon_wrapper {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.index_public_mv_mission .index_public_mv_icon_wrapper {
  background: linear-gradient(135deg, rgba(158, 157, 36, 0.3), rgba(30, 70, 30, 0.3));
  border: 2px solid #9e9d24;
  box-shadow: 0 0 30px rgba(158, 157, 36, 0.4);
}

.index_public_mv_mission .index_public_mv_icon_wrapper i {
  color: #cddc39;
  filter: drop-shadow(0 0 10px rgba(158, 157, 36, 0.8));
}

.index_public_mv_vision .index_public_mv_icon_wrapper {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.3), rgba(30, 70, 30, 0.3));
  border: 2px solid #2e7d32;
  box-shadow: 0 0 30px rgba(46, 125, 50, 0.4);
}

.index_public_mv_vision .index_public_mv_icon_wrapper i {
  color: #4caf50;
  filter: drop-shadow(0 0 10px rgba(46, 125, 50, 0.8));
}

.index_public_mv_title {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0;
}

.index_public_mv_mission .index_public_mv_title {
  background: linear-gradient(135deg, #9e9d24, #cddc39);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.index_public_mv_vision .index_public_mv_title {
  background: linear-gradient(135deg, #2e7d32, #4caf50);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.index_public_mv_text {
  color: #b0bec5;
  line-height: 2;
  font-size: 1.15rem;
  text-align: justify;
}

/* ====================================
   SERVICES
   ==================================== */
.index_public_services_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem;
}

.index_public_service_card {
  background: linear-gradient(135deg, rgba(26, 46, 26, 0.7), rgba(15, 31, 15, 0.7));
  border: 3px solid;
  border-radius: 20px;
  padding: 2.5rem;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.index_public_service_card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, transparent, currentColor, transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.index_public_service_card:hover::after {
  transform: translateX(100%);
}

.index_public_service_card:hover {
  transform: translateY(-15px) scale(1.03);
}

/* Colores de servicios modificados para usar solo verdes y amarillos */
.index_public_service_yellow {
  border-color: #ffc107;
  box-shadow: 0 10px 40px rgba(255, 193, 7, 0.3);
}

.index_public_service_yellow:hover {
  box-shadow: 0 20px 60px rgba(255, 193, 7, 0.5);
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_blue {
  border-color: #2e7d32;
  box-shadow: 0 10px 40px rgba(46, 125, 50, 0.3);
}

.index_public_service_blue:hover {
  box-shadow: 0 20px 60px rgba(46, 125, 50, 0.5);
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_green {
  border-color: #4caf50;
  box-shadow: 0 10px 40px rgba(76, 175, 80, 0.3);
}

.index_public_service_green:hover {
  box-shadow: 0 20px 60px rgba(76, 175, 80, 0.5);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_teal {
  border-color: #9e9d24;
  box-shadow: 0 10px 40px rgba(158, 157, 36, 0.3);
}

.index_public_service_teal:hover {
  box-shadow: 0 20px 60px rgba(158, 157, 36, 0.5);
  background: linear-gradient(135deg, rgba(158, 157, 36, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_red {
  border-color: #ff9800;
  box-shadow: 0 10px 40px rgba(255, 152, 0, 0.3);
}

.index_public_service_red:hover {
  box-shadow: 0 20px 60px rgba(255, 152, 0, 0.5);
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_purple {
  border-color: #689f38;
  box-shadow: 0 10px 40px rgba(104, 159, 56, 0.3);
}

.index_public_service_purple:hover {
  box-shadow: 0 20px 60px rgba(104, 159, 56, 0.5);
  background: linear-gradient(135deg, rgba(104, 159, 56, 0.15), rgba(15, 31, 15, 0.7));
}

.index_public_service_icon {
  margin-bottom: 1.5rem;
}

.index_public_service_yellow .index_public_service_icon {
  color: #ffc107;
  filter: drop-shadow(0 0 20px rgba(255, 193, 7, 0.6));
}

.index_public_service_blue .index_public_service_icon {
  color: #2e7d32;
  filter: drop-shadow(0 0 20px rgba(46, 125, 50, 0.6));
}

.index_public_service_green .index_public_service_icon {
  color: #4caf50;
  filter: drop-shadow(0 0 20px rgba(76, 175, 80, 0.6));
}

.index_public_service_teal .index_public_service_icon {
  color: #9e9d24;
  filter: drop-shadow(0 0 20px rgba(158, 157, 36, 0.6));
}

.index_public_service_red .index_public_service_icon {
  color: #ff9800;
  filter: drop-shadow(0 0 20px rgba(255, 152, 0, 0.6));
}

.index_public_service_purple .index_public_service_icon {
  color: #689f38;
  filter: drop-shadow(0 0 20px rgba(104, 159, 56, 0.6));
}

.index_public_service_title {
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #e0f2f1;
}

.index_public_service_text {
  color: #b0bec5;
  line-height: 1.8;
  font-size: 1.05rem;
}

/* ====================================
   GALLERY
   ==================================== */
.index_public_gallery_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.index_public_gallery_item {
  position: relative;
  height: 280px;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 3px solid transparent;
  background: linear-gradient(#0a1a0a, #0a1a0a) padding-box,
              linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700, #689f38) border-box;
}

.index_public_gallery_item:hover {
  transform: scale(1.08) rotate(2deg);
  box-shadow: 0 20px 60px rgba(158, 157, 36, 0.5), 0 0 100px rgba(255, 215, 0, 0.3);
}

.index_public_gallery_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.5s ease;
  filter: brightness(0.8);
}

.index_public_gallery_item:hover .index_public_gallery_image {
  transform: scale(1.2);
  filter: brightness(0.6);
}

.index_public_gallery_overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, 
    rgba(13, 27, 13, 0.98) 0%, 
    rgba(30, 70, 30, 0.9) 50%,
    transparent 100%);
  padding: 2rem 1.5rem;
  transform: translateY(100%);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.index_public_gallery_item:hover .index_public_gallery_overlay {
  transform: translateY(0);
}

.index_public_gallery_title {
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-size: 1.3rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

/* ====================================
   CALL TO ACTION
   ==================================== */
.index_public_cta {
  background: linear-gradient(135deg, #2e7d32 0%, #1e461e 50%, #1b5e20 100%);
  padding: 6rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.index_public_cta_background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(255, 215, 0, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(158, 157, 36, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(104, 159, 56, 0.1) 0%, transparent 70%);
  animation: index_public_float 20s infinite linear;
}

.index_public_cta_content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.index_public_cta_title {
  font-size: 3.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  text-shadow: 0 4px 30px rgba(255, 215, 0, 0.5);
}

.index_public_cta_subtitle {
  font-size: 1.5rem;
  color: #e0f2f1;
  margin-bottom: 3rem;
  line-height: 1.6;
  font-weight: 500;
}

.index_public_cta_btn {
  background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
  color: #0d1b0d;
  padding: 1.25rem 3.5rem;
  border-radius: 15px;
  border: none;
  font-size: 1.3rem;
  font-weight: 800;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 40px rgba(255, 215, 0, 0.5), 0 0 80px rgba(255, 152, 0, 0.3);
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.index_public_cta_btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.index_public_cta_btn:hover::before {
  width: 400px;
  height: 400px;
}

.index_public_cta_btn:hover {
  transform: translateY(-8px) scale(1.08);
  box-shadow: 0 15px 60px rgba(255, 215, 0, 0.7), 0 0 120px rgba(255, 152, 0, 0.5);
}

/* ====================================
   FOOTER
   ==================================== */
.index_public_footer {
  background: linear-gradient(135deg, #0d1b0d 0%, #050a05 50%, #0d1b0d 100%);
  border-top: 3px solid transparent;
  border-image: linear-gradient(90deg, #2e7d32, #9e9d24, #ffd700, #689f38, #2e7d32) 1;
  padding: 4rem 2rem 2rem;
  position: relative;
}

.index_public_footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: radial-gradient(ellipse at top, rgba(158, 157, 36, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.index_public_footer_container {
  max-width: 1280px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.index_public_footer_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.index_public_footer_column {
  position: relative;
}

.index_public_footer_logo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid transparent;
  background: linear-gradient(#050a05, #050a05) padding-box,
              linear-gradient(135deg, #ffd700, #9e9d24, #689f38) border-box;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 40px rgba(255, 215, 0, 0.4), 0 0 80px rgba(158, 157, 36, 0.3);
  transition: all 0.4s ease;
}

.index_public_footer_logo:hover {
  transform: rotate(360deg) scale(1.1);
  box-shadow: 0 0 60px rgba(255, 215, 0, 0.6), 0 0 120px rgba(158, 157, 36, 0.5);
}

.index_public_footer_title {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
}

.index_public_footer_text {
  color: #b0bec5;
  line-height: 1.9;
  font-size: 1.05rem;
}

.index_public_footer_text strong {
  background: linear-gradient(135deg, #ffd700, #ff9800);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.index_public_footer_links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.index_public_footer_link {
  color: #90a4ae;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.index_public_footer_link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background: linear-gradient(180deg, #ffd700, #9e9d24);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.index_public_footer_link:hover::before {
  transform: scaleY(1);
}

.index_public_footer_link:hover {
  color: #ffd700;
  transform: translateX(10px);
  background: rgba(158, 157, 36, 0.1);
}

.index_public_footer_link .icon {
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.index_public_footer_link:hover .icon {
  transform: scale(1.2) rotate(360deg);
}

.index_public_footer_divider {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(46, 125, 50, 0.5), 
    rgba(158, 157, 36, 0.5), 
    rgba(255, 215, 0, 0.5), 
    rgba(104, 159, 56, 0.5),
    transparent);
  margin: 3rem 0;
  position: relative;
}

.index_public_footer_divider::after {
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(158, 157, 36, 0.6);
}

.index_public_footer_bottom {
  text-align: center;
  color: #90a4ae;
}

.index_public_footer_copyright {
  font-weight: 700;
  color: #b0bec5;
  margin-bottom: 1rem;
  font-size: 1.05rem;
}

.index_public_footer_copyright strong {
  background: linear-gradient(135deg, #ffd700, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.index_public_footer_dedication {
  background: linear-gradient(135deg, #ffd700, #ff9800, #9e9d24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-style: italic;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto;
}

/* ====================================
   ANIMATIONS
   ==================================== */
@keyframes index_public_slide_in_left {
  from {
    opacity: 0;
    transform: translateX(-80px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes index_public_slide_in_right {
  from {
    opacity: 0;
    transform: translateX(80px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes index_public_fade_in {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes index_public_float {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-100px);
  }
}

.index_public_slide_in_left {
  animation: index_public_slide_in_left 1s ease-out;
}

.index_public_slide_in_right {
  animation: index_public_slide_in_right 1s ease-out 0.2s both;
}

.index_public_fade_in {
  animation: index_public_fade_in 0.8s ease-out both;
}

/* ====================================
   RESPONSIVE
   ==================================== */
@media (max-width: 1024px) {
  .index_public_columns {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .index_public_mission_vision {
    grid-template-columns: 1fr;
  }

  .index_public_carousel_title {
    font-size: 3rem;
  }

  .index_public_carousel_subtitle {
    font-size: 1.4rem;
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
    background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 100%);
    padding: 1.5rem;
    border-top: 2px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  }

  .index_public_navbar_menu.is-active {
    display: block;
  }

  .index_public_navbar_start {
    flex-direction: column;
    width: 100%;
  }

  .index_public_nav_link {
    width: 100%;
    justify-content: center;
    padding: 1rem;
  }

  .index_public_navbar_end {
    margin-top: 1rem;
    width: 100%;
  }

  .index_public_login_btn {
    width: 100%;
    justify-content: center;
  }

  .index_public_carousel {
    height: 500px;
  }

  .index_public_carousel_title {
    font-size: 2.2rem;
  }

  .index_public_carousel_subtitle {
    font-size: 1.1rem;
  }

  .index_public_section_title {
    font-size: 2.2rem;
  }

  .index_public_text_large {
    font-size: 1.2rem;
  }

  .index_public_stats_grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }

  .index_public_services_grid {
    grid-template-columns: 1fr;
  }

  .index_public_gallery_grid {
    grid-template-columns: 1fr;
  }

  .index_public_cta_title {
    font-size: 2.5rem;
  }

  .index_public_cta_subtitle {
    font-size: 1.2rem;
  }

  .index_public_footer_grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

@media (max-width: 480px) {
  .index_public_brand_text {
    font-size: 0.9rem;
  }

  .index_public_logo {
    width: 50px;
    height: 50px;
  }

  .index_public_carousel {
    height: 400px;
  }

  .index_public_carousel_title {
    font-size: 1.8rem;
  }

  .index_public_carousel_subtitle {
    font-size: 1rem;
  }

  .index_public_section {
    padding: 4rem 1.5rem;
  }

  .index_public_section_title {
    font-size: 1.8rem;
  }

  .index_public_stat_number {
    font-size: 2.5rem;
  }

  .index_public_cta_title {
    font-size: 2rem;
  }

  .index_public_cta_btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
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

.is-large {
  font-size: 2rem;
}
</style>