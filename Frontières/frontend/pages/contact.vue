<template>
  <div class="contact-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__image-placeholder"></div>
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Get in Touch</h1>
        <p class="hero__subtitle">
          We're here to help you find the perfect barrels for your needs
        </p>
      </div>
    </section>

    <!-- Contact Information -->
    <section class="contact-info">
      <div class="container">
        <div class="contact-info__grid">
          <div class="contact-method">
            <div class="contact-method__icon">
              <div class="contact-method__icon-placeholder"></div>
            </div>
            <h3>Phone</h3>
            <p class="contact-method__primary">+33 1 23 45 67 89</p>
            <p class="contact-method__secondary">Monday - Friday: 8:00 AM - 6:00 PM CET</p>
            <p class="contact-method__secondary">Saturday: 9:00 AM - 2:00 PM CET</p>
          </div>

          <div class="contact-method">
            <div class="contact-method__icon">
              <div class="contact-method__icon-placeholder"></div>
            </div>
            <h3>Email</h3>
            <p class="contact-method__primary">info@millesime-sans-frontieres.com</p>
            <p class="contact-method__secondary">General inquiries</p>
            <p class="contact-method__secondary">Response within 24 hours</p>
          </div>

          <div class="contact-method">
            <div class="contact-method__icon">
              <div class="contact-method__icon-placeholder"></div>
            </div>
            <h3>Professional Services</h3>
            <p class="contact-method__primary">professional@millesime-sans-frontieres.com</p>
            <p class="contact-method__secondary">Bulk orders & custom manufacturing</p>
            <p class="contact-method__secondary">Dedicated support team</p>
          </div>

          <div class="contact-method">
            <div class="contact-method__icon">
              <div class="contact-method__icon-placeholder"></div>
            </div>
            <h3>Office</h3>
            <p class="contact-method__primary">123 Rue du Commerce</p>
            <p class="contact-method__secondary">75015 Paris, France</p>
            <p class="contact-method__secondary">By appointment only</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Form Section -->
    <section class="contact-form-section">
      <div class="container">
        <div class="contact-form-section__content">
          <div class="contact-form-section__text">
            <h2 class="contact-form-section__title">Send Us a Message</h2>
            <p class="contact-form-section__description">
              Have a question about our barrels? Need a custom quote? Want to discuss bulk ordering? 
              Fill out the form below and we'll get back to you as soon as possible.
            </p>
            
            <div class="contact-form-section__features">
              <div class="feature-item">
                <div class="feature-item__icon">✓</div>
                <div class="feature-item__text">
                  <h4>Quick Response</h4>
                  <p>We typically respond within 24 hours</p>
                </div>
              </div>
              
              <div class="feature-item">
                <div class="feature-item__icon">✓</div>
                <div class="feature-item__text">
                  <h4>Expert Support</h4>
                  <p>Our barrel specialists are here to help</p>
                </div>
              </div>
              
              <div class="feature-item">
                <div class="feature-item__icon">✓</div>
                <div class="feature-item__text">
                  <h4>No Obligation</h4>
                  <p>Get information and quotes without commitment</p>
                </div>
              </div>
            </div>
          </div>

          <div class="contact-form-section__form">
            <form class="contact-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="first-name">First Name *</label>
                  <input type="text" id="first-name" name="first-name" required>
                </div>
                <div class="form-group">
                  <label for="last-name">Last Name *</label>
                  <input type="text" id="last-name" name="last-name" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="email">Email Address *</label>
                  <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                  <label for="phone">Phone Number</label>
                  <input type="tel" id="phone" name="phone">
                </div>
              </div>

              <div class="form-group">
                <label for="company">Company/Organization</label>
                <input type="text" id="company" name="company">
              </div>

              <div class="form-group">
                <label for="inquiry-type">Type of Inquiry *</label>
                <select id="inquiry-type" name="inquiry-type" required>
                  <option value="">Select inquiry type</option>
                  <option value="general">General Information</option>
                  <option value="product">Product Questions</option>
                  <option value="bulk">Bulk Ordering</option>
                  <option value="custom">Custom Manufacturing</option>
                  <option value="technical">Technical Support</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div class="form-group">
                <label for="subject">Subject *</label>
                <input type="text" id="subject" name="subject" required>
              </div>

              <div class="form-group">
                <label for="message">Message *</label>
                <textarea id="message" name="message" rows="6" required placeholder="Please describe your inquiry in detail..."></textarea>
              </div>

              <div class="form-group">
                <label class="checkbox-label">
                  <input type="checkbox" name="newsletter" id="newsletter">
                  <span class="checkmark"></span>
                  Subscribe to our newsletter for updates and special offers
                </label>
              </div>

              <button type="submit" class="contact-form__submit">Send Message</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
      <div class="container">
        <h2 class="faq-section__title">Frequently Asked Questions</h2>
        <div class="faq-section__content">
          <div class="faq-item">
            <button class="faq-item__question" @click="toggleFaq(0)">
              What types of barrels do you offer?
              <span class="faq-item__icon">{{ openFaq === 0 ? '−' : '+' }}</span>
            </button>
            <div class="faq-item__answer" :class="{ 'faq-item__answer--open': openFaq === 0 }">
              <p>
                We offer a wide variety of barrels including wine barrels (French, American, and Hungarian oak), 
                whiskey barrels, decorative barrels, and custom-made barrels. Our collection ranges from small 
                decorative pieces to large commercial barrels.
              </p>
            </div>
          </div>

          <div class="faq-item">
            <button class="faq-item__question" @click="toggleFaq(1)">
              Do you ship internationally?
              <span class="faq-item__icon">{{ openFaq === 1 ? '−' : '+' }}</span>
            </button>
            <div class="faq-item__answer" :class="{ 'faq-item__answer--open': openFaq === 1 }">
              <p>
                Yes, we ship worldwide! We have extensive experience in international shipping and can handle 
                customs documentation, special packaging requirements, and delivery to virtually any location. 
                Shipping costs and delivery times vary by destination.
              </p>
            </div>
          </div>

          <div class="faq-item">
            <button class="faq-item__question" @click="toggleFaq(2)">
              What are your minimum order quantities?
              <span class="faq-item__icon">{{ openFaq === 2 ? '−' : '+' }}</span>
            </button>
            <div class="faq-item__answer" :class="{ 'faq-item__answer--open': openFaq === 2 }">
              <p>
                For individual customers, there is no minimum order quantity. For professional buyers and 
                bulk orders, we offer special pricing starting at 10+ units, with additional discounts for 
                larger quantities.
              </p>
            </div>
          </div>

          <div class="faq-item">
            <button class="faq-item__question" @click="toggleFaq(3)">
              Can you create custom barrels?
              <span class="faq-item__icon">{{ openFaq === 3 ? '−' : '+' }}</span>
            </button>
            <div class="faq-item__answer" :class="{ 'faq-item__answer--open': openFaq === 3 }">
              <p>
                Absolutely! We specialize in custom barrel manufacturing. We can create barrels with custom 
                dimensions, wood types, toasting levels, finishes, and even branded elements. Custom orders 
                typically require 8-12 weeks for production.
              </p>
            </div>
          </div>

          <div class="faq-item">
            <button class="faq-item__question" @click="toggleFaq(4)">
              What payment methods do you accept?
              <span class="faq-item__icon">{{ openFaq === 4 ? '−' : '+' }}</span>
            </button>
            <div class="faq-item__answer" :class="{ 'faq-item__answer--open': openFaq === 4 }">
              <p>
                We accept major credit cards (Visa, MasterCard, American Express), bank transfers, and 
                for professional customers, we can arrange payment terms. All transactions are secure and 
                protected by industry-standard encryption.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="map-section">
      <div class="container">
        <h2 class="map-section__title">Visit Our Office</h2>
        <p class="map-section__description">
          Located in the heart of Paris, our office is easily accessible by public transportation. 
          We welcome visitors by appointment for consultations and barrel viewing.
        </p>
        <div class="map-section__map">
          <div class="map-placeholder">
            <div class="map-placeholder__content">
              <h3>Interactive Map</h3>
              <p>123 Rue du Commerce, 75015 Paris, France</p>
              <p>Metro: Commerce (Line 8)</p>
              <p>RER: Porte de Versailles (Line C)</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

