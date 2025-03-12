<template>
  <div class="dashboard-container">
    <nav class="sidenav" :class="{ expanded: isNavExpanded }">
      <div class="nav-top">
        <div class="logo" @click="toggleNav">
          <img src="../../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
          <span class="logo-text">LabEase</span>
        </div>
        <div class="nav-links">
          <router-link to="/admin" class="nav-item active" title="Dashboard">
            <i class="mdi mdi-view-dashboard"></i>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/admin/log-book" class="nav-item" title="Log Book">
            <i class="mdi mdi-book-open"></i>
            <span>Log Book</span>
          </router-link>
          <router-link to="/admin/notifications" class="nav-item" title="Notifications">
            <i class="mdi mdi-bell"></i>
            <span>Notifications</span>
            <span v-if="unreadNotifications" class="notification-badge">{{ unreadNotifications }}</span>
          </router-link>
        </div>
      </div>
      <div class="nav-bottom">
        <button @click="handleLogout" class="nav-item logout" title="Logout">
          <i class="mdi mdi-logout"></i>
          <span>Logout</span>
        </button>
      </div>
    </nav>

    <main class="main-content" :class="{ 'nav-expanded': isNavExpanded }">
      <header class="dashboard-header">
        <div class="header-content">
          <div class="welcome-section">
            <h1>Welcome, {{ userData?.name || 'Admin' }}</h1>
            <div class="header-date">
              <span>{{ currentDate }}</span>
              <span class="date-separator">•</span>
              <span>{{ currentTime }}</span>
            </div>
          </div>
          <div class="user-section">
            <div class="search-bar">
              <i class="mdi mdi-magnify"></i>
              <input type="text" v-model="searchQuery" placeholder="Search...">
            </div>
            <div class="user-dropdown" @click="toggleUserMenu">
              <div class="user-info">
                <div class="user-avatar">
                  <img :src="userData?.avatar || '/default-avatar.png'" alt="User Avatar">
                </div>
                <div class="user-details">
                  <span class="user-name">{{ userData?.name || 'Admin' }}</span>
                  <span class="user-role">Administrator</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div class="dashboard-grid">
        <div class="dashboard-card">
          <div class="card-header">
            <h3>Lab Usage Statistics</h3>
            <select v-model="selectedLab">
              <option value="all">All Labs</option>
              <option v-for="lab in labs" :key="lab.id" :value="lab.id">{{ lab.name }}</option>
            </select>
          </div>
          <div class="chart-container">
            <!-- Add chart component here -->
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-header">
            <h3>Recent Bookings</h3>
            <button class="view-all">View All</button>
          </div>
          <div class="bookings-list">
            <div v-for="booking in recentBookings" :key="booking.id" class="booking-item">
              <div class="booking-info">
                <h4>{{ booking.labName }}</h4>
                <p>{{ booking.date }} | {{ booking.time }}</p>
                <p class="booking-user">{{ booking.userName }}</p>
              </div>
              <div class="booking-status" :class="booking.status.toLowerCase()">
                {{ booking.status }}
              </div>
            </div>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-header">
            <h3>System Status</h3>
          </div>
          <div class="system-status">
            <div v-for="system in systemStatus" :key="system.id" class="status-item">
              <i :class="['mdi', system.icon]" :style="{ color: system.color }"></i>
              <div class="status-info">
                <h4>{{ system.name }}</h4>
                <p>{{ system.status }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { format } from 'date-fns'

const router = useRouter()
const authStore = useAuthStore()

// Navigation state
const isNavExpanded = ref(false)
const toggleNav = () => {
  isNavExpanded.value = !isNavExpanded.value
}

// User data and time
const now = ref(new Date())
const currentDate = computed(() => format(now.value, 'MMMM d, yyyy'))
const currentTime = computed(() => format(now.value, 'EEEE, h:mm a'))

// Dashboard state
const searchQuery = ref('')
const selectedLab = ref('all')
const showNotifications = ref(false)
const unreadNotifications = ref(3)
const userData = ref(null)
const showUserMenu = ref(false)

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// Mock data
const labs = ref([
  { id: 1, name: 'Chemistry Lab 1' },
  { id: 2, name: 'Physics Lab 1' },
  { id: 3, name: 'Biology Lab 1' },
])

const recentBookings = ref([
  {
    id: 1,
    labName: 'Chemistry Lab 1',
    date: '2025-03-12',
    time: '10:00 - 12:00',
    userName: 'John Doe',
    status: 'Approved'
  },
  {
    id: 2,
    labName: 'Physics Lab 1',
    date: '2025-03-12',
    time: '13:00 - 15:00',
    userName: 'Jane Smith',
    status: 'Pending'
  },
])

const systemStatus = ref([
  {
    id: 1,
    name: 'RFID System',
    status: 'Operational',
    icon: 'mdi-check-circle',
    color: '#4CAF50'
  },
  {
    id: 2,
    name: 'Booking System',
    status: 'Operational',
    icon: 'mdi-check-circle',
    color: '#4CAF50'
  },
  {
    id: 3,
    name: 'Notification System',
    status: 'Operational',
    icon: 'mdi-check-circle',
    color: '#4CAF50'
  }
])

onMounted(() => {
  // Load user data
  userData.value = authStore.userData
})

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
/* Global Styles */
:root {
  --primary-color: #DD3859;
  --text-color: #333;
  --border-radius: 8px;
  --transition: all 0.3s ease;
  --heading-color: #1E293B;
  --text-secondary: #64748B;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

/* Dashboard Layout */
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.sidenav {
  background-color: #DD3859;
  width: 72px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  padding: 24px 12px;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow-x: hidden;
  z-index: 1000;
}

.sidenav.expanded {
  width: 240px;
}

.nav-top {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.nav-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 0 4px;
}

.logo img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.logo-text {
  color: white;
  font-size: 20px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.3s ease;
  white-space: nowrap;
}

.expanded .logo-text {
  opacity: 1;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  white-space: nowrap;
  cursor: pointer;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background-color: white;
  color: #DD3859;
}

.nav-item i {
  font-size: 24px;
}

.nav-item span {
  font-size: 16px;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: inherit;
}

.sidenav.expanded .nav-item span {
  opacity: 1;
}

.nav-item .notification-badge {
  background-color: white;
  color: #DD3859;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
}

.main-content {
  flex: 1;
  padding: 2rem;
  margin-left: 72px;
  transition: margin-left 0.3s ease;
  width: calc(100% - 72px);
  min-height: 100vh;
  background-color: #F8FAFC;
  color: #333;
}

.expanded + .main-content {
  margin-left: 240px;
  width: calc(100% - 240px);
}

.dashboard-header {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  color: #333;
}

.welcome-section h1 {
  color: #1E293B;
  font-size: 24px;
  font-weight: 600;
}

.header-date {
  color: #64748B;
}

.stats-card {
  color: #333;
}

.stats-value {
  color: #1E293B;
  font-weight: 600;
}

.stats-label {
  color: #64748B;
}

.activity-item {
  color: #333;
}

.activity-time {
  color: #64748B;
}

.status-info p {
  color: #64748B;
}

.user-name {
  color: #1E293B;
  font-weight: 600;
}

.user-role {
  color: #64748B;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header select {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.booking-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background: #f5f5f5;
}

.booking-info h4 {
  margin: 0;
  color: #333;
}

.booking-info p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.booking-status {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
}

.booking-status.approved {
  background: #E8F5E9;
  color: #4CAF50;
}

.booking-status.pending {
  background: #FFF3E0;
  color: #FF9800;
}

.system-status {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-item i {
  font-size: 24px;
}

.status-info h4 {
  margin: 0;
  color: #333;
}

.status-info p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.view-all {
  padding: 6px 12px;
  border: none;
  background: #f5f5f5;
  border-radius: 6px;
  color: #FF69B4;
  font-weight: 500;
  cursor: pointer;
}

.view-all:hover {
  background: #fce4ec;
}
</style>
