import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import AnimatedEntrance from '../common/AnimatedEntrance';
import { FiCheck } from 'react-icons/fi';

const AmenitiesList = ({ eventId }) => {
  const [amenities, setAmenities] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    if (eventId) {
      fetchAmenities();
    }
  }, [eventId]);
  
  const fetchAmenities = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.EVENTS.AMENITIES(eventId));
      setAmenities(response.data);
    } catch (error) {
      console.error('Failed to fetch amenities:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return null;
  }
  
  if (!amenities || amenities.length === 0) {
    return null;
  }
  
  // Group amenities by category
  const groupedAmenities = amenities.reduce((acc, amenity) => {
    const category = amenity.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(amenity);
    return acc;
  }, {});
  
  return (
    <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
      <div className="card-luxury mb-8">
        <h2 className="font-elegant text-luxury-gold text-3xl mb-8">
          Exclusive Amenities
        </h2>
        
        <div className="space-y-8">
          {Object.entries(groupedAmenities).map(([category, items], categoryIndex) => (
            <div key={categoryIndex}>
              {/* Category Title */}
              <h3 className="text-luxury-champagne font-sans uppercase tracking-wider text-sm mb-4">
                {category}
              </h3>
              
              {/* Amenities Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {items.map((amenity, index) => (
                  <div 
                    key={amenity.id} 
                    className="flex items-start gap-3 p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded hover:border-luxury-gold/40 transition-colors"
                  >
                    <FiCheck className="text-luxury-gold flex-shrink-0 mt-1" size={20} />
                    <div>
                      <p className="text-luxury-off-white font-serif text-base">
                        {amenity.name}
                      </p>
                      {amenity.description && (
                        <p className="text-luxury-champagne/70 font-serif text-sm mt-1">
                          {amenity.description}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-8 p-6 bg-luxury-black/50 border border-luxury-gold/30 rounded">
          <p className="text-luxury-champagne font-serif italic text-center">
            Every detail has been thoughtfully curated to ensure your complete comfort and enjoyment
          </p>
        </div>
      </div>
    </AnimatedEntrance>
  );
};

export default AmenitiesList;