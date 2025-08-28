<template>
  <div class="layout-default">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header__content">
          <!-- Logo -->
          <div class="header__logo">
            <NuxtLink to="/" class="logo">
              <span class="logo__text">Millésime</span>
              <span class="logo__subtext">Sans Frontières</span>
            </NuxtLink>
          </div>

          <!-- Navigation principale -->
          <nav class="header__nav" :class="{ 'header__nav--open': isMobileMenuOpen }">
            <ul class="nav-list">
              <li class="nav-item">
                <NuxtLink to="/" class="nav-link" @click="closeMobileMenu">
                  Accueil
                </NuxtLink>
              </li>
              <li class="nav-item">
                <NuxtLink to="/barrels" class="nav-link" @click="closeMobileMenu">
                  Nos Fûts
                </NuxtLink>
              </li>
              <li class="nav-item">
                <NuxtLink to="/about" class="nav-link" @click="closeMobileMenu">
                  À Propos
                </NuxtLink>
              </li>
              <li class="nav-item">
                <NuxtLink to="/b2b" class="nav-link" @click="closeMobileMenu">
                  Espace Pro
                </NuxtLink>
              </li>
              <li class="nav-item">
                <NuxtLink to="/contact" class="nav-link" @click="closeMobileMenu">
                  Contact
                </NuxtLink>
              </li>
            </ul>
          </nav>

          <!-- Actions du header -->
          <div class="header__actions">
            <!-- Barre de recherche -->
            <div class="search-container">
              <button 
                class="search-toggle"
                @click="toggleSearch"
                aria-label="Ouvrir la recherche"
              >
                <Icon name="heroicons:magnifying-glass" class="w-5 h-5" />
              </button>
              <div v-if="isSearchOpen" class="search-dropdown">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Rechercher un fût..."
                  class="search-input"
                  @keyup.enter="performSearch"
                />
                <button 
                  class="search-close"
                  @click="closeSearch"
                  aria-label="Fermer la recherche"
                >
                  <Icon name="heroicons:x-mark" class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Panier -->
            <NuxtLink to="/cart" class="header__cart" aria-label="Panier">
              <Icon name="heroicons:shopping-cart" class="w-6 h-6" />
              <span v-if="cartItemCount > 0" class="cart-badge">
                {{ cartItemCount }}
              </span>
            </NuxtLink>

            <!-- Menu utilisateur -->
            <div class="user-menu">
              <button 
                v-if="!isAuthenticated"
                @click="openAuthModal"
                class="btn btn--secondary btn--small"
              >
                Connexion
              </button>
              <div v-else class="user-dropdown">
                <button 
                  @click="toggleUserMenu"
                  class="user-toggle"
                  aria-label="Menu utilisateur"
                >
                  <Icon name="heroicons:user-circle" class="w-6 h-6" />
                </button>
                <div v-if="isUserMenuOpen" class="user-dropdown-menu">
                  <NuxtLink to="/profile" class="dropdown-item">
                    Mon Profil
                  </NuxtLink>
                  <NuxtLink to="/orders" class="dropdown-item">
                    Mes Commandes
                  </NuxtLink>
                  <NuxtLink to="/quotes" class="dropdown-item">
                    Mes Devis
                  </NuxtLink>
                  <button @click="logout" class="dropdown-item">
                    Déconnexion
                  </button>
                </div>
              </div>
            </div>

            <!-- Menu mobile -->
            <button 
              class="mobile-menu-toggle"
              @click="toggleMobileMenu"
              aria-label="Menu mobile"
            >
              <span class="mobile-menu-toggle__line"></span>
              <span class="mobile-menu-toggle__line"></span>
              <span class="mobile-menu-toggle__line"></span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenu principal -->
    <main class="main-content">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer__content">
          <!-- Informations de l'entreprise -->
          <div class="footer__section">
            <h3 class="footer__title">Millésime Sans Frontières</h3>
            <p class="footer__description">
              Votre spécialiste des fûts de vin premium du monde entier. 
              Qualité professionnelle pour vignerons, brasseurs et passionnés.
            </p>
          </div>

          <!-- Liens rapides -->
          <div class="footer__section">
            <h4 class="footer__subtitle">Produits</h4>
            <ul class="footer__links">
              <li><NuxtLink to="/barrels" class="footer__link">Nos Fûts</NuxtLink></li>
              <li><NuxtLink to="/barrels?origin=france" class="footer__link">Origine France</NuxtLink></li>
              <li><NuxtLink to="/barrels?origin=usa" class="footer__link">Ex-Bourbon</NuxtLink></li>
              <li><NuxtLink to="/barrels?origin=spain" class="footer__link">Sherry Casks</NuxtLink></li>
            </ul>
          </div>

          <!-- Services -->
          <div class="footer__section">
            <h4 class="footer__subtitle">Services</h4>
            <ul class="footer__links">
              <li><NuxtLink to="/b2b" class="footer__link">Espace Professionnel</NuxtLink></li>
              <li><NuxtLink to="/shipping" class="footer__link">Livraison</NuxtLink></li>
              <li><NuxtLink to="/support" class="footer__link">Support</NuxtLink></li>
              <li><NuxtLink to="/contact" class="footer__link">Contact</NuxtLink></li>
            </ul>
          </div>

          <!-- Informations légales -->
          <div class="footer__section">
            <h4 class="footer__subtitle">Informations</h4>
            <ul class="footer__links">
              <li><NuxtLink to="/about" class="footer__link">À Propos</NuxtLink></li>
              <li><NuxtLink to="/terms" class="footer__link">CGV</NuxtLink></li>
              <li><NuxtLink to="/privacy" class="footer__link">Confidentialité</NuxtLink></li>
              <li><NuxtLink to="/legal" class="footer__link">Mentions Légales</NuxtLink></li>
            </ul>
          </div>
        </div>

        <!-- Newsletter -->
        <div class="footer__newsletter">
          <h4 class="footer__subtitle">Restez informé</h4>
          <p>Recevez nos dernières offres et nouveautés</p>
          <form @submit.prevent="subscribeNewsletter" class="newsletter-form">
            <input
              v-model="newsletterEmail"
              type="email"
              placeholder="Votre email"
              class="newsletter-input"
              required
            />
            <button type="submit" class="btn btn--primary">S'abonner</button>
          </form>
        </div>

        <!-- Réseaux sociaux et copyright -->
        <div class="footer__bottom">
          <div class="footer__social">
            <a href="#" class="social-link" aria-label="Facebook">
              <Icon name="mdi:facebook" class="w-6 h-6" />
            </a>
            <a href="#" class="social-link" aria-label="Instagram">
              <Icon name="mdi:instagram" class="w-6 h-6" />
            </a>
            <a href="#" class="social-link" aria-label="LinkedIn">
              <Icon name="mdi:linkedin" class="w-6 h-6" />
            </a>
          </div>
          <div class="footer__copyright">
            <p>&copy; {{ currentYear }} Millésime Sans Frontières. Tous droits réservés.</p>
          </div>
        </div>
      </div>
    </footer>

    <!-- Modale d'authentification -->
    <AuthModal 
      v-if="isAuthModalOpen"
      @close="closeAuthModal"
      @success="onAuthSuccess"
    />
  </div>
