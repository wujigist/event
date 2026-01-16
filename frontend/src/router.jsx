import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import PrivateRoute from './components/auth/PrivateRoute';
import AdminRoute from './components/auth/AdminRoute';

// =====================
// Public Pages
// =====================
import LandingPage from './pages/public/LandingPage';
import AccessPage from './pages/public/AccessPage';
import NotFoundPage from './pages/public/NotFoundPage';

// =====================
// Member Pages
// =====================
import DashboardPage from './pages/member/DashboardPage';
import EventDetailsPage from './pages/member/EventDetailsPage';
import RSVPPage from './pages/member/RSVPPage';
import LegacyPassPage from './pages/member/LegacyPassPage';
import PassAccessPage from './pages/member/PassAccessPage';
import PaymentPage from './pages/member/PaymentPage';

// =====================
// Admin Pages
// =====================
import AdminDashboard from './pages/admin/AdminDashboard';
import MembersList from './pages/admin/MembersList';
import RSVPManagement from './pages/admin/RSVPManagement';
import PaymentVerification from './pages/admin/PaymentVerification';

// =====================
// Router Configuration
// =====================
const router = createBrowserRouter([
  // ---------- Public Routes ----------
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/access',
    element: <AccessPage />,
  },

  // ---------- Protected Member Routes ----------
  {
    path: '/dashboard',
    element: (
      <PrivateRoute>
        <DashboardPage />
      </PrivateRoute>
    ),
  },
  {
    path: '/event',
    element: (
      <PrivateRoute>
        <EventDetailsPage />
      </PrivateRoute>
    ),
  },
  {
    path: '/rsvp',
    element: (
      <PrivateRoute>
        <RSVPPage />
      </PrivateRoute>
    ),
  },
  {
    path: '/legacy-pass',
    element: (
      <PrivateRoute>
        <LegacyPassPage />
      </PrivateRoute>
    ),
  },
  {
    path: '/pass/:token',
    element: (
      <PrivateRoute>
        <PassAccessPage />
      </PrivateRoute>
    ),
  },
  {
    path: '/payment',
    element: (
      <PrivateRoute>
        <PaymentPage />
      </PrivateRoute>
    ),
  },

  // ---------- Protected Admin Routes ----------
  {
    path: '/admin',
    element: (
      <AdminRoute>
        <AdminDashboard />
      </AdminRoute>
    ),
  },
  {
    path: '/admin/members',
    element: (
      <AdminRoute>
        <MembersList />
      </AdminRoute>
    ),
  },
  {
    path: '/admin/rsvps',
    element: (
      <AdminRoute>
        <RSVPManagement />
      </AdminRoute>
    ),
  },
  {
    path: '/admin/payments',
    element: (
      <AdminRoute>
        <PaymentVerification />
      </AdminRoute>
    ),
  },

  // ---------- Catch-all (404) ----------
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);

export default router;