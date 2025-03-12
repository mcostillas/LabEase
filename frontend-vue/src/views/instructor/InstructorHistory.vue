<template>
  <div class="dashboard-container">
    <nav class="sidenav" :class="{ expanded: isNavExpanded }">
      <div class="nav-top">
        <div class="logo" @click="toggleNav">
          <img src="../../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
          <span class="logo-text">LabEase</span>
        </div>
        <div class="nav-links">
          <router-link to="/instructor" class="nav-item" title="Dashboard">
            <i class="mdi mdi-view-dashboard"></i>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/instructor/notifications" class="nav-item" title="Notifications">
            <i class="mdi mdi-bell"></i>
            <span>Notifications</span>
          </router-link>
          <router-link to="/instructor/schedule" class="nav-item" title="Schedule">
            <i class="mdi mdi-calendar"></i>
            <span>Schedule</span>
          </router-link>
          <router-link to="/instructor/history" class="nav-item active" title="History">
            <i class="mdi mdi-history"></i>
            <span>History</span>
          </router-link>
        </div>
      </div>
      <div class="nav-bottom">
        <router-link to="/instructor/settings" class="nav-item" title="Settings">
          <i class="mdi mdi-cog"></i>
          <span>Settings</span>
        </router-link>
        <button @click="handleLogout" class="nav-item logout" title="Logout">
          <i class="mdi mdi-logout"></i>
          <span>Logout</span>
        </button>
      </div>
    </nav>

    <main class="main-content">
      <div class="dashboard-header">
        <div class="header-content">
          <div class="welcome-section">
            <h1>History of Bookings</h1>
            <div class="header-date">
              <span>{{ currentDate }}</span>
              <span class="date-separator">•</span>
              <span>{{ currentTime }}</span>
            </div>
          </div>
          <div class="user-section">
            <div class="user-dropdown" @click="toggleUserMenu">
              <div class="user-info">
                <div class="user-avatar">
                  <img :src="userData?.avatar || '/default-avatar.png'" alt="User Avatar">
                </div>
                <div class="user-details">
                  <span class="user-name">{{ userData?.name || 'Instructor' }}</span>
                  <span class="user-role">{{ userData?.role || 'Instructor' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bookings-container">
        <div class="filters-section">
          <div class="search-bar">
            <i class="mdi mdi-magnify"></i>
            <input type="text" v-model="searchQuery" placeholder="Search bookings...">
          </div>
          <div class="filter-options">
            <div class="date-range">
              <input type="date" v-model="startDate">
              <span>to</span>
              <input type="date" v-model="endDate">
            </div>
            <select v-model="selectedLab">
              <option value="all">All Laboratories</option>
              <option v-for="lab in labs" :key="lab.id" :value="lab.id">
                {{ lab.name }}
              </option>
            </select>
            <select v-model="statusFilter">
              <option value="all">All Status</option>
              <option value="approved">Approved</option>
              <option value="pending">Pending</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>

        <div class="bookings-grid">
          <div v-for="booking in bookings" :key="booking.id" 
               :class="['booking-card', booking.status.toLowerCase()]">
            <div class="booking-header">
              <div class="booking-date">
                <i class="mdi mdi-calendar"></i>
                <span>{{ booking.date }}</span>
              </div>
              <div class="booking-time">
                <i class="mdi mdi-clock-outline"></i>
                <span>{{ booking.time }}</span>
              </div>
            </div>
            <div class="booking-content">
              <h3>{{ booking.lab }}</h3>
              <p class="booking-purpose">{{ booking.purpose }}</p>
              <div class="student-info">
                <img :src="booking.studentAvatar" :alt="booking.studentName">
                <div>
                  <span class="student-name">{{ booking.studentName }}</span>
                  <span class="student-id">{{ booking.studentId }}</span>
                </div>
              </div>
            </div>
            <div class="booking-footer">
              <span :class="['status-badge', booking.status.toLowerCase()]">
                {{ booking.status }}
              </span>
              <button class="view-details-btn" @click="viewDetails(booking)">
                View Details
              </button>
            </div>
          </div>
        </div>

        <div v-if="bookings.length === 0" class="empty-state">
          <i class="mdi mdi-calendar-blank"></i>
          <p>No bookings found</p>
        </div>

        <div class="pagination">
          <button :disabled="currentPage === 1" @click="bookingsStore.prevPage()">
            <i class="mdi mdi-chevron-left"></i>
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="bookingsStore.nextPage()">
            <i class="mdi mdi-chevron-right"></i>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useBookingsStore } from '../../stores/bookings'
import { format } from 'date-fns'

const router = useRouter()
const authStore = useAuthStore()
const bookingsStore = useBookingsStore()
const userData = ref(authStore.userData)

// Navigation state
const isNavExpanded = ref(false)
const toggleNav = () => {
  isNavExpanded.value = !isNavExpanded.value
}

// Current date and time
const now = ref(new Date('2025-03-12T23:15:02+08:00'))
const currentDate = computed(() => format(now.value, 'MMMM d, yyyy'))
const currentTime = computed(() => format(now.value, 'EEEE, h:mm a'))

// Filters state
const searchQuery = ref('')
const startDate = ref('')
const endDate = ref('')
const selectedLab = ref('all')
const statusFilter = ref('all')
const currentPage = computed(() => bookingsStore.currentPage)
const totalPages = computed(() => bookingsStore.totalPages)

// Computed properties
const labs = computed(() => bookingsStore.labs)
const bookings = computed(() => bookingsStore.bookings)
const loading = computed(() => bookingsStore.loading)

// Methods
const handleSearch = () => {
  bookingsStore.updateFilters({
    search: searchQuery.value,
    startDate: startDate.value,
    endDate: endDate.value,
    selectedLab: selectedLab.value,
    status: statusFilter.value
  })
}

const resetFilters = () => {
  searchQuery.value = ''
  startDate.value = ''
  endDate.value = ''
  selectedLab.value = 'all'
  statusFilter.value = 'all'
  bookingsStore.resetFilters()
}

const viewDetails = (booking) => {
  // TODO: Implement booking details view
  console.log('Viewing booking:', booking)
}

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}

