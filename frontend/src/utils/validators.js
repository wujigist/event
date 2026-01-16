/**
 * Validate email format
 */
export const validateEmail = (email) => {
  if (!email) {
    return {
      valid: false,
      message: 'Please provide an email address.',
    };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  if (!emailRegex.test(email)) {
    return {
      valid: false,
      message: 'Please provide a valid email address.',
    };
  }

  return {
    valid: true,
    message: '',
  };
};

/**
 * Format phone number to (XXX) XXX-XXXX format
 */
export const formatPhoneNumber = (phone) => {
  // Remove all non-numeric characters
  const cleaned = phone.replace(/\D/g, '');
  
  // Check if we have 10 digits
  if (cleaned.length !== 10) {
    return phone; // Return original if not 10 digits
  }
  
  // Format as (XXX) XXX-XXXX
  const formatted = `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  
  return formatted;
};

/**
 * Validate phone number format
 */
export const validatePhone = (phone) => {
  if (!phone) {
    return {
      valid: false,
      message: 'Please provide a phone number.',
    };
  }

  // Remove all non-numeric characters
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length < 10) {
    return {
      valid: false,
      message: 'Phone number must be at least 10 digits.',
    };
  }

  return {
    valid: true,
    message: '',
  };
};

/**
 * Validate required field
 */
export const validateRequired = (value, fieldName = 'This field') => {
  if (!value || value.trim() === '') {
    return {
      valid: false,
      message: `${fieldName} is required.`,
    };
  }

  return {
    valid: true,
    message: '',
  };
};

/**
 * Validate minimum length
 */
export const validateMinLength = (value, minLength, fieldName = 'This field') => {
  if (!value || value.length < minLength) {
    return {
      valid: false,
      message: `${fieldName} must be at least ${minLength} characters.`,
    };
  }

  return {
    valid: true,
    message: '',
  };
};

export default {
  validateEmail,
  formatPhoneNumber,
  validatePhone,
  validateRequired,
  validateMinLength,
};