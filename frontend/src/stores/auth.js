import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userRole: localStorage.getItem('userRole') || null,
    userId: localStorage.getItem('userId') || null,
    fullName: localStorage.getItem('fullName') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    isAdmin: (state) => state.userRole === 'Admin',
    isInstructor: (state) => state.userRole === 'Instructor',
    getUserRole: (state) => state.userRole,
    getFullName: (state) => state.fullName
  },

  actions: {
    async login(email, password) {
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)

        const response = await axios.post('/api/token', formData)
        
        // Store auth data
        this.setAuthData(response.data)
        
        // Configure axios
        this.setAxiosDefaults()
        
        return response.data.role
      } catch (error) {
        throw error
      }
    },

    setAuthData(data) {
      this.token = data.access_token
      this.userRole = data.role
      this.userId = data.user_id
      this.fullName = data.full_name
      this.isAuthenticated = true

      // Store in localStorage
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('userRole', data.role)
      localStorage.setItem('userId', data.user_id)
      localStorage.setItem('fullName', data.full_name)
    },

    setAxiosDefaults() {
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    },

    logout() {
      // Clear state
      this.token = null
      this.userRole = null
      this.userId = null
      this.fullName = null
      this.isAuthenticated = false

      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
      localStorage.removeItem('userId')
      localStorage.removeItem('fullName')

      // Clear axios defaults
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
