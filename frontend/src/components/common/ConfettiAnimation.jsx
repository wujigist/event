import React, { useState, useEffect } from 'react';
import Confetti from 'react-confetti';

const ConfettiAnimation = ({ 
  active = false, 
  duration = 5000,
  onComplete = () => {},
}) => {
  const [isActive, setIsActive] = useState(active);
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });
  
  // Update window size on resize
  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  // Handle active state and duration
  useEffect(() => {
    setIsActive(active);
    
    if (active) {
      const timer = setTimeout(() => {
        setIsActive(false);
        onComplete();
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [active, duration, onComplete]);
  
  if (!isActive) return null;
  
  return (
    <Confetti
      width={windowSize.width}
      height={windowSize.height}
      numberOfPieces={200}
      recycle={false}
      colors={[
        '#D4AF37', // Gold
        '#8B7328', // Dark Gold
        '#F7E7CE', // Champagne
        '#FFD700', // Bright Gold
        '#FFF8DC', // Cornsilk
      ]}
      gravity={0.15}
      wind={0.01}
      opacity={0.8}
    />
  );
};

export default ConfettiAnimation;