<template>
  <div class="mobile-test">
    <!-- Header avec navigation -->
    <AppNavigation />
    
    <!-- Contenu de test -->
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">Test du Menu Mobile</h1>
        <p class="page-description">
          Cette page permet de tester le fonctionnement du menu hamburger (3 traits) sur mobile.
        </p>
        
        <div class="test-instructions">
          <h2>Instructions de test :</h2>
          <ol>
            <li>Redimensionnez votre navigateur à moins de 768px de largeur</li>
            <li>Vous devriez voir le bouton hamburger (3 traits) apparaître</li>
            <li>Cliquez sur le bouton pour ouvrir le menu mobile</li>
            <li>Le menu devrait s'ouvrir avec une animation fluide</li>
            <li>Cliquez sur un lien pour naviguer et fermer le menu</li>
          </ol>
        </div>
        
        <div class="test-features">
          <h2>Fonctionnalités testées :</h2>
          <ul>
            <li>✅ Bouton hamburger visible sur mobile</li>
            <li>✅ Menu s'ouvre et se ferme correctement</li>
            <li>✅ Animation fluide d'ouverture/fermeture</li>
            <li>✅ Navigation fonctionnelle</li>
            <li>✅ Fermeture automatique après clic</li>
            <li>✅ Support tactile (44px minimum)</li>
          </ul>
        </div>
        
        <div class="responsive-demo">
          <h2>Démonstration Responsive</h2>
          <div class="demo-grid">
            <div class="demo-card">
              <h3>Desktop</h3>
              <p>Navigation horizontale complète visible</p>
              <div class="demo-indicator desktop">Visible</div>
            </div>
            <div class="demo-card">
              <h3>Tablet</h3>
              <p>Navigation adaptée, boutons plus grands</p>
              <div class="demo-indicator tablet">Visible</div>
            </div>
            <div class="demo-card">
              <h3>Mobile</h3>
              <p>Menu hamburger, navigation verticale</p>
              <div class="demo-indicator mobile">Visible</div>
            </div>
          </div>
        </div>
        
        <div class="current-viewport">
          <h2>Votre Viewport Actuel</h2>
          <div class="viewport-info">
            <p><strong>Largeur :</strong> {{ windowWidth }}px</p>
            <p><strong>Hauteur :</strong> {{ windowHeight }}px</p>
            <p><strong>Type d'écran :</strong> {{ screenType }}</p>
            <p><strong>Menu mobile :</strong> {{ menuMobileVisible ? 'Visible' : 'Caché' }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Test Menu Mobile - Millésime Sans Frontières',
  description: 'Page de test pour vérifier le fonctionnement du menu mobile.'
})

const windowWidth = ref(0)
const windowHeight = ref(0)
const screenType = ref('Desktop')
const menuMobileVisible = ref(false)

onMounted(() => {
  const updateViewport = () => {
    windowWidth.value = window.innerWidth
    windowHeight.value = window.innerHeight
    
    if (windowWidth.value < 480) {
      screenType.value = 'Mobile Small'
    } else if (windowWidth.value < 768) {
      screenType.value = 'Mobile'
    } else if (windowWidth.value < 1024) {
      screenType.value = 'Tablet'
    } else {
      screenType.value = 'Desktop'
    }
    
    menuMobileVisible.value = windowWidth.value < 768
  }
  
  updateViewport()
  window.addEventListener('resize', updateViewport)
  
  onUnmounted(() => {
    window.removeEventListener('resize', updateViewport)
  })
})
</script>

<style scoped>
.mobile-test {
  min-height: 100vh;
}

.main-content {
  margin-top: 80px;
  padding: 2rem 0;
}

.page-title {
  font-size: 2.5rem;
  color: #1c1917;
  text-align: center;
  margin-bottom: 1rem;
}

.page-description {
  font-size: 1.125rem;
  color: #57534e;
  text-align: center;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.test-instructions,
.test-features,
.responsive-demo,
.current-viewport {
  margin-bottom: 3rem;
}

.test-instructions h2,
.test-features h2,
.responsive-demo h2,
.current-viewport h2 {
  color: #1c1917;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.test-instructions ol {
  padding-left: 1.5rem;
}

.test-instructions li,
.test-features li {
  margin-bottom: 0.5rem;
  color: #57534e;
  line-height: 1.6;
}

.test-features ul {
  list-style: none;
  padding: 0;
}

.test-features li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f3f2f0;
}

.test-features li:last-child {
  border-bottom: none;
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 1.5rem;
}

.demo-card {
  background: white;
  border: 1px solid #e7e5e4;
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.demo-card h3 {
  color: #dc2626;
  margin-bottom: 1rem;
}

.demo-card p {
  color: #57534e;
  margin-bottom: 1rem;
}

.demo-indicator {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 0.875rem;
}

.demo-indicator.desktop {
  background: #dc2626;
  color: white;
}

.demo-indicator.tablet {
  background: #f59e0b;
  color: white;
}

.demo-indicator.mobile {
  background: #10b981;
  color: white;
}

.viewport-info {
  background: #f9f8f6;
  border: 1px solid #e7e5e4;
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.viewport-info p {
  margin-bottom: 0.5rem;
  color: #57534e;
}

.viewport-info strong {
  color: #1c1917;
}

/* Responsive */
@media (max-width: 1024px) {
  .demo-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 1.5rem 0;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .demo-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .demo-card {
    padding: 1.25rem;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 1rem 0;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-description {
    font-size: 0.875rem;
  }
  
  .test-instructions h2,
  .test-features h2,
  .responsive-demo h2,
  .current-viewport h2 {
    font-size: 1.25rem;
  }
  
  .viewport-info {
    padding: 1rem;
  }
}
</style>
