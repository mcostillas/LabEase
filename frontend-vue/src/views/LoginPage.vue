<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo">
        <img src="../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
      </div>
      <h1>Welcome Back!</h1>
      <p class="subtitle">Sign in to continue</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="Enter your email"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              required 
              placeholder="Enter your password"
            >
            <i 
              class="mdi" 
              :class="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click="showPassword = !showPassword"
            ></i>
          </div>
        </div>

        <div class="remember-forgot">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe">
            Remember me
          </label>
          <a href="#" class="forgot-password">Forgot Password?</a>
        </div>

        <button type="submit" class="login-btn">Sign In</button>
      </form>

      <p class="signup-prompt">
        Don't have an account? 
        <router-link to="/signup" class="signup-link">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const error = ref('')

const handleLogin = async () => {
  try {
    // Mock login for testing different roles
    let mockResponse = null;
    
    if (email.value === 'admin@labease.com' && password.value === 'admin123') {
      mockResponse = {
        token: 'mock_token_admin',
        user: {
          name: 'Admin User',
          role: 'admin',
          id: 'ADM001'
        }
      };
    } else if (email.value === 'instructor@labease.com' && password.value === 'instructor123') {
      mockResponse = {
        token: 'mock_token_instructor',
        user: {
          name: 'John Smith',
          role: 'instructor',
          id: 'INS001'
        }
      };
    }
    
    if (mockResponse) {
      // Store auth data
      authStore.setAuth(mockResponse.token, mockResponse.user)
      
      // Redirect based on role
      if (mockResponse.user.role === 'admin') {
        router.push('/admin')
      } else if (mockResponse.user.role === 'instructor') {
        router.push('/instructor')
      } else {
        router.push('/booking')
      }
    } else {
      error.value = 'Invalid credentials. Use admin@labease.com / admin123 for admin access or instructor@labease.com / instructor123 for instructor access'
    }
  } catch (err) {
    error.value = 'Login failed. Please try again.'
    console.error('Login error:', err)
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  font-family: 'Poppins', sans-serif;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.logo {
  text-align: center;
  margin-bottom: 20px;
}

.logo img {
  width: 80px;
  height: 80px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input[type="email"],
input[type="password"],
input[type="text"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.password-input {
  position: relative;
}

.password-input i {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #666;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.forgot-password {
  color: #FF69B4;
  text-decoration: none;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #FF69B4;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #ff4da6;
}

.signup-prompt {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.signup-link {
  color: #FF69B4;
  text-decoration: none;
  font-weight: 600;
}

.signup-link:hover {
  text-decoration: underline;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
}
</style>
