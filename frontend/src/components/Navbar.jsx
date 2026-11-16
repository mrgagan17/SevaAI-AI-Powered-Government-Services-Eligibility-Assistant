import React from 'react';
import { MessageSquare, User, FileText, Home, Info, Shield, LogIn, LogOut, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ activeTab, setActiveTab }) {
  const { user, isAuthenticated, logout, openAuthModal } = useAuth();

  const handleProtectedNav = (tabName) => {
    if (!isAuthenticated) {
      setActiveTab(tabName);
      openAuthModal('login');
    } else {
      setActiveTab(tabName);
    }
  };

  return (
    <header className="navbar">
      <div className="navbar-brand" onClick={() => setActiveTab('home')} style={{ cursor: 'pointer' }}>
        <div className="brand-logo-icon">S</div>
        <div>
          <div className="brand-title">SevaAI</div>
          <div className="brand-subtitle">AI-Powered Government Services & Eligibility Assistant</div>
        </div>
      </div>

      <nav className="navbar-links" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <button
          className={`nav-button ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          <Home size={18} />
          <span>Home</span>
        </button>

        <button
          className={`nav-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => handleProtectedNav('chat')}
        >
          <MessageSquare size={18} />
          <span>Ask Assistant</span>
          {!isAuthenticated && <Lock size={13} style={{ opacity: 0.65, marginLeft: '-2px' }} />}
        </button>

        <button
          className={`nav-button ${activeTab === 'documents' ? 'active' : ''}`}
          onClick={() => handleProtectedNav('documents')}
        >
          <FileText size={18} />
          <span>Official Documents</span>
          {!isAuthenticated && <Lock size={13} style={{ opacity: 0.65, marginLeft: '-2px' }} />}
        </button>

        {/* Citizen Profile is shown ONLY to authenticated users */}
        {isAuthenticated && (
          <button
            className={`nav-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <User size={18} />
            <span>Citizen Profile</span>
          </button>
        )}

        <button
          className={`nav-button ${activeTab === 'about' ? 'active' : ''}`}
          onClick={() => setActiveTab('about')}
        >
          <Info size={18} />
          <span>About Us</span>
        </button>

        <button
          className={`nav-button ${activeTab === 'privacy' ? 'active' : ''}`}
          onClick={() => setActiveTab('privacy')}
        >
          <Shield size={18} />
          <span>Privacy</span>
        </button>

        {/* User Auth Section */}
        <div style={{
          marginLeft: '0.75rem',
          paddingLeft: '0.75rem',
          borderLeft: '1px solid rgba(255, 255, 255, 0.15)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          {isAuthenticated ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <div
                title={user?.email}
                onClick={() => setActiveTab('profile')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  padding: '0.3rem 0.65rem',
                  borderRadius: '9999px',
                  fontSize: '0.825rem',
                  color: '#f8fafc',
                  cursor: 'pointer'
                }}
              >
                <div style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  backgroundColor: '#2563eb',
                  color: '#ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.75rem'
                }}>
                  {user?.full_name ? user.full_name[0].toUpperCase() : 'C'}
                </div>
                <span style={{ maxWidth: '110px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {user?.full_name || 'Citizen'}
                </span>
              </div>

              <button
                onClick={logout}
                title="Sign Out"
                className="nav-button"
                style={{ padding: '0.4rem 0.6rem', color: '#cbd5e1' }}
              >
                <LogOut size={16} />
                <span style={{ fontSize: '0.8rem' }}>Sign Out</span>
              </button>
            </div>
          ) : (
            <button
              onClick={() => openAuthModal('login')}
              className="btn btn-primary"
              style={{
                padding: '0.45rem 0.9rem',
                fontSize: '0.825rem',
                borderRadius: '6px',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem'
              }}
            >
              <LogIn size={15} />
              <span>Sign In / Register</span>
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
