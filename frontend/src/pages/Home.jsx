import React from 'react';
import { MessageSquare, UserCheck, FileCheck, Layers, ArrowRight, LogIn, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Home({ setActiveTab, healthInfo }) {
  const { isAuthenticated, openAuthModal } = useAuth();

  const handleProtectedAction = (targetTab) => {
    setActiveTab(targetTab);
    if (!isAuthenticated) {
      openAuthModal('login');
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      {/* Hero Header */}
      <section className="hero-section">
        <h1 className="hero-title">SevaAI</h1>
        <div className="hero-tagline">
          Understand Government Services. Find What Applies to You.
        </div>
        <p className="hero-desc">
          Ask questions in natural language about government schemes, jobs, scholarships, notifications, benefits, and required documents using trusted source documents.
        </p>

        <div className="hero-buttons">
          <button className="btn btn-primary" onClick={() => handleProtectedAction('chat')}>
            <MessageSquare size={18} />
            <span>Ask Assistant</span>
            {!isAuthenticated ? <Lock size={14} style={{ opacity: 0.75 }} /> : <ArrowRight size={16} />}
          </button>

          <button className="btn btn-secondary" onClick={() => handleProtectedAction('documents')}>
            <FileCheck size={18} />
            <span>Government Documents</span>
            {!isAuthenticated && <Lock size={14} style={{ opacity: 0.75 }} />}
          </button>

          {/* Citizen Profile is shown ONLY to authenticated users */}
          {isAuthenticated ? (
            <button className="btn btn-secondary" onClick={() => setActiveTab('profile')}>
              <UserCheck size={18} />
              <span>Citizen Profile</span>
            </button>
          ) : (
            <button className="btn btn-secondary" onClick={() => openAuthModal('login')}>
              <LogIn size={18} />
              <span>Sign In to Check Eligibility</span>
            </button>
          )}
        </div>
      </section>

      {/* Feature Cards Grid */}
      <div className="feature-grid">
        <div className="card" onClick={() => handleProtectedAction('chat')} style={{ cursor: 'pointer' }}>
          <div className="card-icon">
            <MessageSquare size={24} />
          </div>
          <h3 className="card-title">AI Government Assistant</h3>
          <p className="card-desc">
            Ask questions in plain English or regional languages about government notifications, procedures, and dates.
          </p>
        </div>

        <div className="card" onClick={() => handleProtectedAction('documents')} style={{ cursor: 'pointer' }}>
          <div className="card-icon" style={{ background: '#ecfdf5', color: '#059669' }}>
            <FileCheck size={24} />
          </div>
          <h3 className="card-title">Source-Grounded Answers</h3>
          <p className="card-desc">
            Answers are generated strictly using indexed official PDFs to prevent hallucinated rules or deadlines.
          </p>
        </div>

        <div
          className="card"
          onClick={() => (isAuthenticated ? setActiveTab('profile') : openAuthModal('login'))}
          style={{ cursor: 'pointer' }}
        >
          <div className="card-icon" style={{ background: '#fffbeb', color: '#d97706' }}>
            <UserCheck size={24} />
          </div>
          <h3 className="card-title">Eligibility Guidance</h3>
          <p className="card-desc">
            Transparently compares age, education, and income limits against your personal profile without guessing.
          </p>
        </div>

        <div className="card">
          <div className="card-icon" style={{ background: '#f3e8ff', color: '#9333ea' }}>
            <Layers size={24} />
          </div>
          <h3 className="card-title">Source Citations</h3>
          <p className="card-desc">
            See exact supporting PDF document names, page numbers, and snippet previews for every factual statement.
          </p>
        </div>
      </div>

      {/* Health / System Status Bar */}
      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid #cbd5e1',
        borderRadius: '12px',
        padding: '1.25rem',
        marginTop: '2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>System Status</div>
          <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
            Local LLM: <strong>{healthInfo?.ollama?.model || 'qwen3:4b'}</strong> | Status: <strong>{healthInfo?.ollama?.status || 'checking'}</strong>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#2563eb' }}>
              {healthInfo?.indexed_chunks ?? 0}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Indexed Text Chunks</div>
          </div>

          <button
            className="btn btn-secondary"
            onClick={() => handleProtectedAction('documents')}
            style={{ fontSize: '0.8rem' }}
          >
            Manage Documents
          </button>
        </div>
      </div>
    </div>
  );
}
