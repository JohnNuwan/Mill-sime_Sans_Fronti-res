<template>
  <div class="login-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__background">
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <h1 class="hero__title">Login to Your Account</h1>
        <p class="hero__subtitle">
          Access your professional dashboard and manage your barrel orders
        </p>
      </div>
    </section>

    <!-- Login Form -->
    <section class="login-form">
      <div class="container">
        <div class="form-container">
          <div class="form-card">
            <h2 class="form-title">Welcome Back</h2>
            <p class="form-subtitle">Sign in to continue to your account</p>
            
            <form @submit.prevent="handleLogin" class="form">
              <div class="form-group">
                <label for="email" class="form-label">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="email" 
                  class="form-input" 
                  required
                  placeholder="Enter your email"
                />
              </div>
              
              <div class="form-group">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  class="form-input" 
                  required
                  placeholder="Enter your password"
                />
              </div>
              
              <div class="form-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="rememberMe" class="checkbox" />
                  <span class="checkmark"></span>
                  Remember me
                </label>
                <NuxtLink to="/forgot-password" class="forgot-link">Forgot Password?</NuxtLink>
              </div>
              
              <button type="submit" class="form-button" :disabled="isLoading">
                {{ isLoading ? 'Signing In...' : 'Sign In' }}
              </button>
            </form>
            
            <div class="form-footer">
              <p>Don't have an account? <NuxtLink to="/register" class="link">Sign up</NuxtLink></p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Login - Millésime Sans Frontières',
  description: 'Sign in to your professional account to manage barrel orders and access exclusive services.'
})

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    // TODO: Implement actual login logic
    console.log('Login attempt:', { email: email.value, password: password.value, rememberMe: rememberMe.value })
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // TODO: Redirect to dashboard or home page
    console.log('Login successful')
    
  } catch (error) {
    console.error('Login failed:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
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

/* Login Form */
.login-form {
  padding: 4rem 0;
  background: #fafaf9;
  min-height: 60vh;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 0.5rem;
  text-align: center;
  font-family: 'Playfair Display', serif;
}

.form-subtitle {
  color: #57534e;
  text-align: center;
  margin-bottom: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  color: #292524;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.875rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #1c1917;
}

.form-input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-input::placeholder {
  color: #a8a29e;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #57534e;
  cursor: pointer;
}

.checkbox {
  width: 16px;
  height: 16px;
  accent-color: #dc2626;
}

.forgot-link {
  color: #dc2626;
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  text-decoration: underline;
}

.form-button {
  background: #dc2626;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.form-button:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-2px);
}

.form-button:disabled {
  background: #a8a29e;
  cursor: not-allowed;
  transform: none;
}

.form-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e7e5e4;
  color: #57534e;
}

.link {
  color: #dc2626;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero__title {
    font-size: 2.5rem;
  }
  
  .hero__subtitle {
    font-size: 1rem;
  }
  
  .form-card {
    padding: 2rem;
    margin: 0 1rem;
  }
  
  .form-title {
    font-size: 1.75rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
