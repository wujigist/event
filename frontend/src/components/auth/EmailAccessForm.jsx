import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { validateEmail } from '../../utils/validators';
import Input from '../common/Input';
import Button from '../common/Button';
import { FiMail } from 'react-icons/fi';

const EmailAccessForm = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Clear previous errors
    setError('');
    
    // Validate email
    const validation = validateEmail(email);
    if (!validation.valid) {
      setError(validation.message);
      return;
    }
    
    // Attempt login
    setLoading(true);
    
    try {
      const result = await login(email);
      
      if (result.success) {
        // Redirect to dashboard
        navigate('/dashboard');
      } else {
        setError(result.error || 'This invitation is reserved for selected members.');
      }
    } catch (err) {
      setError('We encountered an issue. Please try again in a moment.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title */}
        <div className="text-center mb-8">
          <h2 className="heading-luxury text-3xl mb-3">
            Access Your Invitation
          </h2>
          <p className="subheading-luxury text-base">
            Paige is expecting you
          </p>
        </div>
        
        {/* Email Input */}
        <Input
          label="Email Address"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your.email@example.com"
          error={error}
          required
          icon={<FiMail size={20} />}
          disabled={loading}
        />
        
        {/* Submit Button */}
        <Button
          type="submit"
          variant="primary"
          fullWidth
          loading={loading}
          disabled={loading || !email}
        >
          {loading ? 'Verifying...' : 'Enter'}
        </Button>
        
        {/* Helper Text */}
        <p className="text-center text-luxury-champagne/70 text-sm font-serif italic">
          Only invited members may access this exclusive experience
        </p>
      </form>
    </div>
  );
};

export default EmailAccessForm;