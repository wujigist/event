import React, { useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';

const RSVPButtons = ({ onAccept, onDecline, loading }) => {
  const [showAcceptModal, setShowAcceptModal] = useState(false);
  const [showDeclineModal, setShowDeclineModal] = useState(false);
  
  const handleAcceptClick = () => {
    setShowAcceptModal(true);
  };
  
  const handleDeclineClick = () => {
    setShowDeclineModal(true);
  };
  
  const confirmAccept = () => {
    setShowAcceptModal(false);
    onAccept();
  };
  
  const confirmDecline = () => {
    setShowDeclineModal(false);
    onDecline();
  };
  
  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        {/* Accept Button */}
        <Button
          variant="primary"
          size="large"
          onClick={handleAcceptClick}
          disabled={loading}
        >
          I Will Be There
        </Button>
        
        {/* Decline Button */}
        <Button
          variant="secondary"
          size="large"
          onClick={handleDeclineClick}
          disabled={loading}
        >
          I'll Be With You in Spirit
        </Button>
      </div>
      
      {/* Accept Confirmation Modal */}
      <Modal
        isOpen={showAcceptModal}
        onClose={() => setShowAcceptModal(false)}
        title="Confirm Your Attendance"
        size="medium"
      >
        <div className="text-center py-6">
          <p className="text-luxury-champagne font-serif text-lg mb-8">
            Are you ready to confirm your attendance for this exclusive evening?
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="primary"
              onClick={confirmAccept}
              loading={loading}
            >
              Yes, Confirm
            </Button>
            <Button
              variant="ghost"
              onClick={() => setShowAcceptModal(false)}
              disabled={loading}
            >
              Go Back
            </Button>
          </div>
        </div>
      </Modal>
      
      {/* Decline Confirmation Modal */}
      <Modal
        isOpen={showDeclineModal}
        onClose={() => setShowDeclineModal(false)}
        title="We'll Miss You"
        size="medium"
      >
        <div className="text-center py-6">
          <p className="text-luxury-champagne font-serif text-lg mb-8">
            We understand that schedules change. Are you sure you won't be able to join us?
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="secondary"
              onClick={confirmDecline}
              loading={loading}
            >
              Yes, Decline
            </Button>
            <Button
              variant="ghost"
              onClick={() => setShowDeclineModal(false)}
              disabled={loading}
            >
              Go Back
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default RSVPButtons;