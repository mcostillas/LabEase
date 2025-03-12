import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookingsStore = defineStore('bookings', {
  state: () => ({
    bookings: [],
    labs: [],
    totalItems: 0,
    totalPages: 0,
    currentPage: 1,
    loading: false,
    error: null,
    filters: {
      search: '',
      startDate: '',
      endDate: '',
      selectedLab: 'all',
      status: 'all'
    }
  }),

  actions: {
    async fetchBookings() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          page: this.currentPage,
          items_per_page: 12,
          ...this.filters.search && { search: this.filters.search },
          ...this.filters.startDate && { start_date: this.filters.startDate },
          ...this.filters.endDate && { end_date: this.filters.endDate },
          ...this.filters.selectedLab !== 'all' && { lab: this.filters.selectedLab },
          ...this.filters.status !== 'all' && { status: this.filters.status }
        }

        const response = await axios.get('/api/instructor/bookings', { params })
        this.bookings = response.data.bookings
        this.totalItems = response.data.total_items
        this.totalPages = response.data.total_pages
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch bookings'
        console.error('Error fetching bookings:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchLabs() {
      try {
        const response = await axios.get('/api/instructor/labs')
        this.labs = response.data
      } catch (error) {
        console.error('Error fetching labs:', error)
      }
    },

    setPage(page) {
      this.currentPage = page
      this.fetchBookings()
    },

    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters }
      this.currentPage = 1 // Reset to first page when filters change
      this.fetchBookings()
    },

    resetFilters() {
      this.filters = {
        search: '',
        startDate: '',
        endDate: '',
        selectedLab: 'all',
        status: 'all'
      }
      this.fetchBookings()
    }
  }
})
