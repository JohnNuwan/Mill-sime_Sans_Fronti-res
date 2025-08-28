<template>
  <div class="terms-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Terms of Service</h1>
        <p class="hero__subtitle">
          Please read these terms carefully before using our services
        </p>
      </div>
    </section>

    <!-- Terms Content -->
    <section class="terms-content">
      <div class="container">
        <div class="content-card">
          <div class="content-section">
            <h2>1. Acceptance of Terms</h2>
            <p>By accessing and using the Millésime Sans Frontières website and services, you accept and agree to be bound by the terms and provision of this agreement.</p>
          </div>

          <div class="content-section">
            <h2>2. Use License</h2>
            <p>Permission is granted to temporarily download one copy of the materials (information or software) on Millésime Sans Frontières's website for personal, non-commercial transitory viewing only.</p>
            <p>This is the grant of a license, not a transfer of title, and under this license you may not:</p>
            <ul>
              <li>modify or copy the materials</li>
              <li>use the materials for any commercial purpose or for any public display</li>
              <li>attempt to reverse engineer any software contained on the website</li>
              <li>remove any copyright or other proprietary notations from the materials</li>
            </ul>
          </div>

          <div class="content-section">
            <h2>3. Disclaimer</h2>
            <p>The materials on Millésime Sans Frontières's website are provided on an 'as is' basis. Millésime Sans Frontières makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
          </div>

          <div class="content-section">
            <h2>4. Limitations</h2>
            <p>In no event shall Millésime Sans Frontières or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on the website.</p>
          </div>

          <div class="content-section">
            <h2>5. Accuracy of Materials</h2>
            <p>The materials appearing on Millésime Sans Frontières's website could include technical, typographical, or photographic errors. Millésime Sans Frontières does not warrant that any of the materials on its website are accurate, complete or current.</p>
          </div>

          <div class="content-section">
            <h2>6. Links</h2>
            <p>Millésime Sans Frontières has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by Millésime Sans Frontières of the site.</p>
          </div>

          <div class="content-section">
            <h2>7. Modifications</h2>
            <p>Millésime Sans Frontières may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these Terms of Service.</p>
          </div>

          <div class="content-section">
            <h2>8. Governing Law</h2>
            <p>These terms and conditions are governed by and construed in accordance with the laws of France and you irrevocably submit to the exclusive jurisdiction of the courts in that location.</p>
          </div>

          <div class="content-section">
            <h2>Contact Information</h2>
            <p>If you have any questions about these Terms of Service, please contact us at:</p>
            <p><strong>Email:</strong> legal@millesime-sans-frontieres.com</p>
            <p><strong>Phone:</strong> +33 123 45 67 89</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Terms of Service - Millésime Sans Frontières',
  description: 'Terms and conditions for using our wine and spirits barrel services.'
})
</script>

<style scoped>
.terms-page {
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

/* Terms Content */
.terms-content {
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
