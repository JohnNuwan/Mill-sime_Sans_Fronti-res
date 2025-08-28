<template>
  <div class="customers-management">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Customers Management</h1>
          <p class="page-subtitle">Manage customer accounts, profiles, and relationships</p>
        </div>
        <div class="header-actions">
          <button class="btn btn--outline" @click="refreshCustomers">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <NuxtLink to="/admin/customers/add" class="btn btn--primary">
            <span class="icon">➕</span>
            Add New Customer
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
          placeholder="Search customers by name, email, company, or location..."
          class="search-input"
        />
        <button class="search-button">
          <span class="icon">🔍</span>
        </button>
      </div>
      
      <div class="filters">
        <select v-model="typeFilter" class="filter-select">
          <option value="">All Customer Types</option>
          <option value="b2b">B2B (Business)</option>
          <option value="b2c">B2C (Individual)</option>
          <option value="wholesale">Wholesale</option>
          <option value="retail">Retail</option>
        </select>
        
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="pending">Pending</option>
          <option value="suspended">Suspended</option>
        </select>
        
        <select v-model="countryFilter" class="filter-select">
          <option value="">All Countries</option>
          <option value="france">France</option>
          <option value="usa">United States</option>
          <option value="uk">United Kingdom</option>
          <option value="germany">Germany</option>
          <option value="italy">Italy</option>
          <option value="spain">Spain</option>
          <option value="canada">Canada</option>
          <option value="australia">Australia</option>
        </select>
        
        <select v-model="sortBy" class="filter-select">
          <option value="name">Sort by Name</option>
          <option value="company">Sort by Company</option>
          <option value="created">Sort by Created Date</option>
          <option value="lastOrder">Sort by Last Order</option>
          <option value="totalSpent">Sort by Total Spent</option>
        </select>
      </div>
    </section>

    <!-- Customers Table -->
    <section class="customers-table">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Customer</th>
              <th>Contact</th>
              <th>Company</th>
              <th>Type</th>
              <th>Location</th>
              <th>Status</th>
              <th>Orders</th>
              <th>Total Spent</th>
              <th>Last Order</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in sortedCustomers" :key="customer.id" class="table-row">
              <td>
                <div class="customer-info">
                  <div class="customer-avatar">
                    <div class="avatar-placeholder">{{ customer.initials }}</div>
                  </div>
                  <div class="customer-details">
                    <h4 class="customer-name">{{ customer.name }}</h4>
                    <p class="customer-id">ID: {{ customer.id }}</p>
                  </div>
                </div>
              </td>
              <td>
                <div class="contact-info">
                  <p class="email">{{ customer.email }}</p>
                  <p class="phone">{{ customer.phone }}</p>
                </div>
              </td>
              <td>
                <div class="company-info">
                  <p class="company-name">{{ customer.company || 'N/A' }}</p>
                  <p class="company-type">{{ customer.companyType || 'Individual' }}</p>
                </div>
              </td>
              <td>
                <span class="type-badge type-{{ customer.type }}">{{ customer.type }}</span>
              </td>
              <td>
                <div class="location-info">
                  <p class="city">{{ customer.city }}, {{ customer.country }}</p>
                  <p class="region">{{ customer.region || '' }}</p>
                </div>
              </td>
              <td>
                <span class="status-badge status-{{ customer.status }}">
                  {{ customer.status }}
                </span>
              </td>
              <td>
                <span class="orders-count">{{ customer.ordersCount }} orders</span>
              </td>
              <td>
                <span class="total-spent">€{{ customer.totalSpent.toLocaleString() }}</span>
              </td>
              <td>
                <span class="last-order">{{ formatDate(customer.lastOrder) }}</span>
              </td>
              <td>
                <div class="actions">
                  <button class="action-btn view" @click="viewCustomer(customer)" title="View">
                    👁️
                  </button>
                  <button class="action-btn edit" @click="editCustomer(customer)" title="Edit">
                    ✏️
                  </button>
                  <button class="action-btn orders" @click="viewOrders(customer)" title="View Orders">
                    📋
                  </button>
                  <button class="action-btn delete" @click="deleteCustomer(customer)" title="Delete">
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
        Showing {{ paginationStart }} to {{ paginationEnd }} of {{ totalCustomers }} customers
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
  title: 'Customers Management - Admin Dashboard',
  description: 'Manage customer accounts, profiles, and relationships.'
})

