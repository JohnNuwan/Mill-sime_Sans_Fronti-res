<template>
  <div class="wines-management">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Wines Management</h1>
          <p class="page-subtitle">Manage your wine catalog and inventory</p>
        </div>
        <div class="header-actions">
          <button class="btn btn--outline" @click="refreshWines">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <NuxtLink to="/admin/wines/add" class="btn btn--primary">
            <span class="icon">➕</span>
            Add New Wine
          </NuxtLink>
        </div>
      </div>
    </header>

    <!-- Search and Filters -->
    <section class="search-filters">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search wines by name, region, or vintage..."
          class="search-input"
        />
        <button class="search-button">
          <span class="icon">🔍</span>
        </button>
      </div>
      
      <div class="filters">
        <select v-model="regionFilter" class="filter-select">
          <option value="">All Regions</option>
          <option value="bordeaux">Bordeaux</option>
          <option value="burgundy">Burgundy</option>
          <option value="champagne">Champagne</option>
          <option value="rhone">Rhône Valley</option>
          <option value="loire">Loire Valley</option>
        </select>
        
        <select v-model="typeFilter" class="filter-select">
          <option value="">All Types</option>
          <option value="red">Red Wine</option>
          <option value="white">White Wine</option>
          <option value="rose">Rosé Wine</option>
          <option value="sparkling">Sparkling Wine</option>
          <option value="dessert">Dessert Wine</option>
        </select>
        
        <select v-model="vintageFilter" class="filter-select">
          <option value="">All Vintages</option>
          <option value="2023">2023</option>
          <option value="2022">2022</option>
          <option value="2021">2021</option>
          <option value="2020">2020</option>
          <option value="2019">2019</option>
          <option value="2018">2018</option>
        </select>
      </div>
    </section>

    <!-- Wines Table -->
    <section class="wines-table">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Region</th>
              <th>Type</th>
              <th>Vintage</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="wine in filteredWines" :key="wine.id" class="table-row">
              <td>
                <div class="wine-image">
                  <div class="image-placeholder">{{ wine.emoji }}</div>
                </div>
              </td>
              <td>
                <div class="wine-info">
                  <h4 class="wine-name">{{ wine.name }}</h4>
                  <p class="wine-producer">{{ wine.producer }}</p>
                </div>
              </td>
              <td>
                <span class="region-badge">{{ wine.region }}</span>
              </td>
              <td>
                <span class="type-badge type-{{ wine.type }}">{{ wine.type }}</span>
              </td>
              <td>
                <span class="vintage">{{ wine.vintage }}</span>
              </td>
              <td>
                <span class="price">€{{ wine.price }}</span>
              </td>
              <td>
                <span class="stock" :class="{ 'low-stock': wine.stock < 10 }">
                  {{ wine.stock }} bottles
                </span>
              </td>
              <td>
                <span class="status-badge status-{{ wine.status }}">
                  {{ wine.status }}
                </span>
              </td>
              <td>
                <div class="actions">
                  <button class="action-btn edit" @click="editWine(wine)" title="Edit">
                    ✏️
                  </button>
                  <button class="action-btn view" @click="viewWine(wine)" title="View">
                    👁️
                  </button>
                  <button class="action-btn delete" @click="deleteWine(wine)" title="Delete">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Pagination -->
    <section class="pagination">
      <div class="pagination-info">
        Showing {{ paginationStart }} to {{ paginationEnd }} of {{ totalWines }} wines
      </div>
      <div class="pagination-controls">
        <button 
          class="pagination-btn" 
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          ← Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          class="pagination-btn" 
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next →
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Wines Management - Admin Dashboard',
  description: 'Manage wine catalog, inventory, and pricing.'
})

// Mock data - replace with actual API calls
const wines = ref([
  {
    id: 1,
    name: 'Château Margaux',
    producer: 'Château Margaux',
    region: 'Bordeaux',
    type: 'red',
    vintage: '2018',
    price: 850,
    stock: 45,
    status: 'active',
    emoji: '🍷'
  },
  {
    id: 2,
    name: 'Dom Pérignon',
    producer: 'Moët & Chandon',
    region: 'Champagne',
    type: 'sparkling',
    vintage: '2012',
    price: 280,
    stock: 23,
    status: 'active',
    emoji: '🍾'
  },
  {
    id: 3,
    name: 'Romanée-Conti',
    producer: 'Domaine de la Romanée-Conti',
    region: 'Burgundy',
    type: 'red',
    vintage: '2019',
    price: 15000,
    stock: 3,
    status: 'active',
    emoji: '🍷'
  },
  {
    id: 4,
    name: 'Sauternes',
    producer: 'Château d\'Yquem',
    region: 'Bordeaux',
    type: 'dessert',
    vintage: '2015',
    price: 450,
    stock: 12,
    status: 'active',
    emoji: '🍯'
  },
  {
    id: 5,
    name: 'Chablis Grand Cru',
    producer: 'Domaine Raveneau',
    region: 'Burgundy',
    type: 'white',
    vintage: '2020',
    price: 180,
    stock: 8,
    status: 'active',
    emoji: '🥂'
  }
])

