<template>
  <div class="signup-page">
    <div class="signup-container">
      <div class="logo">
        <img src="../assets/images/ClassTrackLOGO-Logo Only-Pink BG 1.png" alt="LabEase Logo">
      </div>
      <h1>Create Account</h1>
      <p class="subtitle">Sign up to get started</p>
      
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label for="fullName">Full Name</label>
          <input 
            type="text" 
            id="fullName" 
            v-model="fullName" 
            required 
            placeholder="Enter your full name"
          >
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

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <div class="password-input">
            <input 
              :type="showConfirmPassword ? 'text' : 'password'" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              required 
              placeholder="Confirm your password"
            >
            <i 
              class="mdi" 
              :class="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click="showConfirmPassword = !showConfirmPassword"
            ></i>
          </div>
        </div>

        <div class="form-group">
          <label for="role">Role</label>
          <select id="role" v-model="role" required>
            <option value="">Select your role</option>
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button type="submit" class="signup-btn">Sign Up</button>
      </form>

      <p class="login-prompt">
        Already have an account? 
        <router-link to="/login" class="login-link">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }

  try {
    // TODO: Implement actual signup API call
    const response = await fetch('http://localhost:8000/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        fullName: fullName.value,
        email: email.value,
        password: password.value,
        role: role.value,
      }),
    })

    if (response.ok) {
      router.push('/login')
    } else {
      // Handle signup error
      console.error('Signup failed')
    }
  } catch (error) {
    console.error('Signup error:', error)
  }
}
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  font-family: 'Poppins', sans-serif;
}

.signup-container {
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

input[type="text"],
input[type="email"],
input[type="password"],
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

select {
  background: white;
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

.signup-btn {
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
  margin-top: 20px;
}

.signup-btn:hover {
  background: #ff4da6;
}

.login-prompt {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login-link {
  color: #FF69B4;
  text-decoration: none;
  font-weight: 600;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
