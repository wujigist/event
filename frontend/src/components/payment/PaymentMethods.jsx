import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import LoadingSpinner from '../common/LoadingSpinner';
import { FiCreditCard, FiDollarSign } from 'react-icons/fi';

// Default payment methods fallback
const DEFAULT_METHODS = [
  {
    method: 'bank_transfer',
    name: 'Bank Transfer',
    description: 'Direct bank transfer (ACH or wire)'
  },
  {
    method: 'zelle',
    name: 'Zelle',
    description: 'Quick and secure digital payment'
  },
  {
    method: 'paypal',
    name: 'PayPal',
    description: 'Pay securely with PayPal'
  },
  {
    method: 'cashapp',
    name: 'Cash App',
    description: 'Fast mobile payment'
  },
  {
    method: 'cryptocurrency',
    name: 'Cryptocurrency',
    description: 'Bitcoin, USDT, or other crypto'
  },
  {
    method: 'other',
    name: 'Other Method',
    description: 'Contact us for alternative arrangements'
  }
];

const PaymentMethods = ({ selectedMethod, onSelect }) => {
  const [methods, setMethods] = useState(DEFAULT_METHODS);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchPaymentMethods();
  }, []);
  
  const fetchPaymentMethods = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.PAYMENT.METHODS);
      
      // Backend returns {methods: [...]} so we need to access .methods
      const backendMethods = response.data?.methods || response.data;
      
      // Validate response data
      if (backendMethods && Array.isArray(backendMethods) && backendMethods.length > 0) {
        // Convert backend format (id) to frontend format (method)
        const formattedMethods = backendMethods.map(m => ({
          method: m.id || m.method,
          name: m.name,
          description: m.description
        }));
        setMethods(formattedMethods);
      } else {
        console.log('Using default payment methods');
        // Keep default methods
      }
    } catch (error) {
      console.error('Failed to fetch payment methods, using defaults:', error);
      // Keep default methods
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  // Method icons mapping
  const getMethodIcon = (method) => {
    const iconMap = {
      'bank_transfer': FiDollarSign,
      'credit_card': FiCreditCard,
      'paypal': FiDollarSign,
      'zelle': FiDollarSign,
      'cashapp': FiDollarSign,
      'cryptocurrency': FiDollarSign,
      'wire_transfer': FiDollarSign,
      'other': FiDollarSign,
    };
    
    const Icon = iconMap[method] || FiDollarSign;
    return <Icon className="text-luxury-gold" size={24} />;
  };
  
  return (
    <div>
      <h3 className="font-elegant text-luxury-gold text-2xl mb-6">
        Select Payment Method
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {methods.map((method) => (
          <button
            key={method.method}
            onClick={() => onSelect(method.method)}
            className={`
              p-6 text-left border-2 rounded-lg transition-all duration-300
              hover:border-luxury-gold hover:bg-luxury-black/50
              ${selectedMethod === method.method
                ? 'border-luxury-gold bg-luxury-black/50'
                : 'border-luxury-gold/30 bg-transparent'
              }
            `}
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                {getMethodIcon(method.method)}
              </div>
              
              <div className="flex-1">
                <h4 className="text-luxury-off-white font-sans font-bold text-lg mb-2">
                  {method.name}
                </h4>
                {method.description && (
                  <p className="text-luxury-champagne/80 font-serif text-sm">
                    {method.description}
                  </p>
                )}
              </div>
              
              {/* Radio indicator */}
              <div className={`
                w-5 h-5 rounded-full border-2 flex-shrink-0 mt-1
                ${selectedMethod === method.method
                  ? 'border-luxury-gold bg-luxury-gold'
                  : 'border-luxury-gold/50'
                }
              `}>
                {selectedMethod === method.method && (
                  <div className="w-full h-full flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-luxury-black"></div>
                  </div>
                )}
              </div>
            </div>
          </button>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
        <p className="text-luxury-champagne/70 font-serif text-sm text-center">
          After submitting your contact information, our team will reach out within 24 hours with payment instructions
        </p>
      </div>
    </div>
  );
};

export default PaymentMethods;