definePageMeta({
  title: 'Contact Us - Millésime Sans Frontières',
  description: 'Get in touch with our barrel experts. Contact us for inquiries, quotes, and professional support.'
})

const openFaq = ref(null)

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}
</script>

<style scoped>
.contact-page {
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

.hero__image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-wine-red-700), var(--color-oak-brown-800));
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
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
}

.hero__subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  opacity: 0.9;
}

/* Contact Information */
.contact-info {
  padding: 5rem 0;
  background: var(--color-cream-50);
}

.contact-info__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2.5rem;
}

.contact-method {
  text-align: center;
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--color-cream-200);
  transition: all 0.3s ease;
}

.contact-method:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.contact-method__icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
}

.contact-method__icon-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-whisky-gold-500), var(--color-wine-red-600));
}

.contact-method h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1rem;
}

.contact-method__primary {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-wine-red-600);
  margin-bottom: 0.5rem;
}

.contact-method__secondary {
  font-size: 0.9rem;
  color: var(--color-oak-brown-700);
  line-height: 1.5;
  margin-bottom: 0.25rem;
}

/* Contact Form Section */
.contact-form-section {
  padding: 5rem 0;
  background: white;
}

.contact-form-section__content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.contact-form-section__title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

.contact-form-section__description {
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--color-oak-brown-700);
  margin-bottom: 2rem;
}

