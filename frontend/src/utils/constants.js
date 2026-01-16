// API Base URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    REQUEST_ACCESS: '/api/auth/request-access',
    ME: '/api/auth/me',
    LOGOUT: '/api/auth/logout',
  },
  EVENTS: {
    CURRENT: '/api/events/current',
    DETAIL: (id) => `/api/events/${id}`,
  },
  RSVP: {
    SUBMIT: '/api/rsvp/',
    ME: '/api/rsvp/me',
  },
  LEGACY_PASS: {
    PREVIEW: (token) => `/api/legacy-pass/preview/${token}`,
    FULL: (token) => `/api/legacy-pass/full/${token}`,
  },
  PAYMENT: {
    METHODS: '/api/payment/methods',
    CONTACT: '/api/payment/contact',
    STATUS: (token) => `/api/payment/status/${token}`, // ← ADDED THIS
  },
};

// Local Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  MEMBER: 'member_data',
};

// Payment Amount
export const PAYMENT_AMOUNT = 1000;

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  STORAGE_KEYS,
  PAYMENT_AMOUNT,
};