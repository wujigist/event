import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import Button from '../../components/common/Button';
import { FiUsers, FiCheckCircle, FiXCircle, FiClock, FiDollarSign } from 'react-icons/fi';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    fetchDashboardStats();
  }, []);
  
  const fetchDashboardStats = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.ADMIN.DASHBOARD);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch admin stats:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Title */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="mb-12">
              <h1 className="heading-luxury text-5xl mb-4">
                Admin Dashboard
              </h1>
              <p className="subheading-luxury text-xl">
                Manage your exclusive event
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {/* Total Members */}
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.1}>
              <div className="card-luxury">
                <div className="flex items-start justify-between mb-4">
                  <FiUsers className="text-luxury-gold text-3xl" />
                  <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                    Total
                  </span>
                </div>
                <p className="text-luxury-off-white font-serif text-4xl mb-2">
                  {stats?.member_stats?.total || 0}
                </p>
                <p className="text-luxury-champagne/70 font-sans text-sm">
                  Members
                </p>
              </div>
            </AnimatedEntrance>
            
            {/* RSVPs Accepted */}
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
              <div className="card-luxury">
                <div className="flex items-start justify-between mb-4">
                  <FiCheckCircle className="text-green-400 text-3xl" />
                  <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                    Accepted
                  </span>
                </div>
                <p className="text-luxury-off-white font-serif text-4xl mb-2">
                  {stats?.rsvp_stats?.accepted || 0}
                </p>
                <p className="text-luxury-champagne/70 font-sans text-sm">
                  Attending
                </p>
              </div>
            </AnimatedEntrance>
            
            {/* Pending Payments */}
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.3}>
              <div className="card-luxury">
                <div className="flex items-start justify-between mb-4">
                  <FiClock className="text-yellow-400 text-3xl" />
                  <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                    Pending
                  </span>
                </div>
                <p className="text-luxury-off-white font-serif text-4xl mb-2">
                  {stats?.payment_stats?.pending || 0}
                </p>
                <p className="text-luxury-champagne/70 font-sans text-sm">
                  Payments
                </p>
              </div>
            </AnimatedEntrance>
            
            {/* Verified Payments */}
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
              <div className="card-luxury">
                <div className="flex items-start justify-between mb-4">
                  <FiDollarSign className="text-luxury-gold text-3xl" />
                  <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                    Verified
                  </span>
                </div>
                <p className="text-luxury-off-white font-serif text-4xl mb-2">
                  {stats?.payment_stats?.verified || 0}
                </p>
                <p className="text-luxury-champagne/70 font-sans text-sm">
                  Payments
                </p>
              </div>
            </AnimatedEntrance>
          </div>
          
          {/* Quick Actions */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.5}>
            <div className="card-luxury mb-12">
              <h2 className="font-elegant text-luxury-gold text-3xl mb-6">
                Quick Actions
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button
                  variant="secondary"
                  onClick={() => navigate('/admin/payments')}
                  icon={<FiDollarSign />}
                >
                  Verify Payments
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => navigate('/admin/members')}
                  icon={<FiUsers />}
                >
                  View Members
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => navigate('/admin/rsvps')}
                  icon={<FiCheckCircle />}
                >
                  View RSVPs
                </Button>
              </div>
            </div>
          </AnimatedEntrance>
          
          {/* Recent Activity */}
          {stats?.recent_activity && stats.recent_activity.length > 0 && (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
              <div className="card-luxury">
                <h2 className="font-elegant text-luxury-gold text-3xl mb-6">
                  Recent Activity
                </h2>
                
                <div className="space-y-4">
                  {stats.recent_activity.map((activity, index) => (
                    <div 
                      key={index}
                      className="flex items-start gap-4 p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded"
                    >
                      <div className="flex-1">
                        <p className="text-luxury-off-white font-serif text-base">
                          {activity.message}
                        </p>
                        <p className="text-luxury-champagne/70 font-sans text-sm mt-1">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </AnimatedEntrance>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default AdminDashboard;