</template>

<script setup lang="ts">
// État réactif
const isMobileMenuOpen = ref(false)
const isSearchOpen = ref(false)
const isUserMenuOpen = ref(false)
const isAuthModalOpen = ref(false)
const searchQuery = ref('')
const newsletterEmail = ref('')

// Composables
const { isAuthenticated, user, logout: authLogout } = useAuth()
const { cartItemCount } = useCart()

// Computed
const currentYear = computed(() => new Date().getFullYear())

// Méthodes
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const toggleSearch = () => {
  isSearchOpen.value = !isSearchOpen.value
  if (isSearchOpen.value) {
    nextTick(() => {
      const searchInput = document.querySelector('.search-input') as HTMLInputElement
      searchInput?.focus()
    })
  }
}

const closeSearch = () => {
  isSearchOpen.value = false
  searchQuery.value = ''
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    navigateTo(`/barrels?search=${encodeURIComponent(searchQuery.value.trim())}`)
    closeSearch()
  }
}

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const openAuthModal = () => {
  isAuthModalOpen.value = true
}

const closeAuthModal = () => {
  isAuthModalOpen.value = false
}

const onAuthSuccess = () => {
  closeAuthModal()
  // Redirection ou notification de succès
}

const logout = async () => {
  try {
    await authLogout()
    isUserMenuOpen.value = false
    navigateTo('/')
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
  }
}

