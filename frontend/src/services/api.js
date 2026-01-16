import axios from 'axios';
import Cookies from 'js-cookie';
import { API_BASE_URL, STORAGE_KEYS } from '../utils/constants';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 seconds
});

// Request interceptor - Add JWT token to headers
api.interceptors.request.use(
  (config) => {
    // Get token from cookie
    const token = Cookies.get(STORAGE_KEYS.TOKEN);
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
  (response) => {
    // Return successful response
    return response;
  },
  (error) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to access page
          Cookies.remove(STORAGE_KEYS.TOKEN);
          localStorage.removeItem(STORAGE_KEYS.MEMBER);
          window.location.href = '/access';
          break;
          
        case 403:
          // Forbidden
          console.error('Access denied:', data.detail);
          break;
          
        case 404:
          // Not found
          console.error('Resource not found:', data.detail);
          break;
          
        case 500:
          // Server error
          console.error('Server error:', data.detail);
          break;
          
        default:
          console.error('API Error:', data.detail || 'An error occurred');
      }
      
      // Return error with custom message
      return Promise.reject({
        status,
        message: data.detail || 'An unexpected error occurred',
        data,
      });
    } else if (error.request) {
      // Request made but no response received
      console.error('Network error - no response received');
      return Promise.reject({
        status: 0,
        message: 'Network error. Please check your connection.',
      });
    } else {
      // Something else happened
      console.error('Error:', error.message);
      return Promise.reject({
        status: 0,
        message: error.message || 'An error occurred',
      });
    }
  }
);

export default api;