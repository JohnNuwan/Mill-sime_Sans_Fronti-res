<template>
  <div class="add-wine">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <NuxtLink to="/admin/wines" class="back-link">
            ← Back to Wines
          </NuxtLink>
          <h1 class="page-title">Add New Wine</h1>
          <p class="page-subtitle">Create a new wine entry for your catalog</p>
        </div>
      </div>
    </header>

    <!-- Wine Form -->
    <section class="wine-form">
      <div class="form-container">
        <form @submit.prevent="handleSubmit" class="form">
          <!-- Basic Information -->
          <div class="form-section">
            <h2 class="section-title">Basic Information</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="name" class="form-label">Wine Name *</label>
                <input
                  type="text"
                  id="name"
                  v-model="wineData.name"
                  class="form-input"
                  :class="{ 'error': errors.name }"
                  required
                  placeholder="e.g., Château Margaux 2018"
                />
                <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
              </div>

              <div class="form-group">
                <label for="producer" class="form-label">Producer/Winery *</label>
                <input
                  type="text"
                  id="producer"
                  v-model="wineData.producer"
                  class="form-input"
                  :class="{ 'error': errors.producer }"
                  required
                  placeholder="e.g., Château Margaux"
                />
                <span v-if="errors.producer" class="error-message">{{ errors.producer }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="region" class="form-label">Region *</label>
                <select
                  id="region"
                  v-model="wineData.region"
                  class="form-select"
                  :class="{ 'error': errors.region }"
                  required
                >
                  <option value="">Select region</option>
                  <option value="bordeaux">Bordeaux, France</option>
                  <option value="burgundy">Burgundy, France</option>
                  <option value="champagne">Champagne, France</option>
                  <option value="rhone">Rhône Valley, France</option>
                  <option value="loire">Loire Valley, France</option>
                  <option value="alsace">Alsace, France</option>
                  <option value="tuscany">Tuscany, Italy</option>
                  <option value="piedmont">Piedmont, Italy</option>
                  <option value="veneto">Veneto, Italy</option>
                  <option value="rioja">Rioja, Spain</option>
                  <option value="riorja">Ribera del Duero, Spain</option>
                  <option value="napa">Napa Valley, USA</option>
                  <option value="sonoma">Sonoma County, USA</option>
                  <option value="other">Other</option>
                </select>
                <span v-if="errors.region" class="error-message">{{ errors.region }}</span>
              </div>

              <div class="form-group">
                <label for="country" class="form-label">Country *</label>
                <select
                  id="country"
                  v-model="wineData.country"
                  class="form-select"
                  :class="{ 'error': errors.country }"
                  required
                >
                  <option value="">Select country</option>
                  <option value="france">France</option>
                  <option value="italy">Italy</option>
                  <option value="spain">Spain</option>
                  <option value="usa">United States</option>
                  <option value="germany">Germany</option>
                  <option value="australia">Australia</option>
                  <option value="chile">Chile</option>
                  <option value="argentina">Argentina</option>
                  <option value="new-zealand">New Zealand</option>
                  <option value="other">Other</option>
                </select>
                <span v-if="errors.country" class="error-message">{{ errors.country }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="vintage" class="form-label">Vintage *</label>
                <input
                  type="number"
                  id="vintage"
                  v-model="wineData.vintage"
                  class="form-input"
                  :class="{ 'error': errors.vintage }"
                  required
                  min="1900"
                  max="2024"
                  placeholder="2018"
                />
                <span v-if="errors.vintage" class="error-message">{{ errors.vintage }}</span>
              </div>

              <div class="form-group">
                <label for="wineType" class="form-label">Wine Type *</label>
                <select
                  id="wineType"
                  v-model="wineData.wineType"
                  class="form-select"
                  :class="{ 'error': errors.wineType }"
                  required
                >
                  <option value="">Select wine type</option>
                  <option value="red">Red Wine</option>
                  <option value="white">White Wine</option>
                  <option value="rose">Rosé Wine</option>
                  <option value="sparkling">Sparkling Wine</option>
                  <option value="dessert">Dessert Wine</option>
                  <option value="fortified">Fortified Wine</option>
                </select>
                <span v-if="errors.wineType" class="error-message">{{ errors.wineType }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="description" class="form-label">Description</label>
              <textarea
                id="description"
                v-model="wineData.description"
                class="form-textarea"
                rows="3"
                placeholder="Describe the wine's characteristics, tasting notes, and style..."
              ></textarea>
            </div>
          </div>

          <!-- Grape Varieties -->
          <div class="form-section">
            <h2 class="section-title">Grape Varieties</h2>
            
            <div class="form-group">
              <label for="primaryGrapes" class="form-label">Primary Grape Varieties *</label>
              <input
                type="text"
                id="primaryGrapes"
                v-model="wineData.primaryGrapes"
                class="form-input"
                :class="{ 'error': errors.primaryGrapes }"
                required
                placeholder="e.g., Cabernet Sauvignon, Merlot"
              />
              <span v-if="errors.primaryGrapes" class="error-message">{{ errors.primaryGrapes }}</span>
            </div>

            <div class="form-group">
              <label for="blendPercentage" class="form-label">Blend Percentages</label>
              <input
                type="text"
                id="blendPercentage"
                v-model="wineData.blendPercentage"
                class="form-input"
                placeholder="e.g., 60% Cabernet Sauvignon, 30% Merlot, 10% Cabernet Franc"
              />
            </div>

            <div class="form-group">
              <label for="otherGrapes" class="form-label">Other Grape Varieties</label>
              <input
                type="text"
                id="otherGrapes"
                v-model="wineData.otherGrapes"
                class="form-input"
                placeholder="e.g., Petit Verdot, Malbec"
              />
            </div>
          </div>

          <!-- Pricing & Inventory -->
          <div class="form-section">
            <h2 class="section-title">Pricing & Inventory</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="price" class="form-label">Price (€) *</label>
                <input
                  type="number"
                  id="price"
                  v-model="wineData.price"
                  class="form-input"
                  :class="{ 'error': errors.price }"
                  required
                  min="0"
                  step="0.01"
                  placeholder="45.00"
                />
                <span v-if="errors.price" class="error-message">{{ errors.price }}</span>
              </div>

              <div class="form-group">
                <label for="stock" class="form-label">Stock Quantity *</label>
                <input
                  type="number"
                  id="stock"
                  v-model="wineData.stock"
                  class="form-input"
                  :class="{ 'error': errors.stock }"
                  required
                  min="0"
                  placeholder="150"
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
                  v-model="wineData.minOrder"
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
                  v-model="wineData.maxOrder"
                  class="form-input"
                  min="1"
                  placeholder="100"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="bottleSize" class="form-label">Bottle Size</label>
                <select
                  id="bottleSize"
                  v-model="wineData.bottleSize"
                  class="form-select"
                >
                  <option value="">Select bottle size</option>
                  <option value="187ml">187ml (Quarter)</option>
                  <option value="375ml">375ml (Half)</option>
                  <option value="750ml">750ml (Standard)</option>
                  <option value="1.5L">1.5L (Magnum)</option>
                  <option value="3L">3L (Double Magnum)</option>
                  <option value="6L">6L (Imperial)</option>
                  <option value="9L">9L (Salmanazar)</option>
                  <option value="12L">12L (Balthazar)</option>
                  <option value="15L">15L (Nebuchadnezzar)</option>
                </select>
              </div>

              <div class="form-group">
                <label for="caseSize" class="form-label">Case Size</label>
                <input
                  type="number"
                  id="caseSize"
                  v-model="wineData.caseSize"
                  class="form-input"
                  min="1"
                  placeholder="12"
                />
              </div>
            </div>
          </div>

          <!-- Wine Details -->
          <div class="form-section">
            <h2 class="section-title">Wine Details</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="alcoholContent" class="form-label">Alcohol Content (%)</label>
                <input
                  type="number"
                  id="alcoholContent"
                  v-model="wineData.alcoholContent"
                  class="form-input"
                  min="0"
                  max="25"
                  step="0.1"
                  placeholder="13.5"
                />
              </div>

              <div class="form-group">
                <label for="acidity" class="form-label">Acidity Level</label>
                <select
                  id="acidity"
                  v-model="wineData.acidity"
                  class="form-select"
                >
                  <option value="">Select acidity level</option>
                  <option value="low">Low</option>
                  <option value="medium-low">Medium-Low</option>
                  <option value="medium">Medium</option>
                  <option value="medium-high">Medium-High</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="body" class="form-label">Body</label>
                <select
                  id="body"
                  v-model="wineData.body"
                  class="form-select"
                >
                  <option value="">Select body</option>
                  <option value="light">Light</option>
                  <option value="medium-light">Medium-Light</option>
                  <option value="medium">Medium</option>
                  <option value="medium-full">Medium-Full</option>
                  <option value="full">Full</option>
                </select>
              </div>

              <div class="form-group">
                <label for="tannins" class="form-label">Tannins</label>
                <select
                  id="tannins"
                  v-model="wineData.tannins"
                  class="form-select"
                >
                  <option value="">Select tannin level</option>
                  <option value="low">Low</option>
                  <option value="medium-low">Medium-Low</option>
                  <option value="medium">Medium</option>
                  <option value="medium-high">Medium-High</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="tastingNotes" class="form-label">Tasting Notes</label>
              <textarea
                id="tastingNotes"
                v-model="wineData.tastingNotes"
                class="form-textarea"
                rows="4"
                placeholder="Describe the wine's aromas, flavors, and finish..."
              ></textarea>
            </div>
          </div>

          <!-- Aging & Storage -->
          <div class="form-section">
            <h2 class="section-title">Aging & Storage</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="agingPotential" class="form-label">Aging Potential</label>
                <select
                  id="agingPotential"
                  v-model="wineData.agingPotential"
                  class="form-select"
                >
                  <option value="">Select aging potential</option>
                  <option value="1-3-years">1-3 years</option>
                  <option value="3-5-years">3-5 years</option>
                  <option value="5-10-years">5-10 years</option>
                  <option value="10-20-years">10-20 years</option>
                  <option value="20+years">20+ years</option>
                </select>
              </div>

              <div class="form-group">
                <label for="optimalDrinking" class="form-label">Optimal Drinking Window</label>
                <input
                  type="text"
                  id="optimalDrinking"
                  v-model="wineData.optimalDrinking"
                  class="form-input"
                  placeholder="e.g., 2025-2035"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="storageConditions" class="form-label">Storage Conditions</label>
              <textarea
                id="storageConditions"
                v-model="wineData.storageConditions"
                class="form-textarea"
                rows="3"
                placeholder="Describe optimal storage conditions (temperature, humidity, position)..."
              ></textarea>
            </div>
          </div>

          <!-- Awards & Ratings -->
          <div class="form-section">
            <h2 class="section-title">Awards & Ratings</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="rating" class="form-label">Rating (out of 100)</label>
                <input
                  type="number"
                  id="rating"
                  v-model="wineData.rating"
                  class="form-input"
                  min="0"
                  max="100"
                  placeholder="95"
                />
              </div>

              <div class="form-group">
                <label for="ratingSource" class="form-label">Rating Source</label>
                <input
                  type="text"
                  id="ratingSource"
                  v-model="wineData.ratingSource"
                  class="form-input"
                  placeholder="e.g., Wine Spectator, Robert Parker"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="awards" class="form-label">Awards & Recognition</label>
              <textarea
                id="awards"
                v-model="wineData.awards"
                class="form-textarea"
                rows="3"
                placeholder="List any awards, medals, or special recognition..."
              ></textarea>
            </div>
          </div>

          <!-- Status & Publishing -->
          <div class="form-section">
            <h2 class="section-title">Status & Publishing</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="status" class="form-label">Status *</label>
                <select
                  id="status"
                  v-model="wineData.status"
                  class="form-select"
                  :class="{ 'error': errors.status }"
                  required
                >
                  <option value="">Select status</option>
                  <option value="available">Available</option>
                  <option value="reserved">Reserved</option>
                  <option value="sold-out">Sold Out</option>
                  <option value="aging">Aging</option>
                  <option value="draft">Draft</option>
                </select>
                <span v-if="errors.status" class="error-message">{{ errors.status }}</span>
              </div>

              <div class="form-group">
                <label for="featured" class="form-label">Featured Wine</label>
                <div class="checkbox-group">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="wineData.featured" class="checkbox" />
                    <span class="checkmark"></span>
                    Mark as featured wine
                  </label>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="tags" class="form-label">Tags</label>
              <input
                type="text"
                id="tags"
                v-model="wineData.tags"
                class="form-input"
                placeholder="e.g., premium, organic, biodynamic, limited edition (separate with commas)"
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
              {{ isSubmitting ? 'Creating Wine...' : 'Create Wine' }}
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Add New Wine - Admin Dashboard',
  description: 'Create a new wine entry for the catalog.'
})

// Wine data
const wineData = ref({
  name: '',
  producer: '',
  region: '',
  country: '',
  vintage: '',
  wineType: '',
  description: '',
  primaryGrapes: '',
  blendPercentage: '',
  otherGrapes: '',
  price: '',
  stock: '',
  minOrder: 1,
  maxOrder: 100,
  bottleSize: '',
  caseSize: 12,
  alcoholContent: '',
  acidity: '',
  body: '',
  tannins: '',
  tastingNotes: '',
  agingPotential: '',
  optimalDrinking: '',
  storageConditions: '',
  rating: '',
  ratingSource: '',
  awards: '',
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
  
  if (!wineData.value.name.trim()) {
    errors.value.name = 'Wine name is required'
  }
  
  if (!wineData.value.producer.trim()) {
    errors.value.producer = 'Producer is required'
  }
  
  if (!wineData.value.region) {
    errors.value.region = 'Region is required'
  }
  
  if (!wineData.value.country) {
    errors.value.country = 'Country is required'
  }
  
  if (!wineData.value.vintage || wineData.value.vintage < 1900 || wineData.value.vintage > 2024) {
    errors.value.vintage = 'Valid vintage is required'
  }
  
  if (!wineData.value.wineType) {
    errors.value.wineType = 'Wine type is required'
  }
  
  if (!wineData.value.primaryGrapes.trim()) {
    errors.value.primaryGrapes = 'Primary grape varieties are required'
  }
  
  if (!wineData.value.price || wineData.value.price <= 0) {
    errors.value.price = 'Valid price is required'
  }
  
  if (!wineData.value.stock || wineData.value.stock < 0) {
    errors.value.stock = 'Valid stock quantity is required'
  }
  
  if (!wineData.value.status) {
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
    // TODO: Implement actual API call to create wine
    console.log('Creating wine:', wineData.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Success - redirect to wines list
    navigateTo('/admin/wines')
    
  } catch (error) {
    console.error('Failed to create wine:', error)
    alert('Failed to create wine. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

// Save as draft
const saveDraft = async () => {
  wineData.value.status = 'draft'
  
  try {
    // TODO: Implement actual API call to save draft
    console.log('Saving draft:', wineData.value)
    
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
.add-wine {
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

/* Wine Form */
.wine-form {
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
  .add-wine {
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
