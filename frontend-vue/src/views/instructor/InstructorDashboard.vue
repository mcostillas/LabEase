<template>
  <div class="dashboard-container">
    <nav class="sidenav" :class="{ expanded: isNavExpanded }">
      <div class="nav-top">
        <div class="logo" @click="toggleNav">
          <img src="../../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
          <span class="logo-text">LabEase</span>
        </div>
        <div class="nav-links">
          <router-link to="/instructor" class="nav-item active" title="Dashboard">
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
          <router-link to="/instructor/history" class="nav-item" title="History">
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
            <h1>Welcome, {{ userData?.name || 'Instructor' }}</h1>
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

      <div class="dashboard-grid">
        <div class="dashboard-card">
          <div class="card-header">
            <h3>Today's Schedule</h3>
            <router-link to="/instructor/schedule" class="view-all">View All</router-link>
          </div>
          <div class="schedule-list">
            <div v-for="session in todaySchedule" :key="session.id" class="schedule-item">
              <div class="time-slot">
                <i class="mdi mdi-clock-outline"></i>
                <span>{{ session.time }}</span>
              </div>
              <div class="session-info">
                <h4>{{ session.labName }}</h4>
                <p>{{ session.course }}</p>
                <div class="student-count">
                  <i class="mdi mdi-account-group"></i>
                  <span>{{ session.studentCount }} students</span>
                </div>
              </div>
              <div class="session-status" :class="session.status.toLowerCase()">
                {{ session.status }}
              </div>
            </div>
            <div v-if="todaySchedule.length === 0" class="empty-state">
              <i class="mdi mdi-calendar-blank"></i>
              <p>No sessions scheduled for today</p>
            </div>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-header">
            <h3>Recent Bookings</h3>
            <router-link to="/instructor/history" class="view-all">View All</router-link>
          </div>
          <div class="bookings-list">
            <div v-for="booking in recentBookings" :key="booking.id" class="booking-item">
              <div class="booking-info">
                <h4>{{ booking.studentName }}</h4>
                <p>{{ booking.labName }} | {{ booking.date }}</p>
                <p class="booking-purpose">{{ booking.purpose }}</p>
              </div>
              <div class="booking-actions">
                <button 
                  v-if="booking.status === 'Pending'"
                  class="action-btn approve" 
                  @click="handleBooking(booking.id, 'approve')"
                >
                  Approve
                </button>
                <button 
                  v-if="booking.status === 'Pending'"
                  class="action-btn reject" 
                  @click="handleBooking(booking.id, 'reject')"
                >
                  Reject
                </button>
                <span v-else class="status-badge" :class="booking.status.toLowerCase()">
                  {{ booking.status }}
                </span>
              </div>
            </div>
            <div v-if="recentBookings.length === 0" class="empty-state">
              <i class="mdi mdi-book-clock"></i>
              <p>No recent bookings</p>
            </div>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-header">
            <h3>Lab Usage Statistics</h3>
            <select v-model="statsTimeframe" class="timeframe-select">
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="semester">This Semester</option>
            </select>
          </div>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalSessions }}</div>
              <div class="stat-label">Total Sessions</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalStudents }}</div>
              <div class="stat-label">Total Students</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.avgDuration }}h</div>
              <div class="stat-label">Avg. Duration</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.utilization }}%</div>
              <div class="stat-label">Utilization</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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
const userData = ref(authStore.userData)
const now = ref(new Date('2025-03-12T23:46:59+08:00'))
const currentDate = computed(() => format(now.value, 'MMMM d, yyyy'))
const currentTime = computed(() => format(now.value, 'EEEE, h:mm a'))

// Dashboard state
const selectedLab = ref('all')
const showNotifications = ref(false)
const unreadNotifications = ref(2)
const statsTimeframe = ref('week')

// Mock data
const labs = ref([
  { id: 'lab1', name: 'Computer Networks Lab' },
  { id: 'lab2', name: 'Digital Electronics Lab' },
  { id: 'lab3', name: 'Microprocessors Lab' },
  { id: 'lab4', name: 'Programming Lab' }
])

const todaySchedule = ref([
  {
    id: 1,
    time: '9:00 AM - 11:00 AM',
    labName: 'Computer Networks Lab',
    course: 'CSE3011 - Computer Networks',
    studentCount: 25,
    status: 'Ongoing'
  },
  {
    id: 2,
    time: '2:00 PM - 4:00 PM',
    labName: 'Digital Electronics Lab',
    course: 'ECE2022 - Digital Systems',
    studentCount: 30,
    status: 'Upcoming'
  }
])

const recentBookings = ref([
  {
    id: 1,
    studentName: 'John Smith',
    labName: 'Programming Lab',
    date: 'Today, 10:00 AM',
    purpose: 'Project Work - Database Implementation',
    status: 'Pending'
  },
  {
    id: 2,
    studentName: 'Emma Wilson',
    labName: 'Computer Networks Lab',
    date: 'Today, 2:30 PM',
    purpose: 'Network Protocol Analysis',
    status: 'Approved'
  },
  {
    id: 3,
    studentName: 'Michael Brown',
    labName: 'Digital Electronics Lab',
    date: 'Yesterday, 3:00 PM',
    purpose: 'Circuit Design Practice',
    status: 'Rejected'
  }
])

const stats = ref({
  totalSessions: 42,
  totalStudents: 156,
  avgDuration: 2.5,
  utilization: 78
})

// Methods
const handleBooking = (bookingId, action) => {
  const booking = recentBookings.value.find(b => b.id === bookingId)
  if (booking) {
    booking.status = action === 'approve' ? 'Approved' : 'Rejected'
  }
}

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
}

.sidenav.expanded .nav-item span {
  opacity: 1;
}

.main-content {
  flex: 1;
  padding: 2rem;
  margin-left: 72px;
  transition: margin-left 0.3s ease;
  width: calc(100% - 72px);
  min-height: 100vh;
  background-color: #F8FAFC;
}

.expanded + .main-content {
  margin-left: 240px;
  width: calc(100% - 240px);
}

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

.user-info:hover {
  background-color: rgba(0, 0, 0, 0.05);
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
  font-weight: 600;
  color: #333;
}

.user-role {
  font-size: 0.8rem;
  color: #666;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.dashboard-card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.2s;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  font-size: 1.1rem;
  color: #333;
}

.view-all {
  color: #FF69B4;
  text-decoration: none;
  font-size: 0.9rem;
}

.schedule-list, .bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.schedule-item, .booking-item {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  border: 1px solid #E2E8F0;
  transition: transform 0.2s;
}

.schedule-item:hover, .booking-item:hover {
  transform: translateY(-2px);
}

.time-slot {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.session-info h4 {
  margin: 0.5rem 0;
  color: #1E293B;
  font-weight: 500;
}

.student-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.session-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.session-status.upcoming {
  background-color: #e3f2fd;
  color: #1976d2;
}

.session-status.ongoing {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.booking-info h4 {
  margin: 0;
  color: #1E293B;
  font-weight: 500;
}

.booking-purpose {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.booking-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.action-btn:hover {
  opacity: 0.9;
}

.action-btn.approve {
  background-color: #4caf50;
  color: white;
}

.action-btn.reject {
  background-color: #f44336;
  color: white;
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
  color: #FF9800;
}

.status-badge.rejected {
  background: #FFEBEE;
  color: #F44336;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #666;
}

.empty-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.timeframe-select {
  padding: 8px;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  font-size: 14px;
  color: #1E293B;
  background-color: white;
  min-width: 150px;
}
</style>
