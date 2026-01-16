import React, { useState } from 'react';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Button from '../common/Button';
import { validateEmail, validateRequired } from '../../utils/validators';
import { FiMail, FiUser, FiPhone } from 'react-icons/fi';

const AddMemberModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    phone_number: '',
    membership_tier: 'inner_circle',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  
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
  
  const validate = () => {
    const newErrors = {};
    
    // Validate email
    const emailValidation = validateEmail(formData.email);
    if (!emailValidation.valid) {
      newErrors.email = emailValidation.message;
    }
    
    // Validate full name
    const nameValidation = validateRequired(formData.full_name, 'Full name');
    if (!nameValidation.valid) {
      newErrors.full_name = nameValidation.message;
    }
    
    return newErrors;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Submit to parent component
    setLoading(true);
    try {
      await onSuccess(formData);
      
      // Reset form
      setFormData({
        email: '',
        full_name: '',
        phone_number: '',
        membership_tier: 'inner_circle',
      });
      setErrors({});
      onClose();
    } catch (error) {
      setErrors({ submit: error.message || 'Failed to add member' });
    } finally {
      setLoading(false);
    }
  };
  
  const handleClose = () => {
    if (!loading) {
      setFormData({
        email: '',
        full_name: '',
        phone_number: '',
        membership_tier: 'inner_circle',
      });
      setErrors({});
      onClose();
    }
  };
  
  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Add New Member"
      size="medium"
    >
      <form onSubmit={handleSubmit} className="py-6 space-y-6">
        {/* Full Name */}
        <Input
          label="Full Name"
          type="text"
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          placeholder="John Doe"
          error={errors.full_name}
          required
          icon={<FiUser size={20} />}
          disabled={loading}
        />
        
        {/* Email */}
        <Input
          label="Email Address"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="john.doe@example.com"
          error={errors.email}
          required
          icon={<FiMail size={20} />}
          disabled={loading}
        />
        
        {/* Phone Number (Optional) */}
        <Input
          label="Phone Number (Optional)"
          type="tel"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          placeholder="(555) 123-4567"
          icon={<FiPhone size={20} />}
          disabled={loading}
        />
        
        {/* Membership Tier */}
        <div>
          <label className="block text-luxury-champagne font-serif text-lg mb-2">
            Membership Tier <span className="text-luxury-gold">*</span>
          </label>
          <select
            name="membership_tier"
            value={formData.membership_tier}
            onChange={handleChange}
            disabled={loading}
            className="input-luxury w-full"
          >
            <option value="inner_circle">Inner Circle</option>
            <option value="vip">VIP</option>
            <option value="founding_member">Founding Member</option>
          </select>
          <p className="text-luxury-champagne/60 font-sans text-xs mt-2 italic">
            This determines their access level and benefits
          </p>
        </div>
        
        {/* Submit Error */}
        {errors.submit && (
          <div className="p-4 bg-red-500/20 border border-red-500/50 rounded">
            <p className="text-red-400 font-sans text-sm">
              {errors.submit}
            </p>
          </div>
        )}
        
        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? 'Adding Member...' : 'Add Member'}
          </Button>
          
          <Button
            type="button"
            variant="ghost"
            fullWidth
            onClick={handleClose}
            disabled={loading}
          >
            Cancel
          </Button>
        </div>
        
        {/* Info Notice */}
        <div className="p-4 bg-luxury-black/50 border border-luxury-gold/20 rounded">
          <p className="text-luxury-champagne/70 font-serif text-sm">
            The new member will receive their login credentials and can access 
            the platform immediately using their email address.
          </p>
        </div>
      </form>
    </Modal>
  );
};

export default AddMemberModal;