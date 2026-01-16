import React from 'react';
import { useNavigate } from 'react-router-dom';
import AnimatedEntrance from '../common/AnimatedEntrance';
import Button from '../common/Button';

const HeroSection = () => {
  const navigate = useNavigate();
  
  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-luxury-black via-luxury-off-black to-luxury-black" />
      
      {/* Subtle Pattern Overlay */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle, #D4AF37 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }} />
      </div>
      
      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-5xl mx-auto">
        <AnimatedEntrance animation="fade" duration={1} delay={0.2}>
          {/* Main Title */}
          <h1 className="heading-luxury text-5xl md:text-7xl lg:text-8xl mb-6">
            Paige's Inner Circle
          </h1>
        </AnimatedEntrance>
        
        <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
          {/* Subtitle */}
          <p className="subheading-luxury text-2xl md:text-3xl lg:text-4xl mb-8">
            An Exclusive Invitation
          </p>
        </AnimatedEntrance>
        
        <AnimatedEntrance animation="slideUp" duration={0.8} delay={1}>
          {/* Description */}
          <p className="text-luxury-champagne font-serif text-lg md:text-xl max-w-3xl mx-auto mb-12 leading-relaxed">
            You have been personally selected for an unforgettable evening
            of elegance, sophistication, and celebration.
          </p>
        </AnimatedEntrance>
        
        <AnimatedEntrance animation="scale" duration={0.6} delay={1.4}>
          {/* CTA Button */}
          <Button
            variant="primary"
            size="large"
            onClick={() => navigate('/access')}
          >
            Access Your Invitation
          </Button>
        </AnimatedEntrance>
        
        {/* Signature */}
        <AnimatedEntrance animation="fade" duration={0.8} delay={1.8}>
          <div className="mt-16">
            <p className="font-elegant text-luxury-gold text-3xl italic">
              — Paige
            </p>
          </div>
        </AnimatedEntrance>
      </div>
      
      {/* Bottom Fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-luxury-black to-transparent" />
    </section>
  );
};

export default HeroSection;