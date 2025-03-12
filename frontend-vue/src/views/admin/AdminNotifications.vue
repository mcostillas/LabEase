<template>
  <div class="admin-layout">
    <nav class="sidenav" :class="{ expanded: isNavExpanded }">
      <div class="nav-top">
        <div class="logo" @click="toggleNav">
          <img src="../../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
          <span class="logo-text">LabEase</span>
        </div>
        <div class="nav-links">
          <router-link to="/admin" class="nav-item" title="Dashboard">
            <i class="mdi mdi-view-dashboard"></i>
            <span class="nav-item-text">Dashboard</span>
          </router-link>
          <router-link to="/admin/log-book" class="nav-item" title="Log Book">
            <i class="mdi mdi-book-open"></i>
            <span class="nav-item-text">Log Book</span>
          </router-link>
          <router-link to="/admin/notifications" class="nav-item active" title="Notifications">
            <i class="mdi mdi-bell"></i>
            <span class="nav-item-text">Notifications</span>
            <span v-if="unreadCount" class="notification-badge">{{ unreadCount }}</span>
          </router-link>
        </div>
      </div>
      <div class="nav-bottom">
        <button @click="handleLogout" class="nav-item logout" title="Logout">
          <i class="mdi mdi-logout"></i>
          <span class="nav-item-text">Logout</span>
        </button>
      </div>
    </nav>

    <main class="main-content">
      <header class="page-header">
        <div class="header-left">
          <h1>Notifications</h1>
          <div class="notification-filters">
            <button 
              v-for="filter in filters" 
              :key="filter.value"
              :class="['filter-btn', { active: activeFilter === filter.value }]"
              @click="activeFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="header-actions">
          <button class="mark-all-btn" @click="markAllAsRead">
            Mark all as read
          </button>
        </div>
      </header>

      <div class="notifications-container">
        <div v-for="notification in filteredNotifications" 
             :key="notification.id" 
             :class="['notification-card', { unread: !notification.read }]">
          <div class="notification-icon" :class="notification.type">
            <i :class="getNotificationIcon(notification.type)"></i>
          </div>
          <div class="notification-content">
            <div class="notification-header">
              <h3>{{ notification.title }}</h3>
              <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
            </div>
            <p class="notification-message">{{ notification.message }}</p>
            <div class="notification-actions">
              <template v-if="notification.type === 'request'">
                <button class="action-btn approve" @click="handleAction(notification, 'approve')">
                  <i class="mdi mdi-check"></i>
                  Approve
                </button>
                <button class="action-btn reject" @click="handleAction(notification, 'reject')">
                  <i class="mdi mdi-close"></i>
                  Reject
                </button>
              </template>
              <button v-if="!notification.read" class="action-btn" @click="markAsRead(notification)">
                Mark as read
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredNotifications.length === 0" class="empty-state">
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

// Notification filters
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'Requests', value: 'requests' },
  { label: 'Alerts', value: 'alerts' }
]

const activeFilter = ref('all')

// Mock notifications data
const notifications = ref([
  {
    id: 1,
    type: 'request',
    title: 'Lab Booking Request',
    message: 'John Doe requested to book Chemistry Lab 1 for tomorrow at 10:00 AM',
    timestamp: new Date('2025-03-12T10:00:00'),
    read: false
  },
  {
    id: 2,
    type: 'alert',
    title: 'System Alert',
    message: 'Physics Lab 1 RFID reader is offline',
    timestamp: new Date('2025-03-12T09:30:00'),
    read: false
  },
  {
    id: 3,
    type: 'info',
    title: 'Maintenance Scheduled',
    message: 'Biology Lab 1 will be under maintenance on Friday',
    timestamp: new Date('2025-03-12T09:00:00'),
    read: true
  }
])

// Computed
const filteredNotifications = computed(() => {
  let filtered = [...notifications.value]

  switch (activeFilter.value) {
    case 'unread':
      filtered = filtered.filter(n => !n.read)
      break
    case 'requests':
      filtered = filtered.filter(n => n.type === 'request')
      break
    case 'alerts':
      filtered = filtered.filter(n => n.type === 'alert')
      break
  }

  return filtered.sort((a, b) => b.timestamp - a.timestamp)
})

// Methods
const getNotificationIcon = (type) => {
  switch (type) {
    case 'request':
      return 'mdi mdi-calendar-clock'
    case 'alert':
      return 'mdi mdi-alert'
    case 'info':
      return 'mdi mdi-information'
    default:
      return 'mdi mdi-bell'
  }
}

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp

  if (diff < 60000) { // Less than 1 minute
    return 'Just now'
  } else if (diff < 3600000) { // Less than 1 hour
    const minutes = Math.floor(diff / 60000)
    return `${minutes}m ago`
  } else if (diff < 86400000) { // Less than 1 day
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  } else {
    return timestamp.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    })
  }
}

const markAsRead = (notification) => {
  notification.read = true
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
}

const handleAction = async (notification, action) => {
  try {
    // TODO: Implement actual API call
    console.log(`${action}ing notification:`, notification.id)
    notification.read = true
    // Add success message or update UI accordingly
  } catch (error) {
    console.error(`Error ${action}ing notification:`, error)
    // Handle error appropriately
  }
}

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
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

.admin-layout {
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

.nav-item .nav-item-text {
  font-size: 16px;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: inherit;
}

.nav-item .notification-badge {
  background-color: white;
  color: #DD3859;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
}

/* Main Content Styles */
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

.page-header {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  color: #333;
}

.page-header h1 {
  color: var(--heading-color);
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.notification-filters {
  display: flex;
  gap: 12px;
  color: #64748B;
}

.filter-btn {
  padding: 6px 16px;
  border: none;
  border-radius: 20px;
  background: #f5f5f5;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.filter-btn:hover,
.filter-btn.active {
  background: #FF69B4;
  color: white;
}

.mark-all-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #f5f5f5;
  color: #666;
  cursor: pointer;
  font-size: 14px;
}

.mark-all-btn:hover {
  background: #eee;
}

.notifications-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notification-card.unread {
  border-left: 4px solid #FF69B4;
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

.notification-icon.request {
  background: #E3F2FD;
  color: #2196F3;
}

.notification-icon.alert {
  background: #FFF3E0;
  color: #FF9800;
}

.notification-icon.info {
  background: #E8F5E9;
  color: #4CAF50;
}

.notification-icon i {
  font-size: 24px;
}

.notification-content {
  flex: 1;
  color: var(--text-color);
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.notification-time {
  font-size: 14px;
  color: var(--text-secondary);
}

.notification-message {
  margin: 0 0 16px;
  color: #666;
  line-height: 1.5;
}

.notification-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  background: #f5f5f5;
  color: #666;
}

.action-btn i {
  font-size: 18px;
}

.action-btn.approve {
  background: #E8F5E9;
  color: #4CAF50;
}

.action-btn.reject {
  background: #FFEBEE;
  color: #F44336;
}

.action-btn:hover {
  opacity: 0.9;
}

.empty-state {
  text-align: center;
  padding: 48px;
  background: white;
  border-radius: 12px;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}
</style>
