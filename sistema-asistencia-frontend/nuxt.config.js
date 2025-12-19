export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  
  modules: [
    '@pinia/nuxt',
    '@vueuse/nuxt'
  ],

  runtimeConfig: {
    public: {
      apiBaseUrl: 'http://localhost:8000'
    }
  },

  app: {
    head: {
      title: 'Cooperativa Minera Poopó R.L.',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Sistema de gestión de cooperativistas - Cooperativa Minera Poopó R.L. - Fundada 26 de Diciembre de 1953' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/logo.jfif' },
      ]
    }
  },

  css: [
    'bulma/css/bulma.min.css',
    '~/assets/styles/main.scss',
    '@fortawesome/fontawesome-free/css/all.min.css',
    '@mdi/font/css/materialdesignicons.min.css'
  ]
})