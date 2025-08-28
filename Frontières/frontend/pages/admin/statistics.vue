<template>
  <div class="statistics">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Business Statistics</h1>
          <p class="page-subtitle">Comprehensive overview of your business performance</p>
        </div>
        <div class="header-actions">
          <select v-model="timeRange" class="time-select">
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
            <option value="1y">Last Year</option>
            <option value="all">All Time</option>
          </select>
          <button class="btn btn--outline" @click="refreshStats">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <button class="btn btn--primary" @click="exportReport">
            <span class="icon">📊</span>
            Export Report
          </button>
        </div>
      </div>
    </header>

    <!-- Key Metrics -->
    <section class="key-metrics">
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-header">
            <h3 class="metric-title">Total Revenue</h3>
            <span class="metric-trend positive">+12.5%</span>
          </div>
          <div class="metric-value">€{{ formatNumber(stats.totalRevenue) }}</div>
          <div class="metric-comparison">
            vs €{{ formatNumber(stats.previousRevenue) }} previous period
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <h3 class="metric-title">Orders</h3>
            <span class="metric-trend positive">+8.3%</span>
          </div>
          <div class="metric-value">{{ formatNumber(stats.totalOrders) }}</div>
          <div class="metric-comparison">
            vs {{ formatNumber(stats.previousOrders) }} previous period
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <h3 class="metric-title">Customers</h3>
            <span class="metric-trend positive">+15.2%</span>
          </div>
          <div class="metric-value">{{ formatNumber(stats.totalCustomers) }}</div>
          <div class="metric-comparison">
            vs {{ formatNumber(stats.previousCustomers) }} previous period
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <h3 class="metric-title">Average Order Value</h3>
            <span class="metric-trend positive">+4.7%</span>
          </div>
          <div class="metric-value">€{{ formatNumber(stats.averageOrderValue) }}</div>
          <div class="metric-comparison">
            vs €{{ formatNumber(stats.previousAverageOrder) }} previous period
          </div>
        </div>
      </div>
    </section>

    <!-- Charts Section -->
    <section class="charts-section">
      <div class="charts-grid">
        <!-- Revenue Chart -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">Revenue Trend</h3>
            <div class="chart-legend">
              <span class="legend-item">
                <span class="legend-color current"></span>
                Current Period
              </span>
              <span class="legend-item">
                <span class="legend-color previous"></span>
                Previous Period
              </span>
            </div>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">
              <div class="chart-bars">
                <div 
                  v-for="(bar, index) in revenueData" 
                  :key="index"
                  class="chart-bar"
                  :style="{ height: `${bar.current}%` }"
                >
                  <div class="bar-tooltip">
                    <strong>{{ bar.month }}</strong><br>
                    Current: €{{ formatNumber(bar.currentValue) }}<br>
                    Previous: €{{ formatNumber(bar.previousValue) }}
                  </div>
                </div>
              </div>
              <div class="chart-labels">
                <span v-for="(bar, index) in revenueData" :key="index" class="chart-label">
                  {{ bar.month }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Orders Chart -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">Orders by Status</h3>
          </div>
          <div class="chart-container">
            <div class="pie-chart">
              <div class="pie-segment" style="--percentage: 35; --color: #10b981;">
                <div class="segment-label">Delivered (35%)</div>
              </div>
              <div class="pie-segment" style="--percentage: 25; --color: #3b82f6;">
                <div class="segment-label">Processing (25%)</div>
              </div>
              <div class="pie-segment" style="--percentage: 20; --color: #f59e0b;">
                <div class="segment-label">Shipped (20%)</div>
              </div>
              <div class="pie-segment" style="--percentage: 15; --color: #ef4444;">
                <div class="segment-label">Pending (15%)</div>
              </div>
              <div class="pie-segment" style="--percentage: 5; --color: #6b7280;">
                <div class="segment-label">Cancelled (5%)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Top Products and Customers -->
    <section class="top-lists">
      <div class="lists-grid">
        <!-- Top Products -->
        <div class="list-card">
          <div class="list-header">
            <h3 class="list-title">Top Selling Products</h3>
            <NuxtLink to="/admin/wines" class="view-all-link">View All</NuxtLink>
          </div>
          <div class="list-content">
            <div v-for="(product, index) in topProducts" :key="product.id" class="list-item">
              <div class="item-rank">{{ index + 1 }}</div>
              <div class="item-info">
                <h4 class="item-name">{{ product.name }}</h4>
                <p class="item-category">{{ product.category }}</p>
              </div>
              <div class="item-stats">
                <span class="item-sales">{{ product.sales }} sold</span>
                <span class="item-revenue">€{{ formatNumber(product.revenue) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Customers -->
        <div class="list-card">
          <div class="list-header">
            <h3 class="list-title">Top Customers</h3>
            <NuxtLink to="/admin/customers" class="view-all-link">View All</NuxtLink>
          </div>
          <div class="list-content">
            <div v-for="(customer, index) in topCustomers" :key="customer.id" class="list-item">
              <div class="item-rank">{{ index + 1 }}</div>
              <div class="item-info">
                <h4 class="item-name">{{ customer.name }}</h4>
                <p class="item-company">{{ customer.company }}</p>
              </div>
              <div class="item-stats">
                <span class="item-orders">{{ customer.orders }} orders</span>
                <span class="item-revenue">€{{ formatNumber(customer.revenue) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Geographic Distribution -->
    <section class="geographic-stats">
      <div class="geo-card">
        <div class="geo-header">
          <h3 class="geo-title">Sales by Region</h3>
        </div>
        <div class="geo-content">
          <div class="geo-list">
            <div v-for="region in salesByRegion" :key="region.name" class="geo-item">
              <div class="geo-info">
                <span class="geo-name">{{ region.name }}</span>
                <span class="geo-sales">{{ region.sales }} orders</span>
              </div>
              <div class="geo-bar">
                <div class="geo-bar-fill" :style="{ width: `${region.percentage}%` }"></div>
              </div>
              <span class="geo-percentage">{{ region.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Business Statistics - Admin Dashboard',
  description: 'Comprehensive business analytics and performance metrics.'
})

// Time range filter
const timeRange = ref('30d')

// Mock statistics data
const stats = ref({
  totalRevenue: 1250000,
  previousRevenue: 1110000,
  totalOrders: 2847,
  previousOrders: 2628,
  totalCustomers: 1247,
  previousCustomers: 1083,
  averageOrderValue: 439,
  previousAverageOrder: 420
})

// Revenue chart data
const revenueData = ref([
  { month: 'Jan', currentValue: 98000, previousValue: 85000, current: 65, previous: 55 },
  { month: 'Feb', currentValue: 112000, previousValue: 92000, current: 75, previous: 60 },
  { month: 'Mar', currentValue: 134000, previousValue: 108000, current: 90, previous: 70 },
  { month: 'Apr', currentValue: 156000, previousValue: 125000, current: 100, previous: 80 },
  { month: 'May', currentValue: 142000, previousValue: 118000, current: 95, previous: 75 },
  { month: 'Jun', currentValue: 168000, previousValue: 135000, current: 100, previous: 85 }
])

// Top products
const topProducts = ref([
  { id: 1, name: 'Château Margaux 2018', category: 'Red Wine', sales: 156, revenue: 132600 },
  { id: 2, name: 'Dom Pérignon 2012', category: 'Sparkling Wine', sales: 89, revenue: 24920 },
  { id: 3, name: 'Bordeaux Barrel 225L', category: 'Barrel', sales: 67, revenue: 56950 },
  { id: 4, name: 'Romanée-Conti 2019', category: 'Red Wine', sales: 23, revenue: 345000 },
  { id: 5, name: 'Sauternes 2015', category: 'Dessert Wine', sales: 45, revenue: 20250 }
])

// Top customers
const topCustomers = ref([
  { id: 1, name: 'Jean Dupont', company: 'Château Margaux', orders: 12, revenue: 45000 },
  { id: 2, name: 'Sarah Johnson', company: 'Luxury Wines Ltd.', orders: 15, revenue: 67000 },
  { id: 3, name: 'Maria Rodriguez', company: 'Wine Imports Inc.', orders: 8, revenue: 32000 },
  { id: 4, name: 'Pierre Dubois', company: null, orders: 3, revenue: 2800 },
  { id: 5, name: 'Hans Mueller', company: 'Weingut Mueller', orders: 2, revenue: 1700 }
])

// Sales by region
const salesByRegion = ref([
  { name: 'France', sales: 1247, percentage: 45 },
  { name: 'United States', sales: 856, percentage: 31 },
  { name: 'United Kingdom', sales: 423, percentage: 15 },
  { name: 'Germany', sales: 234, percentage: 8 },
  { name: 'Other', sales: 87, percentage: 3 }
])

// Methods
const refreshStats = () => {
  // TODO: Implement actual API call to refresh statistics
  console.log('Refreshing statistics...')
}

const exportReport = () => {
  // TODO: Implement export functionality
  console.log('Exporting report...')
}

const formatNumber = (num) => {
  return num.toLocaleString('en-US')
}
</script>

<style scoped>
.statistics {
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
  align-items: center;
}

.time-select {
  padding: 0.75rem;
  border: 2px solid #e7e5e4;
  border-radius: 8px;
  background: white;
  color: #1c1917;
  font-size: 0.875rem;
  min-width: 150px;
}

.time-select:focus {
  outline: none;
  border-color: #dc2626;
}

/* Key Metrics */
.key-metrics {
  margin-bottom: 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.metric-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #57534e;
  margin: 0;
}

.metric-trend {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.metric-trend.positive {
  background: #f0fdf4;
  color: #16a34a;
}

.metric-trend.negative {
  background: #fef2f2;
  color: #dc2626;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', serif;
}

.metric-comparison {
  color: #78716c;
  font-size: 0.875rem;
}

/* Charts Section */
.charts-section {
  margin-bottom: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.chart-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1c1917;
  margin: 0;
}

.chart-legend {
  display: flex;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #57534e;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.current {
  background: #dc2626;
}

.legend-color.previous {
  background: #e7e5e4;
}

/* Chart Placeholder */
.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 200px;
  margin-bottom: 1rem;
}

.chart-bar {
  width: 40px;
  background: #dc2626;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: all 0.3s ease;
}

.chart-bar:hover {
  background: #b91c1c;
}

.bar-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #1c1917;
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 10;
}

.chart-bar:hover .bar-tooltip {
  opacity: 1;
}

.chart-labels {
  display: flex;
  gap: 1rem;
}

.chart-label {
  width: 40px;
  text-align: center;
  font-size: 0.75rem;
  color: #57534e;
}

/* Pie Chart */
.pie-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    #10b981 0deg 126deg,
    #3b82f6 126deg 216deg,
    #f59e0b 216deg 288deg,
    #ef4444 288deg 342deg,
    #6b7280 342deg 360deg
  );
  position: relative;
  margin: 0 auto;
}

.pie-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.segment-label {
  position: absolute;
  font-size: 0.75rem;
  font-weight: 500;
  color: #1c1917;
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Top Lists */
.top-lists {
  margin-bottom: 2rem;
}

.lists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.list-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.list-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1c1917;
  margin: 0;
}

.view-all-link {
  color: #dc2626;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
}

.view-all-link:hover {
  text-decoration: underline;
}

.list-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.item-rank {
  width: 32px;
  height: 32px;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: 600;
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.item-category,
.item-company {
  color: #57534e;
  margin: 0;
  font-size: 0.75rem;
}

.item-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.item-sales,
.item-orders {
  color: #57534e;
  font-size: 0.75rem;
}

.item-revenue {
  font-weight: 600;
  color: #16a34a;
  font-size: 0.875rem;
}

/* Geographic Stats */
.geographic-stats {
  margin-bottom: 2rem;
}

.geo-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.geo-header {
  margin-bottom: 1.5rem;
}

.geo-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1c1917;
  margin: 0;
}

.geo-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.geo-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.geo-info {
  display: flex;
  flex-direction: column;
  min-width: 120px;
}

.geo-name {
  font-weight: 500;
  color: #1c1917;
  font-size: 0.875rem;
}

.geo-sales {
  color: #57534e;
  font-size: 0.75rem;
}

.geo-bar {
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.geo-bar-fill {
  height: 100%;
  background: #dc2626;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.geo-percentage {
  min-width: 40px;
  text-align: right;
  font-weight: 600;
  color: #1c1917;
  font-size: 0.875rem;
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
    flex-wrap: wrap;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .lists-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .statistics {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-bars {
    gap: 0.5rem;
  }
  
  .chart-bar {
    width: 30px;
  }
  
  .chart-label {
    width: 30px;
    font-size: 0.625rem;
  }
}
</style>
