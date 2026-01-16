import React from 'react';
import AnimatedEntrance from '../common/AnimatedEntrance';

const EventDetails = ({ event }) => {
  if (!event) return null;
  
  return (
    <AnimatedEntrance animation="slideUp" duration={0.8}>
      <div className="card-luxury mb-8">
        <h2 className="font-elegant text-luxury-gold text-3xl mb-6">
          About This Evening
        </h2>
        
        {/* Event Description */}
        {event.description && (
          <div className="text-luxury-champagne font-serif text-lg leading-relaxed mb-8">
            {event.description.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-4">
                {paragraph}
              </p>
            ))}
          </div>
        )}
        
        {/* Paige's Personal Note */}
        <div className="border-l-4 border-luxury-gold pl-6 py-4 bg-luxury-black/50">
          <p className="text-luxury-champagne font-serif italic text-base leading-relaxed">
            "This evening is about celebrating not just where we've been, but where 
            we're going together. Every detail has been chosen with care to create 
            moments that will stay with you long after the last toast."
          </p>
          <p className="text-luxury-gold font-elegant text-xl mt-4">
            — Paige
          </p>
        </div>
      </div>
    </AnimatedEntrance>
  );
};

export default EventDetails;