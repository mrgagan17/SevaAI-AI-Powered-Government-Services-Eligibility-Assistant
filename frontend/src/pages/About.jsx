import React from 'react';
import { ShieldCheck, FileCheck, Layers, Users, CheckCircle, ArrowRight, BookOpen, AlertTriangle } from 'lucide-react';

export default function About({ setActiveTab }) {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', width: '100%', paddingBottom: '3rem' }}>
      {/* Header */}
      <div style={{ marginBottom: '2.5rem', textAlign: 'center' }}>
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
          marginBottom: '1rem'
        }}>
          <BookOpen size={16} />
          <span>Independent Civic Intelligence Platform</span>
        </div>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.75rem' }}>
          About SevaAI
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#64748b', maxWidth: '700px', margin: '0 auto', lineHeight: 1.6 }}>
          Democratizing citizen access to official government schemes, recruitment notifications, and welfare benefits through verifiable, source-grounded AI.
        </p>
      </div>

      {/* Mission Section */}
      <div className="card" style={{ marginBottom: '2rem', padding: '2rem' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '1rem' }}>
          Our Mission
        </h2>
        <p style={{ fontSize: '1rem', color: '#334155', lineHeight: 1.7, marginBottom: '1rem' }}>
          Every year, millions of eligible citizens miss out on crucial scholarships, employment drives, and social welfare programs because official government notifications are buried in dense, multi-page PDFs written in complex bureaucratic terminology. Meanwhile, third-party blogs often spread outdated or inaccurate criteria.
        </p>
        <p style={{ fontSize: '1rem', color: '#334155', lineHeight: 1.7 }}>
          <strong>SevaAI</strong> bridges this critical gap. We empower citizens, students, and job seekers by transforming authentic government PDF documents into an interactive, natural-language conversational assistant that provides transparent eligibility analysis and verifiable page-by-page citations.
        </p>
      </div>

      {/* Core Architectural Pillars */}
      <h2 style={{ fontSize: '1.35rem', fontWeight: 700, color: '#0f172a', marginBottom: '1.25rem' }}>
        Our Core Guarantees
      </h2>
      <div className="feature-grid" style={{ marginBottom: '2.5rem' }}>
        <div className="card">
          <div className="card-icon" style={{ background: '#ecfdf5', color: '#059669' }}>
            <FileCheck size={24} />
          </div>
          <h3 className="card-title">100% Source-Grounded</h3>
          <p className="card-desc">
            Answers are synthesized strictly from indexed official government PDFs. If a detail is absent in the document, SevaAI explicitly refuses to fabricate it.
          </p>
        </div>

        <div className="card">
          <div className="card-icon" style={{ background: '#eff6ff', color: '#2563eb' }}>
            <Layers size={24} />
          </div>
          <h3 className="card-title">Exact Page Citations</h3>
          <p className="card-desc">
            Every answer includes clickable citation cards detailing the official document title, exact page number, and original text snippet for easy citizen verification.
          </p>
        </div>

        <div className="card">
          <div className="card-icon" style={{ background: '#fffbeb', color: '#d97706' }}>
            <Users size={24} />
          </div>
          <h3 className="card-title">Transparent Eligibility</h3>
          <p className="card-desc">
            Evaluates citizen profiles against age limits, education qualifications, category relaxations, and income thresholds with clear MATCH / NOT_MATCHED classifications.
          </p>
        </div>

        <div className="card">
          <div className="card-icon" style={{ background: '#f3e8ff', color: '#9333ea' }}>
            <ShieldCheck size={24} />
          </div>
          <h3 className="card-title">Zero Privacy Compromise</h3>
          <p className="card-desc">
            Citizen demographic information is used strictly to evaluate eligibility rules and is never sold, monetized, or shared with third-party advertisers.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="card" style={{ marginBottom: '2.5rem', padding: '2rem' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#0f172a', marginBottom: '1.5rem' }}>
          How SevaAI Works
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
          <div style={{ borderLeft: '3px solid #2563eb', paddingLeft: '1rem' }}>
            <div style={{ fontWeight: 700, color: '#1e3a8a', marginBottom: '0.25rem' }}>1. PDF Ingestion</div>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Official government notification PDFs are parsed using PyMuPDF and split into contextual, page-tracked chunks.
            </p>
          </div>
          <div style={{ borderLeft: '3px solid #059669', paddingLeft: '1rem' }}>
            <div style={{ fontWeight: 700, color: '#059669', marginBottom: '0.25rem' }}>2. Semantic Search</div>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Sentence-transformer embeddings index document concepts into a local ChromaDB vector store.
            </p>
          </div>
          <div style={{ borderLeft: '3px solid #d97706', paddingLeft: '1rem' }}>
            <div style={{ fontWeight: 700, color: '#d97706', marginBottom: '0.25rem' }}>3. Guarded Reasoning</div>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Retrieved text context is supplied to a high-precision language model with strict anti-hallucination instructions.
            </p>
          </div>
          <div style={{ borderLeft: '3px solid #9333ea', paddingLeft: '1rem' }}>
            <div style={{ fontWeight: 700, color: '#9333ea', marginBottom: '0.25rem' }}>4. Verified Output</div>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Citizens receive answers alongside supporting citations and a personalized eligibility summary.
            </p>
          </div>
        </div>
      </div>

      {/* Legal & Non-Affiliation Disclaimer */}
      <div style={{
        backgroundColor: '#fffbeb',
        border: '1px solid #fde68a',
        borderRadius: '12px',
        padding: '1.5rem',
        marginBottom: '2.5rem',
        display: 'flex',
        gap: '1rem',
        alignItems: 'flex-start'
      }}>
        <AlertTriangle size={24} color="#d97706" style={{ flexShrink: 0, marginTop: '2px' }} />
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#92400e', marginBottom: '0.35rem' }}>
            Official Non-Affiliation & Verification Notice
          </h3>
          <p style={{ fontSize: '0.875rem', color: '#78350f', lineHeight: 1.6, margin: 0 }}>
            SevaAI is an independent open-access civic technology initiative. SevaAI is <strong>NOT</strong> an official government website, is not affiliated with, authorized, maintained, sponsored, or endorsed by any government ministry, department, or public agency. All information provided by SevaAI is for informational guidance only and must always be cross-referenced with the official issuing authority or gazette notification before taking legal or financial action.
          </p>
        </div>
      </div>

      {/* Action CTA */}
      <div style={{ textAlign: 'center' }}>
        <button className="btn btn-primary" onClick={() => setActiveTab('chat')} style={{ padding: '0.75rem 1.75rem', fontSize: '1rem' }}>
          <span>Start Asking SevaAI</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}

