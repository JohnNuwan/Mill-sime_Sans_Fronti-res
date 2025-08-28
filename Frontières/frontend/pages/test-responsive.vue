<template>
  <div class="test-responsive">
    <!-- Header -->
    <header class="page-header">
      <div class="container">
        <h1 class="page-title">Responsive Design Test</h1>
        <p class="page-subtitle">Test page to verify responsive behavior across different screen sizes</p>
      </div>
    </header>

    <!-- Responsive Grid Test -->
    <section class="responsive-test">
      <div class="container">
        <h2 class="section-title">Grid Layout Test</h2>
        <div class="test-grid">
          <div class="test-card" v-for="i in 6" :key="i">
            <div class="card-header">
              <h3>Card {{ i }}</h3>
            </div>
            <div class="card-content">
              <p>This card demonstrates responsive grid behavior. It should adapt to different screen sizes.</p>
              <div class="card-meta">
                <span class="meta-item">Responsive</span>
                <span class="meta-item">Grid</span>
                <span class="meta-item">Test</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Typography Test -->
    <section class="typography-test">
      <div class="container">
        <h2 class="section-title">Typography Responsiveness</h2>
        <div class="typography-examples">
          <h1>Heading 1 - Main Title</h1>
          <h2>Heading 2 - Section Title</h2>
          <h3>Heading 3 - Subsection</h3>
          <h4>Heading 4 - Minor Section</h4>
          <p class="large-text">Large paragraph text that should be readable on all devices.</p>
          <p>Regular paragraph text with standard line height and spacing.</p>
          <p class="small-text">Smaller text for secondary information.</p>
        </div>
      </div>
    </section>

    <!-- Button Test -->
    <section class="button-test">
      <div class="container">
        <h2 class="section-title">Button Responsiveness</h2>
        <div class="button-examples">
          <button class="btn btn--primary btn--large">Large Primary Button</button>
          <button class="btn btn--secondary btn--large">Large Secondary Button</button>
          <button class="btn btn--outline btn--large">Large Outline Button</button>
          <button class="btn btn--primary">Standard Primary Button</button>
          <button class="btn btn--secondary">Standard Secondary Button</button>
          <button class="btn btn--outline">Standard Outline Button</button>
          <button class="btn btn--primary btn--small">Small Primary Button</button>
          <button class="btn btn--secondary btn--small">Small Secondary Button</button>
        </div>
      </div>
    </section>

    <!-- Form Test -->
    <section class="form-test">
      <div class="container">
        <h2 class="section-title">Form Responsiveness</h2>
        <form class="test-form">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input type="text" id="firstName" class="form-input" placeholder="Enter first name" />
            </div>
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input type="text" id="lastName" class="form-input" placeholder="Enter last name" />
            </div>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" class="form-input" placeholder="Enter email address" />
          </div>
          <div class="form-group">
            <label for="message">Message</label>
            <textarea id="message" class="form-input" rows="4" placeholder="Enter your message"></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn--primary">Submit Form</button>
            <button type="button" class="btn btn--outline">Reset</button>
          </div>
        </form>
      </div>
    </section>

    <!-- Navigation Test -->
    <section class="navigation-test">
      <div class="container">
        <h2 class="section-title">Navigation Responsiveness</h2>
        <nav class="test-navigation">
          <ul class="nav-list">
            <li class="nav-item">
              <a href="#" class="nav-link">Home</a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link">About</a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link">Services</a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link">Contact</a>
            </li>
          </ul>
        </nav>
      </div>
    </section>

    <!-- Screen Size Indicator -->
    <div class="screen-indicator">
      <div class="indicator-content">
        <span class="indicator-label">Screen Size:</span>
        <span class="indicator-value">{{ screenSize }}</span>
        <span class="indicator-width">{{ windowWidth }}px × {{ windowHeight }}px</span>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Responsive Design Test - Millésime Sans Frontières',
  description: 'Test page to verify responsive behavior across different screen sizes.'
})

const screenSize = ref('Desktop')
const windowWidth = ref(0)
const windowHeight = ref(0)

onMounted(() => {
  const updateScreenSize = () => {
    windowWidth.value = window.innerWidth
    windowHeight.value = window.innerHeight
    
    if (windowWidth.value < 480) {
      screenSize.value = 'Mobile Small'
    } else if (windowWidth.value < 768) {
      screenSize.value = 'Mobile'
    } else if (windowWidth.value < 1024) {
      screenSize.value = 'Tablet'
    } else {
      screenSize.value = 'Desktop'
    }
  }
  
  updateScreenSize()
  window.addEventListener('resize', updateScreenSize)
  
  onUnmounted(() => {
    window.removeEventListener('resize', updateScreenSize)
  })
})
</script>

<style scoped>
.test-responsive {
  padding: 2rem 0;
}

.page-header {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  color: white;
  padding: 3rem 0;
  text-align: center;
}

.page-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: white;
}

.page-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
}

.responsive-test,
.typography-test,
.button-test,
.form-test,
.navigation-test {
  padding: 3rem 0;
  border-bottom: 1px solid #e7e5e4;
}

.section-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #1c1917;
}

/* Grid Test */
.test-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.test-card {
  background: white;
  border: 1px solid #e7e5e4;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.test-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-header h3 {
  color: #dc2626;
  margin-bottom: 1rem;
}

.card-content p {
  margin-bottom: 1rem;
  color: #57534e;
}

.card-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.meta-item {
  background: #f3f2f0;
  color: #57534e;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

/* Typography Test */
.typography-examples {
  max-width: 800px;
  margin: 0 auto;
}

.typography-examples h1,
.typography-examples h2,
.typography-examples h3,
.typography-examples h4 {
  margin-bottom: 1rem;
  color: #1c1917;
}

.large-text {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #57534e;
}

.small-text {
  font-size: 0.875rem;
  color: #78716c;
}

/* Button Test */
.button-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

/* Form Test */
.test-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #1c1917;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d6d3d1;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

/* Navigation Test */
.test-navigation {
  background: #f9f8f6;
  padding: 2rem;
  border-radius: 0.5rem;
}

.nav-list {
  display: flex;
  justify-content: center;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #dc2626;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: #dc2626;
  color: white;
}

/* Screen Indicator */
.screen-indicator {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  z-index: 1000;
}

.indicator-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.indicator-label {
  opacity: 0.7;
  font-size: 0.75rem;
}

.indicator-value {
  font-weight: 600;
  color: #f59e0b;
}

.indicator-width {
  opacity: 0.8;
  font-size: 0.75rem;
}

/* Responsive Breakpoints */
@media (max-width: 1024px) {
  .test-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  
  .page-title {
    font-size: 2.5rem;
  }
  
  .page-subtitle {
    font-size: 1.125rem;
  }
}

@media (max-width: 768px) {
  .test-responsive {
    padding: 1rem 0;
  }
  
  .page-header {
    padding: 2rem 0;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .responsive-test,
  .typography-test,
  .button-test,
  .form-test,
  .navigation-test {
    padding: 2rem 0;
  }
  
  .test-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .button-examples {
    flex-direction: column;
    align-items: center;
  }
  
  .nav-list {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .screen-indicator {
    bottom: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.75rem;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-subtitle {
    font-size: 0.875rem;
  }
  
  .test-card {
    padding: 1.25rem;
  }
  
  .button-examples .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .form-actions .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
