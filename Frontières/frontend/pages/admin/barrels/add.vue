<template>
  <div class="add-barrel">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <NuxtLink to="/admin/barrels" class="back-link">
            ← Back to Barrels
          </NuxtLink>
          <h1 class="page-title">Add New Barrel</h1>
          <p class="page-subtitle">Create a new barrel entry for your inventory</p>
        </div>
      </div>
    </header>

    <!-- Barrel Form -->
    <section class="barrel-form">
      <div class="form-container">
        <form @submit.prevent="handleSubmit" class="form">
          <!-- Basic Information -->
          <div class="form-section">
            <h2 class="section-title">Basic Information</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="name" class="form-label">Barrel Name *</label>
                <input
                  type="text"
                  id="name"
                  v-model="barrelData.name"
                  class="form-input"
                  :class="{ 'error': errors.name }"
                  required
                  placeholder="e.g., Bordeaux Barrel"
                />
                <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
              </div>

              <div class="form-group">
                <label for="description" class="form-label">Description</label>
                <input
                  type="text"
                  id="description"
                  v-model="barrelData.description"
                  class="form-input"
                  placeholder="e.g., Traditional 225L French oak barrel"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="woodType" class="form-label">Wood Type *</label>
                <select
                  id="woodType"
                  v-model="barrelData.woodType"
                  class="form-select"
                  :class="{ 'error': errors.woodType }"
                  required
                >
                  <option value="">Select wood type</option>
                  <option value="french-oak">French Oak</option>
                  <option value="american-oak">American Oak</option>
                  <option value="hungarian-oak">Hungarian Oak</option>
                  <option value="slavonian-oak">Slavonian Oak</option>
                  <option value="chestnut">Chestnut</option>
                  <option value="other">Other</option>
                </select>
                <span v-if="errors.woodType" class="error-message">{{ errors.woodType }}</span>
              </div>

              <div class="form-group">
                <label for="size" class="form-label">Size *</label>
                <select
                  id="size"
                  v-model="barrelData.size"
                  class="form-select"
                  :class="{ 'error': errors.size }"
                  required
                >
                  <option value="">Select size</option>
                  <option value="225L">225L (Bordeaux)</option>
                  <option value="228L">228L (Burgundy)</option>
                  <option value="300L">300L (Hogshead)</option>
                  <option value="500L">500L (Puncheon)</option>
                  <option value="1000L">1000L (Tun)</option>
                  <option value="custom">Custom Size</option>
                </select>
                <span v-if="errors.size" class="error-message">{{ errors.size }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="origin" class="form-label">Origin *</label>
                <select
                  id="origin"
                  v-model="barrelData.origin"
                  class="form-select"
                  :class="{ 'error': errors.origin }"
                  required
                >
                  <option value="">Select origin</option>
                  <option value="France">France</option>
                  <option value="USA">United States</option>
                  <option value="Hungary">Hungary</option>
                  <option value="Croatia">Croatia</option>
                  <option value="Italy">Italy</option>
                  <option value="Spain">Spain</option>
                  <option value="Other">Other</option>
                </select>
                <span v-if="errors.origin" class="error-message">{{ errors.origin }}</span>
              </div>

              <div class="form-group">
                <label for="age" class="form-label">Age (Years) *</label>
                <input
                  type="number"
                  id="age"
                  v-model="barrelData.age"
                  class="form-input"
                  :class="{ 'error': errors.age }"
                  required
                  min="0"
                  max="50"
                  placeholder="2"
                />
                <span v-if="errors.age" class="error-message">{{ errors.age }}</span>
              </div>
            </div>
          </div>

          <!-- Pricing and Inventory -->
          <div class="form-section">
            <h2 class="section-title">Pricing & Inventory</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="price" class="form-label">Price (€) *</label>
                <input
                  type="number"
                  id="price"
                  v-model="barrelData.price"
                  class="form-input"
                  :class="{ 'error': errors.price }"
                  required
                  min="0"
                  step="0.01"
                  placeholder="850.00"
                />
                <span v-if="errors.price" class="error-message">{{ errors.price }}</span>
              </div>

              <div class="form-group">
                <label for="stock" class="form-label">Stock Quantity *</label>
                <input
                  type="number"
                  id="stock"
                  v-model="barrelData.stock"
                  class="form-input"
                  :class="{ 'error': errors.stock }"
                  required
                  min="0"
                  placeholder="45"
                />
                <span v-if="errors.stock" class="error-message">{{ errors.stock }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="minOrder" class="form-label">Minimum Order Quantity</label>
                <input
                  type="number"
                  id="minOrder"
                  v-model="barrelData.minOrder"
                  class="form-input"
                  min="1"
                  placeholder="1"
                />
              </div>

              <div class="form-group">
                <label for="maxOrder" class="form-label">Maximum Order Quantity</label>
                <input
                  type="number"
                  id="maxOrder"
                  v-model="barrelData.maxOrder"
                  class="form-input"
                  min="1"
                  placeholder="100"
                />
              </div>
            </div>
          </div>

          <!-- Technical Specifications -->
          <div class="form-section">
            <h2 class="section-title">Technical Specifications</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="toasting" class="form-label">Toasting Level</label>
                <select
                  id="toasting"
                  v-model="barrelData.toasting"
                  class="form-select"
                >
                  <option value="">Select toasting level</option>
                  <option value="light">Light</option>
                  <option value="medium">Medium</option>
                  <option value="medium-plus">Medium Plus</option>
                  <option value="heavy">Heavy</option>
                  <option value="custom">Custom</option>
                </select>
              </div>

              <div class="form-group">
                <label for="grain" class="form-label">Grain Type</label>
                <select
                  id="grain"
                  v-model="barrelData.grain"
                  class="form-select"
                >
                  <option value="">Select grain type</option>
                  <option value="tight">Tight Grain</option>
                  <option value="medium">Medium Grain</option>
                  <option value="coarse">Coarse Grain</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="cooperage" class="form-label">Cooperage</label>
                <input
                  type="text"
                  id="cooperage"
                  v-model="barrelData.cooperage"
                  class="form-input"
                  placeholder="e.g., Tonnellerie François Frères"
                />
              </div>

              <div class="form-group">
                <label for="harvestYear" class="form-label">Wood Harvest Year</label>
                <input
                  type="number"
                  id="harvestYear"
                  v-model="barrelData.harvestYear"
                  class="form-input"
                  min="1990"
                  max="2024"
                  placeholder="2020"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="technicalNotes" class="form-label">Technical Notes</label>
              <textarea
                id="technicalNotes"
                v-model="barrelData.technicalNotes"
                class="form-textarea"
                rows="3"
                placeholder="Additional technical specifications, special features, or notes..."
              ></textarea>
            </div>
          </div>

          <!-- Usage and Applications -->
          <div class="form-section">
            <h2 class="section-title">Usage & Applications</h2>
            
            <div class="form-group">
              <label for="wineTypes" class="form-label">Recommended Wine Types</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="barrelData.wineTypes.red" class="checkbox" />
                  <span class="checkmark"></span>
                  Red Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="barrelData.wineTypes.white" class="checkbox" />
                  <span class="checkmark"></span>
                  White Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="barrelData.wineTypes.rose" class="checkbox" />
                  <span class="checkmark"></span>
                  Rosé Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="barrelData.wineTypes.sparkling" class="checkbox" />
                  <span class="checkmark"></span>
                  Sparkling Wines
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="barrelData.wineTypes.fortified" class="checkbox" />
                  <span class="checkmark"></span>
                  Fortified Wines
                </label>
              </div>
            </div>

            <div class="form-group">
              <label for="agingTime" class="form-label">Recommended Aging Time</label>
              <select
                id="agingTime"
                v-model="barrelData.agingTime"
                class="form-select"
              >
                <option value="">Select aging time</option>
                <option value="6-12-months">6-12 months</option>
                <option value="12-18-months">12-18 months</option>
                <option value="18-24-months">18-24 months</option>
                <option value="24-36-months">24-36 months</option>
                <option value="36+months">36+ months</option>
                <option value="custom">Custom</option>
              </select>
            </div>

            <div class="form-group">
              <label for="applications" class="form-label">Applications</label>
              <textarea
                id="applications"
                v-model="barrelData.applications"
                class="form-textarea"
                rows="3"
                placeholder="Describe specific applications, wine varieties, or regions where this barrel type is commonly used..."
              ></textarea>
            </div>
          </div>

          <!-- Status and Publishing -->
          <div class="form-section">
            <h2 class="section-title">Status & Publishing</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="status" class="form-label">Status *</label>
                <select
                  id="status"
                  v-model="barrelData.status"
                  class="form-select"
                  :class="{ 'error': errors.status }"
                  required
                >
                  <option value="">Select status</option>
                  <option value="available">Available</option>
                  <option value="reserved">Reserved</option>
                  <option value="sold">Sold</option>
                  <option value="aging">Aging</option>
                  <option value="draft">Draft</option>
                </select>
                <span v-if="errors.status" class="error-message">{{ errors.status }}</span>
              </div>

              <div class="form-group">
                <label for="featured" class="form-label">Featured Barrel</label>
                <div class="checkbox-group">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="barrelData.featured" class="checkbox" />
                    <span class="checkmark"></span>
                    Mark as featured barrel
                  </label>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="tags" class="form-label">Tags</label>
              <input
                type="text"
                id="tags"
                v-model="barrelData.tags"
                class="form-input"
                placeholder="e.g., premium, limited edition, organic, sustainable (separate with commas)"
              />
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <button type="button" class="btn btn--outline" @click="saveDraft">
              Save as Draft
            </button>
            <button type="submit" class="btn btn--primary" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="loading-spinner"></span>
              {{ isSubmitting ? 'Creating Barrel...' : 'Create Barrel' }}
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Add New Barrel - Admin Dashboard',
  description: 'Create a new barrel entry for the inventory.'
})

