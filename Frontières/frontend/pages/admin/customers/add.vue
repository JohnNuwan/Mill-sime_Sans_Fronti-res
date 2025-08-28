<template>
  <div class="add-customer">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <NuxtLink to="/admin/customers" class="back-link">
            ← Back to Customers
          </NuxtLink>
          <h1 class="page-title">Add New Customer</h1>
          <p class="page-subtitle">Create a new customer account for your business</p>
        </div>
      </div>
    </header>

    <!-- Customer Form -->
    <section class="customer-form">
      <div class="form-container">
        <form @submit.prevent="handleSubmit" class="form">
          <!-- Personal Information -->
          <div class="form-section">
            <h2 class="section-title">Personal Information</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="firstName" class="form-label">First Name *</label>
                <input
                  type="text"
                  id="firstName"
                  v-model="customerData.firstName"
                  class="form-input"
                  :class="{ 'error': errors.firstName }"
                  required
                  placeholder="e.g., John"
                />
                <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
              </div>

              <div class="form-group">
                <label for="lastName" class="form-label">Last Name *</label>
                <input
                  type="text"
                  id="lastName"
                  v-model="customerData.lastName"
                  class="form-input"
                  :class="{ 'error': errors.lastName }"
                  required
                  placeholder="e.g., Smith"
                />
                <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="email" class="form-label">Email Address *</label>
                <input
                  type="email"
                  id="email"
                  v-model="customerData.email"
                  class="form-input"
                  :class="{ 'error': errors.email }"
                  required
                  placeholder="e.g., john.smith@email.com"
                />
                <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
              </div>

              <div class="form-group">
                <label for="phone" class="form-label">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  v-model="customerData.phone"
                  class="form-input"
                  placeholder="e.g., +33 1 23 45 67 89"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="dateOfBirth" class="form-label">Date of Birth</label>
                <input
                  type="date"
                  id="dateOfBirth"
                  v-model="customerData.dateOfBirth"
                  class="form-input"
                  max="2006-12-31"
                />
              </div>

              <div class="form-group">
                <label for="gender" class="form-label">Gender</label>
                <select
                  id="gender"
                  v-model="customerData.gender"
                  class="form-select"
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                  <option value="prefer-not-to-say">Prefer not to say</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Company Information -->
          <div class="form-section">
            <h2 class="section-title">Company Information</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="companyName" class="form-label">Company Name</label>
                <input
                  type="text"
                  id="companyName"
                  v-model="customerData.companyName"
                  class="form-input"
                  placeholder="e.g., Smith & Co. Wines"
                />
              </div>

              <div class="form-group">
                <label for="jobTitle" class="form-label">Job Title</label>
                <input
                  type="text"
                  id="jobTitle"
                  v-model="customerData.jobTitle"
                  class="form-input"
                  placeholder="e.g., Wine Director"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="companySize" class="form-label">Company Size</label>
                <select
                  id="companySize"
                  v-model="customerData.companySize"
                  class="form-select"
                >
                  <option value="">Select company size</option>
                  <option value="1-10">1-10 employees</option>
                  <option value="11-50">11-50 employees</option>
                  <option value="51-200">51-200 employees</option>
                  <option value="201-500">201-500 employees</option>
                  <option value="500+">500+ employees</option>
                </select>
              </div>

              <div class="form-group">
                <label for="industry" class="form-label">Industry</label>
                <select
                  id="industry"
                  v-model="customerData.industry"
                  class="form-select"
                >
                  <option value="">Select industry</option>
                  <option value="wine-retail">Wine Retail</option>
                  <option value="restaurant">Restaurant</option>
                  <option value="hotel">Hotel</option>
                  <option value="wine-import">Wine Import/Export</option>
                  <option value="wine-distribution">Wine Distribution</option>
                  <option value="wine-production">Wine Production</option>
                  <option value="consulting">Wine Consulting</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="website" class="form-label">Company Website</label>
              <input
                type="url"
                id="website"
                v-model="customerData.website"
                class="form-input"
                placeholder="e.g., https://www.smithwines.com"
              />
            </div>
          </div>

          <!-- Address Information -->
          <div class="form-section">
            <h2 class="section-title">Address Information</h2>
            
            <div class="form-group">
              <label for="addressLine1" class="form-label">Address Line 1 *</label>
              <input
                type="text"
                id="addressLine1"
                v-model="customerData.addressLine1"
                class="form-input"
                :class="{ 'error': errors.addressLine1 }"
                required
                placeholder="e.g., 123 Wine Street"
              />
              <span v-if="errors.addressLine1" class="error-message">{{ errors.addressLine1 }}</span>
            </div>

            <div class="form-group">
              <label for="addressLine2" class="form-label">Address Line 2</label>
              <input
                type="text"
                id="addressLine2"
                v-model="customerData.addressLine2"
                class="form-input"
                placeholder="e.g., Suite 100"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="city" class="form-label">City *</label>
                <input
                  type="text"
                  id="city"
                  v-model="customerData.city"
                  class="form-input"
                  :class="{ 'error': errors.city }"
                  required
                  placeholder="e.g., Paris"
                />
                <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
              </div>

              <div class="form-group">
                <label for="state" class="form-label">State/Province</label>
                <input
                  type="text"
                  id="state"
                  v-model="customerData.state"
                  class="form-input"
                  placeholder="e.g., Île-de-France"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="postalCode" class="form-label">Postal Code *</label>
                <input
                  type="text"
                  id="postalCode"
                  v-model="customerData.postalCode"
                  class="form-input"
                  :class="{ 'error': errors.postalCode }"
                  required
                  placeholder="e.g., 75001"
                />
                <span v-if="errors.postalCode" class="error-message">{{ errors.postalCode }}</span>
              </div>

              <div class="form-group">
                <label for="country" class="form-label">Country *</label>
                <select
                  id="country"
                  v-model="customerData.country"
                  class="form-select"
                  :class="{ 'error': errors.country }"
                  required
                >
                  <option value="">Select country</option>
                  <option value="france">France</option>
                  <option value="germany">Germany</option>
                  <option value="italy">Italy</option>
                  <option value="spain">Spain</option>
                  <option value="united-kingdom">United Kingdom</option>
                  <option value="united-states">United States</option>
                  <option value="canada">Canada</option>
                  <option value="australia">Australia</option>
                  <option value="new-zealand">New Zealand</option>
                  <option value="chile">Chile</option>
                  <option value="argentina">Argentina</option>
                  <option value="south-africa">South Africa</option>
                  <option value="other">Other</option>
                </select>
                <span v-if="errors.country" class="error-message">{{ errors.country }}</span>
              </div>
            </div>
          </div>

          <!-- Account Settings -->
          <div class="form-section">
            <h2 class="section-title">Account Settings</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="customerType" class="form-label">Customer Type *</label>
                <select
                  id="customerType"
                  v-model="customerData.customerType"
                  class="form-select"
                  :class="{ 'error': errors.customerType }"
                  required
                >
                  <option value="">Select customer type</option>
                  <option value="b2b">Business to Business (B2B)</option>
                  <option value="b2c">Business to Consumer (B2C)</option>
                  <option value="wholesale">Wholesale</option>
                  <option value="retail">Retail</option>
                  <option value="distributor">Distributor</option>
                </select>
                <span v-if="errors.customerType" class="error-message">{{ errors.customerType }}</span>
              </div>

              <div class="form-group">
                <label for="status" class="form-label">Account Status *</label>
                <select
                  id="status"
                  v-model="customerData.status"
                  class="form-select"
                  :class="{ 'error': errors.status }"
                  required
                >
                  <option value="">Select status</option>
                  <option value="active">Active</option>
                  <option value="pending">Pending</option>
                  <option value="suspended">Suspended</option>
                  <option value="inactive">Inactive</option>
                </select>
                <span v-if="errors.status" class="error-message">{{ errors.status }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="creditLimit" class="form-label">Credit Limit (€)</label>
                <input
                  type="number"
                  id="creditLimit"
                  v-model="customerData.creditLimit"
                  class="form-input"
                  min="0"
                  step="0.01"
                  placeholder="10000.00"
                />
              </div>

              <div class="form-group">
                <label for="paymentTerms" class="form-label">Payment Terms</label>
                <select
                  id="paymentTerms"
                  v-model="customerData.paymentTerms"
                  class="form-select"
                >
                  <option value="">Select payment terms</option>
                  <option value="net-30">Net 30</option>
                  <option value="net-60">Net 60</option>
                  <option value="net-90">Net 90</option>
                  <option value="immediate">Immediate</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="notes" class="form-label">Internal Notes</label>
              <textarea
                id="notes"
                v-model="customerData.notes"
                class="form-textarea"
                rows="3"
                placeholder="Any internal notes about this customer..."
              ></textarea>
            </div>
          </div>

          <!-- Preferences -->
          <div class="form-section">
            <h2 class="section-title">Preferences</h2>
            
            <div class="form-group">
              <label for="winePreferences" class="form-label">Wine Preferences</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.winePreferences.red" class="checkbox" />
                  <span class="checkmark"></span>
                  Red Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.winePreferences.white" class="checkbox" />
                  <span class="checkmark"></span>
                  White Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.winePreferences.rose" class="checkbox" />
                  <span class="checkmark"></span>
                  Rosé Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.winePreferences.sparkling" class="checkbox" />
                  <span class="checkmark"></span>
                  Sparkling Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.winePreferences.fortified" class="checkbox" />
                  <span class="checkmark"></span>
                  Fortified Wines
                </label>
              </div>
            </div>

            <div class="form-group">
              <label for="priceRange" class="form-label">Preferred Price Range</label>
              <select
                id="priceRange"
                v-model="customerData.priceRange"
                class="form-select"
              >
                <option value="">Select price range</option>
                <option value="budget">Budget (€5-€20)</option>
                <option value="mid-range">Mid-Range (€20-€50)</option>
                <option value="premium">Premium (€50-€100)</option>
                <option value="luxury">Luxury (€100+)</option>
                <option value="any">Any Price Range</option>
              </select>
            </div>

            <div class="form-group">
              <label for="communicationPreferences" class="form-label">Communication Preferences</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.communicationPreferences.email" class="checkbox" />
                  <span class="checkmark"></span>
                  Email
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.communicationPreferences.phone" class="checkbox" />
                  <span class="checkmark"></span>
                  Phone
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.communicationPreferences.sms" class="checkbox" />
                  <span class="checkmark"></span>
                  SMS
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.communicationPreferences.postal" class="checkbox" />
                  <span class="checkmark"></span>
                  Postal Mail
                </label>
              </div>
            </div>

            <div class="form-group">
              <label for="newsletter" class="form-label">Newsletter Subscription</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="customerData.newsletter" class="checkbox" />
                  <span class="checkmark"></span>
                  Subscribe to newsletter and promotional offers
                </label>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <button type="button" class="btn btn--outline" @click="saveDraft">
              Save as Draft
            </button>
            <button type="submit" class="btn btn--primary" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="loading-spinner"></span>
              {{ isSubmitting ? 'Creating Customer...' : 'Create Customer' }}
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Add New Customer - Admin Dashboard',
  description: 'Create a new customer account for the business.'
})

