// API Base URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    REQUEST_ACCESS: '/api/auth/request-access',
    ME: '/api/auth/me',
    LOGOUT: '/api/auth/logout',
    VERIFY: '/api/auth/verify',
  },
  
  // Events
  EVENTS: {
    CURRENT: '/api/events/current',
    LIST: '/api/events',
    DETAIL: (id) => `/api/events/${id}`,
    SCHEDULE: (id) => `/api/events/${id}/schedule`,
    AMENITIES: (id) => `/api/events/${id}/amenities`,
  },
  
  // RSVP
  RSVP: {
    SUBMIT: '/api/rsvp',
    ME: '/api/rsvp/me',
    UPDATE: (id) => `/api/rsvp/${id}`,
  },
  
  // Legacy Pass
  LEGACY_PASS: {
    PREVIEW: (token) => `/api/legacy-pass/preview/${token}`,
    FULL: (token) => `/api/legacy-pass/${token}`,
    BENEFITS: (token) => `/api/legacy-pass/${token}/benefits`,
    DOWNLOAD_PDF: (token) => `/api/legacy-pass/${token}/download`,
  },
  
  // Payment
  PAYMENT: {
    METHODS: '/api/payment/methods',
    CONTACT: '/api/payment/contact',
    STATUS: (token) => `/api/payment/status/${token}`,
    VERIFY: '/api/payment/verify',
    PENDING: '/api/payment/admin/pending',
    ALL: '/api/payment/admin/all',
  },
  
  // Gifts
  GIFTS: {
    MY_GIFTS: '/api/gifts/my-gifts',
    CATEGORIES: '/api/gifts/categories',
  },
  
  // Memories
  MEMORIES: {
    MY_MEMORIES: '/api/memories/my-memories',
    GALLERY: '/api/memories/gallery',
  },
  
  // Admin
  ADMIN: {
    DASHBOARD: '/api/admin/dashboard',
    MEMBERS: '/api/admin/members',
    CREATE_MEMBER: '/api/admin/members',
    MEMBER_DETAILS: (id) => `/api/admin/members/${id}`,
    UPDATE_MEMBER: (id) => `/api/admin/members/${id}`,
    DELETE_MEMBER: (id) => `/api/admin/members/${id}`,
    RSVPS: '/api/admin/rsvps',
    RSVP_SUMMARY: '/api/admin/rsvps/summary',
    STATISTICS: '/api/admin/statistics',
    CREATE_EVENT: '/api/admin/events',
    UPDATE_EVENT: (id) => `/api/admin/events/${id}`,
    DELETE_EVENT: (id) => `/api/admin/events/${id}`,
  },
};

// Local Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  MEMBER: 'member_data',
};

// Payment Amount
export const PAYMENT_AMOUNT = 1000;

// Export as default object (for backward compatibility)
export default {
  API_BASE_URL,
  API_ENDPOINTS,
  STORAGE_KEYS,
  PAYMENT_AMOUNT,
};