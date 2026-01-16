import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import { formatDate, formatMembershipTier, timeAgo } from '../../utils/helpers';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import { FiCheckCircle, FiXCircle, FiClock, FiCalendar, FiUsers } from 'react-icons/fi';

const RSVPManagement = () => {
  const [loading, setLoading] = useState(true);
  const [rsvps, setRsvps] = useState([]);
  const [summary, setSummary] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all', 'accepted', 'declined'
  
  useEffect(() => {
    fetchData();
  }, [filter]);
  
  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch RSVPs
      const endpoint = filter === 'all' 
        ? API_ENDPOINTS.ADMIN.RSVPS
        : `${API_ENDPOINTS.ADMIN.RSVPS}?status=${filter}`;
      
      const rsvpsResponse = await api.get(endpoint);
      setRsvps(rsvpsResponse.data);
      
      // Fetch summary
      const summaryResponse = await api.get(API_ENDPOINTS.ADMIN.RSVP_SUMMARY);
      setSummary(summaryResponse.data);
    } catch (error) {
      console.error('Failed to fetch RSVP data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Title */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="mb-8">
              <h1 className="heading-luxury text-5xl mb-4">
                RSVP Management
              </h1>
              <p className="subheading-luxury text-xl">
                Track who's attending your exclusive event
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Summary Cards */}
          {summary && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.1}>
                <div className="card-luxury">
                  <div className="flex items-center justify-between mb-2">
                    <FiUsers className="text-luxury-gold text-2xl" />
                    <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                      Total
                    </span>
                  </div>
                  <p className="text-luxury-off-white font-serif text-3xl mb-1">
                    {summary.total_responses}
                  </p>
                  <p className="text-luxury-champagne/70 font-sans text-sm">
                    Responses
                  </p>
                </div>
              </AnimatedEntrance>
              
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
                <div className="card-luxury">
                  <div className="flex items-center justify-between mb-2">
                    <FiCheckCircle className="text-green-400 text-2xl" />
                    <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                      Accepted
                    </span>
                  </div>
                  <p className="text-luxury-off-white font-serif text-3xl mb-1">
                    {summary.accepted}
                  </p>
                  <p className="text-luxury-champagne/70 font-sans text-sm">
                    Attending
                  </p>
                </div>
              </AnimatedEntrance>
              
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.3}>
                <div className="card-luxury">
                  <div className="flex items-center justify-between mb-2">
                    <FiXCircle className="text-luxury-champagne/50 text-2xl" />
                    <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                      Declined
                    </span>
                  </div>
                  <p className="text-luxury-off-white font-serif text-3xl mb-1">
                    {summary.declined}
                  </p>
                  <p className="text-luxury-champagne/70 font-sans text-sm">
                    Not Attending
                  </p>
                </div>
              </AnimatedEntrance>
              
              <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
                <div className="card-luxury">
                  <div className="flex items-center justify-between mb-2">
                    <FiCheckCircle className="text-luxury-gold text-2xl" />
                    <span className="text-luxury-champagne/70 font-sans text-xs uppercase">
                      Rate
                    </span>
                  </div>
                  <p className="text-luxury-off-white font-serif text-3xl mb-1">
                    {summary.acceptance_rate.toFixed(1)}%
                  </p>
                  <p className="text-luxury-champagne/70 font-sans text-sm">
                    Acceptance
                  </p>
                </div>
              </AnimatedEntrance>
            </div>
          )}
          
          {/* Filter Tabs */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.5}>
            <div className="flex gap-4 mb-8">
              <button
                onClick={() => setFilter('all')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'all'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                All ({rsvps.length})
              </button>
              
              <button
                onClick={() => setFilter('accepted')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'accepted'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                Accepted
              </button>
              
              <button
                onClick={() => setFilter('declined')}
                className={`
                  px-6 py-3 font-sans font-bold uppercase tracking-wider transition-all
                  ${filter === 'declined'
                    ? 'bg-luxury-gold text-luxury-black'
                    : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                  }
                `}
              >
                Declined
              </button>
            </div>
          </AnimatedEntrance>
          
          {/* RSVPs List */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.6}>
            <div className="space-y-4">
              {rsvps.length === 0 ? (
                <div className="card-luxury text-center py-12">
                  <FiCheckCircle className="text-luxury-gold text-5xl mx-auto mb-4" />
                  <p className="text-luxury-champagne font-serif text-lg">
                    No RSVPs found
                  </p>
                </div>
              ) : (
                rsvps.map((rsvp) => (
                  <div key={rsvp.rsvp_id} className="card-luxury">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                      {/* RSVP Info */}
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          {rsvp.status === 'accepted' ? (
                            <FiCheckCircle className="text-green-400 text-2xl" />
                          ) : (
                            <FiXCircle className="text-luxury-champagne/50 text-2xl" />
                          )}
                          <h3 className="text-luxury-off-white font-sans text-xl font-bold">
                            {rsvp.member.name}
                          </h3>
                          <span className={`
                            px-3 py-1 rounded-full text-xs font-sans font-bold uppercase
                            ${rsvp.status === 'accepted' 
                              ? 'bg-green-400/20 text-green-400' 
                              : 'bg-luxury-champagne/20 text-luxury-champagne'
                            }
                          `}>
                            {rsvp.status}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              Member Tier
                            </p>
                            <p className="text-luxury-gold font-serif">
                              {formatMembershipTier(rsvp.member.tier)}
                            </p>
                          </div>
                          
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              Email
                            </p>
                            <p className="text-luxury-off-white font-serif text-sm">
                              {rsvp.member.email}
                            </p>
                          </div>
                          
                          <div>
                            <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                              Event
                            </p>
                            <p className="text-luxury-off-white font-serif">
                              {rsvp.event.title}
                            </p>
                          </div>
                          
                          {rsvp.event.date && (
                            <div>
                              <p className="text-luxury-champagne/70 font-sans text-xs uppercase mb-1">
                                <FiCalendar className="inline mr-1" size={12} />
                                Event Date
                              </p>
                              <p className="text-luxury-off-white font-serif">
                                {formatDate(rsvp.event.date)}
                              </p>
                            </div>
                          )}
                        </div>
                        
                        {rsvp.response_message && (
                          <div className="p-3 bg-luxury-black/50 border border-luxury-gold/20 rounded mb-4">
                            <p className="text-luxury-champagne/80 font-serif text-sm italic">
                              "{rsvp.response_message}"
                            </p>
                          </div>
                        )}
                        
                        <div className="text-luxury-champagne/70 font-sans text-sm">
                          <FiClock className="inline mr-1" size={14} />
                          Responded {timeAgo(rsvp.responded_at)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </AnimatedEntrance>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default RSVPManagement;