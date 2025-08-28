<template>
  <div class="professional-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__image-placeholder"></div>
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Professional Services</h1>
        <p class="hero__subtitle">
          Dedicated solutions for wineries, distilleries, and professional barrel buyers
        </p>
      </div>
    </section>

    <!-- Services Overview -->
    <section class="services-overview">
      <div class="container">
        <h2 class="services-overview__title">Professional Solutions</h2>
        <div class="services-overview__grid">
          <div class="service-card">
            <div class="service-card__icon">
              <div class="service-card__icon-placeholder"></div>
            </div>
            <h3 class="service-card__title">Bulk Orders</h3>
            <p class="service-card__description">
              Special pricing and dedicated support for large volume orders. 
              Minimum order quantities and volume discounts available.
            </p>
            <ul class="service-card__features">
              <li>Volume discounts starting at 10+ units</li>
              <li>Dedicated account manager</li>
              <li>Priority shipping and handling</li>
              <li>Custom payment terms</li>
            </ul>
          </div>

          <div class="service-card">
            <div class="service-card__icon">
              <div class="service-card__icon-placeholder"></div>
            </div>
            <h3 class="service-card__title">Custom Specifications</h3>
            <p class="service-card__description">
              Tailored barrel solutions to meet your specific requirements. 
              Custom sizes, wood types, toasting levels, and finishes.
            </p>
            <ul class="service-card__features">
              <li>Custom dimensions and capacities</li>
              <li>Specialized wood treatments</li>
              <li>Branded barrel heads</li>
              <li>Custom finishing options</li>
            </ul>
          </div>

          <div class="service-card">
            <div class="service-card__icon">
              <div class="service-card__icon-placeholder"></div>
            </div>
            <h3 class="service-card__title">Technical Support</h3>
            <p class="service-card__description">
              Expert guidance on barrel selection, maintenance, and optimal usage 
              for your specific wine or spirit production needs.
            </p>
            <ul class="service-card__features">
              <li>Barrel selection consultation</li>
              <li>Maintenance best practices</li>
              <li>Production optimization advice</li>
              <li>24/7 technical support</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Bulk Ordering -->
    <section class="bulk-ordering">
      <div class="container">
        <div class="bulk-ordering__content">
          <div class="bulk-ordering__text">
            <h2 class="bulk-ordering__title">Bulk Ordering Program</h2>
            <p class="bulk-ordering__description">
              Our bulk ordering program is designed for professional buyers who need consistent, 
              high-quality barrels in large quantities. We offer competitive pricing, 
              flexible payment terms, and dedicated support for bulk orders.
            </p>
            <div class="bulk-ordering__benefits">
              <div class="benefit-item">
                <div class="benefit-item__icon">✓</div>
                <div class="benefit-item__text">
                  <h4>Volume Discounts</h4>
                  <p>Up to 25% off for orders of 50+ units</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-item__icon">✓</div>
                <div class="benefit-item__text">
                  <h4>Priority Production</h4>
                  <p>Faster turnaround times for bulk orders</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-item__icon">✓</div>
                <div class="benefit-item__text">
                  <h4>Dedicated Support</h4>
                  <p>Personal account manager for all orders</p>
                </div>
              </div>
            </div>
          </div>
          <div class="bulk-ordering__form">
            <h3 class="bulk-ordering__form-title">Request Bulk Quote</h3>
            <form class="bulk-form">
              <div class="form-group">
                <label for="company">Company Name</label>
                <input type="text" id="company" name="company" required>
              </div>
              <div class="form-group">
                <label for="contact">Contact Person</label>
                <input type="text" id="contact" name="contact" required>
              </div>
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
              </div>
              <div class="form-group">
                <label for="quantity">Estimated Quantity</label>
                <select id="quantity" name="quantity" required>
                  <option value="">Select quantity range</option>
                  <option value="10-25">10-25 units</option>
                  <option value="26-50">26-50 units</option>
                  <option value="51-100">51-100 units</option>
                  <option value="100+">100+ units</option>
                </select>
              </div>
              <div class="form-group">
                <label for="timeline">Delivery Timeline</label>
                <select id="timeline" name="timeline" required>
                  <option value="">Select timeline</option>
                  <option value="1-2 months">1-2 months</option>
                  <option value="3-4 months">3-4 months</option>
                  <option value="5-6 months">5-6 months</option>
                  <option value="6+ months">6+ months</option>
                </select>
              </div>
              <div class="form-group">
                <label for="requirements">Special Requirements</label>
                <textarea id="requirements" name="requirements" rows="4" placeholder="Describe any special specifications, customizations, or requirements..."></textarea>
              </div>
              <button type="submit" class="bulk-form__submit">Request Quote</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- Custom Manufacturing -->
    <section class="custom-manufacturing">
      <div class="container">
        <h2 class="custom-manufacturing__title">Custom Manufacturing</h2>
        <p class="custom-manufacturing__description">
          We specialize in creating custom barrels that meet your exact specifications. 
          From unique dimensions to specialized treatments, our master coopers can bring your vision to life.
        </p>
        
        <div class="custom-manufacturing__options">
          <div class="custom-option">
            <h3>Custom Dimensions</h3>
            <ul>
              <li>Non-standard barrel sizes</li>
              <li>Custom height and diameter</li>
              <li>Specialized capacity requirements</li>
              <li>Unique shape modifications</li>
            </ul>
          </div>
          
          <div class="custom-option">
            <h3>Wood Treatments</h3>
            <ul>
              <li>Custom toasting levels</li>
              <li>Specialized charring techniques</li>
              <li>Wood aging and seasoning</li>
              <li>Custom wood combinations</li>
            </ul>
          </div>
          
          <div class="custom-option">
            <h3>Finishing Options</h3>
            <ul>
              <li>Custom barrel head designs</li>
              <li>Branded markings and logos</li>
              <li>Specialized surface treatments</li>
              <li>Custom hardware options</li>
            </ul>
          </div>
        </div>
        
        <div class="custom-manufacturing__cta">
          <h3>Ready to Create Your Custom Barrel?</h3>
          <p>Contact our custom manufacturing team to discuss your requirements and get a detailed quote.</p>
          <button class="custom-manufacturing__button">Start Custom Project</button>
        </div>
      </div>
    </section>

    <!-- Professional Support -->
    <section class="professional-support">
      <div class="container">
        <h2 class="professional-support__title">Professional Support Services</h2>
        <div class="professional-support__grid">
          <div class="support-service">
            <h3>Barrel Selection Consultation</h3>
            <p>
              Our experts will help you choose the perfect barrels for your specific wine or spirit production. 
              We consider your production methods, desired flavor profiles, and budget to recommend the ideal solution.
            </p>
            <ul>
              <li>Production method analysis</li>
              <li>Flavor profile recommendations</li>
              <li>Budget optimization</li>
              <li>Long-term planning</li>
            </ul>
          </div>
          
          <div class="support-service">
            <h3>Maintenance & Care</h3>
            <p>
              Proper barrel maintenance is crucial for optimal performance and longevity. 
              We provide comprehensive guidance on cleaning, storage, and maintenance procedures.
            </p>
            <ul>
              <li>Cleaning protocols</li>
              <li>Storage best practices</li>
              <li>Maintenance schedules</li>
              <li>Troubleshooting guides</li>
            </ul>
          </div>
          
          <div class="support-service">
            <h3>Production Optimization</h3>
            <p>
              Maximize your barrel investment with expert advice on production techniques, 
              aging strategies, and quality control measures.
            </p>
            <ul>
              <li>Production workflow optimization</li>
              <li>Aging strategy development</li>
              <li>Quality control implementation</li>
              <li>Efficiency improvements</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section class="contact-section">
      <div class="container">
        <div class="contact-section__content">
          <h2 class="contact-section__title">Get Professional Support</h2>
          <p class="contact-section__description">
            Our professional services team is ready to help you find the perfect barrel solutions. 
            Contact us today to discuss your needs and learn how we can support your business.
          </p>
          
          <div class="contact-section__methods">
            <div class="contact-method">
              <h3>Phone Support</h3>
              <p>+33 1 23 45 67 89</p>
              <p>Monday - Friday: 8:00 AM - 6:00 PM CET</p>
            </div>
            
            <div class="contact-method">
              <h3>Email Support</h3>
              <p>professional@millesime-sans-frontieres.com</p>
              <p>Response within 24 hours</p>
            </div>
            
            <div class="contact-method">
              <h3>Video Consultation</h3>
              <p>Schedule a virtual meeting with our experts</p>
              <p>Available worldwide</p>
            </div>
          </div>
          
          <button class="contact-section__button">Schedule Consultation</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Professional Services - Millésime Sans Frontières',
  description: 'Professional barrel solutions for wineries, distilleries, and bulk buyers. Custom manufacturing, bulk ordering, and expert support.'
})
</script>

