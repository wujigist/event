import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import RSVPButtons from '../../components/rsvp/RSVPButtons';
import AcceptFlow from '../../components/rsvp/AcceptFlow';
import DeclineFlow from '../../components/rsvp/DeclineFlow';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { formatDate } from '../../utils/helpers';

const RSVPPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [event, setEvent] = useState(null);
  const [rsvp, setRsvp] = useState(null);
  const [rsvpStatus, setRsvpStatus] = useState(null); // 'accepted' or 'declined'
  const [rsvpData, setRsvpData] = useState(null);
  const [legacyToken, setLegacyToken] = useState(null);
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      // Fetch current event (will have id after backend update)
      const eventResponse = await api.get(API_ENDPOINTS.EVENTS.CURRENT);
      setEvent(eventResponse.data);
      
      // Check existing RSVP
      try {
        const rsvpResponse = await api.get(API_ENDPOINTS.RSVP.ME);
        setRsvp(rsvpResponse.data);
        setRsvpStatus(rsvpResponse.data.status);
        setRsvpData(rsvpResponse.data);
        if (rsvpResponse.data.legacy_pass_token) {
          setLegacyToken(rsvpResponse.data.legacy_pass_token);
        }
      } catch (error) {
        // No RSVP yet, that's fine
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleAccept = async () => {
    if (!event || !event.id) {
      alert('Unable to submit RSVP. Please refresh the page and try again.');
      return;
    }
    
    setSubmitting(true);
    
    try {
      const response = await api.post(API_ENDPOINTS.RSVP.SUBMIT, {
        event_id: event.id,
        status: 'accepted',
      });
      
      setRsvpStatus('accepted');
      setRsvpData(response.data);
      setLegacyToken(response.data.legacy_pass_token);
    } catch (error) {
      console.error('Failed to submit RSVP:', error);
      alert(error.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };
  
  const handleDecline = async () => {
    if (!event || !event.id) {
      alert('Unable to submit RSVP. Please refresh the page and try again.');
      return;
    }
    
    setSubmitting(true);
    
    try {
      const response = await api.post(API_ENDPOINTS.RSVP.SUBMIT, {
        event_id: event.id,
        status: 'declined',
      });
      
      setRsvpStatus('declined');
      setRsvpData(response.data);
    } catch (error) {
      console.error('Failed to submit RSVP:', error);
      alert(error.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  if (!event) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="heading-luxury text-4xl mb-4">No Event Found</h1>
            <p className="text-luxury-champagne font-serif">
              There is no active event at this time.
            </p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Show Accept/Decline Flow if already responded */}
          {rsvpStatus === 'accepted' && (
            <AcceptFlow token={legacyToken} data={rsvpData} />
          )}
          
          {rsvpStatus === 'declined' && (
            <DeclineFlow data={rsvpData} />
          )}
          
          {/* Show RSVP Form if not yet responded */}
          {!rsvpStatus && (
            <div>
              {/* Event Summary */}
              <AnimatedEntrance animation="slideUp" duration={0.8}>
                <div className="text-center mb-12">
                  <h1 className="heading-luxury text-5xl mb-4">
                    {event.title}
                  </h1>
                  <p className="text-luxury-champagne font-serif text-xl mb-6">
                    {formatDate(event.event_date)}
                  </p>
                  {event.venue_name && (
                    <p className="text-luxury-gold font-sans text-lg">
                      {event.venue_name}
                    </p>
                  )}
                </div>
              </AnimatedEntrance>
              
              {/* RSVP Question */}
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
                <div className="card-luxury text-center mb-8">
                  <h2 className="font-elegant text-luxury-gold text-3xl mb-6">
                    Will You Join Us?
                  </h2>
                  
                  <p className="text-luxury-champagne font-serif text-lg leading-relaxed max-w-2xl mx-auto mb-8">
                    This evening has been designed with you in mind. Your presence 
                    would make it truly complete. Please let us know if you'll be 
                    able to attend.
                  </p>
                  
                  <RSVPButtons 
                    onAccept={handleAccept}
                    onDecline={handleDecline}
                    loading={submitting}
                  />
                </div>
              </AnimatedEntrance>
              
              {/* Investment Notice */}
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
                <div className="text-center">
                  <p className="text-luxury-champagne/70 font-serif text-sm italic">
                    A $1,000 investment secures your Legacy Pass and exclusive gifts
                  </p>
                </div>
              </AnimatedEntrance>
            </div>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default RSVPPage;