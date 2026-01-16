import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import { formatCurrency, formatDate, timeAgo } from '../../utils/helpers';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import { FiDollarSign, FiCheck, FiClock, FiMail, FiPhone } from 'react-icons/fi';

const PaymentVerification = () => {
  const [loading, setLoading] = useState(true);
  const [payments, setPayments] = useState([]);
  const [filter, setFilter] = useState('pending'); // 'all', 'pending', 'verified'
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [verifying, setVerifying] = useState(false);
  const [showVerifyModal, setShowVerifyModal] = useState(false);
  
  useEffect(() => {
    fetchPayments();
  }, [filter]);
  
  const fetchPayments = async () => {
    try {
      setLoading(true);
      const endpoint = filter === 'pending' 
        ? API_ENDPOINTS.PAYMENT.PENDING 
        : `${API_ENDPOINTS.PAYMENT.ALL}?status=${filter === 'all' ? '' : filter}`;
      
      const response = await api.get(endpoint);
      setPayments(response.data);
    } catch (error) {
      console.error('Failed to fetch payments:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleVerifyClick = (payment) => {
    setSelectedPayment(payment);
    setShowVerifyModal(true);
  };
  
  const confirmVerify = async () => {
    setVerifying(true);
    
    try {
      await api.post(API_ENDPOINTS.PAYMENT.VERIFY, {
        payment_id: selectedPayment.id,
      });
      
      // Refresh payments list
      await fetchPayments();
      
      setShowVerifyModal(false);
      setSelectedPayment(null);
      
      alert('Payment verified successfully! Member now has full pass access.');
    } catch (error) {
      console.error('Failed to verify payment:', error);
      alert('Failed to verify payment. Please try again.');
    } finally {
      setVerifying(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Title */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="mb-8">
              <h1 className="heading-luxury text-5xl mb-4">
                Payment Verification
              </h1>
              <p className="subheading-luxury text-xl">
                Verify member payments to unlock full pass access
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Filter Tabs */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
            <div className="flex gap-4 mb-8">
              <button
                onClick={() => setFilter('pending')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'pending'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                Pending ({payments.filter(p => p.status === 'pending').length})
              </button>
              
              <button
                onClick={() => setFilter('verified')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'verified'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                Verified
              </button>
              
              <button
                onClick={() => setFilter('all')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'all'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                All
              </button>
            </div>
          </AnimatedEntrance>
          
          {/* Payments List */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
            <div className="space-y-4">
              {payments.length === 0 ? (
                <div className="card-luxury text-center py-12">
                  <p className="text-luxury-champagne font-serif text-lg">
                    No payments found
                  </p>
                </div>
              ) : (
                payments.map((payment) => (
                  <div key={payment.id} className="card-luxury">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
                      {/* Payment Info */}
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <FiDollarSign className="text-luxury-gold text-2xl" />
                          <h3 className="text-luxury-off-white font-sans text-xl font-bold">
                            {payment.member_name}
                          </h3>
                          <span className={`
                            px-3 py-1 rounded-full text-xs font-sans font-bold uppercase
                            ${payment.status === 'verified' 
                              ? 'bg-green-400/20 text-green-400' 
                              : 'bg-yellow-400/20 text-yellow-400'
                            }
                          `}>
                            {payment.status}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              Amount
                            </p>
                            <p className="text-luxury-gold font-serif text-lg font-bold">
                              {formatCurrency(payment.amount)}
                            </p>
                          </div>
                          
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              Payment Method
                            </p>
                            <p className="text-luxury-off-white font-serif">
                              {payment.payment_method?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </p>
                          </div>
                          
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              <FiMail className="inline mr-1" size={12} />
                              Contact Email
                            </p>
                            <p className="text-luxury-off-white font-serif">
                              {payment.contact_email}
                            </p>
                          </div>
                          
                          {payment.contact_phone && (
                            <div>
                              <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                                <FiPhone className="inline mr-1" size={12} />
                                Phone
                              </p>
                              <p className="text-luxury-off-white font-serif">
                                {payment.contact_phone}
                              </p>
                            </div>
                          )}
                        </div>
                        
                        <div className="text-luxury-champagne/70 font-sans text-sm">
                          <FiClock className="inline mr-1" size={14} />
                          Submitted {timeAgo(payment.created_at)}
                        </div>
                        
                        {payment.verified_at && (
                          <div className="text-green-400/70 font-sans text-sm mt-2">
                            <FiCheck className="inline mr-1" size={14} />
                            Verified {timeAgo(payment.verified_at)}
                          </div>
                        )}
                      </div>
                      
                      {/* Actions */}
                      <div>
                        {payment.status === 'pending' && (
                          <Button
                            variant="primary"
                            onClick={() => handleVerifyClick(payment)}
                            icon={<FiCheck />}
                          >
                            Verify Payment
                          </Button>
                        )}
                        
                        {payment.status === 'verified' && (
                          <div className="flex items-center gap-2 text-green-400">
                            <FiCheck size={20} />
                            <span className="font-sans font-bold">Verified</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </AnimatedEntrance>
        </div>
      </main>
      
      {/* Verify Confirmation Modal */}
      <Modal
        isOpen={showVerifyModal}
        onClose={() => !verifying && setShowVerifyModal(false)}
        title="Verify Payment"
        size="medium"
      >
        {selectedPayment && (
          <div className="py-6">
            <p className="text-luxury-champagne font-serif text-lg mb-6">
              Are you sure you want to verify this payment? This will grant 
              <strong className="text-luxury-gold"> {selectedPayment.member_name}</strong> full 
              access to their Legacy Pass with QR code.
            </p>
            
            <div className="bg-luxury-black/50 border border-luxury-gold/30 rounded p-4 mb-6">
              <p className="text-luxury-champagne/70 font-sans text-sm mb-2">
                Member: <span className="text-luxury-off-white">{selectedPayment.member_name}</span>
              </p>
              <p className="text-luxury-champagne/70 font-sans text-sm mb-2">
                Amount: <span className="text-luxury-gold font-bold">{formatCurrency(selectedPayment.amount)}</span>
              </p>
              <p className="text-luxury-champagne/70 font-sans text-sm">
                Method: <span className="text-luxury-off-white">{selectedPayment.payment_method?.replace(/_/g, ' ')}</span>
              </p>
            </div>
            
            <div className="flex gap-4">
              <Button
                variant="primary"
                onClick={confirmVerify}
                loading={verifying}
                disabled={verifying}
                fullWidth
              >
                Confirm Verification
              </Button>
              
              <Button
                variant="ghost"
                onClick={() => setShowVerifyModal(false)}
                disabled={verifying}
                fullWidth
              >
                Cancel
              </Button>
            </div>
          </div>
        )}
      </Modal>
      
      <Footer />
    </div>
  );
};

export default PaymentVerification;