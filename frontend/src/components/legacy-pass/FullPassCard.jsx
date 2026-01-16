import React from 'react';
import { formatAccessLevel, formatGiftTier, formatDate } from '../../utils/helpers';

const FullPassCard = ({ pass, event }) => {
  if (!pass) return null;
  
  // QR Code URL from backend
  const qrCodeUrl = pass.qr_code_path 
    ? `${import.meta.env.VITE_API_BASE_URL}/static/qr_codes/${pass.qr_code_path}`
    : null;
  
  return (
    <div className="max-w-2xl mx-auto">
      {/* Front Side */}
      <div className="card-luxury mb-6 bg-gradient-to-br from-luxury-off-black to-luxury-black border-2 border-luxury-gold">
        <div className="p-8">
          {/* Header */}
          <div className="flex items-start justify-between mb-8">
            <div>
              <h3 className="font-elegant text-luxury-gold text-3xl mb-2">
                Legacy Pass
              </h3>
              <p className="text-luxury-champagne font-serif text-sm">
                Paige's Inner Circle
              </p>
            </div>
            <div className="text-right">
              <p className="text-luxury-gold font-sans text-xl font-bold">
                {pass.pass_number}
              </p>
              <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide mt-1">
                Not Transferable
              </p>
            </div>
          </div>
          
          {/* Member Info */}
          <div className="space-y-4 mb-6">
            <div>
              <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide mb-1">
                Member Name
              </p>
              <p className="text-luxury-off-white font-serif text-2xl">
                {pass.member_name}
              </p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide mb-1">
                  Access Level
                </p>
                <p className="text-luxury-gold font-sans text-lg font-bold">
                  {formatAccessLevel(pass.access_level)}
                </p>
              </div>
              <div>
                <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide mb-1">
                  Gift Tier
                </p>
                <p className="text-luxury-gold font-sans text-lg font-bold">
                  {formatGiftTier(pass.gift_tier)}
                </p>
              </div>
            </div>
          </div>
          
          {/* Signature */}
          <div className="border-t border-luxury-gold/30 pt-4">
            <p className="text-luxury-gold font-elegant text-2xl text-right italic">
              Paige
            </p>
          </div>
        </div>
      </div>
      
      {/* Back Side - QR Code */}
      <div className="card-luxury bg-gradient-to-br from-luxury-off-black to-luxury-black border-2 border-luxury-gold">
        <div className="p-8">
          {/* QR Code */}
          <div className="flex items-center justify-center mb-6">
            {qrCodeUrl ? (
              <div className="bg-white p-4 rounded-lg">
                <img 
                  src={qrCodeUrl} 
                  alt="QR Code" 
                  className="w-48 h-48"
                />
              </div>
            ) : (
              <div className="w-48 h-48 bg-luxury-off-white rounded-lg flex items-center justify-center">
                <p className="text-luxury-black font-sans text-sm">QR Code</p>
              </div>
            )}
          </div>
          
          {/* Instructions */}
          <div className="text-center space-y-3 mb-6">
            <p className="text-luxury-champagne font-serif text-base">
              Present this QR code at the entrance
            </p>
            <p className="text-luxury-champagne/70 font-sans text-xs">
              {event && formatDate(event.event_date)}
            </p>
          </div>
          
          {/* Token ID */}
          <div className="border-t border-luxury-gold/30 pt-4 space-y-2">
            <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide text-center">
              Token ID
            </p>
            <p className="text-luxury-off-white font-mono text-xs text-center break-all">
              {pass.token}
            </p>
          </div>
          
          {/* Security Notice */}
          <div className="mt-6 p-3 bg-luxury-black/50 border border-luxury-gold/20 rounded">
            <p className="text-luxury-champagne/60 font-sans text-xs text-center">
              This pass is uniquely generated for you and cannot be transferred
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FullPassCard;