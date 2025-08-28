<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-card">
        <!-- Logo -->
        <div class="logo-section">
          <div class="logo">
            <span class="logo__brand">Millésime</span>
            <span class="logo__tagline">SANS FRONTIÈRES</span>
          </div>
          <h1 class="login-title">Admin Access</h1>
          <p class="login-subtitle">Sign in to access the administrative dashboard</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              class="form-input" 
              required
              placeholder="Enter your username"
              autocomplete="username"
            />
          </div>
          
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <div class="password-input">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="password" 
                class="form-input" 
                required
                placeholder="Enter your password"
                autocomplete="current-password"
              />
              <button 
                type="button" 
                class="password-toggle" 
                @click="togglePassword"
              >
                {{ showPassword ? '👁️' : '🙈' }}
              </button>
            </div>
          </div>
          
          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" class="checkbox" />
              <span class="checkmark"></span>
              Remember me for 30 days
            </label>
          </div>
          
          <button type="submit" class="login-button" :disabled="isLoading">
            <span v-if="isLoading" class="loading-spinner"></span>
            {{ isLoading ? 'Signing In...' : 'Sign In' }}
          </button>
        </form>

        <!-- Security Notice -->
        <div class="security-notice">
          <div class="security-icon">🔒</div>
          <p>This is a secure administrative area. Unauthorized access attempts will be logged and reported.</p>
        </div>

        <!-- Back to Main Site -->
        <div class="back-to-site">
          <NuxtLink to="/" class="back-link">
            ← Back to Main Site
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Admin Login - Millésime Sans Frontières',
  description: 'Secure administrative access for site management.'
})

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)
const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alert('Please enter both username and password')
    return
  }

  isLoading.value = true
  
  try {
    // TODO: Implement actual admin authentication
    console.log('Admin login attempt:', { 
      username: username.value, 
      password: password.value, 
      rememberMe: rememberMe.value 
    })
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // For demo purposes, accept any login
    if (username.value && password.value) {
      // TODO: Store admin token/session
      console.log('Admin login successful')
      navigateTo('/admin')
    } else {
      alert('Invalid credentials')
    }
    
  } catch (error) {
    console.error('Admin login failed:', error)
    alert('Login failed. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e293b, #334155);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

/* Logo Section */
.logo-section {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.logo__brand {
  font-size: 2rem;
  font-weight: 700;
  color: #1c1917;
  font-family: 'Playfair Display', serif;
  line-height: 1;
}

.logo__tagline {
  font-size: 0.75rem;
  font-weight: 600;
  color: #dc2626;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  line-height: 1;
}

.login-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', serif;
}

.login-subtitle {
  color: #57534e;
  font-size: 1rem;
  margin: 0;
}

/* Login Form */
.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #292524;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #1c1917;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-input::placeholder {
  color: #a8a29e;
}

.password-input {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.password-toggle:hover {
  background: #f3f4f6;
}

.form-options {
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #57534e;
  cursor: pointer;
  font-size: 0.875rem;
}

.checkbox {
  width: 16px;
  height: 16px;
  accent-color: #dc2626;
}

.login-button {
  width: 100%;
  background: #dc2626;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-button:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-2px);
}

.login-button:disabled {
  background: #a8a29e;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Security Notice */
.security-notice {
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.security-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.security-notice p {
  color: #92400e;
  font-size: 0.875rem;
  margin: 0;
  line-height: 1.4;
}

/* Back to Site */
.back-to-site {
  text-align: center;
}

.back-link {
  color: #57534e;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #dc2626;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-login {
    padding: 1rem;
  }
  
  .login-card {
    padding: 2rem;
  }
  
  .logo__brand {
    font-size: 1.75rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>
