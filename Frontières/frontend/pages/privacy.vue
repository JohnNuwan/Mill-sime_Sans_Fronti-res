<template>
  <div class="privacy-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Privacy Policy</h1>
        <p class="hero__subtitle">
          How we collect, use, and protect your personal information
        </p>
      </div>
    </section>

    <!-- Privacy Content -->
    <section class="privacy-content">
      <div class="container">
        <div class="content-card">
          <div class="content-section">
            <h2>1. Information We Collect</h2>
            <p>We collect information you provide directly to us, such as when you create an account, make a purchase, or contact us for support. This may include:</p>
            <ul>
              <li>Name and contact information (email, phone, address)</li>
              <li>Company information and professional details</li>
              <li>Payment and billing information</li>
              <li>Communication preferences</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>2. How We Use Your Information</h2>
            <p>We use the information we collect to:</p>
            <ul>
              <li>Provide, maintain, and improve our services</li>
              <li>Process transactions and send related information</li>
              <li>Send technical notices, updates, and support messages</li>
              <li>Respond to your comments and questions</li>
              <li>Communicate with you about products, services, and events</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>3. Information Sharing</h2>
            <p>We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy. We may share your information with:</p>
            <ul>
              <li>Service providers who assist in our operations</li>
              <li>Legal authorities when required by law</li>
              <li>Business partners with your explicit consent</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>4. Data Security</h2>
            <p>We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. These measures include:</p>
            <ul>
              <li>Encryption of sensitive data</li>
              <li>Regular security assessments</li>
              <li>Access controls and authentication</li>
              <li>Secure data transmission protocols</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>5. Cookies and Tracking</h2>
            <p>We use cookies and similar technologies to enhance your browsing experience, analyze site traffic, and understand where our visitors are coming from. You can control cookie settings through your browser preferences.</p>
          </div>

          <div class="content-section">
            <h2>6. Your Rights</h2>
            <p>You have the right to:</p>
            <ul>
              <li>Access and review your personal information</li>
              <li>Request correction of inaccurate data</li>
              <li>Request deletion of your personal information</li>
              <li>Opt-out of marketing communications</li>
              <li>Withdraw consent for data processing</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>7. Data Retention</h2>
            <p>We retain your personal information for as long as necessary to provide our services and fulfill the purposes outlined in this policy. We may retain certain information for legal, regulatory, or business purposes.</p>
          </div>

          <div class="content-section">
            <h2>8. International Transfers</h2>
            <p>Your information may be transferred to and processed in countries other than your own. We ensure that such transfers comply with applicable data protection laws and implement appropriate safeguards.</p>
          </div>

          <div class="content-section">
            <h2>9. Children's Privacy</h2>
            <p>Our services are not intended for children under the age of 16. We do not knowingly collect personal information from children under 16. If you believe we have collected such information, please contact us immediately.</p>
          </div>

          <div class="content-section">
            <h2>10. Changes to This Policy</h2>
            <p>We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the "Last Updated" date.</p>
          </div>

          <div class="content-section">
            <h2>Contact Us</h2>
            <p>If you have any questions about this Privacy Policy or our data practices, please contact us at:</p>
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
  title: 'Privacy Policy - Millésime Sans Frontières',
  description: 'Learn how we collect, use, and protect your personal information.'
})
</script>

<style scoped>
.privacy-page {
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

/* Privacy Content */
.privacy-content {
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
}
</style>