<style scoped>
.professional-page {
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
  background: linear-gradient(135deg, var(--color-oak-brown-900), var(--color-wine-red-800));
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

/* Services Overview */
.services-overview {
  padding: 5rem 0;
  background: var(--color-cream-50);
}

.services-overview__title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 3rem;
  font-family: 'Playfair Display', serif;
}

.services-overview__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
}

.service-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--color-cream-200);
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.service-card__icon {
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
  border-radius: 50%;
  overflow: hidden;
}

.service-card__icon-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-wine-red-500), var(--color-whisky-gold-500));
}

.service-card__title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1rem;
}

.service-card__description {
  color: var(--color-oak-brown-700);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.service-card__features {
  list-style: none;
  padding: 0;
}

.service-card__features li {
  padding: 0.5rem 0;
  color: var(--color-oak-brown-700);
  position: relative;
  padding-left: 1.5rem;
}

.service-card__features li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: var(--color-wine-red-600);
  font-weight: 700;
}

/* Bulk Ordering */
.bulk-ordering {
  padding: 5rem 0;
  background: white;
}

.bulk-ordering__content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.bulk-ordering__title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 2rem;
  font-family: 'Playfair Display', serif;
}

.bulk-ordering__description {
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--color-oak-brown-700);
  margin-bottom: 2rem;
}

