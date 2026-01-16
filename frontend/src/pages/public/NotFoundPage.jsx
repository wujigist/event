import React from 'react';
import { useNavigate } from 'react-router-dom';
import AnimatedEntrance from '../components/common/AnimatedEntrance';
import Button from '../components/common/Button';
import Footer from '../components/layout/Footer';
import { FiHome, FiMail } from 'react-icons/fi';

const NotFoundPage = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen flex flex-col">
      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="max-w-2xl mx-auto text-center">
          <AnimatedEntrance animation="fade" duration={0.8}>
            {/* Decorative Element */}
            <div className="mb-8">
              <div className="inline-block p-8 border-2 border-luxury-gold rounded-full">
                <span className="text-luxury-gold font-elegant text-8xl">404</span>
              </div>
            </div>
            
            {/* Title */}
            <h1 className="heading-luxury text-5xl md:text-6xl mb-6">
              Lost Your Way?
            </h1>
            
            {/* Subtitle */}
            <p className="subheading-luxury text-2xl mb-8">
              This page seems to have wandered off
            </p>
            
            {/* Description */}
            <p className="text-luxury-champagne font-serif text-lg leading-relaxed mb-12 max-w-xl mx-auto">
              The page you're looking for doesn't exist or may have been moved. 
              Let's get you back to somewhere more familiar and elegant.
            </p>
            
            {/* Divider */}
            <div className="divider-luxury mb-12" />
            
            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                variant="primary"
                size="large"
                onClick={() => navigate('/')}
                icon={<FiHome />}
              >
                Return Home
              </Button>
              
              <Button
                variant="secondary"
                size="large"
                onClick={() => window.location.href = 'mailto:contact@paigeinnercircle.com'}
                icon={<FiMail />}
              >
                Contact Support
              </Button>
            </div>
            
            {/* Helpful Links */}
            <div className="mt-12 pt-8 border-t border-luxury-gold/30">
              <p className="text-luxury-champagne/70 font-sans text-sm uppercase tracking-wider mb-4">
                Looking for something specific?
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <button
                  onClick={() => navigate('/access')}
                  className="text-luxury-gold hover:text-luxury-dark-gold font-serif text-base transition-colors"
                >
                  Member Access
                </button>
                <span className="text-luxury-champagne/30">•</span>
                <button
                  onClick={() => navigate('/dashboard')}
                  className="text-luxury-gold hover:text-luxury-dark-gold font-serif text-base transition-colors"
                >
                  Dashboard
                </button>
                <span className="text-luxury-champagne/30">•</span>
                <a
                  href="mailto:contact@paigeinnercircle.com"
                  className="text-luxury-gold hover:text-luxury-dark-gold font-serif text-base transition-colors"
                >
                  Contact Us
                </a>
              </div>
            </div>
          </AnimatedEntrance>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default NotFoundPage;