// Mock data - replace with actual API calls
const customers = ref([
  {
    id: 'CUST001',
    name: 'Jean Dupont',
    initials: 'JD',
    email: 'jean.dupont@chateau-margaux.fr',
    phone: '+33 1 23 45 67 89',
    company: 'Château Margaux',
    companyType: 'Winery',
    type: 'b2b',
    city: 'Margaux',
    region: 'Bordeaux',
    country: 'France',
    status: 'active',
    ordersCount: 12,
    totalSpent: 45000,
    lastOrder: '2024-01-15',
    createdAt: '2022-03-10'
  },
  {
    id: 'CUST002',
    name: 'Maria Rodriguez',
    initials: 'MR',
    email: 'm.rodriguez@wineimports.com',
    phone: '+1 555 123 4567',
    company: 'Wine Imports Inc.',
    companyType: 'Distributor',
    type: 'wholesale',
    city: 'New York',
    region: 'NY',
    country: 'USA',
    status: 'active',
    ordersCount: 8,
    totalSpent: 32000,
    lastOrder: '2024-01-20',
    createdAt: '2022-06-15'
  },
  {
    id: 'CUST003',
    name: 'Pierre Dubois',
    initials: 'PD',
    email: 'pierre.dubois@email.com',
    phone: '+33 6 12 34 56 78',
    company: null,
    companyType: null,
    type: 'b2c',
    city: 'Paris',
    region: 'Île-de-France',
    country: 'France',
    status: 'active',
    ordersCount: 3,
    totalSpent: 2800,
    lastOrder: '2024-01-10',
    createdAt: '2023-09-20'
  },
  {
    id: 'CUST004',
    name: 'Sarah Johnson',
    initials: 'SJ',
    email: 'sarah.j@luxurywines.co.uk',
    phone: '+44 20 7946 0958',
    company: 'Luxury Wines Ltd.',
    companyType: 'Retailer',
    type: 'retail',
    city: 'London',
    region: 'England',
    country: 'UK',
    status: 'active',
    ordersCount: 15,
    totalSpent: 67000,
    lastOrder: '2024-01-25',
    createdAt: '2021-11-05'
  },
  {
    id: 'CUST005',
    name: 'Hans Mueller',
    initials: 'HM',
    email: 'h.mueller@weingut-mueller.de',
    phone: '+49 30 12345678',
    company: 'Weingut Mueller',
    companyType: 'Winery',
    type: 'b2b',
    city: 'Berlin',
    region: 'Berlin',
    country: 'Germany',
    status: 'pending',
    ordersCount: 0,
    totalSpent: 0,
    lastOrder: null,
    createdAt: '2024-01-28'
  }
])

// Search and filters
const searchQuery = ref('')
const typeFilter = ref('')
const statusFilter = ref('')
const countryFilter = ref('')
const sortBy = ref('name')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredCustomers = computed(() => {
  let filtered = customers.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(customer => 
      customer.name.toLowerCase().includes(query) ||
      customer.email.toLowerCase().includes(query) ||
      (customer.company && customer.company.toLowerCase().includes(query)) ||
      customer.city.toLowerCase().includes(query) ||
      customer.country.toLowerCase().includes(query)
    )
  }

  if (typeFilter.value) {
    filtered = filtered.filter(customer => customer.type === typeFilter.value)
  }

  if (statusFilter.value) {
    filtered = filtered.filter(customer => customer.status === statusFilter.value)
  }

  if (countryFilter.value) {
    filtered = filtered.filter(customer => customer.country.toLowerCase() === countryFilter.value)
  }

  return filtered
})

const sortedCustomers = computed(() => {
  const filtered = [...filteredCustomers.value]
  
  switch (sortBy.value) {
    case 'name':
      return filtered.sort((a, b) => a.name.localeCompare(b.name))
    case 'company':
      return filtered.sort((a, b) => {
        const companyA = a.company || 'Z'
        const companyB = b.company || 'Z'
        return companyA.localeCompare(companyB)
      })
    case 'created':
      return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    case 'lastOrder':
      return filtered.sort((a, b) => {
        if (!a.lastOrder && !b.lastOrder) return 0
        if (!a.lastOrder) return 1
        if (!b.lastOrder) return -1
        return new Date(b.lastOrder) - new Date(a.lastOrder)
      })
    case 'totalSpent':
      return filtered.sort((a, b) => b.totalSpent - a.totalSpent)
    default:
      return filtered
  }
})

