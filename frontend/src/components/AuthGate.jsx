import React from 'react';
import { Lock, LogIn, UserPlus, ArrowLeft, ShieldCheck, FileText, MessageSquare, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AuthGate({ type = 'chat', setActiveTab }) {
  const { openAuthModal } = useAuth();

  const configs = {
    chat: {
      icon: MessageSquare,
      title: 'Sign In to Ask SevaAI Assistant',
      desc: 'To ask questions, evaluate scheme eligibility, and save your verified source citations, please sign in or create an account.',
      badge: 'Protected Assistant'
    },
    documents: {
      icon: FileText,
      title: 'Sign In to View Official Documents',
      desc: 'Access to the official government PDF repository, recruitment gazettes, and scholarship circulars requires citizen authentication.',
      badge: 'Verified Repository'
    },
    profile: {
      icon: User,
      title: 'Citizen Profile Access Restricted',
      desc: 'Citizen profiles are private and personal to each user. Please sign in to view and update your eligibility criteria.',
      badge: 'Private Citizen Profile'
    }
  };

  const current = configs[type] || configs.chat;
  const IconComponent = current.icon;

  return (
    <div style={{
      maxWidth: '620px',
      margin: '3rem auto',
      width: '100%',
      padding: '0 1rem'
    }}>
      <div className="card" style={{
        padding: '2.5rem 2rem',
        textAlign: 'center',
        border: '1px solid #cbd5e1',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
        borderRadius: '16px'
      }}>
        {/* Badge */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          padding: '0.3rem 0.8rem',
          backgroundColor: '#eff6ff',
          color: '#1e3a8a',
          borderRadius: '9999px',
          fontSize: '0.8rem',
          fontWeight: 600,
          marginBottom: '1.25rem'
        }}>
          <Lock size={14} color="#2563eb" />
          <span>{current.badge}</span>
        </div>

        {/* Icon Circle */}
        <div style={{
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          backgroundColor: '#f1f5f9',
          color: '#1e3a8a',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1.25rem',
          border: '1px solid #e2e8f0'
        }}>
          <IconComponent size={30} color="#1e3a8a" />
        </div>

        {/* Heading & Description */}
        <h2 style={{ fontSize: '1.45rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.75rem' }}>
          {current.title}
        </h2>
        <p style={{ fontSize: '0.95rem', color: '#64748b', lineHeight: 1.6, marginBottom: '2rem', maxWidth: '480px', margin: '0 auto 2rem' }}>
          {current.desc}
        </p>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
          <button
            className="btn btn-primary"
            onClick={() => openAuthModal('login')}
            style={{ padding: '0.65rem 1.5rem', fontSize: '0.925rem' }}
          >
            <LogIn size={17} />
            <span>Sign In to Continue</span>
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => openAuthModal('register')}
            style={{ padding: '0.65rem 1.5rem', fontSize: '0.925rem' }}
          >
            <UserPlus size={17} />
            <span>Create Free Account</span>
          </button>
        </div>

        {/* Return to Home link */}
        <button
          onClick={() => setActiveTab('home')}
          style={{
            background: 'none',
            border: 'none',
            color: '#64748b',
            fontSize: '0.875rem',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            padding: '0.25rem 0.5rem',
            borderRadius: '4px',
            transition: 'color 0.2s'
          }}
          onMouseEnter={(e) => (e.target.style.color = '#0f172a')}
          onMouseLeave={(e) => (e.target.style.color = '#64748b')}
        >
          <ArrowLeft size={15} />
          <span>Return to Home Dashboard</span>
        </button>

        {/* Feature points */}
        <div style={{
          marginTop: '2rem',
          paddingTop: '1.5rem',
          borderTop: '1px solid #f1f5f9',
          display: 'flex',
          justifyContent: 'center',
          gap: '1.5rem',
          flexWrap: 'wrap',
          fontSize: '0.8rem',
          color: '#64748b'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <ShieldCheck size={15} color="#059669" />
            <span>Private & Isolated</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <ShieldCheck size={15} color="#059669" />
            <span>Source-Grounded Citations</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <ShieldCheck size={15} color="#059669" />
            <span>Zero Data Sharing</span>
          </div>
        </div>
      </div>
    </div>
  );
}
