import React from 'react';
import { useNavigate } from 'react-router-dom';
import AnimatedEntrance from '../common/AnimatedEntrance';
import ConfettiAnimation from '../common/ConfettiAnimation';
import Button from '../common/Button';
import { FiCheckCircle, FiGift } from 'react-icons/fi';

const AcceptFlow = ({ token }) => {
  const navigate = useNavigate();
  
  return (
    <div>
      {/* Confetti Animation */}
      <ConfettiAnimation active={true} duration={5000} />
      
      <AnimatedEntrance animation="scale" duration={0.8}>
        <div className="text-center py-12">
          {/* Success Icon */}
          <div className="mb-8">
            <FiCheckCircle className="text-luxury-gold text-7xl mx-auto animate-bounce" />
          </div>
          
          {/* Success Message */}
          <h2 className="heading-luxury text-4xl md:text-5xl mb-6">
            Wonderful!
          </h2>
          
          <div className="max-w-2xl mx-auto space-y-6 mb-12">
            <p className="subheading-luxury text-2xl">
              I can't wait to share this moment with you
            </p>
            
            <p className="text-luxury-champagne font-serif text-lg leading-relaxed">
              Your Legacy Pass has been generated and is ready for you. 
              Complete your $1,000 investment to unlock full access and receive 
              your exclusive gifts.
            </p>
            
            <div className="border-l-4 border-luxury-gold pl-6 py-4 bg-luxury-black/50 text-left">
              <p className="text-luxury-champagne font-serif italic text-base">
                "This evening will be one we remember forever. Thank you for 
                being part of something truly special."
              </p>
              <p className="text-luxury-gold font-elegant text-2xl mt-4">
                — Paige
              </p>
            </div>
          </div>
          
          {/* Next Steps */}
          <div className="card-luxury inline-block text-left max-w-xl mb-8">
            <h3 className="font-elegant text-luxury-gold text-2xl mb-4 text-center">
              What's Next
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-luxury-gold flex items-center justify-center text-luxury-black font-bold">
                  1
                </div>
                <div>
                  <p className="text-luxury-off-white font-serif">
                    View your blurred Legacy Pass preview
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-luxury-gold flex items-center justify-center text-luxury-black font-bold">
                  2
                </div>
                <div>
                  <p className="text-luxury-off-white font-serif">
                    Complete your $1,000 investment
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-luxury-gold flex items-center justify-center text-luxury-black font-bold">
                  3
                </div>
                <div>
                  <p className="text-luxury-off-white font-serif">
                    Access your full Legacy Pass with QR code
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-luxury-gold flex items-center justify-center text-luxury-black font-bold">
                  4
                </div>
                <div>
                  <p className="text-luxury-off-white font-serif">
                    Present your pass at the event entrance
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* CTA Button */}
          <Button
            variant="primary"
            size="large"
            onClick={() => navigate('/legacy-pass')}
            icon={<FiGift />}
          >
            View Your Legacy Pass
          </Button>
        </div>
      </AnimatedEntrance>
    </div>
  );
};

export default AcceptFlow;