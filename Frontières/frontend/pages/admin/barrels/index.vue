<template>
  <div class="barrels-management">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Barrels Management</h1>
          <p class="page-subtitle">Manage your barrel inventory and specifications</p>
        </div>
        <div class="header-actions">
          <button class="btn btn--outline" @click="refreshBarrels">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <NuxtLink to="/admin/barrels/add" class="btn btn--primary">
            <span class="icon">➕</span>
            Add New Barrel
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
          placeholder="Search barrels by type, wood, size, or origin..."
          class="search-input"
        />
        <button class="search-button">
          <span class="icon">🔍</span>
        </button>
      </div>
      
      <div class="filters">
        <select v-model="woodTypeFilter" class="filter-select">
          <option value="">All Wood Types</option>
          <option value="french-oak">French Oak</option>
          <option value="american-oak">American Oak</option>
          <option value="hungarian-oak">Hungarian Oak</option>
          <option value="slavonian-oak">Slavonian Oak</option>
          <option value="chestnut">Chestnut</option>
        </select>
        
        <select v-model="sizeFilter" class="filter-select">
          <option value="">All Sizes</option>
          <option value="225L">225L (Bordeaux)</option>
          <option value="228L">228L (Burgundy)</option>
          <option value="300L">300L (Hogshead)</option>
          <option value="500L">500L (Puncheon)</option>
          <option value="1000L">1000L (Tun)</option>
        </select>
        
        <select v-model="originFilter" class="filter-select">
          <option value="">All Origins</option>
          <option value="france">France</option>
          <option value="usa">United States</option>
          <option value="hungary">Hungary</option>
          <option value="croatia">Croatia</option>
          <option value="italy">Italy</option>
        </select>
        
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Statuses</option>
          <option value="available">Available</option>
          <option value="reserved">Reserved</option>
          <option value="sold">Sold</option>
          <option value="aging">Aging</option>
        </select>
      </div>
    </section>

    <!-- Barrels Table -->
    <section class="barrels-table">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Type</th>
              <th>Wood</th>
              <th>Size</th>
              <th>Origin</th>
              <th>Age</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="barrel in filteredBarrels" :key="barrel.id" class="table-row">
              <td>
                <div class="barrel-image">
                  <div class="image-placeholder">{{ barrel.emoji }}</div>
                </div>
              </td>
              <td>
                <div class="barrel-info">
                  <h4 class="barrel-name">{{ barrel.name }}</h4>
                  <p class="barrel-description">{{ barrel.description }}</p>
                </div>
              </td>
              <td>
                <span class="wood-badge wood-{{ barrel.woodType }}">{{ barrel.woodType }}</span>
              </td>
              <td>
                <span class="size-badge">{{ barrel.size }}</span>
              </td>
              <td>
                <span class="origin-badge">{{ barrel.origin }}</span>
              </td>
              <td>
                <span class="age">{{ barrel.age }} years</span>
              </td>
              <td>
                <span class="price">€{{ barrel.price }}</span>
              </td>
              <td>
                <span class="stock" :class="{ 'low-stock': barrel.stock < 5 }">
                  {{ barrel.stock }} units
                </span>
              </td>
              <td>
                <span class="status-badge status-{{ barrel.status }}">
                  {{ barrel.status }}
                </span>
              </td>
              <td>
                <div class="actions">
                  <button class="action-btn edit" @click="editBarrel(barrel)" title="Edit">
                    ✏️
                  </button>
                  <button class="action-btn view" @click="viewBarrel(barrel)" title="View">
                    👁️
                  </button>
                  <button class="action-btn delete" @click="deleteBarrel(barrel)" title="Delete">
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
        Showing {{ paginationStart }} to {{ paginationEnd }} of {{ totalBarrels }} barrels
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
  title: 'Barrels Management - Admin Dashboard',
  description: 'Manage barrel inventory, specifications, and pricing.'
})