// Customer data
const customerData = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  dateOfBirth: '',
  gender: '',
  companyName: '',
  jobTitle: '',
  companySize: '',
  industry: '',
  website: '',
  addressLine1: '',
  addressLine2: '',
  city: '',
  state: '',
  postalCode: '',
  country: '',
  customerType: '',
  status: '',
  creditLimit: '',
  paymentTerms: '',
  notes: '',
  winePreferences: {
    red: false,
    white: false,
    rose: false,
    sparkling: false,
    fortified: false
  },
  priceRange: '',
  communicationPreferences: {
    email: true,
    phone: false,
    sms: false,
    postal: false
  },
  newsletter: false
})

// Form state
const isSubmitting = ref(false)
const errors = ref({})

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!customerData.value.firstName.trim()) {
    errors.value.firstName = 'First name is required'
  }
  
  if (!customerData.value.lastName.trim()) {
    errors.value.lastName = 'Last name is required'
  }
  
  if (!customerData.value.email.trim()) {
    errors.value.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(customerData.value.email)) {
    errors.value.email = 'Valid email format is required'
  }
  
  if (!customerData.value.addressLine1.trim()) {
    errors.value.addressLine1 = 'Address is required'
  }
  
  if (!customerData.value.city.trim()) {
    errors.value.city = 'City is required'
  }
  
  if (!customerData.value.postalCode.trim()) {
    errors.value.postalCode = 'Postal code is required'
  }
  
  if (!customerData.value.country) {
    errors.value.country = 'Country is required'
  }
  
  if (!customerData.value.customerType) {
    errors.value.customerType = 'Customer type is required'
  }
  
  if (!customerData.value.status) {
    errors.value.status = 'Status is required'
  }
  
  return Object.keys(errors.value).length === 0
}

