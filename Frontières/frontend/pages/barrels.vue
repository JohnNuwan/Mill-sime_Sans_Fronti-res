<template>
  <div class="barrels-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Premium Wine & Whiskey Barrels</h1>
        <p class="hero__subtitle">
          Discover our exclusive collection of high-quality barrels for aging, decoration, and professional use
        </p>
      </div>
    </section>

    <!-- Filters Section -->
    <section class="filters">
      <div class="container">
        <div class="filters__content">
          <div class="filters__group">
            <label for="type-filter" class="filters__label">Type</label>
            <select id="type-filter" class="filters__select">
              <option value="">All Types</option>
              <option value="wine">Wine Barrels</option>
              <option value="whiskey">Whiskey Barrels</option>
              <option value="decorative">Decorative Barrels</option>
            </select>
          </div>

          <div class="filters__group">
            <label for="size-filter" class="filters__label">Size</label>
            <select id="size-filter" class="filters__select">
              <option value="">All Sizes</option>
              <option value="small">Small (5-10L)</option>
              <option value="medium">Medium (20-50L)</option>
              <option value="large">Large (100-225L)</option>
            </select>
          </div>

          <div class="filters__group">
            <label for="wood-filter" class="filters__label">Wood Type</label>
            <select id="wood-filter" class="filters__select">
              <option value="">All Woods</option>
              <option value="oak">Oak</option>
              <option value="cherry">Cherry</option>
              <option value="maple">Maple</option>
            </select>
          </div>

          <div class="filters__group">
            <label for="price-filter" class="filters__label">Price Range</label>
            <select id="price-filter" class="filters__select">
              <option value="">All Prices</option>
              <option value="low">Under $100</option>
              <option value="medium">$100 - $500</option>
              <option value="high">Over $500</option>
            </select>
          </div>
        </div>
      </div>
    </section>

    <!-- Barrels Grid -->
    <section class="barrels-grid">
      <div class="container">
        <div class="barrels-grid__content">
          <!-- Barrel Card 1 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">French Oak Wine Barrel</h3>
              <p class="barrel-card__description">
                Premium French oak barrel, perfect for wine aging. 225L capacity, medium toast.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Wine</span>
                <span class="barrel-card__detail">Size: 225L</span>
                <span class="barrel-card__detail">Wood: French Oak</span>
              </div>
              <div class="barrel-card__price">$850</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>

          <!-- Barrel Card 2 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">American Oak Whiskey Barrel</h3>
              <p class="barrel-card__description">
                Traditional American oak barrel for whiskey aging. 200L capacity, charred finish.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Whiskey</span>
                <span class="barrel-card__detail">Size: 200L</span>
                <span class="barrel-card__detail">Wood: American Oak</span>
              </div>
              <div class="barrel-card__price">$750</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>

          <!-- Barrel Card 3 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">Decorative Cherry Barrel</h3>
              <p class="barrel-card__description">
                Beautiful decorative barrel made from cherry wood. Perfect for home decoration.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Decorative</span>
                <span class="barrel-card__detail">Size: 50L</span>
                <span class="barrel-card__detail">Wood: Cherry</span>
              </div>
              <div class="barrel-card__price">$300</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>

          <!-- Barrel Card 4 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">Hungarian Oak Wine Barrel</h3>
              <p class="barrel-card__description">
                Premium Hungarian oak barrel with unique flavor profile. 225L capacity.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Wine</span>
                <span class="barrel-card__detail">Size: 225L</span>
                <span class="barrel-card__detail">Wood: Hungarian Oak</span>
              </div>
              <div class="barrel-card__price">$920</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>

          <!-- Barrel Card 5 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">Small Maple Whiskey Barrel</h3>
              <p class="barrel-card__description">
                Compact maple barrel perfect for small-batch whiskey production. 20L capacity.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Whiskey</span>
                <span class="barrel-card__detail">Size: 20L</span>
                <span class="barrel-card__detail">Wood: Maple</span>
              </div>
              <div class="barrel-card__price">$180</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>

          <!-- Barrel Card 6 -->
          <div class="barrel-card">
            <div class="barrel-card__image">
              <div class="barrel-card__image-placeholder"></div>
            </div>
            <div class="barrel-card__content">
              <h3 class="barrel-card__title">Vintage Oak Decorative Barrel</h3>
              <p class="barrel-card__description">
                Authentic vintage oak barrel with rich patina. Ideal for rustic decoration.
              </p>
              <div class="barrel-card__details">
                <span class="barrel-card__detail">Type: Decorative</span>
                <span class="barrel-card__detail">Size: 100L</span>
                <span class="barrel-card__detail">Wood: Aged Oak</span>
              </div>
              <div class="barrel-card__price">$450</div>
              <button class="barrel-card__button">Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="cta">
      <div class="container">
        <div class="cta__content">
          <h2 class="cta__title">Need Custom Barrels?</h2>
          <p class="cta__description">
            We specialize in custom barrel manufacturing for professional use. Contact us for bulk orders and custom specifications.
          </p>
          <button class="cta__button">Contact Us</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Our Barrels - Millésime Sans Frontières',
  description: 'Discover our premium collection of wine and whiskey barrels for aging, decoration, and professional use.'
})
</script>

<style scoped>
.barrels-page {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  position: relative;
  height: 60vh;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
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

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #991b1b, #57534e);
  z-index: 2;
}

.hero__content {
  position: relative;
  z-index: 3;
  max-width: 800px;
  padding: 0 2rem;
}

.hero__title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero__subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* Filters Section */
.filters {
  background: #fafaf9;
  padding: 3rem 0;
  border-bottom: 1px solid #e7e5e4;
}

.filters__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  align-items: end;
}

.filters__group {
  display: flex;
  flex-direction: column;
}

.filters__label {
  font-weight: 600;
  color: #292524;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filters__select {
  padding: 0.75rem;
  border: 2px solid #d6d3d1;
  border-radius: 8px;
  background: white;
  color: #292524;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.filters__select:focus {
  outline: none;
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(185, 28, 28, 0.1);
}

/* Barrels Grid */
.barrels-grid {
  padding: 4rem 0;
  background: white;
}

.barrels-grid__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
}

.barrel-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e7e5e4;
}

.barrel-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.barrel-card__image {
  height: 250px;
  overflow: hidden;
}

.barrel-card__image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f59e0b, #a8a29e);
}

.barrel-card__content {
  padding: 1.5rem;
}

.barrel-card__title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 0.75rem;
  font-family: 'Playfair Display', serif;
}

.barrel-card__description {
  color: #44403c;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.barrel-card__details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.barrel-card__detail {
  background: #f5f5f4;
  color: #44403c;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.barrel-card__price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 1rem;
}

.barrel-card__button {
  width: 100%;
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.875rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.barrel-card__button:hover {
  background: #b91c1c;
  transform: translateY(-2px);
}

/* Call to Action */
.cta {
  background: #1c1917;
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.cta__content {
  max-width: 600px;
  margin: 0 auto;
}

.cta__title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
  color: white;
}

.cta__description {
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  color: white;
  opacity: 0.9;
}

.cta__button {
  background: #f59e0b;
  color: #1c1917;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta__button:hover {
  background: #fbbf24;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero__title {
    font-size: 2.5rem;
  }

  .hero__subtitle {
    font-size: 1.125rem;
  }

  .filters__content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .barrels-grid__content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .cta__title {
    font-size: 2rem;
  }
}
</style>
