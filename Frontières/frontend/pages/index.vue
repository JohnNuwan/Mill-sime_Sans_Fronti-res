<template>
  <div class="homepage">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__image-placeholder"></div>
        <div class="hero__overlay"></div>
      </div>
      
      <div class="container">
        <div class="hero__content">
          <h1 class="hero__title">
            Quality Wine Barrels from Around the World
          </h1>
          <p class="hero__subtitle">
            Discover our exclusive collection of premium barrels for wine aging, 
            decoration, and professional use
          </p>
          <div class="hero__actions">
            <NuxtLink to="/barrels" class="btn btn--primary btn--large">
              Explore Our Barrels
            </NuxtLink>
            <NuxtLink to="/professional" class="btn btn--secondary btn--large">
              Professional Inquiries
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Sections -->
    <section class="featured-sections">
      <div class="container">
        <div class="featured-grid">
          <!-- New Arrivals -->
          <div class="featured-card">
            <div class="featured-card__image">
              <div class="featured-card__image-placeholder"></div>
            </div>
            <div class="featured-card__content">
              <h3 class="featured-card__title">New Arrivals</h3>
              <p class="featured-card__description">
                Discover our latest exceptional barrel arrivals
              </p>
              <NuxtLink to="/barrels?category=new" class="btn btn--accent">
                View More
              </NuxtLink>
            </div>
          </div>

          <!-- French Origin -->
          <div class="featured-card">
            <div class="featured-card__image">
              <div class="featured-card__image-placeholder"></div>
            </div>
            <div class="featured-card__content">
              <h3 class="featured-card__title">French Origin</h3>
              <p class="featured-card__description">
                Guaranteed French tradition, exceptional quality
              </p>
              <NuxtLink to="/barrels?origin=france" class="btn btn--accent">
                Explore
              </NuxtLink>
            </div>
          </div>

          <!-- Ex-Bourbon Casks -->
          <div class="featured-card">
            <div class="featured-card__image">
              <div class="featured-card__image-placeholder"></div>
            </div>
            <div class="featured-card__content">
              <h3 class="featured-card__title">Ex-Bourbon Casks</h3>
              <p class="featured-card__description">
                Unique American character, intense flavors
              </p>
              <NuxtLink to="/barrels?origin=usa" class="btn btn--accent">
                Discover
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Statistics Section -->
    <section class="statistics">
      <div class="container">
        <div class="statistics-grid">
          <div class="statistic-item">
            <div class="statistic-item__number">500+</div>
            <div class="statistic-item__label">Available Barrels</div>
          </div>
          <div class="statistic-item">
            <div class="statistic-item__number">25+</div>
            <div class="statistic-item__label">Countries of Origin</div>
          </div>
          <div class="statistic-item">
            <div class="statistic-item__number">50+</div>
            <div class="statistic-item__label">Satisfied Clients</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials">
      <div class="container">
        <div class="testimonial-card">
          <div class="testimonial-card__quote">
            "Excellent quality barrels, perfect for our winery. Fast international shipping!"
          </div>
          <div class="testimonial-card__author">
            - Jean Dupont, Château de Bordeaux
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">
            Ready to Start Your Barrel Collection?
          </h2>
          <div class="cta-actions">
            <NuxtLink to="/barrels" class="btn btn--primary btn--large">
              Browse Catalog
            </NuxtLink>
            <NuxtLink to="/contact" class="btn btn--secondary btn--large">
              Contact Sales Team
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Configuration de la page
useHead({
  title: 'Millésime Sans Frontières - Premium Wine Barrels',
  meta: [
    { 
      name: 'description', 
      content: 'Discover our exclusive collection of premium wine barrels from around the world. Professional quality for winemakers, brewers, and enthusiasts.' 
    },
    { 
      name: 'keywords', 
      content: 'wine barrels, casks, French oak, ex-bourbon, winemakers, brewers, spirits' 
    }
  ]
})

// État réactif pour les animations
const isVisible = ref(false)

// Intersection Observer pour les animations
onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true
        }
      })
    },
    { threshold: 0.1 }
  )

  const elements = document.querySelectorAll('.featured-card, .statistic-item, .testimonial-card')
  elements.forEach((el) => observer.observe(el))

  return () => observer.disconnect()
})
</script>

<style scoped>
/* Hero Section */
.hero {
  position: relative;
  height: 80vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero__background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.hero__image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-wine-red-800), var(--color-oak-brown-600));
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(139, 38, 53, 0.8) 0%,
    rgba(139, 115, 85, 0.6) 100%
  );
}

.hero__content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  color: var(--color-white);
}