.bulk-ordering__benefits {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.benefit-item__icon {
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

.benefit-item__text h4 {
  font-weight: 600;
  color: var(--color-oak-brown-900);
  margin-bottom: 0.25rem;
}

.benefit-item__text p {
  color: var(--color-oak-brown-700);
  line-height: 1.5;
}

/* Bulk Ordering Form */
.bulk-ordering__form {
  background: var(--color-cream-50);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--color-cream-200);
}

.bulk-ordering__form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1.5rem;
  text-align: center;
}

.bulk-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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
  min-height: 100px;
}

.bulk-form__submit {
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

.bulk-form__submit:hover {
  background: var(--color-wine-red-700);
  transform: translateY(-2px);
}

/* Custom Manufacturing */
.custom-manufacturing {
  padding: 5rem 0;
  background: var(--color-oak-brown-900);
  color: white;
}

.custom-manufacturing__title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

.custom-manufacturing__description {
  text-align: center;
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0.9;
}

.custom-manufacturing__options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.custom-option {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.custom-option h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--color-whisky-gold-400);
}

.custom-option ul {
  list-style: none;
  padding: 0;
}

.custom-option li {
  padding: 0.5rem 0;
  opacity: 0.9;
  position: relative;
  padding-left: 1.5rem;
}

.custom-option li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--color-whisky-gold-400);
  font-weight: 700;
}

.custom-manufacturing__cta {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.custom-manufacturing__cta h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--color-whisky-gold-400);
}

.custom-manufacturing__cta p {
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.custom-manufacturing__button {
  background: var(--color-whisky-gold-500);
  color: var(--color-oak-brown-900);
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-manufacturing__button:hover {
  background: var(--color-whisky-gold-400);
  transform: translateY(-2px);
}

/* Professional Support */
.professional-support {
  padding: 5rem 0;
  background: white;
}

.professional-support__title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 3rem;
  font-family: 'Playfair Display', serif;
}

.professional-support__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
}

.support-service {
  background: var(--color-cream-50);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--color-cream-200);
}

.support-service h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1rem;
}

.support-service p {
  color: var(--color-oak-brown-700);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.support-service ul {
  list-style: none;
  padding: 0;
}

.support-service li {
  padding: 0.5rem 0;
  color: var(--color-oak-brown-700);
  position: relative;
  padding-left: 1.5rem;
}

.support-service li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: var(--color-wine-red-600);
  font-weight: 700;
}

/* Contact Section */
.contact-section {
  padding: 5rem 0;
  background: var(--color-cream-100);
}

.contact-section__content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.contact-section__title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

.contact-section__description {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--color-oak-brown-700);
  margin-bottom: 3rem;
}

.contact-section__methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.contact-method {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-cream-200);
}

.contact-method h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-oak-brown-900);
  margin-bottom: 1rem;
}

.contact-method p {
  color: var(--color-oak-brown-700);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.contact-method p:last-child {
  margin-bottom: 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.contact-section__button {
  background: var(--color-wine-red-600);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.contact-section__button:hover {
  background: var(--color-wine-red-700);
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
  
  .bulk-ordering__content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .services-overview__title,
  .bulk-ordering__title,
  .custom-manufacturing__title,
  .professional-support__title,
  .contact-section__title {
    font-size: 2rem;
  }
  
  .services-overview__grid,
  .professional-support__grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .custom-manufacturing__options {
    grid-template-columns: 1fr;
  }
  
  .contact-section__methods {
    grid-template-columns: 1fr;
  }
}
</style>
