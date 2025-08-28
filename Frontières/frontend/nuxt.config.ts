// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Mode de développement - désactivé pour améliorer les performances
  devtools: { enabled: false },
  
  // Modules
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt'
  ],

  // Configuration des modules
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    configPath: 'tailwind.config.ts',
    exposeConfig: false,
    injectPosition: 0,
    viewer: false, // Désactivé pour améliorer les performances
  },

  // Configuration Pinia
  pinia: {
    autoImports: ['defineStore', 'acceptHMRUpdate']
  },

  // Configuration de l'application
  app: {
    head: {
      title: 'Millésime Sans Frontières - Premium Wine Barrels',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          hid: 'description', 
          name: 'description', 
          content: 'Discover our exclusive collection of premium wine barrels from around the world. Professional quality for winemakers, brewers and enthusiasts.' 
        },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { 
          rel: 'preconnect', 
          href: 'https://fonts.googleapis.com' 
        },
        { 
          rel: 'preconnect', 
          href: 'https://fonts.gstatic.com',
          crossorigin: '' 
        },
        { 
          rel: 'stylesheet', 
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap' 
        }
      ]
    }
  },

  // Configuration CSS - optimisée pour les performances
  css: [
    '~/assets/css/main.css'
  ],

  // Configuration des composants
  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],

  // Configuration des pages
  pages: true,

  // Configuration du router
  router: {
    options: {
      strict: false
    }
  },

  // Configuration des variables d'environnement
  runtimeConfig: {
    // Variables privées (côté serveur uniquement)
    apiSecret: process.env.API_SECRET,
    
    // Variables publiques (côté client et serveur)
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000',
      appName: 'Millésime Sans Frontières',
      appVersion: '1.0.0'
    }
  },

  // Configuration des imports automatiques
  imports: {
    dirs: ['composables/**', 'utils/**']
  },

  // Configuration TypeScript
  typescript: {
    typeCheck: false, // Désactivé pour améliorer les performances
    strict: false
  },

  // Configuration Nitro pour optimiser le serveur
  nitro: {
    compressPublicAssets: true,
    minify: true
  },

  // Configuration Vite pour optimiser le build
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['vue', 'vue-router'],
            ui: ['@headlessui/vue', '@heroicons/vue']
          }
        }
      }
    },
    optimizeDeps: {
      include: ['vue', 'vue-router', '@pinia/nuxt']
    }
  }
})