.hero__title {
  font-family: var(--font-headings);
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: var(--spacing-l);
  line-height: 1.1;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.hero__subtitle {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-2xl);
  line-height: 1.6;
  opacity: 0.95;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.hero__actions {
  display: flex;
  gap: var(--spacing-m);
  justify-content: center;
  flex-wrap: wrap;
}

/* Featured Sections */
.featured-sections {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-off-white);
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-xl);
}

.featured-card {
  background-color: var(--color-white);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all var(--transition-normal);
}

.featured-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.featured-card__image {
  height: 250px;
  overflow: hidden;
}

.featured-card__image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-whisky-gold-500), var(--color-oak-brown-400));
}

.featured-card:hover .featured-card__image-placeholder {
  transform: scale(1.05);
}

.featured-card__content {
  padding: var(--spacing-xl);
  text-align: center;
}

.featured-card__title {
  font-family: var(--font-headings);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-m);
  color: var(--color-very-dark-gray);
}

.featured-card__description {
  color: var(--color-dark-gray);
  margin-bottom: var(--spacing-l);
  line-height: 1.6;
}

/* Statistics Section */
.statistics {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-white);
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-2xl);
  text-align: center;
}

.statistic-item {
  padding: var(--spacing-xl);
}

.statistic-item__number {
  font-family: var(--font-headings);
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-wine-red);
  margin-bottom: var(--spacing-s);
  line-height: 1;
}

.statistic-item__label {
  font-size: 1.125rem;
  color: var(--color-dark-gray);
  font-weight: 500;
}

/* Testimonials Section */
.testimonials {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-very-light-gray);
}

.testimonial-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: var(--spacing-2xl);
}

.testimonial-card__quote {
  font-family: var(--font-headings);
  font-size: 1.5rem;
  font-style: italic;
  color: var(--color-very-dark-gray);
  margin-bottom: var(--spacing-l);
  line-height: 1.4;
  position: relative;
}

.testimonial-card__quote::before,
.testimonial-card__quote::after {
  content: '"';
  font-size: 3rem;
  color: var(--color-whisky-gold);
  position: absolute;
  top: -20px;
}

.testimonial-card__quote::before {
  left: -40px;
}

.testimonial-card__quote::after {
  right: -40px;
}

.testimonial-card__author {
  font-size: 1.125rem;
  color: var(--color-medium-gray);
  font-weight: 500;
}

/* CTA Section */
.cta-section {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-wine-red);
  color: var(--color-white);
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-family: var(--font-headings);
  font-size: 2.5rem;
  margin-bottom: var(--spacing-xl);
  color: var(--color-white);
}

.cta-actions {
  display: flex;
  gap: var(--spacing-m);
  justify-content: center;
  flex-wrap: wrap;
}

/* Boutons personnalisés */
.btn--large {
  padding: 16px 32px;
  font-size: 1.125rem;
  min-height: 56px;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .hero {
    height: 70vh;
    min-height: 500px;
  }

  .hero__title {
    font-size: 2.5rem;
    line-height: 1.2;
    margin-bottom: 1rem;
  }

  .hero__subtitle {
    font-size: 1.125rem;
    line-height: 1.5;
    margin-bottom: 2rem;
  }

  .hero__actions {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .featured-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-l);
  }

  .statistics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
  }

  .statistic-item__number {
    font-size: 2.5rem;
  }

  .testimonial-card__quote {
    font-size: 1.25rem;
  }

  .testimonial-card__quote::before,
  .testimonial-card__quote::after {
    font-size: 2rem;
    top: -15px;
  }

  .testimonial-card__quote::before {
    left: -20px;
  }

  .testimonial-card__quote::after {
    right: -20px;
  }

  .cta-title {
    font-size: 2rem;
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.75rem;
  }
  
  .hero {
    height: 60vh;
    min-height: 400px;
  }

  .hero__title {
    font-size: 1.75rem;
    line-height: 1.3;
  }

  .hero__subtitle {
    font-size: 1rem;
    line-height: 1.4;
  }

  .hero__actions .btn {
    padding: 0.875rem 1.5rem;
    font-size: 1rem;
  }

  .featured-card__content {
    padding: var(--spacing-l);
  }

  .statistic-item {
    padding: var(--spacing-l);
  }

  .testimonial-card {
    padding: var(--spacing-xl);
  }
  
  .cta-title {
    font-size: 1.75rem;
  }
}

/* Animations */
.featured-card,
.statistic-item,
.testimonial-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.featured-card.visible,
.statistic-item.visible,
.testimonial-card.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Hover effects */
.featured-card:hover {
  transform: translateY(-8px);
}

.statistic-item:hover .statistic-item__number {
  color: var(--color-wine-red-dark);
  transform: scale(1.1);
  transition: all 0.3s ease;
}

/* Focus states pour l'accessibilité */
.btn:focus,
.featured-card:focus-within {
  outline: 2px solid var(--color-white);
  outline-offset: 2px;
}
</style>
