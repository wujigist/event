import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../common/LoadingSpinner';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  // Show loading while checking authentication
  if (loading) {
    return <LoadingSpinner fullScreen message="Verifying access..." />;
  }
  
  // Redirect to access page if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/access" replace />;
  }
  
  // Render protected content
  return children;
};

export default PrivateRoute;