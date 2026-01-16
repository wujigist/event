import { createContext, useContext, useState, useEffect } from 'react';
import {
  requestAccess,
  getCurrentMember,
  logout as logoutService,
  isAuthenticated as checkAuth,
  getStoredMember,
} from '../services/authService';

// Create Auth Context
const AuthContext = createContext(null);

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [member, setMember] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth on app load
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      // Check if token exists
      if (checkAuth()) {
        // Get stored member data
        const storedMember = getStoredMember();
        
        if (storedMember) {
          setMember(storedMember);
          setIsAuthenticated(true);
        } else {
          // Fetch fresh member data from API
          const memberData = await getCurrentMember();
          setMember(memberData);
          setIsAuthenticated(true);
        }
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
      // Clear invalid session
      setMember(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (email) => {
    try {
      setLoading(true);
      const { member: memberData } = await requestAccess(email);
      
      setMember(memberData);
      setIsAuthenticated(true);
      
      return { success: true, member: memberData };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.message || 'Login failed. Please try again.' 
      };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      setLoading(true);
      await logoutService();
      
      setMember(null);
      setIsAuthenticated(false);
      
      // Redirect to landing page
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if API call fails
      setMember(null);
      setIsAuthenticated(false);
      window.location.href = '/';
    } finally {
      setLoading(false);
    }
  };

  // Refresh member data
  const refreshMember = async () => {
    try {
      const memberData = await getCurrentMember();
      setMember(memberData);
      return memberData;
    } catch (error) {
      console.error('Refresh member error:', error);
      throw error;
    }
  };

  const value = {
    member,
    isAuthenticated,
    loading,
    login,
    logout,
    refreshMember,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default AuthContext;