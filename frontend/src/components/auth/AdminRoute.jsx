import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../common/LoadingSpinner';

const AdminRoute = ({ children }) => {
  const { isAuthenticated, member, loading } = useAuth();
  
  // Show loading while checking authentication
  if (loading) {
    return <LoadingSpinner fullScreen message="Verifying admin access..." />;
  }
  
  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/access" replace />;
  }
  
  // Check if user is admin
  const isAdmin = member?.membership_tier === 'admin' || 
                  member?.email?.endsWith('@paigeinnercircle.com');
  
  // Redirect to dashboard if not admin
  if (!isAdmin) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md">
          <h1 className="heading-luxury text-4xl mb-4">Access Denied</h1>
          <p className="text-luxury-champagne font-serif mb-8">
            You don't have permission to access this area.
          </p>
          <a href="/dashboard" className="text-luxury-gold hover:text-luxury-dark-gold">
            Return to Dashboard
          </a>
        </div>
      </div>
    );
  }
  
  // Render admin content
  return children;
};

export default AdminRoute;