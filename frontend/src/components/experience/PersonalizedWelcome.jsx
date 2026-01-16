import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { formatMembershipTier } from '../../utils/helpers';
import AnimatedEntrance from '../common/AnimatedEntrance';

const PersonalizedWelcome = () => {
  const { member } = useAuth();
  
  if (!member) return null;
  
  return (
    <AnimatedEntrance animation="slideUp" duration={0.8}>
      <div className="card-luxury mb-8">
        <div className="text-center">
          {/* Greeting */}
          <h1 className="heading-luxury text-4xl md:text-5xl mb-4">
            Welcome Back, {member.full_name}
          </h1>
          
          {/* Personal Message */}
          <p className="subheading-luxury text-xl mb-6">
            I'm so glad you're here
          </p>
          
          {/* Divider */}
          <div className="divider-luxury" />
          
          {/* Member Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            {/* Membership Tier */}
            <div className="text-center">
              <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-2">
                Membership
              </p>
              <p className="text-luxury-gold font-serif text-xl">
                {formatMembershipTier(member.membership_tier)}
              </p>
            </div>
            
            {/* Member Number */}
            <div className="text-center">
              <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-2">
                Member Number
              </p>
              <p className="text-luxury-gold font-serif text-xl">
                {member.membership_number}
              </p>
            </div>
          </div>
          
          {/* Personal Note */}
          <div className="mt-8 p-6 bg-luxury-black/50 border border-luxury-gold/30 rounded">
            <p className="text-luxury-champagne font-serif italic text-base leading-relaxed">
              "Your presence makes this circle truly special. I've prepared 
              something extraordinary for our time together."
            </p>
            <p className="text-luxury-gold font-elegant text-2xl mt-4">
              — Paige
            </p>
          </div>
        </div>
      </div>
    </AnimatedEntrance>
  );
};

export default PersonalizedWelcome;