import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import FullPassCard from '../../components/legacy-pass/FullPassCard';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { FiDownload, FiCheckCircle } from 'react-icons/fi';
import { downloadFile } from '../../utils/helpers';

const PassAccessPage = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [pass, setPass] = useState(null);
  const [event, setEvent] = useState(null);
  const [paymentStatus, setPaymentStatus] = useState(null);
  const [benefits, setBenefits] = useState([]);
  
  useEffect(() => {
    if (token) {
      fetchFullPass();
    }
  }, [token]);
  
  const fetchFullPass = async () => {
    try {
      // Check payment status first
      const paymentResponse = await api.get(API_ENDPOINTS.PAYMENT.STATUS(token));
      setPaymentStatus(paymentResponse.data.status);
      
      if (paymentResponse.data.status !== 'verified') {
        // Redirect back to preview if not paid
        navigate('/legacy-pass');
        return;
      }
      
      // Get full pass
      const passResponse = await api.get(API_ENDPOINTS.LEGACY_PASS.FULL(token));
      setPass(passResponse.data);
      
      // Get event details
      const eventResponse = await api.get(API_ENDPOINTS.EVENTS.CURRENT);
      setEvent(eventResponse.data);
      
      // Get benefits
      const benefitsResponse = await api.get(API_ENDPOINTS.LEGACY_PASS.BENEFITS(token));
      setBenefits(benefitsResponse.data.benefits || []);
    } catch (error) {
      console.error('Failed to fetch full pass:', error);
      if (error.status === 402) {
        // Payment required
        navigate('/legacy-pass');
      }
    } finally {
      setLoading(false);
    }
  };
  
  const handleDownloadPDF = async () => {
    try {
      const response = await api.get(
        API_ENDPOINTS.LEGACY_PASS.DOWNLOAD_PDF(token),
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      downloadFile(url, `Legacy_Pass_${pass.pass_number}.pdf`);
    } catch (error) {
      console.error('Failed to download PDF:', error);
      alert('Failed to download. Please try again.');
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  if (!pass) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="heading-luxury text-4xl mb-4">Pass Not Found</h1>
            <p className="text-luxury-champagne font-serif">
              This pass could not be accessed.
            </p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Success Message */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="text-center mb-8">
              <div className="inline-block mb-4">
                <FiCheckCircle className="text-green-400 text-6xl" />
              </div>
              <h1 className="heading-luxury text-5xl mb-4">
                Your Pass Is Ready
              </h1>
              <p className="subheading-luxury text-xl">
                Everything you need for an unforgettable evening
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Full Pass Cards */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
            <FullPassCard pass={pass} event={event} />
          </AnimatedEntrance>
          
          {/* Download Options */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
            <div className="card-luxury mt-8">
              <h2 className="font-elegant text-luxury-gold text-2xl mb-6 text-center">
                Download Your Pass
              </h2>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  variant="primary"
                  onClick={handleDownloadPDF}
                  icon={<FiDownload />}
                >
                  Download PDF
                </Button>
              </div>
              
              <p className="text-center text-luxury-champagne/70 font-serif text-sm mt-6">
                Save your pass to your device for easy access on event day
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Benefits */}
          {benefits && benefits.length > 0 && (
            <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
              <div className="card-luxury mt-8">
                <h2 className="font-elegant text-luxury-gold text-2xl mb-6">
                  Your Exclusive Benefits
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {benefits.map((benefit, index) => (
                    <div 
                      key={index}
                      className="flex items-start gap-3 p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded"
                    >
                      <div className="w-6 h-6 rounded-full bg-luxury-gold flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-luxury-black font-bold text-xs">✓</span>
                      </div>
                      <p className="text-luxury-off-white font-serif text-base">
                        {benefit}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </AnimatedEntrance>
          )}
          
          {/* Event Day Instructions */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.8}>
            <div className="card-luxury mt-8 bg-luxury-black/50">
              <h3 className="font-elegant text-luxury-gold text-xl mb-4 text-center">
                Event Day Instructions
              </h3>
              
              <div className="space-y-4 text-luxury-champagne font-serif text-base">
                <div className="flex items-start gap-3">
                  <span className="text-luxury-gold font-bold">1.</span>
                  <p>Bring your phone with this digital pass or a printed copy</p>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-luxury-gold font-bold">2.</span>
                  <p>Present the QR code at the entrance for scanning</p>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-luxury-gold font-bold">3.</span>
                  <p>Arrive 30 minutes early for check-in and gift collection</p>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-luxury-gold font-bold">4.</span>
                  <p>Enjoy an unforgettable evening!</p>
                </div>
              </div>
            </div>
          </AnimatedEntrance>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default PassAccessPage;