import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import AnimatedEntrance from '../common/AnimatedEntrance';
import { FiClock, FiCalendar, FiMapPin } from 'react-icons/fi';

const Schedule = ({ eventId }) => {
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    if (eventId) {
      fetchSchedule();
    }
  }, [eventId]);
  
  const fetchSchedule = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.EVENTS.SCHEDULE(eventId));
      setSchedule(response.data);
    } catch (error) {
      console.error('Failed to fetch schedule:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return null;
  }
  
  if (!schedule || schedule.length === 0) {
    return null;
  }
  
  return (
    <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
      <div className="card-luxury mb-8">
        <h2 className="font-elegant text-luxury-gold text-3xl mb-8">
          Evening Timeline
        </h2>
        
        <div className="space-y-6">
          {schedule.map((item, index) => (
            <div 
              key={item.id} 
              className="flex gap-6 pb-6 border-b border-luxury-gold/20 last:border-b-0 last:pb-0"
            >
              {/* Time */}
              <div className="flex-shrink-0 w-24">
                <div className="flex items-center gap-2 text-luxury-gold">
                  <FiClock size={18} />
                  <span className="font-sans font-bold text-lg">
                    {item.time}
                  </span>
                </div>
              </div>
              
              {/* Content */}
              <div className="flex-1">
                <h3 className="text-luxury-off-white font-serif text-xl mb-2">
                  {item.title}
                </h3>
                {item.description && (
                  <p className="text-luxury-champagne/80 font-serif text-base leading-relaxed">
                    {item.description}
                  </p>
                )}
                {item.location && (
                  <div className="flex items-center gap-2 text-luxury-gold/70 mt-2">
                    <FiMapPin size={14} />
                    <span className="font-sans text-sm">
                      {item.location}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-8 p-4 bg-luxury-black/50 border border-luxury-gold/30 rounded">
          <p className="text-luxury-champagne/70 font-serif text-sm italic text-center">
            Times are approximate and subject to the natural flow of the evening
          </p>
        </div>
      </div>
    </AnimatedEntrance>
  );
};

export default Schedule;