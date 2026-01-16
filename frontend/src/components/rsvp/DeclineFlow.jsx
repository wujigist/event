import React from 'react';
import { useNavigate } from 'react-router-dom';
import AnimatedEntrance from '../common/AnimatedEntrance';
import Button from '../common/Button';

const DeclineFlow = () => {
  const navigate = useNavigate();
  
  return (
    <AnimatedEntrance animation="fade" duration={0.8}>
      <div className="text-center py-12">
        {/* Thank You Message */}
        <h2 className="heading-luxury text-4xl md:text-5xl mb-6">
          Thank You
        </h2>
        
        <div className="max-w-2xl mx-auto space-y-6 mb-12">
          <p className="text-luxury-champagne font-serif text-lg leading-relaxed">
            While we're disappointed you won't be able to join us, we completely 
            understand. Your place in the Inner Circle remains secure.
          </p>
          
          <div className="card-luxury bg-luxury-black/50 p-8">
            <p className="text-luxury-champagne font-serif italic text-base leading-relaxed">
              "Though you won't be with us physically, you'll be in our thoughts 
              throughout the evening. I hope we'll have another opportunity to 
              celebrate together soon."
            </p>
            <p className="text-luxury-gold font-elegant text-2xl mt-6">
              — Paige
            </p>
          </div>
          
          <p className="text-luxury-champagne/80 font-serif text-base">
            You'll receive early access to future exclusive events and gatherings.
          </p>
        </div>
        
        {/* Digital Appreciation Card */}
        <div className="card-luxury max-w-xl mx-auto mb-8">
          <h3 className="font-elegant text-luxury-gold text-2xl mb-4">
            Until We Meet Again
          </h3>
          
          <div className="space-y-4 text-left">
            <p className="text-luxury-champagne font-serif text-base">
              As a token of our appreciation for your continued membership:
            </p>
            
            <ul className="space-y-2 text-luxury-champagne/80 font-serif text-sm">
              <li>✨ Priority access to our next gathering</li>
              <li>✨ Exclusive updates and behind-the-scenes content</li>
              <li>✨ Special consideration for future VIP experiences</li>
            </ul>
          </div>
        </div>
        
        {/* Return to Dashboard */}
        <Button
          variant="secondary"
          onClick={() => navigate('/dashboard')}
        >
          Return to Dashboard
        </Button>
      </div>
    </AnimatedEntrance>
  );
};

export default DeclineFlow;