import React from 'react';
import { ShieldCheck, ExternalLink, Heart } from 'lucide-react';

export default function Footer({ setActiveTab }) {
  return (
    <footer style={{
      backgroundColor: '#0f172a',
      color: '#94a3b8',
      borderTop: '1px solid rgba(255, 255, 255, 0.08)',
      padding: '2.5rem 1.5rem 1.5rem',
      marginTop: 'auto'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '2rem',
        marginBottom: '2rem'
      }}>
        {/* Brand Column */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.75rem', cursor: 'pointer' }} onClick={() => setActiveTab('home')}>
            <div className="brand-logo-icon" style={{ width: '32px', height: '32px', fontSize: '1rem' }}>S</div>
            <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#ffffff' }}>SevaAI</span>
          </div>
          <p style={{ fontSize: '0.85rem', lineHeight: 1.6, color: '#94a3b8', margin: 0 }}>
            Source-grounded AI assistant for official government schemes, employment recruitments, and scholarship notifications with exact citations.
          </p>
        </div>

        {/* Navigation Links */}
        <div>
          <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.85rem' }}>
            Features
          </div>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
            <li>
              <button
                onClick={() => setActiveTab('home')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                Home Dashboard
              </button>
            </li>
            <li>
              <button
                onClick={() => setActiveTab('chat')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                Ask Assistant
              </button>
            </li>
            <li>
              <button
                onClick={() => setActiveTab('profile')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                Eligibility Profile
              </button>
            </li>
            <li>
              <button
                onClick={() => setActiveTab('documents')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                Official Documents
              </button>
            </li>
          </ul>
        </div>

        {/* Company & Legal */}
        <div>
          <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.85rem' }}>
            Transparency & Legal
          </div>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
            <li>
              <button
                onClick={() => setActiveTab('about')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                About SevaAI
              </button>
            </li>
            <li>
              <button
                onClick={() => setActiveTab('privacy')}
                style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', padding: 0 }}
              >
                Privacy Policy
              </button>
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#10b981', fontSize: '0.8rem' }}>
              <ShieldCheck size={14} />
              <span>Zero-Hallucination Verified</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar with Disclaimer */}
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        paddingTop: '1.5rem',
        borderTop: '1px solid rgba(255, 255, 255, 0.08)',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '1rem',
        fontSize: '0.8rem',
        color: '#64748b'
      }}>
        <div>
          © 2026 SevaAI. Independent AI Assistance Platform. All rights reserved.
        </div>
        <div style={{ maxWidth: '600px', textAlign: 'right' }}>
          Non-Affiliation: SevaAI is not affiliated with or endorsed by any government entity. Always verify with official gazettes.
        </div>
      </div>
    </footer>
  );
}

