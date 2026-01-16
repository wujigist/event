import React from 'react';
import { formatAccessLevel, formatGiftTier } from '../../utils/helpers';

const BlurredPassCard = ({ pass }) => {
  if (!pass) return null;
  
  return (
    <div className="max-w-2xl mx-auto">
      {/* Front Side */}
      <div className="card-luxury mb-6 relative overflow-hidden">
        {/* Blur Overlay */}
        <div className="absolute inset-0 backdrop-blur-md bg-luxury-black/60 z-10 flex items-center justify-center">
          <div className="text-center">
            <p className="text-luxury-gold font-elegant text-2xl mb-2">
              Preview Only
            </p>
            <p className="text-luxury-champagne font-serif text-sm">
              Complete payment to unlock
            </p>
          </div>
        </div>
        
        {/* Card Content (blurred in background) */}
        <div className="p-8 filter blur-sm">
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
            </div>
          </div>
          
          <div className="space-y-3">
            <div>
              <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide">Member</p>
              <p className="text-luxury-off-white font-serif text-lg">{pass.member_name}</p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide">Access Level</p>
                <p className="text-luxury-gold font-sans text-sm font-bold">
                  {formatAccessLevel(pass.access_level)}
                </p>
              </div>
              <div>
                <p className="text-luxury-champagne/70 text-xs uppercase tracking-wide">Gift Tier</p>
                <p className="text-luxury-gold font-sans text-sm font-bold">
                  {formatGiftTier(pass.gift_tier)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Back Side Preview */}
      <div className="card-luxury relative overflow-hidden">
        {/* Blur Overlay */}
        <div className="absolute inset-0 backdrop-blur-md bg-luxury-black/60 z-10 flex items-center justify-center">
          <div className="text-center">
            <p className="text-luxury-gold font-elegant text-2xl mb-2">
              QR Code Hidden
            </p>
            <p className="text-luxury-champagne font-serif text-sm">
              Available after payment
            </p>
          </div>
        </div>
        
        {/* Back Content (blurred) */}
        <div className="p-8 filter blur-sm">
          <div className="flex items-center justify-center mb-6">
            <div className="w-48 h-48 bg-luxury-off-white rounded-lg"></div>
          </div>
          
          <div className="text-center space-y-2">
            <p className="text-luxury-champagne/70 text-xs uppercase">Token ID</p>
            <p className="text-luxury-off-white font-mono text-sm">
              {pass.token ? pass.token.substring(0, 8) + '...' : '••••••••'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlurredPassCard;