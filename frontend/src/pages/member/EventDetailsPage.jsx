import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import EventDetails from '../../components/event/EventDetails';
import Schedule from '../../components/event/Schedule';
import AmenitiesList from '../../components/experience/AmenitiesList';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { formatDate } from '../../utils/helpers';

const EventDetailsPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [event, setEvent] = useState(null);
  const [rsvp, setRsvp] = useState(null);
  
  useEffect(() => {
    fetchEventData();
  }, []);
  
  const fetchEventData = async () => {
    try {
      // Fetch event
      const eventResponse = await api.get(API_ENDPOINTS.EVENTS.CURRENT);
      setEvent(eventResponse.data);
      
      // Check RSVP status
      try {
        const rsvpResponse = await api.get(API_ENDPOINTS.RSVP.ME);
        setRsvp(rsvpResponse.data);
      } catch (error) {
        // No RSVP yet
        setRsvp(null);
      }
    } catch (error) {
      console.error('Failed to fetch event data:', error);
    } finally {
      setLoading(false);
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
        <div className="max-w-6xl mx-auto">
          {/* Event Header */}
          <AnimatedEntrance animation="fade" duration={0.8}>
            <div className="text-center mb-12">
              <h1 className="heading-luxury text-5xl md:text-6xl mb-4">
                {event.title}
              </h1>
              {event.subtitle && (
                <p className="subheading-luxury text-2xl mb-6">
                  {event.subtitle}
                </p>
              )}
              <div className="inline-block bg-luxury-off-black border border-luxury-gold px-8 py-3">
                <p className="text-luxury-champagne font-serif text-lg">
                  {formatDate(event.event_date)}
                </p>
              </div>
            </div>
          </AnimatedEntrance>
          
          {/* Event Details */}
          <EventDetails event={event} />
          
          {/* Schedule */}
          <Schedule eventId={event.id} />
          
          {/* Amenities */}
          <AmenitiesList eventId={event.id} />
          
          {/* RSVP CTA */}
          {!rsvp && (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
              <div className="card-luxury text-center">
                <h3 className="font-elegant text-luxury-gold text-3xl mb-4">
                  Will You Join Us?
                </h3>
                <p className="text-luxury-champagne font-serif text-lg mb-8 max-w-2xl mx-auto">
                  Your presence would make this evening truly complete.
                  Please let us know if you'll be able to attend.
                </p>
                <Button
                  variant="primary"
                  size="large"
                  onClick={() => navigate('/rsvp')}
                >
                  Respond to Invitation
                </Button>
              </div>
            </AnimatedEntrance>
          )}
          
          {/* Already RSVP'd */}
          {rsvp && rsvp.status === 'accepted' && (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
              <div className="card-luxury text-center">
                <h3 className="font-elegant text-luxury-gold text-3xl mb-4">
                  You're Confirmed!
                </h3>
                <p className="text-luxury-champagne font-serif text-lg mb-8">
                  We can't wait to see you there.
                </p>
                <Button
                  variant="secondary"
                  onClick={() => navigate('/legacy-pass')}
                >
                  View Your Legacy Pass
                </Button>
              </div>
            </AnimatedEntrance>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default EventDetailsPage;