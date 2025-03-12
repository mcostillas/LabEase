<template>
  <div class="landing-page">
    <!-- Side Navigation -->
    <nav class="sidenav">
      <div class="logo">
        <img src="../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
      </div>
      <div class="nav-icons">
        <div class="nav-icon info-icon">
          <i class="mdi mdi-information"></i>
        </div>
        <div class="nav-icon exit-icon" @click="handleLogout">
          <i class="mdi mdi-exit-to-app"></i>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-left">
        <h1 class="highlight">Book a<br>Laboratory now.</h1>
        <p>Effortless Lab Booking at Your Fingertips—Access, Reserve,<br>and Manage Your Lab Sessions Anytime, Anywhere.</p>
        <button class="get-started-btn" @click="handleGetStarted">Get Started</button>
      </div>
      <div class="content-right">
        <div class="calendar-illustration">
          <img src="../assets/images/image 12.png" alt="Calendar Illustration">
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const handleGetStarted = () => {
  localStorage.removeItem('labease_auth_token')
  localStorage.removeItem('labease_user_data')
  router.push('/login')
}

const handleLogout = () => {
  localStorage.removeItem('labease_auth_token')
  localStorage.removeItem('labease_user_data')
  router.push('/login')
}
</script>

<style scoped>
:root {
  --primary-color: #DD3859;
  --primary-light: #FF4D6E;
  --primary-dark: #99183A;
  --text-color: #000000;
  --text-light: #000000;
  --border-radius: 8px;
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

body {
  background-color: #F8FAFC;
}

.landing-page {
  display: flex;
  min-height: 100vh;
  background-color: #F8FAFC;
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

.nav-icons {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 16px;
}

.nav-icon {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  cursor: pointer;
  color: white;
  transition: background-color 0.2s ease;
  border-radius: var(--border-radius);
}

.nav-icon:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-icon i {
  font-size: 24px;
}

.main-content {
  flex: 1;
  display: flex;
  padding: 80px;
  margin-left: 72px;
  transition: margin-left 0.3s ease;
  background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%);
}

.content-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.content-left .highlight{
  color:#DD3859
}

h1 {
  font-size: 56px;
  font-weight: 800;
  color: var(--primary-color);
  margin-bottom: 20px;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

p {
  font-size: 20px;
  line-height: 1.6;
  color: black;
  margin-bottom: 40px;
  max-width: 600px;
  font-weight: 500;
}

@keyframes heartbeat {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 15px rgba(221, 56, 89, 0.4);
  }
  14% {
    transform: scale(1.15);
    box-shadow: 0 6px 18px rgba(221, 56, 89, 0.6);
  }
  28% {
    transform: scale(1);
    box-shadow: 0 4px 15px rgba(221, 56, 89, 0.4);
  }
  42% {
    transform: scale(1.15);
    box-shadow: 0 6px 18px rgba(221, 56, 89, 0.6);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 4px 15px rgba(221, 56, 89, 0.4);
  }
}

.get-started-btn {
  width: fit-content;
  padding: 16px 40px;
  background: #DD3859;
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  animation: heartbeat 1.5s ease-in-out infinite;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(221, 56, 89, 0.4);
}

.get-started-btn:hover {
  background: var(--primary-light);
  box-shadow: 0 8px 20px rgba(221, 56, 89, 0.5);
  animation: none;
  transform: translateY(-3px);
}

.get-started-btn:active {
  background: var(--primary-dark);
  transform: translateY(1px);
  box-shadow: 0 2px 8px rgba(221, 56, 89, 0.3);
}

.content-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-illustration img {
  max-width: 100%;
  height: auto;
}

.highlight {
  color: var(--primary-color);
}

.hero-text p {
  font-size: 1.125rem;
  color: var(--text-light);
  line-height: 1.6;
  margin-bottom: 2rem;
  max-width: 600px;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
}

.primary-btn {
  padding: 0.875rem 2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.primary-btn:hover {
  background: var(--primary-light);
  transform: translateY(-2px);
}

.secondary-btn {
  padding: 0.875rem 2rem;
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background: rgba(221, 56, 89, 0.1);
  transform: translateY(-2px);
}

.hero-image {
  flex: 1;
  position: relative;
}

.main-illustration {
  width: 100%;
  max-width: 600px;
  height: auto;
}

.floating-card {
  position: absolute;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.floating-card i {
  color: var(--primary-color);
  font-size: 1.5rem;
}

.card-1 {
  top: 10%;
  left: 0;
}

.card-2 {
  top: 40%;
  right: 0;
}

.card-3 {
  bottom: 20%;
  left: 20%;
}

/* Features Section */
.features {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.features h2 {
  text-align: center;
  font-size: 2.5rem;
  color: var(--text-color);
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-card i {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: var(--text-light);
  line-height: 1.5;
}
</style>
