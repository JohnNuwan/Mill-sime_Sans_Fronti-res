<template>
  <header class="header">
    <div class="container">
      <div class="header__content">
        <!-- Logo -->
        <div class="header__logo">
          <NuxtLink to="/" class="logo">
            <span class="logo__brand">Millésime</span>
            <span class="logo__tagline">SANS FRONTIÈRES</span>
          </NuxtLink>
        </div>

        <!-- Navigation -->
        <nav class="nav">
          <ul class="nav__list">
            <li class="nav__item">
              <NuxtLink to="/" class="nav__link" :class="{ 'nav__link--active': $route.path === '/' }">
                Home
              </NuxtLink>
            </li>
            <li class="nav__item">
              <NuxtLink to="/barrels" class="nav__link" :class="{ 'nav__link--active': $route.path === '/barrels' }">
                Our Barrels
              </NuxtLink>
            </li>
            <li class="nav__item">
              <NuxtLink to="/about" class="nav__link" :class="{ 'nav__link--active': $route.path === '/about' }">
                About
              </NuxtLink>
            </li>
            <li class="nav__item">
              <NuxtLink to="/professional" class="nav__link" :class="{ 'nav__link--active': $route.path === '/professional' }">
                Professional
              </NuxtLink>
            </li>
            <li class="nav__item">
              <NuxtLink to="/contact" class="nav__link" :class="{ 'nav__link--active': $route.path === '/contact' }">
                Contact
              </NuxtLink>
            </li>
          </ul>
        </nav>

        <!-- Actions -->
        <div class="header__actions">
          <NuxtLink to="/contact" class="btn btn--outline">
            Get in Touch
          </NuxtLink>
          <NuxtLink to="/login" class="btn btn--primary">
            Login
          </NuxtLink>
        </div>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle" @click="toggleMobileMenu" :aria-expanded="isMobileMenuOpen">
          <span class="mobile-menu-toggle__line"></span>
          <span class="mobile-menu-toggle__line"></span>
          <span class="mobile-menu-toggle__line"></span>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div class="mobile-menu" :class="{ 'mobile-menu--open': isMobileMenuOpen }">
        <nav class="mobile-nav">
          <ul class="mobile-nav__list">
            <li class="mobile-nav__item">
              <NuxtLink to="/" class="mobile-nav__link" @click="closeMobileMenu">
                Home
              </NuxtLink>
            </li>
            <li class="mobile-nav__item">
              <NuxtLink to="/barrels" class="mobile-nav__link" @click="closeMobileMenu">
                Our Barrels
              </NuxtLink>
            </li>
            <li class="mobile-nav__item">
              <NuxtLink to="/about" class="mobile-nav__link" @click="closeMobileMenu">
                About
              </NuxtLink>
            </li>
            <li class="mobile-nav__item">
              <NuxtLink to="/professional" class="mobile-nav__link" @click="closeMobileMenu">
                Professional
              </NuxtLink>
            </li>
            <li class="mobile-nav__item">
              <NuxtLink to="/contact" class="mobile-nav__link" @click="closeMobileMenu">
                Contact
              </NuxtLink>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-cream-200);
  z-index: 1000;
  transition: all 0.3s ease;
}

.header__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

/* Logo */
.logo {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.logo__brand {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  font-family: 'Playfair Display', serif;
  line-height: 1;
}

.logo__tagline {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-wine-red-600);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  line-height: 1;
}

/* Navigation */
.nav__list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav__link {
  text-decoration: none;
  color: var(--color-oak-brown-700);
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav__link:hover {
  color: var(--color-wine-red-600);
}

.nav__link--active {
  color: var(--color-wine-red-600);
}

.nav__link--active::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--color-wine-red-600);
  border-radius: 1px;
}

/* Actions */
.header__actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  gap: 0.25rem;
}

.mobile-menu-toggle__line {
  width: 24px;
  height: 2px;
  background: var(--color-oak-brown-800);
  transition: all 0.3s ease;
}

/* Mobile Menu */
.mobile-menu {
  display: none;
  background: white;
  border-top: 1px solid var(--color-cream-200);
  padding: 1rem 0;
  transform: translateY(-100%);
  opacity: 0;
  transition: all 0.3s ease;
}

.mobile-menu--open {
  transform: translateY(0);
  opacity: 1;
}

.mobile-nav__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav__link {
  display: block;
  padding: 0.75rem 0;
  text-decoration: none;
  color: var(--color-oak-brown-700);
  font-weight: 500;
  transition: all 0.3s ease;
}

.mobile-nav__link:hover {
  color: var(--color-wine-red-600);
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav {
    display: none;
  }
  
  .header__actions {
    display: none;
  }
  
  .mobile-menu-toggle {
    display: flex;
  }
  
  .mobile-menu {
    display: block;
  }
  
  .logo__brand {
    font-size: 1.5rem;
  }
  
  .logo__tagline {
    font-size: 0.7rem;
  }
}

/* Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.btn--outline {
  background: transparent;
  color: var(--color-wine-red-600);
  border: 2px solid var(--color-wine-red-600);
}

.btn--outline:hover {
  background: var(--color-wine-red-600);
  color: white;
  transform: translateY(-2px);
}
</style>
