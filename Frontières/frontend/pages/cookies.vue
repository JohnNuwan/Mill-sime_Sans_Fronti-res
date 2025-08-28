<template>
  <div class="cookies-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Cookie Policy</h1>
        <p class="hero__subtitle">
          Understanding how we use cookies to improve your experience
        </p>
      </div>
    </section>

    <!-- Cookies Content -->
    <section class="cookies-content">
      <div class="container">
        <div class="content-card">
          <div class="content-section">
            <h2>What Are Cookies?</h2>
            <p>Cookies are small text files that are placed on your device when you visit our website. They help us provide you with a better experience by remembering your preferences and analyzing how you use our site.</p>
          </div>

          <div class="content-section">
            <h2>Types of Cookies We Use</h2>
            
            <div class="cookie-type">
              <h3>Essential Cookies</h3>
              <p>These cookies are necessary for the website to function properly. They enable basic functions like page navigation, access to secure areas, and form submissions. The website cannot function properly without these cookies.</p>
              <ul>
                <li>Authentication cookies</li>
                <li>Security cookies</li>
                <li>Session management cookies</li>
              </ul>
            </div>

            <div class="cookie-type">
              <h3>Performance Cookies</h3>
              <p>These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously. This helps us improve the way our website works.</p>
              <ul>
                <li>Analytics cookies</li>
                <li>Error tracking cookies</li>
                <li>Performance monitoring cookies</li>
              </ul>
            </div>

            <div class="cookie-type">
              <h3>Functional Cookies</h3>
              <p>These cookies enable enhanced functionality and personalization, such as remembering your language preferences and customizing content based on your interests.</p>
              <ul>
                <li>Language preference cookies</li>
                <li>User preference cookies</li>
                <li>Customization cookies</li>
              </ul>
            </div>

            <div class="cookie-type">
              <h3>Marketing Cookies</h3>
              <p>These cookies are used to track visitors across websites to display relevant and engaging advertisements. They may also be used to limit the number of times you see an ad.</p>
              <ul>
                <li>Advertising cookies</li>
                <li>Social media cookies</li>
                <li>Retargeting cookies</li>
              </ul>
            </div>
          </div>

          <div class="content-section">
            <h2>Third-Party Cookies</h2>
            <p>Some cookies on our website are set by third-party services that we use to enhance your experience. These may include:</p>
            <ul>
              <li><strong>Google Analytics:</strong> To analyze website traffic and user behavior</li>
              <li><strong>Social Media Platforms:</strong> To enable social sharing and integration</li>
              <li><strong>Payment Processors:</strong> To securely process transactions</li>
              <li><strong>Customer Support Tools:</strong> To provide better assistance</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>Managing Your Cookie Preferences</h2>
            <p>You have several options for managing cookies:</p>
            
            <div class="management-option">
              <h3>Browser Settings</h3>
              <p>Most web browsers allow you to control cookies through their settings. You can:</p>
              <ul>
                <li>Block all cookies</li>
                <li>Block only third-party cookies</li>
                <li>Delete existing cookies</li>
                <li>Set preferences for specific websites</li>
              </ul>
            </div>

            <div class="management-option">
              <h3>Cookie Consent</h3>
              <p>When you first visit our website, you'll see a cookie consent banner. You can:</p>
              <ul>
                <li>Accept all cookies</li>
                <li>Accept only essential cookies</li>
                <li>Customize your preferences</li>
                <li>Change your settings later</li>
              </ul>
            </div>

            <div class="management-option">
              <h3>Opt-Out Tools</h3>
              <p>For specific types of cookies, you can use opt-out tools provided by third-party services:</p>
              <ul>
                <li>Google Analytics Opt-out Browser Add-on</li>
                <li>Digital Advertising Alliance (DAA) Opt-out</li>
                <li>European Interactive Digital Advertising Alliance (EDAA)</li>
              </ul>
            </div>
          </div>

          <div class="content-section">
            <h2>Impact of Disabling Cookies</h2>
            <p>Please note that disabling certain cookies may affect the functionality of our website:</p>
            <ul>
              <li>Some features may not work properly</li>
              <li>Your preferences may not be remembered</li>
              <li>You may need to re-enter information</li>
              <li>Some content may not be personalized</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>Updates to This Policy</h2>
            <p>We may update this Cookie Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. We will notify you of any material changes by posting the updated policy on our website.</p>
          </div>

          <div class="content-section">
            <h2>Contact Us</h2>
            <p>If you have any questions about our use of cookies or this Cookie Policy, please contact us at:</p>
            <p><strong>Email:</strong> privacy@millesime-sans-frontieres.com</p>
            <p><strong>Phone:</strong> +33 123 45 67 89</p>
            <p><strong>Address:</strong> 123 Wine Street, Bordeaux, France</p>
          </div>

          <div class="content-section">
            <p><em>Last Updated: August 28, 2025</em></p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Cookie Policy - Millésime Sans Frontières',
  description: 'Learn about how we use cookies to improve your website experience.'
})
</script>

<style scoped>
.cookies-page {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  position: relative;
  height: 40vh;
  min-height: 300px;
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
  max-width: 600px;
  padding: 0 2rem;
}

.hero__title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  font-family: 'Playfair Display', serif;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero__subtitle {
  font-size: 1.125rem;
  line-height: 1.6;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* Cookies Content */
.cookies-content {
  padding: 4rem 0;
  background: #fafaf9;
  min-height: 60vh;
}

.content-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

.content-section {
  margin-bottom: 2.5rem;
}

.content-section:last-child {
  margin-bottom: 0;
}

.content-section h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 1rem;
  font-family: 'Playfair Display', serif;
}

.content-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #292524;
  margin-bottom: 0.75rem;
  margin-top: 1.5rem;
}

.content-section p {
  color: #44403c;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.content-section ul {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.content-section li {
  color: #44403c;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.content-section strong {
  color: #1c1917;
  font-weight: 600;
}

.content-section em {
  color: #78716c;
  font-style: italic;
}

.cookie-type, .management-option {
  background: #f5f5f4;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
  border-left: 4px solid #dc2626;
}

.cookie-type h3, .management-option h3 {
  margin-top: 0;
  color: #dc2626;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero__title {
    font-size: 2.5rem;
  }
  
  .hero__subtitle {
    font-size: 1rem;
  }
  
  .content-card {
    padding: 2rem;
    margin: 0 1rem;
  }
  
  .content-section h2 {
    font-size: 1.25rem;
  }
  
  .content-section h3 {
    font-size: 1.125rem;
  }
  
  .cookie-type, .management-option {
    padding: 1rem;
  }
}
</style>