const subscribeNewsletter = async () => {
  try {
    // Appel API pour l'inscription à la newsletter
    console.log('Inscription newsletter:', newsletterEmail.value)
    newsletterEmail.value = ''
    // Notification de succès
  } catch (error) {
    console.error('Erreur newsletter:', error)
  }
}

// Fermer les menus lors du clic à l'extérieur
onClickOutside(isUserMenuOpen, () => {
  isUserMenuOpen.value = false
})

onClickOutside(isSearchOpen, () => {
  isSearchOpen.value = false
})

// Fermer le menu mobile lors du redimensionnement
onMounted(() => {
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      isMobileMenuOpen.value = false
    }
  })
})
</script>

<style scoped>
/* Header */
.header {
  background-color: var(--color-white);
  border-bottom: 1px solid var(--color-very-light-gray);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-m) 0;
}

/* Logo */
.logo {
  display: flex;
  flex-direction: column;
  text-decoration: none;
}

.logo__text {
  font-family: var(--font-headings);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-wine-red);
  line-height: 1;
}

.logo__subtext {
  font-family: var(--font-primary);
  font-size: 0.75rem;
  color: var(--color-medium-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Navigation */
.header__nav {
  display: flex;
  align-items: center;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--spacing-xl);
}

.nav-link {
  font-family: var(--font-primary);
  font-size: 16px;
  font-weight: 500;
  color: var(--color-dark-gray);
  text-decoration: none;
  transition: color var(--transition-fast);
  padding: var(--spacing-s) 0;
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-wine-red);
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-wine-red);
}

/* Actions du header */
.header__actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-m);
}

/* Recherche */
.search-container {
  position: relative;
}

.search-toggle {
  background: none;
  border: none;
  color: var(--color-dark-gray);
  cursor: pointer;
  padding: var(--spacing-s);
  border-radius: 50%;
  transition: all var(--transition-fast);
}

.search-toggle:hover {
  background-color: var(--color-very-light-gray);
  color: var(--color-wine-red);
}

.search-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--color-white);
  border: 1px solid var(--color-very-light-gray);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-m);
  min-width: 300px;
  z-index: 1001;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--color-light-gray);
  border-radius: 6px;
  font-size: 14px;
}

.search-close {
  position: absolute;
  top: var(--spacing-s);
  right: var(--spacing-s);
  background: none;
  border: none;
  color: var(--color-medium-gray);
  cursor: pointer;
  padding: 4px;
}

/* Panier */
.header__cart {
  position: relative;
  color: var(--color-dark-gray);
  padding: var(--spacing-s);
  border-radius: 50%;
  transition: all var(--transition-fast);
}

.header__cart:hover {
  color: var(--color-wine-red);
  background-color: var(--color-very-light-gray);
}

.cart-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: var(--color-wine-red);
  color: var(--color-white);
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

/* Menu utilisateur */
.user-menu {
  position: relative;
}

.user-toggle {
  background: none;
  border: none;
  color: var(--color-dark-gray);
  cursor: pointer;
  padding: var(--spacing-s);
  border-radius: 50%;
  transition: all var(--transition-fast);
}

.user-toggle:hover {
  color: var(--color-wine-red);
  background-color: var(--color-very-light-gray);
}

