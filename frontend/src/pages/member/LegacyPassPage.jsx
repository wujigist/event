import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import BlurredPassCard from '../../components/legacy-pass/BlurredPassCard';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { FiLock, FiDollarSign } from 'react-icons/fi';

const LegacyPassPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rsvp, setRsvp] = useState(null);
  const [passPreview, setPassPreview] = useState(null);
  const [paymentStatus, setPaymentStatus] = useState(null);
  
  useEffect(() => {
    fetchPassData();
  }, []);
  
  const fetchPassData = async () => {
    try {
      // Get RSVP with token
      const rsvpResponse = await api.get(API_ENDPOINTS.RSVP.ME);
      console.log('RSVP Response:', rsvpResponse.data);
      
      const data = rsvpResponse.data;
      
      // Check if there's an RSVP
      if (!data.has_rsvp) {
        setError('not_accepted');
        setLoading(false);
        return;
      }
      
      // Check if user has accepted (rsvp_status is at the top level)
      if (data.rsvp_status !== 'accepted') {
        setError('not_accepted');
        setLoading(false);
        return;
      }
      
      // Set the full data as rsvp
      setRsvp(data);
      
      // Get token from top level of response
      const token = data.legacy_pass_token;
      
      if (!token) {
        console.error('No token found in response. Full data:', data);
        setError('no_token');
        setLoading(false);
        return;
      }
      
      console.log('Legacy Pass Token:', token);
      
      // Get pass preview
      try {
        const previewResponse = await api.get(
          API_ENDPOINTS.LEGACY_PASS.PREVIEW(token)
        );
        console.log('Pass Preview:', previewResponse.data);
        setPassPreview(previewResponse.data);
      } catch (err) {
        console.error('Failed to fetch pass preview:', err);
        setError('preview_failed');
      }
      
      // Check payment status
      try {
        const paymentResponse = await api.get(
          API_ENDPOINTS.PAYMENT.STATUS(token)
        );
        console.log('Payment Status:', paymentResponse.data);
        setPaymentStatus(paymentResponse.data.status);
      } catch (err) {
        console.error('Failed to fetch payment status:', err);
        // Payment status check failing is OK - might not exist yet
        setPaymentStatus('pending');
      }
    } catch (error) {
      console.error('Failed to fetch pass data:', error);
      setError('fetch_failed');
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  // Error states
  if (error === 'not_accepted' || !rsvp || rsvp.rsvp_status !== 'accepted') {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center px-6">
          <div className="text-center max-w-md">
            <h1 className="heading-luxury text-4xl mb-4">RSVP Required</h1>
            <p className="text-luxury-champagne font-serif mb-8">
              You need to accept your RSVP first to access your Legacy Pass.
            </p>
            <Button
              variant="primary"
              onClick={() => navigate('/rsvp')}
            >
              Go to RSVP
            </Button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
  
  if (error === 'no_token') {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center px-6">
          <div className="text-center max-w-md">
            <h1 className="heading-luxury text-4xl mb-4">Pass Being Generated</h1>
            <p className="text-luxury-champagne font-serif mb-8">
              Your Legacy Pass is being generated. Please check back in a moment or contact support if this persists.
            </p>
            <div className="flex gap-4 justify-center">
              <Button
                variant="secondary"
                onClick={() => window.location.reload()}
              >
                Refresh Page
              </Button>
              <Button
                variant="primary"
                onClick={() => navigate('/dashboard')}
              >
                Back to Dashboard
              </Button>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
  
  // Payment verified - redirect to full pass
  if (paymentStatus === 'verified') {
    navigate(`/pass/${rsvp.legacy_pass_token}`);
    return null;
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
                Your Legacy Pass
              </h1>
              <p className="subheading-luxury text-xl">
                Preview Only - Payment Required
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Pass Preview */}
          {passPreview ? (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
              <BlurredPassCard pass={passPreview} />
            </AnimatedEntrance>
          ) : (
            <div className="card-luxury text-center">
              <p className="text-luxury-champagne font-serif">
                Loading your pass preview...
              </p>
            </div>
          )}
          
          {/* Payment Notice */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
            <div className="card-luxury mt-8">
              <div className="flex items-start gap-4 mb-6">
                <FiLock className="text-luxury-gold text-3xl flex-shrink-0 mt-1" />
                <div>
                  <h2 className="font-elegant text-luxury-gold text-2xl mb-3">
                    Complete Your Investment
                  </h2>
                  <p className="text-luxury-champagne font-serif text-base leading-relaxed mb-4">
                    Your Legacy Pass has been generated and is ready for you. 
                    To unlock full access and receive your exclusive gifts, 
                    please complete your $1,000 donation to our charity.
                  </p>
                </div>
              </div>
              
              {/* What's Included */}
              <div className="border-t border-luxury-gold/30 pt-6 mt-6">
                <h3 className="text-luxury-champagne font-sans uppercase tracking-wider text-sm mb-4">
                  What's Included
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-luxury-gold flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-luxury-black font-bold text-xs">✓</span>
                    </div>
                    <p className="text-luxury-off-white font-serif">
                      Full access to exclusive evening event
                    </p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-luxury-gold flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-luxury-black font-bold text-xs">✓</span>
                    </div>
                    <p className="text-luxury-off-white font-serif">
                      Curated luxury gift collection
                    </p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-luxury-gold flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-luxury-black font-bold text-xs">✓</span>
                    </div>
                    <p className="text-luxury-off-white font-serif">
                      VIP seating and amenities
                    </p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-luxury-gold flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-luxury-black font-bold text-xs">✓</span>
                    </div>
                    <p className="text-luxury-off-white font-serif">
                      Collectible Legacy Pass with QR code
                    </p>
                  </div>
                </div>
              </div>
              
              {/* CTA */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
                <Button
                  variant="primary"
                  size="large"
                  onClick={() => navigate('/payment')}
                  icon={<FiDollarSign />}
                >
                  Complete Payment ($1,000)
                </Button>
              </div>
            </div>
          </AnimatedEntrance>
          
          {/* Security Notice */}
          <AnimatedEntrance animation="fade" duration={0.8} delay={0.6}>
            <div className="text-center mt-8">
              <p className="text-luxury-champagne/70 font-serif text-sm italic">
                Your pass is secured and waiting. Complete payment to unlock full access.
              </p>
            </div>
          </AnimatedEntrance>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default LegacyPassPage;