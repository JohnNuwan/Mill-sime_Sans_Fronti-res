<template>
  <div class="orders-management">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Orders Management</h1>
          <p class="page-subtitle">Monitor and manage customer orders and fulfillment</p>
        </div>
        <div class="header-actions">
          <button class="btn btn--outline" @click="refreshOrders">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <button class="btn btn--outline" @click="exportOrders">
            <span class="icon">📊</span>
            Export
          </button>
        </div>
      </div>
    </header>

    <!-- Search and Filters -->
    <section class="search-filters">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search orders by ID, customer name, or email..."
          class="search-input"
        />
        <button class="search-button">
          <span class="icon">🔍</span>
        </button>
      </div>
      
      <div class="filters">
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="processing">Processing</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
          <option value="refunded">Refunded</option>
        </select>
        
        <select v-model="customerTypeFilter" class="filter-select">
          <option value="">All Customer Types</option>
          <option value="b2b">B2B</option>
          <option value="b2c">B2C</option>
          <option value="wholesale">Wholesale</option>
        </select>
        
        <select v-model="dateFilter" class="filter-select">
          <option value="">All Dates</option>
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="quarter">This Quarter</option>
          <option value="year">This Year</option>
        </select>
        
        <select v-model="sortBy" class="filter-select">
          <option value="date">Sort by Date</option>
          <option value="amount">Sort by Amount</option>
          <option value="status">Sort by Status</option>
          <option value="customer">Sort by Customer</option>
        </select>
      </div>
    </section>

    <!-- Orders Table -->
    <section class="orders-table">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Total</th>
              <th>Status</th>
              <th>Date</th>
              <th>Payment</th>
              <th>Shipping</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in sortedOrders" :key="order.id" class="table-row">
              <td>
                <div class="order-id">
                  <span class="id-number">#{{ order.id }}</span>
                  <span class="order-type" :class="order.customerType">{{ order.customerType.toUpperCase() }}</span>
                </div>
              </td>
              <td>
                <div class="customer-info">
                  <h4 class="customer-name">{{ order.customerName }}</h4>
                  <p class="customer-email">{{ order.customerEmail }}</p>
                  <p class="customer-company" v-if="order.customerCompany">{{ order.customerCompany }}</p>
                </div>
              </td>
              <td>
                <div class="order-items">
                  <div class="items-summary">
                    <span class="items-count">{{ order.itemsCount }} items</span>
                    <span class="items-preview">{{ order.itemsPreview }}</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="order-total">
                  <span class="total-amount">€{{ order.total.toLocaleString() }}</span>
                  <span class="currency">EUR</span>
                </div>
              </td>
              <td>
                <span class="status-badge status-{{ order.status }}">
                  {{ order.status }}
                </span>
              </td>
              <td>
                <div class="order-date">
                  <span class="date">{{ formatDate(order.orderDate) }}</span>
                  <span class="time">{{ formatTime(order.orderDate) }}</span>
                </div>
              </td>
              <td>
                <div class="payment-info">
                  <span class="payment-method">{{ order.paymentMethod }}</span>
                  <span class="payment-status" :class="order.paymentStatus">{{ order.paymentStatus }}</span>
                </div>
              </td>
              <td>
                <div class="shipping-info">
                  <span class="shipping-method">{{ order.shippingMethod }}</span>
                  <span class="tracking-number" v-if="order.trackingNumber">{{ order.trackingNumber }}</span>
                </div>
              </td>
              <td>
                <div class="actions">
                  <button class="action-btn view" @click="viewOrder(order)" title="View Details">
                    👁️
                  </button>
                  <button class="action-btn edit" @click="editOrder(order)" title="Edit Order">
                    ✏️
                  </button>
                  <button class="action-btn status" @click="updateStatus(order)" title="Update Status">
                    🔄
                  </button>
                  <button class="action-btn invoice" @click="generateInvoice(order)" title="Generate Invoice">
                    📄
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
        Showing {{ paginationStart }} to {{ paginationEnd }} of {{ totalOrders }} orders
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
  title: 'Orders Management - Admin Dashboard',
  description: 'Monitor and manage customer orders and fulfillment.'
})

