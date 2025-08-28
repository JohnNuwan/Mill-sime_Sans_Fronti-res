import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}',
    './app.vue'
  ],
  theme: {
    extend: {
      // Couleurs personnalisées selon notre charte graphique
      colors: {
        // Couleurs principales
        'wine-red': {
          50: '#fdf2f3',
          100: '#fce7ea',
          200: '#f9d3d9',
          300: '#f4b3c0',
          400: '#ed8a9e',
          500: '#e25a7a',
          600: '#d13a5f',
          700: '#b12a4a',
          800: '#8B2635',
          900: '#5A1A23',
          950: '#3d0f17'
        },
        'oak-brown': {
          50: '#faf8f5',
          100: '#f4f0ea',
          200: '#e8dfd1',
          300: '#d8c7ad',
          400: '#c4a883',
          500: '#b08b5f',
          600: '#8B7355',
          700: '#A68B6B',
          800: '#5D4A3A',
          900: '#4a3b2e',
          950: '#2a2118'
        },
        'whisky-gold': {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#D4AF37',
          950: '#B8941F'
        },
        // Couleurs neutres
        'off-white': '#F8F6F3',
        'very-light-gray': '#F0EDE8',
        'light-gray': '#E0DCD5',
        'medium-gray': '#B8B3A8',
        'dark-gray': '#6B655C',
        'very-dark-gray': '#2C2A26',
        // Couleurs sémantiques
        'success': {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#28A745',
          600: '#16a34a',
          700: '#15803d'
        },
        'warning': {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#FF8C00',
          600: '#d97706',
          700: '#b45309'
        },
        'error': {
          50: '#fef2f2',
          100: '#fee2e2',
          500: '#DC3545',
          600: '#dc2626',
          700: '#b91c1c'
        },
        'info': {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#007BFF',
          600: '#2563eb',
          700: '#1d4ed8'
        }
      },
      // Typographie personnalisée
      fontFamily: {
        'primary': ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        'headings': ['Playfair Display', 'Georgia', 'serif'],
        'mono': ['JetBrains Mono', 'ui-monospace', 'monospace']
      },
      // Tailles de police personnalisées
      fontSize: {
        'xs': ['12px', { lineHeight: '1.4' }],
        'sm': ['14px', { lineHeight: '1.5' }],
        'base': ['16px', { lineHeight: '1.6' }],
        'lg': ['18px', { lineHeight: '1.6' }],
        'xl': ['20px', { lineHeight: '1.4' }],
        '2xl': ['24px', { lineHeight: '1.4' }],
        '3xl': ['36px', { lineHeight: '1.3' }],
        '4xl': ['48px', { lineHeight: '1.2' }]
      },
      // Espacement personnalisé (base 8px)
      spacing: {
        'xs': '4px',
        's': '8px',
        'm': '16px',
        'l': '24px',
        'xl': '32px',
        '2xl': '48px',
        '3xl': '64px'
      },
      // Bordures personnalisées
      borderRadius: {
        'xs': '4px',
        'sm': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px'
      },
      // Ombres personnalisées
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'medium': '0 4px 16px rgba(0, 0, 0, 0.15)',
        'large': '0 8px 32px rgba(0, 0, 0, 0.2)',
        'wine': '0 4px 12px rgba(139, 38, 53, 0.3)',
        'oak': '0 8px 32px rgba(139, 115, 85, 0.1)'
      },
      // Transitions personnalisées
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
      },
      // Breakpoints personnalisés
      screens: {
        'xs': '320px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1440px'
      },
      // Container personnalisé
      container: {
        center: true,
        padding: {
          DEFAULT: '1rem',
          sm: '2rem',
          lg: '2rem',
          xl: '2rem',
          '2xl': '2rem'
        },
        screens: {
          sm: '640px',
          md: '768px',
          lg: '1024px',
          xl: '1280px',
          '2xl': '1440px'
        }
      }
    }
  },
  plugins: [
    // Plugin pour les composants personnalisés
    function({ addComponents, theme }) {
      addComponents({
        '.btn-primary': {
          backgroundColor: theme('colors.wine-red.800'),
          color: theme('colors.white'),
          padding: '12px 24px',
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          fontSize: theme('fontSize.base'),
          border: 'none',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          '&:hover': {
            backgroundColor: theme('colors.wine-red.900'),
            transform: 'translateY(-1px)',
            boxShadow: theme('boxShadow.wine')
          }
        },
        '.btn-secondary': {
          backgroundColor: 'transparent',
          color: theme('colors.wine-red.800'),
          padding: '12px 24px',
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          fontSize: theme('fontSize.base'),
          border: `2px solid ${theme('colors.wine-red.800')}`,
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          '&:hover': {
            backgroundColor: theme('colors.wine-red.800'),
            color: theme('colors.white')
          }
        },
        '.btn-accent': {
          backgroundColor: theme('colors.whisky-gold.900'),
          color: theme('colors.very-dark-gray'),
          padding: '12px 24px',
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          fontSize: theme('fontSize.base'),
          border: 'none',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          '&:hover': {
            backgroundColor: theme('colors.whisky-gold.950'),
            transform: 'translateY(-1px)'
          }
        }
      })
    }
  ]
} satisfies Config
