import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';
import { formatMembershipTier } from '../../utils/helpers';
import Header from '../../components/layout/Header';
import Footer from '../../components/layout/Footer';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import AnimatedEntrance from '../../components/common/AnimatedEntrance';
import Button from '../../components/common/Button';
import AddMemberModal from '../../components/admin/AddMemberModal';
import { FiUsers, FiMail, FiPhone, FiCalendar, FiUserPlus } from 'react-icons/fi';

const MembersList = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [members, setMembers] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'founding_member', 'vip', 'inner_circle'
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  
  useEffect(() => {
    fetchMembers();
  }, [filter]);
  
  const fetchMembers = async () => {
    try {
      setLoading(true);
      const tierParam = filter === 'all' ? '' : `?tier=${filter}`;
      const response = await api.get(`${API_ENDPOINTS.ADMIN.MEMBERS}${tierParam}`);
      setMembers(response.data);
    } catch (error) {
      console.error('Failed to fetch members:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleAddMember = async (memberData) => {
    try {
      await api.post(API_ENDPOINTS.ADMIN.CREATE_MEMBER, memberData);
      
      // Refresh members list
      await fetchMembers();
      
      alert('Member added successfully!');
    } catch (error) {
      console.error('Failed to add member:', error);
      throw new Error(
        error.response?.data?.detail || 'Failed to add member. Please try again.'
      );
    }
  };
  
  const getTierColor = (tier) => {
    const colors = {
      founding_member: 'text-purple-400',
      vip: 'text-blue-400',
      inner_circle: 'text-green-400',
      admin: 'text-luxury-gold',
    };
    return colors[tier] || 'text-luxury-champagne';
  };
  
  // Filter members by search term
  const filteredMembers = members.filter(member => 
    member.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  if (loading) {
    return <LoadingSpinner fullScreen />;
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 py-12 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Title & Add Button */}
          <AnimatedEntrance animation="slideUp" duration={0.8}>
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="heading-luxury text-5xl mb-4">
                  Members List
                </h1>
                <p className="subheading-luxury text-xl">
                  View and manage all Inner Circle members
                </p>
              </div>
              
              <Button
                variant="primary"
                onClick={() => setShowAddModal(true)}
                icon={<FiUserPlus />}
              >
                Add Member
              </Button>
            </div>
          </AnimatedEntrance>
          
          {/* Search & Filter */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.2}>
            <div className="card-luxury mb-8">
              <div className="flex flex-col md:flex-row gap-4">
                {/* Search */}
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Search by name or email..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="input-luxury w-full"
                  />
                </div>
                
                {/* Filter Buttons */}
                <div className="flex gap-2 flex-wrap">
                  <button
                    onClick={() => setFilter('all')}
                    className={`
                      px-4 py-2 font-sans text-sm uppercase tracking-wider transition-all
                      ${filter === 'all'
                        ? 'bg-luxury-gold text-luxury-black'
                        : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                      }
                    `}
                  >
                    All
                  </button>
                  
                  <button
                    onClick={() => setFilter('founding_member')}
                    className={`
                      px-4 py-2 font-sans text-sm uppercase tracking-wider transition-all
                      ${filter === 'founding_member'
                        ? 'bg-luxury-gold text-luxury-black'
                        : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                      }
                    `}
                  >
                    Founding
                  </button>
                  
                  <button
                    onClick={() => setFilter('vip')}
                    className={`
                      px-4 py-2 font-sans text-sm uppercase tracking-wider transition-all
                      ${filter === 'vip'
                        ? 'bg-luxury-gold text-luxury-black'
                        : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                      }
                    `}
                  >
                    VIP
                  </button>
                  
                  <button
                    onClick={() => setFilter('inner_circle')}
                    className={`
                      px-4 py-2 font-sans text-sm uppercase tracking-wider transition-all
                      ${filter === 'inner_circle'
                        ? 'bg-luxury-gold text-luxury-black'
                        : 'bg-luxury-off-black text-luxury-champagne border border-luxury-gold/30 hover:border-luxury-gold'
                      }
                    `}
                  >
                    Inner Circle
                  </button>
                </div>
              </div>
            </div>
          </AnimatedEntrance>
          
          {/* Members Count */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.3}>
            <div className="mb-6">
              <p className="text-luxury-champagne font-serif text-lg">
                Showing {filteredMembers.length} member{filteredMembers.length !== 1 ? 's' : ''}
              </p>
            </div>
          </AnimatedEntrance>
          
          {/* Members Grid */}
          <AnimatedEntrance animation="slideUp" duration={0.8} delay={0.4}>
            <div className="space-y-4">
              {filteredMembers.length === 0 ? (
                <div className="card-luxury text-center py-12">
                  <FiUsers className="text-luxury-gold text-6xl mx-auto mb-4" />
                  <p className="text-luxury-champagne font-serif text-lg">
                    {searchTerm ? 'No members match your search' : 'No members found'}
                  </p>
                </div>
              ) : (
                filteredMembers.map((member) => (
                  <div key={member.id} className="card-luxury hover:border-luxury-gold/60 transition-all">
                    <div className="flex flex-col md:flex-row md:items-center gap-6">
                      {/* Member Icon */}
                      <div className="flex-shrink-0">
                        <div className="w-16 h-16 rounded-full bg-luxury-gold/20 flex items-center justify-center">
                          <FiUsers className="text-luxury-gold text-2xl" />
                        </div>
                      </div>
                      
                      {/* Member Info */}
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h3 className="text-luxury-off-white font-serif text-2xl mb-1">
                              {member.full_name}
                            </h3>
                            <p className={`font-sans text-sm font-bold uppercase ${getTierColor(member.membership_tier)}`}>
                              {formatMembershipTier(member.membership_tier)}
                            </p>
                          </div>
                          <span className="text-luxury-gold font-mono text-sm">
                            {member.membership_number}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          <div className="flex items-center gap-2 text-luxury-champagne">
                            <FiMail size={16} />
                            <span className="font-serif text-sm">{member.email}</span>
                          </div>
                          
                          {member.phone_number && (
                            <div className="flex items-center gap-2 text-luxury-champagne">
                              <FiPhone size={16} />
                              <span className="font-serif text-sm">{member.phone_number}</span>
                            </div>
                          )}
                          
                          <div className="flex items-center gap-2 text-luxury-champagne/70">
                            <FiCalendar size={16} />
                            <span className="font-sans text-xs">
                              Joined: {new Date(member.created_at).toLocaleDateString()}
                            </span>
                          </div>
                          
                          <div className="flex items-center gap-2">
                            <span className={`
                              px-3 py-1 rounded-full text-xs font-sans font-bold uppercase
                              ${member.has_logged_in
                                ? 'bg-green-400/20 text-green-400'
                                : 'bg-gray-400/20 text-gray-400'
                              }
                            `}>
                              {member.has_logged_in ? 'Active' : 'Not Logged In'}
                            </span>
                          </div>
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
      
      {/* Add Member Modal */}
      <AddMemberModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSuccess={handleAddMember}
      />
      
      <Footer />
    </div>
  );
};

export default MembersList;