import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import Footer from '../components/layout/Footer';
import { FiHome, FiRefreshCw } from 'react-icons/fi';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

const ErrorFallback = ({ error }) => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen flex flex-col bg-luxury-black">
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="max-w-2xl mx-auto text-center">
          {/* Decorative Element */}
          <div className="mb-8">
            <div className="inline-block p-8 border-2 border-luxury-gold rounded-full">
              <span className="text-luxury-gold text-6xl">⚠️</span>
            </div>
          </div>
          
          {/* Title */}
          <h1 className="heading-luxury text-5xl md:text-6xl mb-6">
            Something Went Wrong
          </h1>
          
          {/* Subtitle */}
          <p className="subheading-luxury text-2xl mb-8">
            We encountered an unexpected issue
          </p>
          
          {/* Description */}
          <p className="text-luxury-champagne font-serif text-lg leading-relaxed mb-12 max-w-xl mx-auto">
            Don't worry—this happens sometimes. Please try refreshing the page 
            or return home to continue your experience.
          </p>
          
          {/* Divider */}
          <div className="w-32 h-px bg-luxury-gold mx-auto mb-12" />
          
          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="primary"
              size="large"
              onClick={() => window.location.reload()}
              icon={<FiRefreshCw />}
            >
              Refresh Page
            </Button>
            
            <Button
              variant="secondary"
              size="large"
              onClick={() => window.location.href = '/'}
              icon={<FiHome />}
            >
              Return Home
            </Button>
          </div>
          
          {/* Error Details (development only) */}
          {process.env.NODE_ENV === 'development' && error && (
            <div className="mt-12 p-4 bg-red-900/20 border border-red-500/30 rounded text-left">
              <p className="text-red-400 font-mono text-xs break-all">
                {error.toString()}
              </p>
            </div>
          )}
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default ErrorBoundary;