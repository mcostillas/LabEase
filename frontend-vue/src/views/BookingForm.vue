<template>
  <div class="booking-page">
    <nav class="sidenav">
      <div class="logo">
        <img src="../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
      </div>
      <div class="nav-items">
        <router-link to="/booking" class="nav-item active">
          <i class="mdi mdi-calendar"></i>
          <span>Book Lab</span>
        </router-link>
        <router-link to="/history" class="nav-item">
          <i class="mdi mdi-history"></i>
          <span>History</span>
        </router-link>
      </div>
      <div class="nav-bottom">
        <button class="nav-item" @click="handleLogout">
          <i class="mdi mdi-logout"></i>
          <span>Logout</span>
        </button>
      </div>
    </nav>

    <main class="main-content">
      <header class="page-header">
        <h1>Book a Laboratory</h1>
        <p>Fill in the details below to book a laboratory session</p>
      </header>

      <form @submit.prevent="handleBooking" class="booking-form">
        <div class="form-section">
          <h2>Laboratory Details</h2>
          
          <div class="form-group">
            <label for="laboratory">Laboratory</label>
            <select id="laboratory" v-model="formData.laboratory" required>
              <option value="">Select a laboratory</option>
              <option v-for="lab in laboratories" :key="lab.id" :value="lab.id">
                {{ lab.name }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="date">Date</label>
              <input 
                type="date" 
                id="date" 
                v-model="formData.date"
                :min="minDate"
                required
              >
            </div>

            <div class="form-group">
              <label for="time">Time Slot</label>
              <select id="time" v-model="formData.timeSlot" required>
                <option value="">Select a time slot</option>
                <option v-for="slot in availableTimeSlots" :key="slot.id" :value="slot.id">
                  {{ slot.start }} - {{ slot.end }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>Purpose</h2>
          
          <div class="form-group">
            <label for="subject">Subject</label>
            <input 
              type="text" 
              id="subject" 
              v-model="formData.subject"
              placeholder="Enter the subject"
              required
            >
          </div>

          <div class="form-group">
            <label for="purpose">Purpose of Use</label>
            <textarea 
              id="purpose" 
              v-model="formData.purpose"
              placeholder="Describe the purpose of your laboratory session"
              required
            ></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn">Book Laboratory</button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Mock data - replace with actual API calls
const laboratories = ref([
  { id: 1, name: 'Chemistry Lab 1' },
  { id: 2, name: 'Physics Lab 1' },
  { id: 3, name: 'Biology Lab 1' },
])

const availableTimeSlots = ref([
  { id: 1, start: '08:00', end: '10:00' },
  { id: 2, start: '10:00', end: '12:00' },
  { id: 3, start: '13:00', end: '15:00' },
  { id: 4, start: '15:00', end: '17:00' },
])

const formData = ref({
  laboratory: '',
  date: '',
  timeSlot: '',
  subject: '',
  purpose: '',
})

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const handleBooking = async () => {
  try {
    // TODO: Implement actual booking API call
    const response = await fetch('http://localhost:8000/api/bookings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('labease_auth_token')}`,
      },
      body: JSON.stringify(formData.value),
    })

    if (response.ok) {
      alert('Booking successful!')
      // Reset form
      formData.value = {
        laboratory: '',
        date: '',
        timeSlot: '',
        subject: '',
        purpose: '',
      }
    } else {
      alert('Booking failed. Please try again.')
    }
  } catch (error) {
    console.error('Booking error:', error)
    alert('An error occurred. Please try again.')
  }
}

const handleLogout = () => {
  localStorage.removeItem('labease_auth_token')
  localStorage.removeItem('labease_user_data')
  router.push('/login')
}
</script>

<style scoped>
.booking-page {
  display: flex;
  min-height: 100vh;
}

.sidenav {
  width: 250px;
  background: #FF69B4;
  padding: 20px;
  display: flex;
  flex-direction: column;
  color: white;
}

.logo {
  text-align: center;
  margin-bottom: 40px;
}

.logo img {
  width: 80px;
  height: 80px;
}

.nav-items {
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  font-size: 16px;
}

.nav-item:hover,
.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
}

.nav-item i {
  font-size: 24px;
}

.main-content {
  flex: 1;
  padding: 40px;
  background: #f5f5f5;
}

.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 8px;
}

.page-header p {
  color: #666;
}

.booking-form {
  max-width: 800px;
}

.form-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.form-section h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

textarea {
  height: 120px;
  resize: vertical;
}

.form-actions {
  margin-top: 32px;
}

.submit-btn {
  padding: 12px 32px;
  background: #FF69B4;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-btn:hover {
  background: #ff4da6;
}
</style>
