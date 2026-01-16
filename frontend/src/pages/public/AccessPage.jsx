import React from 'react';
import EmailAccessForm from '../../components/auth/EmailAccessForm';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import Footer from '../../components/layout/Footer';

const AccessPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-2xl">
          <AnimatedEntrance animation="fade" duration={0.8}>
            {/* Decorative Border */}
            <div className="border-2 border-luxury-gold p-8 md:p-12 bg-luxury-off-black/50 backdrop-blur-sm">
              <EmailAccessForm />
            </div>
          </AnimatedEntrance>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AccessPage;