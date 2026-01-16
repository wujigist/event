/**
 * Format date to elegant display
 * Example: "February 15, 2026"
 */
export const formatDate = (date) => {
  if (!date) return '';
  
  const dateObj = new Date(date);
  
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };
  
  return dateObj.toLocaleDateString('en-US', options);
};

/**
 * Format date with time
 * Example: "February 15, 2026 at 7:00 PM"
 */
export const formatDateTime = (date, time) => {
  if (!date) return '';
  
  const formattedDate = formatDate(date);
  
  if (time) {
    return `${formattedDate} at ${time}`;
  }
  
  return formattedDate;
};

/**
 * Format currency with luxury style
 * Example: "$1,000.00"
 */
export const formatCurrency = (amount, currency = 'USD') => {
  if (amount === null || amount === undefined) return '';
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  
  if (text.length <= maxLength) {
    return text;
  }
  
  return text.substring(0, maxLength).trim() + '...';
};

/**
 * Capitalize first letter of each word
 */
export const capitalizeWords = (text) => {
  if (!text) return '';
  
  return text
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Format membership tier for display
 */
export const formatMembershipTier = (tier) => {
  if (!tier) return '';
  
  const tierMap = {
    inner_circle: 'Inner Circle',
    vip: 'VIP',
    founding_member: 'Founding Member',
    admin: 'Administrator',
  };
  
  return tierMap[tier] || capitalizeWords(tier.replace(/_/g, ' '));
};

/**
 * Format gift tier for display
 */
export const formatGiftTier = (tier) => {
  if (!tier) return '';
  
  const tierMap = {
    standard: 'Standard',
    premium: 'Premium',
    elite: 'Elite',
  };
  
  return tierMap[tier] || capitalizeWords(tier);
};

/**
 * Format access level for display
 */
export const formatAccessLevel = (level) => {
  if (!level) return '';
  
  const levelMap = {
    gold: 'Gold',
    platinum: 'Platinum',
    diamond: 'Diamond',
  };
  
  return levelMap[level] || capitalizeWords(level);
};

/**
 * Get time ago text
 * Example: "2 hours ago"
 */
export const timeAgo = (date) => {
  if (!date) return '';
  
  const now = new Date();
  const past = new Date(date);
  const diffMs = now - past;
  
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  
  if (diffMinutes < 1) return 'Just now';
  if (diffMinutes < 60) return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffDays < 30) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  
  return formatDate(date);
};

/**
 * Download file from URL
 */
export const downloadFile = (url, filename) => {
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Copy text to clipboard
 */
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return { success: true, message: 'Copied to clipboard' };
  } catch (error) {
    console.error('Copy failed:', error);
    return { success: false, message: 'Failed to copy' };
  }
};

/**
 * Sleep/delay function for animations
 */
export const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

export default {
  formatDate,
  formatDateTime,
  formatCurrency,
  truncateText,
  capitalizeWords,
  formatMembershipTier,
  formatGiftTier,
  formatAccessLevel,
  timeAgo,
  downloadFile,
  copyToClipboard,
  sleep,
};