// Mock data - replace with actual API calls
const orders = ref([
  {
    id: 'ORD001',
    customerName: 'Jean Dupont',
    customerEmail: 'jean.dupont@chateau-margaux.fr',
    customerCompany: 'Château Margaux',
    customerType: 'b2b',
    itemsCount: 3,
    itemsPreview: 'Château Margaux 2018, Dom Pérignon 2012, Sauternes 2015',
    total: 1580,
    status: 'confirmed',
    orderDate: '2024-01-28T10:30:00',
    paymentMethod: 'Bank Transfer',
    paymentStatus: 'paid',
    shippingMethod: 'Express',
    trackingNumber: 'TRK123456789'
  },
  {
    id: 'ORD002',
    customerName: 'Maria Rodriguez',
    customerEmail: 'm.rodriguez@wineimports.com',
    customerCompany: 'Wine Imports Inc.',
    customerType: 'wholesale',
    itemsCount: 8,
    itemsPreview: 'Bordeaux Barrels (5), Burgundy Barrels (3)',
    total: 7200,
    status: 'processing',
    orderDate: '2024-01-27T14:15:00',
    paymentMethod: 'Credit Card',
    paymentStatus: 'paid',
    shippingMethod: 'Standard',
    trackingNumber: null
  },
  {
    id: 'ORD003',
    customerName: 'Pierre Dubois',
    customerEmail: 'pierre.dubois@email.com',
    customerCompany: null,
    customerType: 'b2c',
    itemsCount: 1,
    itemsPreview: 'Chablis Grand Cru 2020',
    total: 180,
    status: 'shipped',
    orderDate: '2024-01-26T09:45:00',
    paymentMethod: 'PayPal',
    paymentStatus: 'paid',
    shippingMethod: 'Standard',
    trackingNumber: 'TRK987654321'
  },
  {
    id: 'ORD004',
    customerName: 'Sarah Johnson',
    customerEmail: 'sarah.j@luxurywines.co.uk',
    customerCompany: 'Luxury Wines Ltd.',
    customerType: 'b2b',
    itemsCount: 12,
    itemsPreview: 'Various Premium Wines and Barrels',
    total: 15400,
    status: 'delivered',
    orderDate: '2024-01-25T16:20:00',
    paymentMethod: 'Bank Transfer',
    paymentStatus: 'paid',
    shippingMethod: 'Express',
    trackingNumber: 'TRK456789123'
  },
  {
    id: 'ORD005',
    customerName: 'Hans Mueller',
    customerEmail: 'h.mueller@weingut-mueller.de',
    customerCompany: 'Weingut Mueller',
    customerType: 'b2b',
    itemsCount: 2,
    itemsPreview: 'French Oak Barrels (2)',
    total: 1700,
    status: 'pending',
    orderDate: '2024-01-28T11:00:00',
    paymentMethod: 'Bank Transfer',
    paymentStatus: 'pending',
    shippingMethod: 'Standard',
    trackingNumber: null
  }
])

// Search and filters
const searchQuery = ref('')
const statusFilter = ref('')
const customerTypeFilter = ref('')
const dateFilter = ref('')
const sortBy = ref('date')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Computed properties
const filteredOrders = computed(() => {
  let filtered = orders.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(order => 
      order.id.toLowerCase().includes(query) ||
      order.customerName.toLowerCase().includes(query) ||
      order.customerEmail.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(order => order.status === statusFilter.value)
  }

  if (customerTypeFilter.value) {
    filtered = filtered.filter(order => order.customerType === customerTypeFilter.value)
  }

  if (dateFilter.value) {
    const now = new Date()
    const orderDate = new Date(order.orderDate)
    
    switch (dateFilter.value) {
      case 'today':
        filtered = filtered.filter(order => {
          const orderDate = new Date(order.orderDate)
          return orderDate.toDateString() === now.toDateString()
        })
        break
      case 'week':
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        filtered = filtered.filter(order => new Date(order.orderDate) >= weekAgo)
        break
      case 'month':
        const monthAgo = new Date(now.getFullYear(), now.getMonth(), 1)
        filtered = filtered.filter(order => new Date(order.orderDate) >= monthAgo)
        break
      case 'quarter':
        const quarterStart = new Date(now.getFullYear(), Math.floor(now.getMonth() / 3) * 3, 1)
        filtered = filtered.filter(order => new Date(order.orderDate) >= quarterStart)
        break
      case 'year':
        const yearStart = new Date(now.getFullYear(), 0, 1)
        filtered = filtered.filter(order => new Date(order.orderDate) >= yearStart)
        break
    }
  }

  return filtered
})

