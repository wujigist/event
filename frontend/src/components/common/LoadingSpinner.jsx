import React from 'react';

const LoadingSpinner = ({ 
  size = 'medium', 
  message = 'Preparing your experience...',
  fullScreen = false,
}) => {
  // Size classes
  const sizes = {
    small: 'w-8 h-8',
    medium: 'w-12 h-12',
    large: 'w-16 h-16',
  };
  
  const spinnerSize = sizes[size] || sizes.medium;
  
  const SpinnerContent = () => (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className={`spinner-luxury ${spinnerSize}`} />
      {message && (
        <p className="text-luxury-champagne font-serif text-lg italic animate-pulse">
          {message}
        </p>
      )}
    </div>
  );
  
  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-luxury-black bg-opacity-95 backdrop-blur-sm flex items-center justify-center z-50">
        <SpinnerContent />
      </div>
    );
  }
  
  return (
    <div className="flex items-center justify-center p-8">
      <SpinnerContent />
    </div>
  );
};

export default LoadingSpinner;