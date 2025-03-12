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
          <router-link to="/instructor/notifications" class="nav-item active" title="Notifications">
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
            <h1>Notifications</h1>
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

      <div class="notifications-container">
        <div class="notifications-header">
          <div class="filter-buttons">
            <button 
              v-for="filter in filters" 
              :key="filter.value"
              :class="['filter-btn', { active: currentFilter === filter.value }]"
              @click="currentFilter = filter.value"
            >
              {{ filter.label }}
              <span v-if="getFilterCount(filter.value)" class="count-badge">
                {{ getFilterCount(filter.value) }}
              </span>
            </button>
          </div>
          <button class="mark-all-read" @click="markAllAsRead" v-if="hasUnread">
            <i class="mdi mdi-check-all"></i>
            Mark all as read
          </button>
        </div>

        <div class="notifications-list" v-if="filteredNotifications.length">
          <div 
            v-for="notification in filteredNotifications" 
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.read }"
          >
            <div class="notification-icon" :class="notification.type">
              <i :class="getNotificationIcon(notification.type)"></i>
            </div>
            <div class="notification-content">
              <div class="notification-header">
                <h3>{{ notification.title }}</h3>
                <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
              </div>
              <p class="notification-message">{{ notification.message }}</p>
              <div class="notification-actions" v-if="notification.actions">
                <button 
                  v-for="action in notification.actions" 
                  :key="action.label"
                  class="action-btn"
                  :class="action.type"
                  @click="handleAction(notification.id, action.type)"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="mdi mdi-bell-off"></i>
          <p>No notifications to display</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { format, formatDistanceToNow } from 'date-fns'

const router = useRouter()
const authStore = useAuthStore()

// Navigation state
const isNavExpanded = ref(false)
const toggleNav = () => {
  isNavExpanded.value = !isNavExpanded.value
}

// User data and time
const userData = ref(authStore.userData)
const now = ref(new Date('2025-03-13T00:10:03+08:00'))
const currentDate = computed(() => format(now.value, 'MMMM d, yyyy'))
const currentTime = computed(() => format(now.value, 'EEEE, h:mm a'))

// Notification filters
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'Bookings', value: 'booking' },
  { label: 'System', value: 'system' }
]
const currentFilter = ref('all')

// Mock notifications data
const notifications = ref([
  {
    id: 1,
    type: 'booking',
    title: 'New Lab Booking Request',
    message: 'John Smith has requested to book the Programming Lab for tomorrow at 10:00 AM',
    timestamp: new Date('2025-03-12T23:45:00+08:00'),
    read: false,
    actions: [
      { label: 'Approve', type: 'approve' },
      { label: 'Reject', type: 'reject' }
    ]
  },
  {
    id: 2,
    type: 'system',
    title: 'System Maintenance',
    message: 'The lab booking system will undergo maintenance on March 15th from 2 AM to 4 AM',
    timestamp: new Date('2025-03-12T20:30:00+08:00'),
    read: true
  },
  {
    id: 3,
    type: 'booking',
    title: 'Booking Cancellation',
    message: 'Emma Wilson has cancelled their booking for Digital Electronics Lab today at 2:30 PM',
    timestamp: new Date('2025-03-12T14:15:00+08:00'),
    read: false
  }
])

// Computed
const filteredNotifications = computed(() => {
  if (currentFilter.value === 'all') return notifications.value
  if (currentFilter.value === 'unread') return notifications.value.filter(n => !n.read)
  return notifications.value.filter(n => n.type === currentFilter.value)
})

const hasUnread = computed(() => notifications.value.some(n => !n.read))

// Methods
const getFilterCount = (filter) => {
  if (filter === 'all') return notifications.value.length
  if (filter === 'unread') return notifications.value.filter(n => !n.read).length
  return notifications.value.filter(n => n.type === filter).length
}

const getNotificationIcon = (type) => {
  const icons = {
    booking: 'mdi mdi-calendar-clock',
    system: 'mdi mdi-information',
    warning: 'mdi mdi-alert',
    success: 'mdi mdi-check-circle'
  }
  return icons[type] || 'mdi mdi-bell'
}

const formatTime = (timestamp) => {
  return formatDistanceToNow(timestamp, { addSuffix: true })
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

const handleAction = (notificationId, actionType) => {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true
    // TODO: Implement actual API call for handling actions
    console.log(`Handling ${actionType} for notification ${notificationId}`)
  }
}

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
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
  font-weight: 500;
  color: #1E293B;
}

.user-role {
  font-size: 14px;
  color: #64748B;
}

.notifications-container {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 1.5rem;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  background: white;
  color: #64748B;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-btn:hover {
  border-color: #FF69B4;
  color: #FF69B4;
}

.filter-btn.active {
  background: #FF69B4;
  color: white;
  border-color: #FF69B4;
}

.count-badge {
  background: #E2E8F0;
  color: #64748B;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 12px;
}

.active .count-badge {
  background: white;
  color: #FF69B4;
}

.mark-all-read {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #FF69B4;
  cursor: pointer;
  font-size: 14px;
}

.mark-all-read:hover {
  text-decoration: underline;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.notification-item:hover {
  transform: translateY(-2px);
}

.notification-item.unread {
  background: #F8FAFC;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.booking {
  background: #E8F5E9;
  color: #4CAF50;
}

.notification-icon.system {
  background: #E3F2FD;
  color: #1976D2;
}

.notification-icon.warning {
  background: #FFF3E0;
  color: #FF9800;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.notification-header h3 {
  font-size: 1rem;
  color: #1E293B;
  margin: 0;
}

.notification-time {
  font-size: 12px;
  color: #64748B;
}

.notification-message {
  color: #64748B;
  font-size: 14px;
  margin: 0;
  margin-bottom: 1rem;
}

.notification-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.action-btn:hover {
  opacity: 0.9;
}

.action-btn.approve {
  background: #4CAF50;
  color: white;
}

.action-btn.reject {
  background: #F44336;
  color: white;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #64748B;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1rem;
  margin: 0;
}
</style>