// Search and filters
const searchQuery = ref('')
const regionFilter = ref('')
const typeFilter = ref('')
const vintageFilter = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredWines = computed(() => {
  let filtered = wines.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(wine => 
      wine.name.toLowerCase().includes(query) ||
      wine.producer.toLowerCase().includes(query) ||
      wine.region.toLowerCase().includes(query) ||
      wine.vintage.includes(query)
    )
  }

  if (regionFilter.value) {
    filtered = filtered.filter(wine => wine.region.toLowerCase() === regionFilter.value)
  }

  if (typeFilter.value) {
    filtered = filtered.filter(wine => wine.type === typeFilter.value)
  }

  if (vintageFilter.value) {
    filtered = filtered.filter(wine => wine.vintage === vintageFilter.value)
  }

  return filtered
})

const totalWines = computed(() => filteredWines.value.length)
const totalPages = computed(() => Math.ceil(totalWines.value / itemsPerPage))
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, totalWines.value))

// Methods
const refreshWines = () => {
  // TODO: Implement actual API call to refresh wines
  console.log('Refreshing wines...')
}

const editWine = (wine) => {
  // TODO: Navigate to edit page or open edit modal
  console.log('Editing wine:', wine)
  navigateTo(`/admin/wines/${wine.id}/edit`)
}

const viewWine = (wine) => {
  // TODO: Navigate to view page or open view modal
  console.log('Viewing wine:', wine)
  navigateTo(`/admin/wines/${wine.id}`)
}

const deleteWine = (wine) => {
  if (confirm(`Are you sure you want to delete "${wine.name}"?`)) {
    // TODO: Implement actual delete API call
    console.log('Deleting wine:', wine)
    wines.value = wines.value.filter(w => w.id !== wine.id)
  }
}

const changePage = (page) => {
  currentPage.value = page
}
</script>

<style scoped>
.wines-management {
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
  gap: 2rem;
}

.header-left {
  flex: 1;
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

.header-actions {
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
}

/* Search and Filters */
.search-filters {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.search-bar {
  display: flex;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 0.875rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px 0 0 8px;
  font-size: 1rem;
  border-right: none;
}

.search-input:focus {
  outline: none;
  border-color: #dc2626;
}

.search-button {
  padding: 0.875rem 1.5rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-button:hover {
  background: #b91c1c;
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px;
  background: white;
  color: #1c1917;
  font-size: 0.875rem;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #dc2626;
}

/* Wines Table */
.wines-table {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #1c1917;
  border-bottom: 1px solid #e7e5e4;
}

.table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.table-row:hover {
  background: #f8fafc;
}

/* Wine Image */
.wine-image {
  width: 50px;
  height: 50px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: #fef3c7;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

/* Wine Info */
.wine-info {
  min-width: 200px;
}

.wine-name {
  font-weight: 600;
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.wine-producer {
  color: #57534e;
  margin: 0;
  font-size: 0.875rem;
}

/* Badges */
.region-badge {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.type-red {
  background: #fef2f2;
  color: #dc2626;
}

.type-white {
  background: #f0fdf4;
  color: #16a34a;
}

.type-rose {
  background: #fdf2f8;
  color: #ec4899;
}

.type-sparkling {
  background: #f0f9ff;
  color: #0284c7;
}

.type-dessert {
  background: #fefce8;
  color: #ca8a04;
}

.vintage {
  font-weight: 600;
  color: #1c1917;
}

.price {
  font-weight: 600;
  color: #16a34a;
}

.stock {
  font-weight: 500;
  color: #1c1917;
}

.low-stock {
  color: #dc2626;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-active {
  background: #f0fdf4;
  color: #16a34a;
}

.status-inactive {
  background: #fef2f2;
  color: #dc2626;
}

.status-draft {
  background: #f3f4f6;
  color: #6b7280;
}

/* Actions */
.actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.action-btn.edit {
  background: #fef3c7;
  color: #d97706;
}

.action-btn.edit:hover {
  background: #f59e0b;
  color: white;
}

.action-btn.view {
  background: #dbeafe;
  color: #2563eb;
}

.action-btn.view:hover {
  background: #3b82f6;
  color: white;
}

.action-btn.delete {
  background: #fee2e2;
  color: #dc2626;
}

.action-btn.delete:hover {
  background: #ef4444;
  color: white;
}

/* Pagination */
.pagination {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-info {
  color: #57534e;
  font-size: 0.875rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e7e5e4;
  background: white;
  color: #1c1917;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.pagination-btn:hover:not(:disabled) {
  border-color: #dc2626;
  color: #dc2626;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #57534e;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
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

.btn--primary:hover {
  background: #b91c1c;
  transform: translateY(-2px);
}

.icon {
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: flex-start;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-select {
    min-width: auto;
  }
}

@media (max-width: 768px) {
  .wines-management {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .table th,
  .table td {
    padding: 0.75rem 0.5rem;
  }
  
  .wine-info {
    min-width: 150px;
  }
  
  .pagination {
    flex-direction: column;
    text-align: center;
  }
}
</style>
