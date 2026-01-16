import React from 'react';
import { motion } from 'framer-motion';

const AnimatedEntrance = ({ 
  children, 
  animation = 'fade',
  delay = 0,
  duration = 0.6,
  className = '',
}) => {
  // Animation variants
  const animations = {
    fade: {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    },
    slideUp: {
      hidden: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0 },
    },
    slideDown: {
      hidden: { opacity: 0, y: -20 },
      visible: { opacity: 1, y: 0 },
    },
    slideLeft: {
      hidden: { opacity: 0, x: 20 },
      visible: { opacity: 1, x: 0 },
    },
    slideRight: {
      hidden: { opacity: 0, x: -20 },
      visible: { opacity: 1, x: 0 },
    },
    scale: {
      hidden: { opacity: 0, scale: 0.8 },
      visible: { opacity: 1, scale: 1 },
    },
  };
  
  const selectedAnimation = animations[animation] || animations.fade;
  
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={selectedAnimation}
      transition={{
        duration: duration,
        delay: delay,
        ease: 'easeOut',
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export default AnimatedEntrance;