import React from 'react';
import HeroSection from '../../components/landing/HeroSection';
import PaigeMessage from '../../components/landing/PaigeMessage';
import EventTeaser from '../../components/landing/EventTeaser';
import Footer from '../../components/layout/Footer';

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <HeroSection />
      <PaigeMessage />
      <EventTeaser />
      <Footer />
    </div>
  );
};

export default LandingPage;