const sortedOrders = computed(() => {
  const filtered = [...filteredOrders.value]
  
  switch (sortBy.value) {
    case 'date':
      return filtered.sort((a, b) => new Date(b.orderDate) - new Date(a.orderDate))
    case 'amount':
      return filtered.sort((a, b) => b.total - a.total)
    case 'status':
      return filtered.sort((a, b) => a.status.localeCompare(b.status))
    case 'customer':
      return filtered.sort((a, b) => a.customerName.localeCompare(b.customerName))
    default:
      return filtered
  }
})

const totalOrders = computed(() => filteredOrders.value.length)
const totalPages = computed(() => Math.ceil(totalOrders.value / itemsPerPage))
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, totalOrders.value))

// Methods
const refreshOrders = () => {
  // TODO: Implement actual API call to refresh orders
  console.log('Refreshing orders...')
}

const exportOrders = () => {
  // TODO: Implement export functionality
  console.log('Exporting orders...')
}

const viewOrder = (order) => {
  // TODO: Navigate to view page or open view modal
  console.log('Viewing order:', order)
  navigateTo(`/admin/orders/${order.id}`)
}

const editOrder = (order) => {
  // TODO: Navigate to edit page or open edit modal
  console.log('Editing order:', order)
  navigateTo(`/admin/orders/${order.id}/edit`)
}

const updateStatus = (order) => {
  // TODO: Open status update modal
  console.log('Updating status for order:', order)
}

const generateInvoice = (order) => {
  // TODO: Generate and download invoice
  console.log('Generating invoice for order:', order)
}

const changePage = (page) => {
  currentPage.value = page
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.orders-management {
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

/* Orders Table */
.orders-table {
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

/* Order ID */
.order-id {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.id-number {
  font-weight: 600;
  color: #1c1917;
  font-size: 1rem;
  font-family: monospace;
}

.order-type {
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.order-type.b2b {
  background: #dbeafe;
  color: #2563eb;
}

.order-type.b2c {
  background: #fef3c7;
  color: #d97706;
}

.order-type.wholesale {
  background: #ecfdf5;
  color: #059669;
}

/* Customer Info */
.customer-info {
  min-width: 180px;
}

.customer-name {
  font-weight: 600;
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.customer-email {
  color: #57534e;
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.customer-company {
  color: #78716c;
  margin: 0;
  font-size: 0.75rem;
  font-style: italic;
}

/* Order Items */
.order-items {
  min-width: 200px;
}

.items-summary {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.items-count {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.items-preview {
  color: #57534e;
  font-size: 0.75rem;
  line-height: 1.3;
}

/* Order Total */
.order-total {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.total-amount {
  font-weight: 600;
  color: #16a34a;
  font-size: 1rem;
}

.currency {
  color: #78716c;
  font-size: 0.75rem;
}

/* Status Badge */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-pending {
  background: #fef3c7;
  color: #d97706;
}

.status-confirmed {
  background: #dbeafe;
  color: #2563eb;
}

.status-processing {
  background: #f3e8ff;
  color: #7c3aed;
}

.status-shipped {
  background: #ecfdf5;
  color: #059669;
}

.status-delivered {
  background: #f0fdf4;
  color: #16a34a;
}

.status-cancelled {
  background: #fef2f2;
  color: #dc2626;
}

.status-refunded {
  background: #f3f4f6;
  color: #6b7280;
}

/* Order Date */
.order-date {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.date {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.time {
  color: #57534e;
  font-size: 0.75rem;
}

/* Payment Info */
.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.payment-method {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.payment-status {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  text-transform: capitalize;
}

.payment-status.paid {
  background: #f0fdf4;
  color: #16a34a;
}

.payment-status.pending {
  background: #fef3c7;
  color: #d97706;
}

.payment-status.failed {
  background: #fef2f2;
  color: #dc2626;
}

/* Shipping Info */
.shipping-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.shipping-method {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.tracking-number {
  color: #57534e;
  font-size: 0.75rem;
  font-family: monospace;
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

.action-btn.status {
  background: #ecfdf5;
  color: #059669;
}

.action-btn.status:hover {
  background: #10b981;
  color: white;
}

.action-btn.invoice {
  background: #f3e8ff;
  color: #7c3aed;
}

.action-btn.invoice:hover {
  background: #8b5cf6;
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
  .orders-management {
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