.contact-form-section__features {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.feature-item__icon {
  background: var(--color-wine-red-600);
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.feature-item__text h4 {
  font-weight: 600;
  color: var(--color-oak-brown-900);
  margin-bottom: 0.25rem;
}

.feature-item__text p {
  color: var(--color-oak-brown-700);
  line-height: 1.5;
  font-size: 0.9rem;
}

/* Contact Form */
.contact-form-section__form {
  background: var(--color-cream-50);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--color-cream-200);
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: var(--color-oak-brown-800);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid var(--color-cream-300);
  border-radius: 8px;
  background: white;
  color: var(--color-oak-brown-800);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-wine-red-500);
  box-shadow: 0 0 0 3px rgba(185, 28, 28, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

/* Checkbox Styling */
.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--color-oak-brown-700);
  line-height: 1.5;
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-cream-400);
  border-radius: 4px;
  background: white;
  flex-shrink: 0;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-label input[type="checkbox"]:checked + .checkmark {
  background: var(--color-wine-red-600);
  border-color: var(--color-wine-red-600);
}

.checkbox-label input[type="checkbox"]:checked + .checkmark::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
}

.contact-form__submit {
  background: var(--color-wine-red-600);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.contact-form__submit:hover {
  background: var(--color-wine-red-700);
  transform: translateY(-2px);
}

/* FAQ Section */
.faq-section {
  padding: 5rem 0;
  background: var(--color-cream-50);
}

.faq-section__title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 3rem;
  font-family: 'Playfair Display', serif;
}

.faq-section__content {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: white;
  border-radius: 12px;
  margin-bottom: 1rem;
  border: 1px solid var(--color-cream-200);
  overflow: hidden;
}

.faq-item__question {
  width: 100%;
  background: none;
  border: none;
  padding: 1.5rem;
  text-align: left;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-oak-brown-900);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.faq-item__question:hover {
  background: var(--color-cream-50);
}

.faq-item__icon {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-wine-red-600);
  transition: all 0.3s ease;
}

.faq-item__answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.faq-item__answer--open {
  max-height: 200px;
}

.faq-item__answer p {
  padding: 0 1.5rem 1.5rem;
  color: var(--color-oak-brown-700);
  line-height: 1.6;
  margin: 0;
}

/* Map Section */
.map-section {
  padding: 5rem 0;
  background: white;
}

.map-section__title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

.map-section__description {
  text-align: center;
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--color-oak-brown-700);
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.map-section__map {
  max-width: 800px;
  margin: 0 auto;
}

.map-placeholder {
  height: 400px;
  background: var(--color-cream-100);
  border-radius: 16px;
  border: 2px dashed var(--color-cream-300);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.map-placeholder__content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-800);
  margin-bottom: 1rem;
}

.map-placeholder__content p {
  color: var(--color-oak-brown-700);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero__title {
    font-size: 2.5rem;
  }
  
  .hero__subtitle {
    font-size: 1.125rem;
  }
  
  .contact-form-section__content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .contact-form-section__title,
  .faq-section__title,
  .map-section__title {
    font-size: 2rem;
  }
  
  .contact-info__grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