const totalCustomers = computed(() => filteredCustomers.value.length)
const totalPages = computed(() => Math.ceil(totalCustomers.value / itemsPerPage))
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, totalCustomers.value))

// Methods
const refreshCustomers = () => {
  // TODO: Implement actual API call to refresh customers
  console.log('Refreshing customers...')
}

const viewCustomer = (customer) => {
  // TODO: Navigate to view page or open view modal
  console.log('Viewing customer:', customer)
  navigateTo(`/admin/customers/${customer.id}`)
}

const editCustomer = (customer) => {
  // TODO: Navigate to edit page or open edit modal
  console.log('Editing customer:', customer)
  navigateTo(`/admin/customers/${customer.id}/edit`)
}

const viewOrders = (customer) => {
  // TODO: Navigate to orders page filtered by customer
  console.log('Viewing orders for customer:', customer)
  navigateTo(`/admin/orders?customer=${customer.id}`)
}

const deleteCustomer = (customer) => {
  if (confirm(`Are you sure you want to delete customer "${customer.name}"? This action cannot be undone.`)) {
    // TODO: Implement actual delete API call
    console.log('Deleting customer:', customer)
    customers.value = customers.value.filter(c => c.id !== customer.id)
  }
}

const changePage = (page) => {
  currentPage.value = page
}

const formatDate = (dateString) => {
  if (!dateString) return 'Never'
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}
</script>

<style scoped>
.customers-management {
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

/* Customers Table */
.customers-table {
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

/* Customer Info */
.customer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 200px;
}

.customer-avatar {
  width: 50px;
  height: 50px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 600;
}

.customer-name {
  font-weight: 600;
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.customer-id {
  color: #78716c;
  margin: 0;
  font-size: 0.75rem;
  font-family: monospace;
}

/* Contact Info */
.contact-info {
  min-width: 180px;
}

.contact-info p {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.email {
  color: #1c1917;
  font-weight: 500;
}

.phone {
  color: #57534e;
}

/* Company Info */
.company-info {
  min-width: 150px;
}

.company-info p {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.company-name {
  color: #1c1917;
  font-weight: 500;
}

.company-type {
  color: #57534e;
  font-size: 0.75rem;
}

/* Location Info */
.location-info {
  min-width: 120px;
}

.location-info p {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.city {
  color: #1c1917;
  font-weight: 500;
}

.region {
  color: #57534e;
  font-size: 0.75rem;
}

/* Badges */
.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.type-b2b {
  background: #dbeafe;
  color: #2563eb;
}

.type-b2c {
  background: #fef3c7;
  color: #d97706;
}

.type-wholesale {
  background: #ecfdf5;
  color: #059669;
}

.type-retail {
  background: #f3e8ff;
  color: #7c3aed;
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

.status-pending {
  background: #fef3c7;
  color: #d97706;
}

.status-suspended {
  background: #f3f4f6;
  color: #6b7280;
}

/* Data Display */
.orders-count {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.total-spent {
  font-weight: 600;
  color: #16a34a;
  font-size: 0.875rem;
}

.last-order {
  color: #57534e;
  font-size: 0.875rem;
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

.action-btn.view {
  background: #dbeafe;
  color: #2563eb;
}

.action-btn.view:hover {
  background: #3b82f6;
  color: white;
}

.action-btn.edit {
  background: #fef3c7;
  color: #d97706;
}

.action-btn.edit:hover {
  background: #f59e0b;
  color: white;
}

.action-btn.orders {
  background: #ecfdf5;
  color: #059669;
}

.action-btn.orders:hover {
  background: #10b981;
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
  .customers-management {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .table th,
  .table td {
    padding: 0.75rem 0.5rem;
  }
  
  .customer-info {
    min-width: 150px;
  }
  
  .pagination {
    flex-direction: column;
    text-align: center;
  }
}
</style>
