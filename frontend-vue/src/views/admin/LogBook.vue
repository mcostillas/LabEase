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
            <span>Dashboard</span>
          </router-link>
          <router-link to="/admin/log-book" class="nav-item active" title="Log Book">
            <i class="mdi mdi-book-open"></i>
            <span>Log Book</span>
          </router-link>
          <router-link to="/admin/notifications" class="nav-item" title="Notifications">
            <i class="mdi mdi-bell"></i>
            <span>Notifications</span>
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
      <header class="page-header">
        <div class="header-content">
          <div class="welcome-section">
            <h1>Laboratory Log Book</h1>
            <div class="header-date">
              <span>{{ currentDate }}</span>
              <span class="date-separator">•</span>
              <span>{{ currentTime }}</span>
            </div>
          </div>
          <div class="header-actions">
            <div class="date-range">
              <input type="date" v-model="startDate" class="date-input">
              <span>to</span>
              <input type="date" v-model="endDate" class="date-input">
            </div>
            <button class="export-btn" @click="exportData">
              <i class="mdi mdi-download"></i>
              Export Data
            </button>
          </div>
        </div>
      </header>

      <div class="log-book-content">
        <div class="filters">
          <div class="search-bar">
            <i class="mdi mdi-magnify"></i>
            <input type="text" v-model="searchQuery" placeholder="Search logs...">
          </div>
          <div class="filter-options">
            <select v-model="statusFilter">
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <select v-model="sortBy">
              <option value="date">Sort by Date</option>
              <option value="lab">Sort by Laboratory</option>
              <option value="user">Sort by User</option>
            </select>
          </div>
        </div>

        <div class="log-table">
          <table>
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Laboratory</th>
                <th>User</th>
                <th>Purpose</th>
                <th>Duration</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in filteredLogs" :key="log.id">
                <td>
                  <div class="date-time">
                    <span class="date">{{ formatDate(log.date) }}</span>
                    <span class="time">{{ log.time }}</span>
                  </div>
                </td>
                <td>{{ log.laboratory }}</td>
                <td>
                  <div class="user-info">
                    <img :src="log.userAvatar" :alt="log.userName">
                    <div>
                      <span class="name">{{ log.userName }}</span>
                      <span class="role">{{ log.userRole }}</span>
                    </div>
                  </div>
                </td>
                <td>{{ log.purpose }}</td>
                <td>{{ log.duration }}</td>
                <td>
                  <span class="status-badge" :class="log.status.toLowerCase()">
                    {{ log.status }}
                  </span>
                </td>
                <td>
                  <div class="actions">
                    <button class="action-btn" @click="viewDetails(log)">
                      <i class="mdi mdi-eye"></i>
                    </button>
                    <button class="action-btn" @click="editLog(log)">
                      <i class="mdi mdi-pencil"></i>
                    </button>
                    <button class="action-btn delete" @click="deleteLog(log)">
                      <i class="mdi mdi-delete"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination">
          <button :disabled="currentPage === 1" @click="currentPage--">
            <i class="mdi mdi-chevron-left"></i>
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++">
            <i class="mdi mdi-chevron-right"></i>
          </button>
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

// Form controls
const selectedLab = ref('all')
const startDate = ref('')
const endDate = ref('')
const searchQuery = ref('')
const statusFilter = ref('all')
const sortBy = ref('date')
const currentPage = ref(1)

// Mock data
const labs = ref([
  { id: 1, name: 'Chemistry Lab 1' },
  { id: 2, name: 'Physics Lab 1' },
  { id: 3, name: 'Biology Lab 1' },
])

const logs = ref([
  {
    id: 1,
    date: '2025-03-12',
    time: '10:00 - 12:00',
    laboratory: 'Chemistry Lab 1',
    userName: 'John Doe',
    userRole: 'Student',
    userAvatar: 'path/to/avatar1.jpg',
    purpose: 'Chemistry Experiment',
    duration: '2 hours',
    status: 'Active'
  },
  {
    id: 2,
    date: '2025-03-12',
    time: '13:00 - 15:00',
    laboratory: 'Physics Lab 1',
    userName: 'Jane Smith',
    userRole: 'Student',
    userAvatar: 'path/to/avatar2.jpg',
    purpose: 'Physics Experiment',
    duration: '2 hours',
    status: 'Completed'
  },
])

// Computed properties
const filteredLogs = computed(() => {
  let filtered = [...logs.value]

  // Apply filters
  if (selectedLab !== 'all') {
    filtered = filtered.filter(log => log.laboratory === selectedLab.value)
  }

  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(log => log.status.toLowerCase() === statusFilter.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(log => 
      log.laboratory.toLowerCase().includes(query) ||
      log.userName.toLowerCase().includes(query) ||
      log.purpose.toLowerCase().includes(query)
    )
  }

  // Apply sorting
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'date':
        return new Date(b.date) - new Date(a.date)
      case 'lab':
        return a.laboratory.localeCompare(b.laboratory)
      case 'user':
        return a.userName.localeCompare(b.userName)
      default:
        return 0
    }
  })

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredLogs.value.length / 10))

// Methods
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const exportData = () => {
  // TODO: Implement export functionality
  console.log('Exporting data...')
}

const viewDetails = (log) => {
  // TODO: Implement view details functionality
  console.log('Viewing details for log:', log.id)
}

const editLog = (log) => {
  // TODO: Implement edit functionality
  console.log('Editing log:', log.id)
}

const deleteLog = (log) => {
  // TODO: Implement delete functionality
  if (confirm('Are you sure you want to delete this log?')) {
    console.log('Deleting log:', log.id)
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

.page-header {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: var(--border-radius);
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  color: #333;
}

.page-header h1 {
  color: var(--heading-color);
  font-size: 24px;
  font-weight: 600;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-section h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.header-date {
  color: var(--text-secondary);
  font-size: 14px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-input {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  outline: none;
  color: var(--text-color);
  font-size: 0.875rem;
  background: white;
}

.date-input:focus {
  border-color: var(--primary-color);
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--success-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 0.875rem;
}

.export-btn:hover {
  background: var(--success-dark);
}

.filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-bar {
  display: flex;
  align-items: center;
  background: white;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  width: 300px;
}

.search-bar i {
  color: var(--text-light);
  margin-right: 0.5rem;
}

.search-bar input {
  border: none;
  outline: none;
  width: 100%;
  background: transparent;
  font-size: 0.875rem;
  color: var(--text-color);
}

.filter-options {
  display: flex;
  gap: 1rem;
}

.filter-options select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  outline: none;
  color: var(--text-color);
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.filter-options select:focus {
  border-color: var(--primary-color);
}

.log-table {
  background: white;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: var(--bg-color);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--heading-color);
  font-size: 0.875rem;
}

td {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  color: #333;
}

.date-time {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.date {
  font-weight: 500;
}

.date-time .time {
  color: var(--text-secondary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-info img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--primary-light);
}

.user-info .name {
  font-weight: 500;
}

.user-info .role {
  color: var(--text-secondary);
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background: var(--primary-light);
  color: var(--primary-color);
}

.status-badge.completed {
  background: var(--success-light);
  color: var(--success-color);
}

.status-badge.cancelled {
  background: var(--error-light);
  color: var(--error-color);
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius);
  border: none;
  background: var(--bg-color);
  color: var(--text-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--primary-light);
  color: var(--primary-color);
}

.action-btn.delete:hover {
  background: var(--error-light);
  color: var(--error-color);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  background: white;
  color: var(--text-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:not(:disabled):hover {
  background: var(--primary-light);
  color: var(--primary-color);
  border-color: var(--primary-color);
}
</style>
