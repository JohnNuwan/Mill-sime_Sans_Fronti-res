<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">Admin Dashboard</h1>
        <div class="header-actions">
          <button class="btn btn--outline" @click="refreshStats">
            <span class="icon">🔄</span>
            Refresh
          </button>
          <button class="btn btn--primary" @click="logout">
            <span class="icon">🚪</span>
            Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Stats Overview -->
    <section class="stats-overview">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🍷</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalWines }}</h3>
            <p class="stat-label">Total Wines</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🛢️</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalBarrels }}</h3>
            <p class="stat-label">Total Barrels</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalCustomers }}</h3>
            <p class="stat-label">Total Customers</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalOrders }}</h3>
            <p class="stat-label">Total Orders</p>
          </div>
        </div>
      </div>
    </section>

                    <!-- Quick Actions -->
                <section class="quick-actions">
                  <h2 class="section-title">Quick Actions</h2>
                  <div class="actions-grid">
                    <NuxtLink to="/admin/wines" class="action-card">
                      <div class="action-icon">🍷</div>
                      <h3>Manage Wines</h3>
                      <p>View and manage wine catalog</p>
                    </NuxtLink>

                    <NuxtLink to="/admin/barrels" class="action-card">
                      <div class="action-icon">🛢️</div>
                      <h3>Manage Barrels</h3>
                      <p>View and manage barrel inventory</p>
                    </NuxtLink>

                    <NuxtLink to="/admin/customers" class="action-card">
                      <div class="action-icon">👥</div>
                      <h3>Manage Customers</h3>
                      <p>View and manage customer accounts</p>
                    </NuxtLink>

                    <NuxtLink to="/admin/orders" class="action-card">
                      <div class="action-icon">📋</div>
                      <h3>Manage Orders</h3>
                      <p>Monitor and manage orders</p>
                    </NuxtLink>

                    <NuxtLink to="/admin/statistics" class="action-card">
                      <div class="action-icon">📊</div>
                      <h3>View Statistics</h3>
                      <p>Business analytics and reports</p>
                    </NuxtLink>

                    <NuxtLink to="/admin/wines/add" class="action-card">
                      <div class="action-icon">➕</div>
                      <h3>Add New Wine</h3>
                      <p>Add a new wine to the catalog</p>
                    </NuxtLink>
                  </div>
                </section>

    <!-- Recent Activity -->
    <section class="recent-activity">
      <h2 class="section-title">Recent Activity</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <p class="activity-text">{{ activity.text }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Admin Dashboard - Millésime Sans Frontières',
  description: 'Administrative dashboard for managing wines, barrels, customers, and orders.'
})

// Mock data - replace with actual API calls
const stats = ref({
  totalWines: 156,
  totalBarrels: 89,
  totalCustomers: 342,
  totalOrders: 127
})

const recentActivities = ref([
  {
    id: 1,
    icon: '🍷',
    text: 'New wine "Château Margaux 2018" added to catalog',
    time: '2 hours ago'
  },
  {
    id: 2,
    icon: '🛢️',
    text: 'Barrel inventory updated - 15 new French oak barrels',
    time: '4 hours ago'
  },
  {
    id: 3,
    icon: '👥',
    text: 'New customer registration: John Smith',
    time: '6 hours ago'
  },
  {
    id: 4,
    icon: '📋',
    text: 'Order #1234 completed - $2,450',
    time: '1 day ago'
  },
  {
    id: 5,
    icon: '🍷',
    text: 'Wine "Dom Pérignon 2012" stock updated',
    time: '1 day ago'
  }
])

const refreshStats = () => {
  // TODO: Implement actual API call to refresh statistics
  console.log('Refreshing statistics...')
}

const logout = () => {
  // TODO: Implement logout logic
  console.log('Logging out...')
  navigateTo('/admin/login')
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: #f8fafc;
  padding: 2rem;
}

/* Dashboard Header */
.dashboard-header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1c1917;
  font-family: 'Playfair Display', serif;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Stats Overview */
.stats-overview {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 3rem;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fef3c7;
  border-radius: 50%;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1c1917;
  margin: 0;
  line-height: 1;
}

.stat-label {
  color: #57534e;
  font-size: 1rem;
  margin: 0;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1c1917;
  margin-bottom: 1.5rem;
  font-family: 'Playfair Display', serif;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1c1917;
  margin-bottom: 0.5rem;
}

.action-card p {
  color: #57534e;
  margin: 0;
}

/* Recent Activity */
.recent-activity {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background: #f8fafc;
}

.activity-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #1c1917;
  margin: 0 0 0.25rem 0;
  font-weight: 500;
}

.activity-time {
  color: #78716c;
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
}

.icon {
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .dashboard-title {
    font-size: 2rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 1.5rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
}
</style>
