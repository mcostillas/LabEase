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
          <router-link to="/instructor/schedule" class="nav-item active" title="Schedule">
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
            <h1>Schedule</h1>
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

      <div class="schedule-container">
        <div class="schedule-header">
          <div class="date-navigation">
            <button @click="previousWeek" class="nav-btn">
              <i class="mdi mdi-chevron-left"></i>
            </button>
            <h2>{{ weekRange }}</h2>
            <button @click="nextWeek" class="nav-btn">
              <i class="mdi mdi-chevron-right"></i>
            </button>
          </div>
          <div class="schedule-actions">
            <button class="action-btn" @click="exportSchedule">
              <i class="mdi mdi-download"></i>
              Export
            </button>
            <button class="action-btn primary" @click="createBooking">
              <i class="mdi mdi-plus"></i>
              New Booking
            </button>
          </div>
        </div>

        <div class="schedule-grid">
          <div class="time-column">
            <div class="time-header">Time</div>
            <div v-for="time in timeSlots" :key="time" class="time-slot">
              {{ time }}
            </div>
          </div>
          <div v-for="day in weekDays" :key="day.date" class="day-column">
            <div class="day-header">
              <span class="day-name">{{ day.name }}</span>
              <span class="day-date">{{ day.date }}</span>
            </div>
            <div v-for="time in timeSlots" :key="time" class="schedule-cell">
              <div 
                v-for="booking in getBookingsForTimeAndDay(time, day.date)" 
                :key="booking.id"
                :class="['booking-item', booking.status.toLowerCase()]"
                @click="viewBookingDetails(booking)"
              >
                <div class="booking-time">{{ booking.startTime }} - {{ booking.endTime }}</div>
                <div class="booking-title">{{ booking.title }}</div>
                <div class="booking-details">
                  <span class="lab-name">{{ booking.lab }}</span>
                  <span class="student-count">
                    <i class="mdi mdi-account-group"></i>
                    {{ booking.studentCount }}
                  </span>
                </div>
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
import { format, addDays, startOfWeek, endOfWeek } from 'date-fns'

const router = useRouter()
const authStore = useAuthStore()
const userData = ref(authStore.userData)

// Navigation state
const isNavExpanded = ref(false)
const toggleNav = () => {
  isNavExpanded.value = !isNavExpanded.value
}

// Current date and time
const now = ref(new Date())
const currentDate = computed(() => format(now.value, 'MMMM d, yyyy'))
const currentTime = computed(() => format(now.value, 'EEEE, h:mm a'))

// Schedule state
const selectedWeekStart = ref(startOfWeek(new Date()))
const timeSlots = [
  '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
  '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'
]

const weekDays = computed(() => {
  const days = []
  for (let i = 0; i < 7; i++) {
    const date = addDays(selectedWeekStart.value, i)
    days.push({
      name: format(date, 'EEE'),
      date: format(date, 'MMM d'),
      fullDate: date
    })
  }
  return days
})

const weekRange = computed(() => {
  const start = format(selectedWeekStart.value, 'MMM d')
  const end = format(endOfWeek(selectedWeekStart.value), 'MMM d, yyyy')
  return `${start} - ${end}`
})

// Mock bookings data
const bookings = ref([
  {
    id: 1,
    date: '2025-03-12',
    startTime: '10:00 AM',
    endTime: '12:00 PM',
    title: 'Chemistry Lab',
    lab: 'Chemistry Lab 1',
    studentCount: 25,
    status: 'upcoming'
  },
  {
    id: 2,
    date: '2025-03-12',
    startTime: '2:00 PM',
    endTime: '4:00 PM',
    title: 'Physics Lab',
    lab: 'Physics Lab 1',
    studentCount: 20,
    status: 'ongoing'
  }
])

// Methods
const getBookingsForTimeAndDay = (time, date) => {
  return bookings.value.filter(booking => 
    booking.date === date && booking.startTime === time
  )
}

const previousWeek = () => {
  selectedWeekStart.value = addDays(selectedWeekStart.value, -7)
}

const nextWeek = () => {
  selectedWeekStart.value = addDays(selectedWeekStart.value, 7)
}

const exportSchedule = () => {
  // TODO: Implement export functionality
  console.log('Exporting schedule...')
}

const createBooking = () => {
  // TODO: Implement booking creation
  console.log('Creating new booking...')
}

const viewBookingDetails = (booking) => {
  // TODO: Implement booking details view
  console.log('Viewing booking:', booking)
}

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}

// Update time every minute
onMounted(() => {
  setInterval(() => {
    now.value = new Date()
  }, 60000)
})
</script>

<style scoped>
/* Global Styles */
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
  border-radius: 12px;
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
  color: #DD3859;
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
  transition: background-color 0.2s;
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

/* Schedule Styles */
.schedule-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.date-navigation {
  display: flex;
  align-items: center;
  gap: 16px;
}

.date-navigation h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1E293B;
}

.nav-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  background: white;
  color: #64748B;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: #F8F9FA;
  color: #1E293B;
}

.schedule-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  background: white;
  color: #64748B;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #F8F9FA;
  color: #1E293B;
}

.action-btn.primary {
  background: #DD3859;
  color: white;
  border: none;
}

.action-btn.primary:hover {
  background: #C42B4C;
}

.schedule-grid {
  display: grid;
  grid-template-columns: 100px repeat(7, 1fr);
  gap: 1px;
  background: #E2E8F0;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  overflow: hidden;
}

.time-column, .day-column {
  background: white;
}

.time-header, .day-header {
  padding: 16px;
  background: #F8F9FA;
  border-bottom: 1px solid #E2E8F0;
  text-align: center;
}

.day-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.day-name {
  font-weight: 600;
  color: #1E293B;
}

.day-date {
  font-size: 14px;
  color: #64748B;
}

.time-slot {
  height: 60px;
  padding: 8px;
  border-bottom: 1px solid #E2E8F0;
  color: #64748B;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.schedule-cell {
  height: 60px;
  padding: 4px;
  border-bottom: 1px solid #E2E8F0;
  position: relative;
}

.booking-item {
  position: absolute;
  left: 4px;
  right: 4px;
  padding: 8px;
  border-radius: 6px;
  background: #F8F9FA;
  cursor: pointer;
  transition: transform 0.2s;
}

.booking-item:hover {
  transform: scale(1.02);
}

.booking-item.upcoming {
  background: #E3F2FD;
  color: #2196F3;
}

.booking-item.ongoing {
  background: #E8F5E9;
  color: #4CAF50;
}

.booking-time {
  font-size: 12px;
  margin-bottom: 4px;
}

.booking-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.booking-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.student-count {
  display: flex;
  align-items: center;
  gap: 4px;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 1rem;
  }

  .schedule-grid {
    grid-template-columns: 80px repeat(7, 1fr);
    font-size: 12px;
  }

  .booking-item {
    padding: 4px;
  }

  .booking-details {
    display: none;
  }
}
</style>
