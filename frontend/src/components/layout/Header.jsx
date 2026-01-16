import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Button from '../common/Button';
import { FiMenu, FiX, FiHome, FiCalendar, FiCreditCard, FiUsers, FiCheckSquare, FiDollarSign } from 'react-icons/fi';

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, member, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Check if user is admin
  const isAdmin = member?.membership_tier === 'admin' || 
                  member?.email?.endsWith('@paigeinnercircle.com');

  // Member navigation
  const memberNavItems = [
    { path: '/dashboard', label: 'Dashboard', icon: FiHome },
    { path: '/event', label: 'Event Details', icon: FiCalendar },
    { path: '/legacy-pass', label: 'Legacy Pass', icon: FiCreditCard },
  ];

  // Admin navigation
  const adminNavItems = [
    { path: '/admin', label: 'Admin Dashboard', icon: FiHome },
    { path: '/admin/members', label: 'Members', icon: FiUsers },
    { path: '/admin/rsvps', label: 'RSVPs', icon: FiCheckSquare },
    { path: '/admin/payments', label: 'Payments', icon: FiDollarSign },
  ];

  const navItems = isAdmin ? adminNavItems : memberNavItems;

  const isActive = (path) => location.pathname === path;

  const handleNavigation = (path) => {
    navigate(path);
    setMobileMenuOpen(false);
  };

  return (
    <header className="bg-luxury-black border-b border-luxury-gold/30 py-4 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          {/* Logo/Brand */}
          <button
            onClick={() => navigate(isAuthenticated ? (isAdmin ? '/admin' : '/dashboard') : '/')}
            className="font-elegant text-luxury-gold text-2xl md:text-3xl tracking-wide hover:text-luxury-dark-gold transition-colors"
          >
            Paige's Inner Circle
          </button>

          {/* Desktop Navigation & Member Info */}
          {isAuthenticated && member && (
            <div className="hidden md:flex items-center gap-6">
              {/* Navigation Links */}
              <nav className="flex items-center gap-6">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.path}
                      onClick={() => navigate(item.path)}
                      className={`
                        flex items-center gap-2 font-sans text-sm transition-colors
                        ${isActive(item.path)
                          ? 'text-luxury-gold'
                          : 'text-luxury-champagne hover:text-luxury-gold'
                        }
                      `}
                    >
                      <Icon size={16} />
                      {item.label}
                    </button>
                  );
                })}
              </nav>

              {/* Divider */}
              <div className="h-10 w-px bg-luxury-gold/30" />

              {/* Member Name & Role */}
              <div className="text-right">
                <p className="text-luxury-champagne font-serif text-sm">
                  {isAdmin ? 'Administrator' : 'Welcome back,'}
                </p>
                <p className="text-luxury-gold font-sans font-bold">
                  {member.full_name}
                </p>
              </div>

              {/* Logout Button */}
              <Button
                variant="ghost"
                size="small"
                onClick={logout}
              >
                Sign Out
              </Button>
            </div>
          )}

          {/* Mobile Menu Button */}
          {isAuthenticated && member && (
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-luxury-gold hover:text-luxury-dark-gold transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          )}
        </div>

        {/* Mobile Navigation Menu */}
        {isAuthenticated && member && mobileMenuOpen && (
          <div className="md:hidden mt-6 pt-6 border-t border-luxury-gold/30">
            {/* Member Info */}
            <div className="mb-6 pb-6 border-b border-luxury-gold/20">
              <p className="text-luxury-champagne font-serif text-sm mb-1">
                {isAdmin ? 'Administrator' : 'Welcome back,'}
              </p>
              <p className="text-luxury-gold font-sans font-bold text-lg">
                {member.full_name}
              </p>
            </div>

            {/* Navigation Links */}
            <nav className="flex flex-col gap-4 mb-6">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.path}
                    onClick={() => handleNavigation(item.path)}
                    className={`
                      flex items-center gap-3 font-sans text-base py-2 transition-colors text-left
                      ${isActive(item.path)
                        ? 'text-luxury-gold'
                        : 'text-luxury-champagne hover:text-luxury-gold'
                      }
                    `}
                  >
                    <Icon size={20} />
                    {item.label}
                  </button>
                );
              })}
            </nav>

            {/* Logout Button */}
            <Button
              variant="ghost"
              size="small"
              onClick={() => {
                logout();
                setMobileMenuOpen(false);
              }}
              className="w-full"
            >
              Sign Out
            </Button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;