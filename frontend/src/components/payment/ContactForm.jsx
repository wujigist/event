import React, { useState } from 'react';
import { validateEmail } from '../../utils/validators';
import Input from '../common/Input';
import Button from '../common/Button';
import { FiMail, FiPhone } from 'react-icons/fi';

const ContactForm = ({ paymentMethod, onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    notes: '',
  });
  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate
    const newErrors = {};
    
    const emailValidation = validateEmail(formData.email);
    if (!emailValidation.valid) {
      newErrors.email = emailValidation.message;
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Submit
    onSubmit({
      ...formData,
      payment_method: paymentMethod,
    });
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h3 className="font-elegant text-luxury-gold text-2xl mb-4">
          Contact Information
        </h3>
        <p className="text-luxury-champagne font-serif text-base mb-6">
          We'll use this information to send you payment instructions within 24 hours.
        </p>
      </div>
      
      {/* Email */}
      <Input
        label="Email Address"
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="your.email@example.com"
        error={errors.email}
        required
        icon={<FiMail size={20} />}
        disabled={loading}
      />
      
      {/* Phone (Optional) */}
      <Input
        label="Phone Number (Optional)"
        type="tel"
        name="phone"
        value={formData.phone}
        onChange={handleChange}
        placeholder="(555) 123-4567"
        icon={<FiPhone size={20} />}
        disabled={loading}
      />
      
      {/* Additional Notes */}
      <div>
        <label className="block text-luxury-champagne font-serif text-lg mb-2">
          Additional Notes (Optional)
        </label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          placeholder="Any specific questions or preferences..."
          rows={4}
          disabled={loading}
          className="input-luxury w-full resize-none"
        />
      </div>
      
      {/* Payment Method Summary */}
      <div className="p-4 bg-luxury-black/50 border border-luxury-gold/30 rounded">
        <p className="text-luxury-champagne/70 font-sans text-sm mb-2">
          Selected Payment Method:
        </p>
        <p className="text-luxury-gold font-sans font-bold text-lg">
          {paymentMethod.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </p>
      </div>
      
      {/* Submit Button */}
      <Button
        type="submit"
        variant="primary"
        fullWidth
        loading={loading}
        disabled={loading}
      >
        {loading ? 'Submitting...' : 'Request Payment Instructions'}
      </Button>
      
      {/* Privacy Notice */}
      <p className="text-luxury-champagne/60 font-serif text-xs text-center italic">
        Your contact information will only be used to facilitate your payment and will never be shared with third parties
      </p>
    </form>
  );
};

export default ContactForm;