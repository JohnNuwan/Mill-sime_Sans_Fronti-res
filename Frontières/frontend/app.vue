<template>
  <div id="app">
    <AppNavigation />
    <main class="main-content">
      <NuxtPage />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
// This file serves as the main app layout
// The navigation and footer will appear on all pages
</script>

<style>
@import './assets/responsive.css';

/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--color-oak-brown-900);
  background-color: white;
}

/* CSS Variables for colors */
:root {
  --color-wine-red-50: #fef2f2;
  --color-wine-red-100: #fee2e2;
  --color-wine-red-200: #fecaca;
  --color-wine-red-300: #fca5a5;
  --color-wine-red-400: #f87171;
  --color-wine-red-500: #ef4444;
  --color-wine-red-600: #dc2626;
  --color-wine-red-700: #b91c1c;
  --color-wine-red-800: #991b1b;
  --color-wine-red-900: #7f1d1d;

  --color-oak-brown-50: #fafaf9;
  --color-oak-brown-100: #f5f5f4;
  --color-oak-brown-200: #e7e5e4;
  --color-oak-brown-300: #d6d3d1;
  --color-oak-brown-400: #a8a29e;
  --color-oak-brown-500: #78716c;
  --color-oak-brown-600: #57534e;
  --color-oak-brown-700: #44403c;
  --color-oak-brown-800: #292524;
  --color-oak-brown-900: #1c1917;

  --color-whisky-gold-50: #fffbeb;
  --color-whisky-gold-100: #fef3c7;
  --color-whisky-gold-200: #fde68a;
  --color-whisky-gold-300: #fcd34d;
  --color-whisky-gold-400: #fbbf24;
  --color-whisky-gold-500: #f59e0b;
  --color-whisky-gold-600: #d97706;
  --color-whisky-gold-700: #b45309;
  --color-whisky-gold-800: #92400e;
  --color-whisky-gold-900: #78350f;

  --color-cream-50: #fefefe;
  --color-cream-100: #fdfcfb;
  --color-cream-200: #f9f8f6;
  --color-cream-300: #f3f2f0;
  --color-cream-400: #e8e6e1;
  --color-cream-500: #d4cfc7;
  --color-cream-600: #b8b2a8;
  --color-cream-700: #9c9589;
  --color-cream-800: #807a6e;
  --color-cream-900: #645f55;

  --transition-normal: 0.3s ease;
  --transition-fast: 0.15s ease;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Main content area */
.main-content {
  margin-top: 80px; /* Account for fixed header */
  min-height: calc(100vh - 80px - 400px); /* Viewport height minus header and footer */
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  line-height: 1.2;
}

h1 {
  font-size: 3rem;
}

h2 {
  font-size: 2.5rem;
}

h3 {
  font-size: 2rem;
}

h4 {
  font-size: 1.5rem;
}

h5 {
  font-size: 1.25rem;
}

h6 {
  font-size: 1rem;
}

p {
  margin-bottom: 1rem;
}

/* Button styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all var(--transition-normal);
  cursor: pointer;
  border: none;
  font-family: inherit;
}

.btn--primary {
  background: var(--color-wine-red-600);
  color: white;
}

.btn--primary:hover {
  background: var(--color-wine-red-700);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn--secondary {
  background: var(--color-oak-brown-600);
  color: white;
}

.btn--secondary:hover {
  background: var(--color-oak-brown-700);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn--accent {
  background: var(--color-whisky-gold-500);
  color: var(--color-oak-brown-900);
}

.btn--accent:hover {
  background: var(--color-whisky-gold-400);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn--large {
  padding: 1rem 2rem;
  font-size: 1rem;
}

/* Utility classes */
.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-5 { margin-bottom: 1.25rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-8 { margin-bottom: 2rem; }
.mb-10 { margin-bottom: 2.5rem; }
.mb-12 { margin-bottom: 3rem; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mt-5 { margin-top: 1.25rem; }
.mt-6 { margin-top: 1.5rem; }
.mt-8 { margin-top: 2rem; }
.mt-10 { margin-top: 2.5rem; }
.mt-12 { margin-top: 3rem; }

/* Responsive utilities */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  h2 {
    font-size: 2rem;
  }
  
  h3 {
    font-size: 1.75rem;
  }
  
  .main-content {
    margin-top: 70px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.75rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  h2 {
    font-size: 1.75rem;
  }
  
  h3 {
    font-size: 1.5rem;
  }
}
</style>