// Mock data - replace with actual API calls
const barrels = ref([
  {
    id: 1,
    name: 'Bordeaux Barrel',
    description: 'Traditional 225L French oak barrel',
    woodType: 'french-oak',
    size: '225L',
    origin: 'France',
    age: 2,
    price: 850,
    stock: 45,
    status: 'available',
    emoji: '🛢️'
  },
  {
    id: 2,
    name: 'Burgundy Barrel',
    description: '228L French oak for Pinot Noir',
    woodType: 'french-oak',
    size: '228L',
    origin: 'France',
    age: 3,
    price: 920,
    stock: 28,
    status: 'available',
    emoji: '🛢️'
  },
  {
    id: 3,
    name: 'American Oak Hogshead',
    description: '300L American white oak barrel',
    woodType: 'american-oak',
    size: '300L',
    origin: 'USA',
    age: 1,
    price: 680,
    stock: 15,
    status: 'available',
    emoji: '🛢️'
  },
  {
    id: 4,
    name: 'Hungarian Oak Puncheon',
    description: '500L Hungarian oak for aging',
    woodType: 'hungarian-oak',
    size: '500L',
    origin: 'Hungary',
    age: 4,
    price: 1200,
    stock: 8,
    status: 'reserved',
    emoji: '🛢️'
  },
  {
    id: 5,
    name: 'Slavonian Oak Tun',
    description: '1000L Croatian oak for large batches',
    woodType: 'slavonian-oak',
    size: '1000L',
    origin: 'Croatia',
    age: 5,
    price: 2200,
    stock: 3,
    status: 'available',
    emoji: '🛢️'
  }
])

// Search and filters
const searchQuery = ref('')
const woodTypeFilter = ref('')
const sizeFilter = ref('')
const originFilter = ref('')
const statusFilter = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredBarrels = computed(() => {
  let filtered = barrels.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(barrel => 
      barrel.name.toLowerCase().includes(query) ||
      barrel.description.toLowerCase().includes(query) ||
      barrel.woodType.toLowerCase().includes(query) ||
      barrel.size.toLowerCase().includes(query) ||
      barrel.origin.toLowerCase().includes(query)
    )
  }

  if (woodTypeFilter.value) {
    filtered = filtered.filter(barrel => barrel.woodType === woodTypeFilter.value)
  }

  if (sizeFilter.value) {
    filtered = filtered.filter(barrel => barrel.size === sizeFilter.value)
  }

  if (originFilter.value) {
    filtered = filtered.filter(barrel => barrel.origin.toLowerCase() === originFilter.value)
  }

  if (statusFilter.value) {
    filtered = filtered.filter(barrel => barrel.status === statusFilter.value)
  }

  return filtered
})

const totalBarrels = computed(() => filteredBarrels.value.length)
const totalPages = computed(() => Math.ceil(totalBarrels.value / itemsPerPage))
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, totalBarrels.value))

// Methods
const refreshBarrels = () => {
  // TODO: Implement actual API call to refresh barrels
  console.log('Refreshing barrels...')
}

const editBarrel = (barrel) => {
  // TODO: Navigate to edit page or open edit modal
  console.log('Editing barrel:', barrel)
  navigateTo(`/admin/barrels/${barrel.id}/edit`)
}

const viewBarrel = (barrel) => {
  // TODO: Navigate to view page or open view modal
  console.log('Viewing barrel:', barrel)
  navigateTo(`/admin/barrels/${barrel.id}`)
}

const deleteBarrel = (barrel) => {
  if (confirm(`Are you sure you want to delete "${barrel.name}"?`)) {
    // TODO: Implement actual delete API call
    console.log('Deleting barrel:', barrel)
    barrels.value = barrels.value.filter(b => b.id !== barrel.id)
  }
}

const changePage = (page) => {
  currentPage.value = page
}
</script>

<style scoped>
.barrels-management {
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

/* Barrels Table */
.barrels-table {
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

/* Barrel Image */
.barrel-image {
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

/* Barrel Info */
.barrel-info {
  min-width: 200px;
}

.barrel-name {
  font-weight: 600;
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.barrel-description {
  color: #57534e;
  margin: 0;
  font-size: 0.875rem;
}

/* Badges */
.wood-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.wood-french-oak {
  background: #fef3c7;
  color: #d97706;
}

.wood-american-oak {
  background: #dbeafe;
  color: #2563eb;
}

.wood-hungarian-oak {
  background: #f3e8ff;
  color: #7c3aed;
}

.wood-slavonian-oak {
  background: #ecfdf5;
  color: #059669;
}

.wood-chestnut {
  background: #fef2f2;
  color: #dc2626;
}

.size-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.origin-badge {
  background: #e0e7ff;
  color: #3730a3;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.age {
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

.status-available {
  background: #f0fdf4;
  color: #16a34a;
}

.status-reserved {
  background: #fef3c7;
  color: #d97706;
}

.status-sold {
  background: #fef2f2;
  color: #dc2626;
}

.status-aging {
  background: #f0f9ff;
  color: #0284c7;
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
  .barrels-management {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .table th,
  .table td {
    padding: 0.75rem 0.5rem;
  }
  
  .barrel-info {
    min-width: 150px;
  }
  
  .pagination {
    flex-direction: column;
    text-align: center;
  }
}
</style>
