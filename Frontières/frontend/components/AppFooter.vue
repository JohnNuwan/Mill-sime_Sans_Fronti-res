<template>
  <footer class="footer">
    <div class="container">
      <div class="footer__content">
        <!-- Company Information -->
        <div class="footer__section">
          <div class="footer__logo">
            <span class="footer__logo-brand">Millésime</span>
            <span class="footer__logo-tagline">SANS FRONTIÈRES</span>
          </div>
          <p class="footer__description">
            Connecting the world through exceptional wine and spirits barrels since 1995. 
            Premium quality, authentic craftsmanship, and global expertise.
          </p>
          <div class="footer__social">
            <a href="#" class="footer__social-link" aria-label="Facebook">
              <div class="footer__social-icon-placeholder"></div>
            </a>
            <a href="#" class="footer__social-link" aria-label="LinkedIn">
              <div class="footer__social-icon-placeholder"></div>
            </a>
            <a href="#" class="footer__social-link" aria-label="Instagram">
              <div class="footer__social-icon-placeholder"></div>
            </a>
            <a href="#" class="footer__social-link" aria-label="YouTube">
              <div class="footer__social-icon-placeholder"></div>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="footer__section">
          <h3 class="footer__section-title">Quick Links</h3>
          <ul class="footer__links">
            <li><NuxtLink to="/barrels" class="footer__link">Our Barrels</NuxtLink></li>
            <li><NuxtLink to="/about" class="footer__link">About Us</NuxtLink></li>
            <li><NuxtLink to="/professional" class="footer__link">Professional Services</NuxtLink></li>
            <li><NuxtLink to="/contact" class="footer__link">Contact</NuxtLink></li>
            <li><NuxtLink to="/barrels?category=new" class="footer__link">New Arrivals</NuxtLink></li>
          </ul>
        </div>

        <!-- Professional Services -->
        <div class="footer__section">
          <h3 class="footer__section-title">Professional Services</h3>
          <ul class="footer__links">
            <li><NuxtLink to="/professional" class="footer__link">Bulk Ordering</NuxtLink></li>
            <li><NuxtLink to="/professional" class="footer__link">Custom Manufacturing</NuxtLink></li>
            <li><NuxtLink to="/professional" class="footer__link">Technical Support</NuxtLink></li>
            <li><NuxtLink to="/professional" class="footer__link">Consultation</NuxtLink></li>
            <li><NuxtLink to="/professional" class="footer__link">International Shipping</NuxtLink></li>
          </ul>
        </div>

        <!-- Contact Information -->
        <div class="footer__section">
          <h3 class="footer__section-title">Contact Us</h3>
          <div class="footer__contact">
            <div class="footer__contact-item">
              <div class="footer__contact-icon-placeholder"></div>
              <div>
                <p class="footer__contact-label">Phone</p>
                <p class="footer__contact-value">+33 1 23 45 67 89</p>
              </div>
            </div>
            <div class="footer__contact-item">
              <div class="footer__contact-icon-placeholder"></div>
              <div>
                <p class="footer__contact-label">Email</p>
                <p class="footer__contact-value">info@millesime-sans-frontieres.com</p>
              </div>
            </div>
            <div class="footer__contact-item">
              <div class="footer__contact-icon-placeholder"></div>
              <div>
                <p class="footer__contact-label">Office</p>
                <p class="footer__contact-value">123 Rue du Commerce<br>75015 Paris, France</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer__bottom">
        <div class="footer__bottom-content">
          <p class="footer__copyright">
            © {{ currentYear }} Millésime Sans Frontières. All rights reserved.
          </p>
          <div class="footer__legal">
            <NuxtLink to="/privacy" class="footer__legal-link">Privacy Policy</NuxtLink>
            <NuxtLink to="/terms" class="footer__legal-link">Terms of Service</NuxtLink>
            <NuxtLink to="/cookies" class="footer__legal-link">Cookie Policy</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background: var(--color-oak-brown-900);
  color: white;
  padding: 4rem 0 2rem;
}

.footer__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

/* Company Information */
.footer__logo {
  margin-bottom: 1.5rem;
}

.footer__logo-brand {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  font-family: 'Playfair Display', serif;
  color: var(--color-whisky-gold-400);
  line-height: 1;
}

.footer__logo-tagline {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-whisky-gold-500);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  line-height: 1;
}

.footer__description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.footer__social {
  display: flex;
  gap: 1rem;
}

.footer__social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.footer__social-link:hover {
  background: var(--color-whisky-gold-500);
  transform: translateY(-2px);
}

.footer__social-icon-placeholder {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 2px;
}

/* Section Titles */
.footer__section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-whisky-gold-400);
  margin-bottom: 1.5rem;
}

/* Links */
.footer__links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__links li {
  margin-bottom: 0.75rem;
}

.footer__link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
}

.footer__link:hover {
  color: var(--color-whisky-gold-400);
}

/* Contact Information */
.footer__contact {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.footer__contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.footer__contact-icon-placeholder {
  width: 20px;
  height: 20px;
  background: var(--color-whisky-gold-500);
  border-radius: 4px;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.footer__contact-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-whisky-gold-400);
  margin-bottom: 0.25rem;
}

.footer__contact-value {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  font-size: 0.875rem;
}

/* Footer Bottom */
.footer__bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 2rem;
}

.footer__bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer__copyright {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
}

.footer__legal {
  display: flex;
  gap: 2rem;
}

.footer__legal-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.footer__legal-link:hover {
  color: var(--color-whisky-gold-400);
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer__content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer__bottom-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer__legal {
    justify-content: center;
  }
}
</style>