.user-dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--color-white);
  border: 1px solid var(--color-very-light-gray);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 1001;
  overflow: hidden;
}

.dropdown-item {
  display: block;
  padding: var(--spacing-m);
  color: var(--color-dark-gray);
  text-decoration: none;
  transition: all var(--transition-fast);
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: var(--font-primary);
  font-size: 14px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: var(--color-very-light-gray);
  color: var(--color-wine-red);
}

/* Menu mobile */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-s);
}

.mobile-menu-toggle__line {
  width: 24px;
  height: 2px;
  background-color: var(--color-dark-gray);
  transition: all var(--transition-normal);
}

/* Contenu principal */
.main-content {
  flex: 1;
  min-height: calc(100vh - 200px);
}

/* Footer */
.footer {
  background-color: var(--color-very-dark-gray);
  color: var(--color-white);
  padding: var(--spacing-3xl) 0 var(--spacing-xl);
  margin-top: auto;
}

.footer__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
}

.footer__title {
  font-family: var(--font-headings);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-m);
  color: var(--color-whisky-gold);
}

.footer__subtitle {
  font-family: var(--font-headings);
  font-size: 1.125rem;
  margin-bottom: var(--spacing-m);
  color: var(--color-whisky-gold);
}

.footer__description {
  color: var(--color-light-gray);
  line-height: 1.6;
}

.footer__links {
  list-style: none;
  margin: 0;
  padding: 0;
}

.footer__link {
  color: var(--color-light-gray);
  text-decoration: none;
  transition: color var(--transition-fast);
  display: block;
  padding: var(--spacing-s) 0;
}

.footer__link:hover {
  color: var(--color-whisky-gold);
}

/* Newsletter */
.footer__newsletter {
  text-align: center;
  padding: var(--spacing-2xl) 0;
  border-top: 1px solid var(--color-dark-gray);
  margin-bottom: var(--spacing-xl);
}

.newsletter-form {
  display: flex;
  gap: var(--spacing-m);
  max-width: 500px;
  margin: var(--spacing-m) auto 0;
}

.newsletter-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--color-dark-gray);
  border-radius: 8px;
  background-color: var(--color-dark-gray);
  color: var(--color-white);
}

.newsletter-input::placeholder {
  color: var(--color-medium-gray);
}

/* Footer bottom */
.footer__bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-dark-gray);
}

.footer__social {
  display: flex;
  gap: var(--spacing-m);
}

.social-link {
  color: var(--color-light-gray);
  transition: color var(--transition-fast);
  padding: var(--spacing-s);
  border-radius: 50%;
}

.social-link:hover {
  color: var(--color-whisky-gold);
}

.footer__copyright {
  color: var(--color-medium-gray);
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .header__nav {
    position: fixed;
    top: 80px;
    left: 0;
    width: 100%;
    height: calc(100vh - 80px);
    background-color: var(--color-white);
    transform: translateX(-100%);
    transition: transform var(--transition-normal);
    overflow-y: auto;
    z-index: 999;
  }

  .header__nav--open {
    transform: translateX(0);
  }

  .nav-list {
    flex-direction: column;
    gap: 0;
    padding: var(--spacing-l);
  }

  .nav-link {
    padding: var(--spacing-m) 0;
    border-bottom: 1px solid var(--color-very-light-gray);
  }

  .mobile-menu-toggle {
    display: flex;
  }

  .header__actions {
    gap: var(--spacing-s);
  }

  .search-dropdown {
    min-width: 250px;
    right: -50px;
  }

  .footer__content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .newsletter-form {
    flex-direction: column;
  }

  .footer__bottom {
    flex-direction: column;
    gap: var(--spacing-m);
    text-align: center;
  }
}

@media (max-width: 480px) {
  .header__content {
    padding: var(--spacing-s) 0;
  }

  .logo__text {
    font-size: 1.25rem;
  }

  .search-dropdown {
    min-width: 200px;
    right: -100px;
  }
}
</style>
