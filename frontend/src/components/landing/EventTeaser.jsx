import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../../utils/constants';
import AnimatedEntrance from '../common/AnimatedEntrance';
import { formatDate } from '../../utils/helpers';

const EventTeaser = () => {
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchEventTeaser();
  }, []);
  
  const fetchEventTeaser = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.EVENTS.CURRENT);
      setEvent(response.data);
    } catch (error) {
      console.error('Failed to fetch event teaser:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading || !event) {
    return null;
  }
  
  return (
    <section className="py-20 px-6 bg-luxury-black">
      <div className="max-w-4xl mx-auto text-center">
        <AnimatedEntrance animation="slideUp" duration={0.8}>
          <h2 className="font-elegant text-luxury-gold text-4xl md:text-5xl mb-6">
            {event.title}
          </h2>
          
          {event.subtitle && (
            <p className="subheading-luxury text-xl md:text-2xl mb-8">
              {event.subtitle}
            </p>
          )}
          
          {/* Date Display */}
          <div className="inline-block bg-luxury-off-black border border-luxury-gold px-8 py-4 mb-8">
            <p className="text-luxury-champagne font-serif text-lg">
              {formatDate(event.event_date)}
            </p>
          </div>
          
          {/* Theme */}
          {event.theme && (
            <p className="text-luxury-gold font-sans uppercase tracking-widest text-sm mb-8">
              {event.theme}
            </p>
          )}
          
          {/* Mystery Message */}
          <div className="max-w-2xl mx-auto">
            <p className="text-luxury-champagne/80 font-serif italic text-base leading-relaxed">
              Full details will be revealed upon access to your exclusive invitation.
              An evening of unparalleled luxury awaits...
            </p>
          </div>
        </AnimatedEntrance>
      </div>
    </section>
  );
};

export default EventTeaser;