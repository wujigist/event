import api from './api';
import Cookies from 'js-cookie';
import { API_ENDPOINTS, STORAGE_KEYS } from '../utils/constants';

/**
 * Request access with email (login)
 */
export const requestAccess = async (email) => {
  try {
    const response = await api.post(API_ENDPOINTS.AUTH.REQUEST_ACCESS, { email });
    
    const { access_token, member } = response.data;
    
    // Store token in cookie (30 days expiration)
    Cookies.set(STORAGE_KEYS.TOKEN, access_token, { expires: 30 });
    
    // Store member data in localStorage
    localStorage.setItem(STORAGE_KEYS.MEMBER, JSON.stringify(member));
    
    return { token: access_token, member };
  } catch (error) {
    throw error;
  }
};

/**
 * Get current logged-in member
 */
export const getCurrentMember = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.AUTH.ME);
    
    // Update stored member data
    localStorage.setItem(STORAGE_KEYS.MEMBER, JSON.stringify(response.data));
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout - clear session
 */
export const logout = async () => {
  try {
    // Call backend logout endpoint
    await api.post(API_ENDPOINTS.AUTH.LOGOUT);
  } catch (error) {
    // Continue with logout even if API call fails
    console.error('Logout API error:', error);
  } finally {
    // Clear local storage
    Cookies.remove(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.MEMBER);
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  const token = Cookies.get(STORAGE_KEYS.TOKEN);
  return !!token;
};

/**
 * Get stored token
 */
export const getToken = () => {
  return Cookies.get(STORAGE_KEYS.TOKEN);
};

/**
 * Set token manually (for testing or special cases)
 */
export const setToken = (token) => {
  Cookies.set(STORAGE_KEYS.TOKEN, token, { expires: 30 });
};

/**
 * Get stored member data
 */
export const getStoredMember = () => {
  const memberData = localStorage.getItem(STORAGE_KEYS.MEMBER);
  return memberData ? JSON.parse(memberData) : null;
};

/**
 * Verify token is still valid
 */
export const verifyToken = async () => {
  try {
    const response = await api.post(API_ENDPOINTS.AUTH.VERIFY_TOKEN);
    return response.data.valid;
  } catch (error) {
    return false;
  }
};

export default {
  requestAccess,
  getCurrentMember,
  logout,
  isAuthenticated,
  getToken,
  setToken,
  getStoredMember,
  verifyToken,
};