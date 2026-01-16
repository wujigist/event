import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import PersonalizedWelcome from '../../components/experience/PersonalizedWelcome';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import { formatDate } from '../../utils/helpers';
import { FiCalendar, FiCheckCircle, FiClock } from 'react-icons/fi';

const DashboardPage = () => {
  const { member } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [event, setEvent] = useState(null);
  const [rsvp, setRsvp] = useState(null);
  
  useEffect(() => {
    fetchDashboardData();
  }, []);
  
  const fetchDashboardData = async () => {
    try {
      // Fetch current event
      const eventResponse = await api.get(API_ENDPOINTS.EVENTS.CURRENT);
      setEvent(eventResponse.data);
      
      // Fetch RSVP status
      try {
        const rsvpResponse = await api.get(API_ENDPOINTS.RSVP.ME);
        const rsvpData = rsvpResponse.data;
        
        // Check if member has RSVP
        if (rsvpData.has_rsvp) {
          // Member has responded - set the full response data
          setRsvp(rsvpData);
        } else {
          // Member hasn't responded yet
          setRsvp(null);
        }
      } catch (error) {
        // No RSVP yet, that's okay
        setRsvp(null);
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
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
        <div className="max-w-6xl mx-auto">
          {/* Personalized Welcome */}
          <PersonalizedWelcome />
          
          {/* Event Overview */}
          {event && (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
              <div className="card-luxury mb-8">
                <div className="flex items-start gap-4 mb-6">
                  <FiCalendar className="text-luxury-gold text-3xl flex-shrink-0 mt-1" />
                  <div className="flex-1">
                    <h2 className="font-elegant text-luxury-gold text-3xl mb-2">
                      {event.title}
                    </h2>
                    {event.subtitle && (
                      <p className="text-luxury-champagne font-serif text-lg italic">
                        {event.subtitle}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="border-t border-luxury-gold/30 pt-6 mt-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Date */}
                    <div>
                      <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-2">
                        Date
                      </p>
                      <p className="text-luxury-off-white font-serif text-lg">
                        {formatDate(event.event_date)}
                      </p>
                    </div>
                    
                    {/* Venue */}
                    {event.venue_name && (
                      <div>
                        <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-2">
                          Venue
                        </p>
                        <p className="text-luxury-off-white font-serif text-lg">
                          {event.venue_name}
                        </p>
                      </div>
                    )}
                    
                    {/* Theme */}
                    {event.theme && (
                      <div>
                        <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-2">
                          Theme
                        </p>
                        <p className="text-luxury-off-white font-serif text-lg">
                          {event.theme}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="mt-8 flex flex-col sm:flex-row gap-4">
                  <Button
                    variant="primary"
                    onClick={() => navigate('/event')}
                  >
                    View Full Details
                  </Button>
                </div>
              </div>
            </AnimatedEntrance>
          )}
          
          {/* RSVP Status */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
            <div className="card-luxury">
              <h3 className="font-elegant text-luxury-gold text-2xl mb-6">
                Your RSVP
              </h3>
              
              {rsvp ? (
                <div>
                  {rsvp.rsvp_status === 'accepted' && (
                    <div className="flex items-center gap-3 text-green-400 mb-4">
                      <FiCheckCircle size={24} />
                      <span className="font-serif text-lg">You've confirmed your attendance</span>
                    </div>
                  )}
                  
                  {rsvp.rsvp_status === 'declined' && (
                    <div className="text-luxury-champagne/70 mb-4">
                      <span className="font-serif text-lg">You've declined this invitation</span>
                    </div>
                  )}
                  
                  <p className="text-luxury-champagne font-serif">
                    {rsvp.rsvp_status === 'accepted' 
                      ? "I can't wait to see you there!"
                      : "You'll be in our thoughts. We hope to see you at a future gathering."
                    }
                  </p>
                  
                  {rsvp.rsvp_status === 'accepted' && (
                    <div className="mt-6">
                      <Button
                        variant="secondary"
                        onClick={() => navigate('/legacy-pass')}
                      >
                        View Your Legacy Pass
                      </Button>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <div className="flex items-center gap-3 text-luxury-gold mb-4">
                    <FiClock size={24} />
                    <span className="font-serif text-lg">Awaiting your response</span>
                  </div>
                  
                  <p className="text-luxury-champagne font-serif mb-6">
                    Will you join us for this unforgettable evening?
                  </p>
                  
                  <Button
                    variant="primary"
                    onClick={() => navigate('/rsvp')}
                  >
                    Respond to Invitation
                  </Button>
                </div>
              )}
            </div>
          </AnimatedEntrance>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default DashboardPage;