// Fetch initial data
onMounted(async () => {
  await Promise.all([
    bookingsStore.fetchBookings(),
    bookingsStore.fetchLabs()
  ])
})
</script>

<style scoped>
/* Global Styles */
:root {
  --primary-color: #DD3859;
  --text-color: #333;
  --border-radius: 8px;
  --transition: all 0.3s ease;
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

/* Sidebar Navigation */
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

.sidenav.expanded .logo-text {
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
}

.sidenav.expanded .nav-item span {
  opacity: 1;
}

.nav-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 16px;
}

.nav-item.logout {
  background-color: #DD3859;
  color: white;
  margin-top: 8px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.nav-item.logout:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 72px;
  padding: 2rem;
  transition: margin-left 0.3s ease;
}

.sidenav.expanded + .main-content {
  margin-left: 240px;
}

/* Dashboard Header */
.dashboard-header {
  background-color: #FFFFFF;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  margin-bottom: 24px;
  padding: 24px;
  position: relative;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.welcome-section h1 {
  color: #99183A;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.header-date {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748B;
  font-size: 14px;
}

.date-separator {
  color: #DD3859;
  font-weight: 600;
}

.user-section {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
}

.user-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: #1E293B;
}

.user-role {
  font-size: 14px;
  color: #64748B;
}

/* Bookings Container */
.bookings-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.filters-section {
  margin-bottom: 24px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #F8F9FA;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.search-bar i {
  color: #64748B;
  margin-right: 12px;
}

.search-bar input {
  border: none;
  background: none;
  outline: none;
  width: 100%;
  font-size: 14px;
}

.filter-options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-range input {
  padding: 8px;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
}

.filter-options select {
  padding: 8px;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  background: white;
  min-width: 150px;
}

.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.booking-card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 16px;
  transition: transform 0.2s;
}

.booking-card:hover {
  transform: translateY(-2px);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  color: #64748B;
  font-size: 14px;
}

.booking-date, .booking-time {
  display: flex;
  align-items: center;
  gap: 8px;
}

.booking-content h3 {
  color: #1E293B;
  margin-bottom: 8px;
}

.booking-purpose {
  color: #64748B;
  font-size: 14px;
  margin-bottom: 16px;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.student-info img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.student-info div {
  display: flex;
  flex-direction: column;
}

.student-name {
  font-weight: 500;
  color: #1E293B;
}

.student-id {
  font-size: 12px;
  color: #64748B;
}

.booking-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.approved {
  background: #E8F5E9;
  color: #4CAF50;
}

.status-badge.pending {
  background: #FFF3E0;
  color: #F59E0B;
}

.status-badge.cancelled {
  background: #FFEBEE;
  color: #F44336;
}

.view-details-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: #F8F9FA;
  color: #64748B;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-details-btn:hover {
  background: #E2E8F0;
  color: #1E293B;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #64748B;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.pagination button {
  width: 36px;
  height: 36px;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  background: white;
  color: #64748B;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:not(:disabled):hover {
  background: #F8F9FA;
  color: #1E293B;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 1rem;
  }

  .filter-options {
    flex-direction: column;
  }

  .bookings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