// Barrel data
const barrelData = ref({
  name: '',
  description: '',
  woodType: '',
  size: '',
  origin: '',
  age: '',
  price: '',
  stock: '',
  minOrder: 1,
  maxOrder: 100,
  toasting: '',
  grain: '',
  cooperage: '',
  harvestYear: '',
  technicalNotes: '',
  wineTypes: {
    red: false,
    white: false,
    rose: false,
    sparkling: false,
    fortified: false
  },
  agingTime: '',
  applications: '',
  status: '',
  featured: false,
  tags: ''
})

// Form state
const isSubmitting = ref(false)
const errors = ref({})

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!barrelData.value.name.trim()) {
    errors.value.name = 'Barrel name is required'
  }
  
  if (!barrelData.value.woodType) {
    errors.value.woodType = 'Wood type is required'
  }
  
  if (!barrelData.value.size) {
    errors.value.size = 'Size is required'
  }
  
  if (!barrelData.value.origin) {
    errors.value.origin = 'Origin is required'
  }
  
  if (!barrelData.value.age || barrelData.value.age < 0) {
    errors.value.age = 'Valid age is required'
  }
  
  if (!barrelData.value.price || barrelData.value.price <= 0) {
    errors.value.price = 'Valid price is required'
  }
  
  if (!barrelData.value.stock || barrelData.value.stock < 0) {
    errors.value.stock = 'Valid stock quantity is required'
  }
  
  if (!barrelData.value.status) {
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
    // TODO: Implement actual API call to create barrel
    console.log('Creating barrel:', barrelData.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Success - redirect to barrels list
    navigateTo('/admin/barrels')
    
  } catch (error) {
    console.error('Failed to create barrel:', error)
    alert('Failed to create barrel. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

// Save as draft
const saveDraft = async () => {
  barrelData.value.status = 'draft'
  
  try {
    // TODO: Implement actual API call to save draft
    console.log('Saving draft:', barrelData.value)
    
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
.add-barrel {
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

/* Barrel Form */
.barrel-form {
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
  .add-barrel {
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
