import React from 'react';
import AnimatedEntrance from '../common/AnimatedEntrance';

const PaigeMessage = () => {
  return (
    <section className="py-20 px-6 bg-luxury-off-black">
      <div className="max-w-4xl mx-auto">
        <AnimatedEntrance animation="slideUp" duration={0.8}>
          {/* Border Frame */}
          <div className="border-2 border-luxury-gold p-8 md:p-12 relative">
            {/* Corner Decorations */}
            <div className="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-luxury-gold" />
            <div className="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-luxury-gold" />
            <div className="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-luxury-gold" />
            <div className="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-luxury-gold" />
            
            {/* Message Content */}
            <div className="text-center">
              <h2 className="font-elegant text-luxury-gold text-3xl md:text-4xl mb-6">
                A Personal Note
              </h2>
              
              <div className="space-y-6 text-luxury-champagne font-serif text-lg leading-relaxed">
                <p>
                  My dearest friend,
                </p>
                
                <p>
                  This evening is more than just an event—it's a celebration 
                  of the extraordinary journey we've shared and the incredible 
                  community we've built together.
                </p>
                
                <p>
                  I've carefully curated every moment to create an experience 
                  that reflects the elegance, warmth, and genuine connection 
                  that defines our Inner Circle.
                </p>
                
                <p>
                  Your presence would make this evening truly complete.
                </p>
                
                <p className="italic text-luxury-gold mt-8">
                  With anticipation and gratitude,
                </p>
                
                <p className="font-elegant text-luxury-gold text-3xl mt-4">
                  Paige
                </p>
              </div>
            </div>
          </div>
        </AnimatedEntrance>
      </div>
    </section>
  );
};

export default PaigeMessage;