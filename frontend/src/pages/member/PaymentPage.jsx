import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS, PAYMENT_AMOUNT } from '../../utils/constants';
import { formatCurrency } from '../../utils/helpers';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import PaymentMethods from '../../components/payment/PaymentMethods';
import ContactForm from '../../components/payment/ContactForm';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { FiCheckCircle } from 'react-icons/fi';

const PaymentPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [rsvp, setRsvp] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [showContactForm, setShowContactForm] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  
  useEffect(() => {
    checkAccess();
  }, []);
  
  const checkAccess = async () => {
    try {
      // Check RSVP status
      const rsvpResponse = await api.get(API_ENDPOINTS.RSVP.ME);
      const data = rsvpResponse.data;
      
      // Check if user has RSVP and accepted
      if (!data.has_rsvp || data.rsvp_status !== 'accepted') {
        navigate('/rsvp');
        return;
      }
      
      // Check if token exists
      if (!data.legacy_pass_token) {
        navigate('/rsvp');
        return;
      }
      
      setRsvp(data);
      
      // Check if already paid
      try {
        const paymentResponse = await api.get(
          API_ENDPOINTS.PAYMENT.STATUS(data.legacy_pass_token)
        );
        
        if (paymentResponse.data.status === 'verified') {
          // Already paid, redirect to full pass
          navigate(`/pass/${data.legacy_pass_token}`);
          return;
        }
      } catch (err) {
        // Payment check failed - that's OK, they probably haven't paid yet
        console.log('Payment not found, continuing...');
      }
    } catch (error) {
      console.error('Failed to check access:', error);
      navigate('/rsvp');
    } finally {
      setLoading(false);
    }
  };
  
  const handleMethodSelect = (method) => {
    setSelectedMethod(method);
    setShowContactForm(true);
  };
  
  const handleContactSubmit = async (contactData) => {
    setSubmitting(true);
    
    try {
      await api.post(API_ENDPOINTS.PAYMENT.CONTACT, {
        legacy_token: rsvp.legacy_pass_token,
        contact_email: contactData.email,
        payment_method: selectedMethod
      });
      
      setSubmitted(true);
    } catch (error) {
      console.error('Failed to submit contact:', error);
      alert('An error occurred. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Title */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="text-center mb-12">
              <h1 className="heading-luxury text-5xl mb-4">
                Complete Your Investment
              </h1>
              <p className="subheading-luxury text-2xl mb-6">
                {formatCurrency(PAYMENT_AMOUNT)}
              </p>
              <p className="text-luxury-champagne font-serif text-base max-w-2xl mx-auto">
                Secure your place at this exclusive evening and unlock your complete Legacy Pass
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Success State */}
          {submitted && (
            <AnimatedEntrance animation="scale" duration={0.8}>
              <div className="card-luxury text-center">
                <div className="mb-6">
                  <FiCheckCircle className="text-green-400 text-6xl mx-auto" />
                </div>
                
                <h2 className="heading-luxury text-4xl mb-4">
                  Request Received
                </h2>
                
                <p className="text-luxury-champagne font-serif text-lg leading-relaxed mb-6">
                  Thank you! We've received your payment request and will contact you 
                  within 24 hours with detailed payment instructions.
                </p>
                
                <div className="p-6 bg-luxury-black/50 border border-luxury-gold/30 rounded mb-8">
                  <h3 className="text-luxury-gold font-sans font-bold text-lg mb-3">
                    What Happens Next
                  </h3>
                  <div className="space-y-3 text-luxury-champagne font-serif text-base text-left">
                    <p>✓ You'll receive an email confirmation shortly</p>
                    <p>✓ Our team will reach out within 24 hours</p>
                    <p>✓ Complete payment using your selected method</p>
                    <p>✓ Access your full Legacy Pass immediately</p>
                  </div>
                </div>
                
                <p className="text-luxury-champagne/70 font-serif text-sm italic">
                  You can close this page. We'll notify you via email when it's time for the next step.
                </p>
              </div>
            </AnimatedEntrance>
          )}
          
          {/* Payment Flow */}
          {!submitted && (
            <div>
              {/* Investment Details */}
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
                <div className="card-luxury mb-8">
                  <h2 className="font-elegant text-luxury-gold text-2xl mb-6">
                    Your Donation Contribution gives you benefits that includes
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
                      <h4 className="text-luxury-gold font-sans font-bold mb-2">
                        Exclusive Event Access
                      </h4>
                      <p className="text-luxury-champagne/80 font-serif text-sm">
                        Full access to an evening of luxury and elegance
                      </p>
                    </div>
                    
                    <div className="p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
                      <h4 className="text-luxury-gold font-sans font-bold mb-2">
                        Curated Gift Collection
                      </h4>
                      <p className="text-luxury-champagne/80 font-serif text-sm">
                        Carefully selected luxury gifts based on your tier
                      </p>
                    </div>
                    
                    <div className="p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
                      <h4 className="text-luxury-gold font-sans font-bold mb-2">
                        VIP Treatment
                      </h4>
                      <p className="text-luxury-champagne/80 font-serif text-sm">
                        Premium seating, exclusive amenities, and special services
                      </p>
                    </div>
                    
                    <div className="p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
                      <h4 className="text-luxury-gold font-sans font-bold mb-2">
                        Legacy Pass
                      </h4>
                      <p className="text-luxury-champagne/80 font-serif text-sm">
                        Collectible pass with QR code and digital certificate
                      </p>
                    </div>
                  </div>
                </div>
              </AnimatedEntrance>
              
              {/* Payment Method Selection */}
              {!showContactForm && (
                <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
                  <div className="card-luxury">
                    <PaymentMethods
                      selectedMethod={selectedMethod}
                      onSelect={handleMethodSelect}
                    />
                  </div>
                </AnimatedEntrance>
              )}
              
              {/* Contact Form */}
              {showContactForm && (
                <AnimatedEntrance animation="slideUp" duration={0.8}>
                  <div className="card-luxury">
                    <ContactForm
                      paymentMethod={selectedMethod}
                      onSubmit={handleContactSubmit}
                      loading={submitting}
                    />
                  </div>
                </AnimatedEntrance>
              )}
            </div>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default PaymentPage;