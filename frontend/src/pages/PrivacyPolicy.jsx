import React from 'react';
import { Shield, Lock, EyeOff, UserCheck, Trash2, Mail } from 'lucide-react';

export default function PrivacyPolicy() {
  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', width: '100%', paddingBottom: '3rem' }}>
      {/* Header */}
      <div style={{ marginBottom: '2.5rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.35rem 0.85rem',
          backgroundColor: '#eff6ff',
          color: '#1e3a8a',
          borderRadius: '9999px',
          fontSize: '0.85rem',
          fontWeight: 600,
          marginBottom: '0.75rem'
        }}>
          <Shield size={16} />
          <span>Citizen Data Protection</span>
        </div>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
          Privacy Policy
        </h1>
        <p style={{ fontSize: '0.95rem', color: '#64748b' }}>
          Effective Date: November 2026 | Last Revised: 2026-11-14
        </p>
      </div>

      {/* Intro Card */}
      <div className="card" style={{ marginBottom: '2rem', padding: '1.75rem', borderLeft: '4px solid #2563eb' }}>
        <p style={{ fontSize: '1rem', color: '#334155', lineHeight: 1.7, margin: 0 }}>
          At <strong>SevaAI</strong>, we respect your privacy and are committed to safeguarding citizen data. This Privacy Policy details how we handle account credentials, demographic profile inputs, and query histories when you use our platform.
        </p>
      </div>

      {/* Policy Sections */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {/* Section 1 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <UserCheck size={20} color="#2563eb" />
            1. Information We Collect
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6, marginBottom: '0.75rem' }}>
            We only collect information directly provided by you to enable personalized scheme matching and query persistence:
          </p>
          <ul style={{ paddingLeft: '1.5rem', fontSize: '0.925rem', color: '#475569', lineHeight: 1.7 }}>
            <li><strong>Account Information:</strong> Name, email address, and a securely hashed password when you create an account.</li>
            <li><strong>Citizen Profile Attributes:</strong> Age, State, District, Highest Education, Social Category (General, OBC, SC, ST, EWS), Gender, Annual Income, and Disability Status. Providing these is voluntary and solely used to evaluate scheme eligibility rules.</li>
            <li><strong>Query History:</strong> Questions submitted to the assistant and the resulting source citations, saved to allow you to review previous answers.</li>
          </ul>
        </section>

        {/* Section 2 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Lock size={20} color="#059669" />
            2. How We Use Your Information
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6, marginBottom: '0.75rem' }}>
            Your information is processed strictly for the following purposes:
          </p>
          <ul style={{ paddingLeft: '1.5rem', fontSize: '0.925rem', color: '#475569', lineHeight: 1.7 }}>
            <li>Matching eligibility criteria (such as minimum education or upper age limit) against indexed government notifications.</li>
            <li>Generating source-grounded answers with exact PDF page references.</li>
            <li>Persisting your session and history across browser visits when logged in.</li>
          </ul>
        </section>

        {/* Section 3 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <EyeOff size={20} color="#dc2626" />
            3. Zero Data Monetization & Third-Party Disclosure
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6, marginBottom: '0.75rem' }}>
            We adhere to strict civic data ethics:
          </p>
          <ul style={{ paddingLeft: '1.5rem', fontSize: '0.925rem', color: '#475569', lineHeight: 1.7 }}>
            <li><strong>No Sale of Data:</strong> We never sell, rent, or lease citizen profile details or questions to data brokers, ad networks, or commercial enterprises.</li>
            <li><strong>No Tracking:</strong> We do not track your browsing activities across other third-party websites or services.</li>
            <li><strong>No Interception:</strong> We never intercept official government portal logins or credentials.</li>
          </ul>
        </section>

        {/* Section 4 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Trash2 size={20} color="#d97706" />
            4. Citizen Control, Retention & Deletion
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6, marginBottom: '0.75rem' }}>
            You maintain full sovereignty over your data:
          </p>
          <ul style={{ paddingLeft: '1.5rem', fontSize: '0.925rem', color: '#475569', lineHeight: 1.7 }}>
            <li>You can view and modify your Citizen Profile fields at any time from the <strong>My Profile</strong> page.</li>
            <li>You can wipe your entire conversation history with a single click using the <strong>Clear History</strong> button in the chat interface.</li>
          </ul>
        </section>

        {/* Section 5 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Shield size={20} color="#9333ea" />
            5. Sensitive Identification Warning
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6 }}>
            SevaAI does <strong>NOT</strong> require and strongly advises citizens <strong>NEVER</strong> to input sensitive government identification numbers (such as Aadhaar numbers, PAN details, Voter ID numbers, Passport numbers) or financial credentials (Bank account numbers, OTPs, or PINs) into chat queries. SevaAI is an educational and guidance assistant, not an application submission portal.
          </p>
        </section>

        {/* Section 6 */}
        <section className="card" style={{ padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Mail size={20} color="#2563eb" />
            6. Inquiries & Feedback
          </h2>
          <p style={{ fontSize: '0.925rem', color: '#475569', lineHeight: 1.6 }}>
            For privacy inquiries, questions regarding our source-grounding safeguards, or feedback regarding data processing, please contact the maintainers at <a href="mailto:privacy@sevaai.org" style={{ color: '#2563eb', textDecoration: 'none', fontWeight: 600 }}>privacy@sevaai.org</a>.
          </p>
        </section>
      </div>
    </div>
  );
}

