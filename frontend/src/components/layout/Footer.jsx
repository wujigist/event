import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-luxury-black border-t border-luxury-gold/30 py-8 px-6 mt-auto">
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          {/* Brand */}
          <h3 className="font-elegant text-luxury-gold text-xl mb-4">
            Paige's Inner Circle
          </h3>
          
          {/* Tagline */}
          <p className="text-luxury-champagne font-serif italic text-sm mb-6">
            An Exclusive Experience of Elegance & Excellence
          </p>
          
          {/* Divider */}
          <div className="border-t border-luxury-gold/30 my-6 max-w-md mx-auto" />
          
          {/* Copyright */}
          <p className="text-luxury-champagne/70 font-sans text-xs">
            © {currentYear} Paige's Inner Circle. All rights reserved.
          </p>
          
          {/* Contact Info (optional) */}
          <p className="text-luxury-champagne/70 font-sans text-xs mt-2">
            For inquiries: <a href="mailto:contact@paigeinnercircle.com" className="text-luxury-gold hover:text-luxury-dark-gold transition-colors">
              contact@paigeinnercircle.com
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;