// Form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    // TODO: Implement actual API call to create customer
    console.log('Creating customer:', customerData.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Success - redirect to customers list
    navigateTo('/admin/customers')
    
  } catch (error) {
    console.error('Failed to create customer:', error)
    alert('Failed to create customer. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

// Save as draft
const saveDraft = async () => {
  customerData.value.status = 'pending'
  
  try {
    // TODO: Implement actual API call to save draft
    console.log('Saving draft:', customerData.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    alert('Draft saved successfully!')
    
  } catch (error) {
    console.error('Failed to save draft:', error)
    alert('Failed to save draft. Please try again.')
  }
}
</script>

<style scoped>
.add-customer {
  min-height: 100vh;
  background: #f8fafc;
  padding: 2rem;
}

/* Page Header */
.page-header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.back-link {
  color: #57534e;
  text-decoration: none;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  display: inline-block;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #dc2626;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', serif;
}

.page-subtitle {
  color: #57534e;
  font-size: 1.125rem;
  margin: 0;
}

/* Customer Form */
.customer-form {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.form-container {
  padding: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Form Sections */
.form-section {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 2rem;
}

.form-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1c1917;
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

/* Form Layout */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
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

.form-input,
.form-select,
.form-textarea {
  padding: 0.875rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #1c1917;
  font-family: inherit;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-input.error,
.form-select.error {
  border-color: #dc2626;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #a8a29e;
}

/* Error Messages */
.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Checkbox Groups */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
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

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #f1f5f9;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  min-width: 120px;
  justify-content: center;
}

.btn--outline {
  background: transparent;
  color: #dc2626;
  border: 2px solid #dc2626;
}

.btn--outline:hover {
  background: #dc2626;
  color: white;
}

.btn--primary {
  background: #dc2626;
  color: white;
}

.btn--primary:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
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

/* Responsive Design */
@media (max-width: 1024px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .add-customer {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .form-container {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
