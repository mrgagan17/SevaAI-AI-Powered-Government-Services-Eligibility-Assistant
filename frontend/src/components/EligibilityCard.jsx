import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle, ShieldAlert } from 'lucide-react';

export default function EligibilityCard({ eligibility }) {
  if (!eligibility) return null;

  const getStatusBadge = (status) => {
    switch (status) {
      case 'MATCH':
        return <span className="badge badge-match"><CheckCircle2 size={14} /> MATCH</span>;
      case 'PARTIAL_MATCH':
        return <span className="badge badge-partial"><AlertTriangle size={14} /> PARTIAL MATCH</span>;
      case 'NOT_MATCHED':
        return <span className="badge badge-notmatched"><XCircle size={14} /> NOT MATCHED</span>;
      default:
        return <span className="badge badge-unknown"><HelpCircle size={14} /> UNKNOWN</span>;
    }
  };

  return (
    <div style={{
      marginTop: '1rem',
      backgroundColor: '#ffffff',
      border: '1px solid #cbd5e1',
      borderRadius: '8px',
      padding: '1rem'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#0f172a' }}>
          Eligibility Guidance Assessment
        </div>
        {getStatusBadge(eligibility.status)}
      </div>

      <p style={{ fontSize: '0.875rem', color: '#334155', marginBottom: '0.75rem' }}>
        {eligibility.summary}
      </p>

      {eligibility.criteria && eligibility.criteria.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem', marginBottom: '0.75rem' }}>
          {eligibility.criteria.map((item, idx) => (
            <div key={idx} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem',
              fontSize: '0.8125rem',
              padding: '0.375rem 0.5rem',
              backgroundColor: '#f8fafc',
              borderRadius: '4px'
            }}>
              {item.status === 'MATCH' && <CheckCircle2 size={16} color="#059669" style={{ flexShrink: 0, marginTop: '2px' }} />}
              {item.status === 'PARTIAL_MATCH' && <AlertTriangle size={16} color="#d97706" style={{ flexShrink: 0, marginTop: '2px' }} />}
              {item.status === 'NOT_MATCHED' && <XCircle size={16} color="#dc2626" style={{ flexShrink: 0, marginTop: '2px' }} />}
              {item.status === 'UNKNOWN' && <HelpCircle size={16} color="#64748b" style={{ flexShrink: 0, marginTop: '2px' }} />}
              
              <div>
                <strong>{item.criterion}:</strong> {item.note}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{ fontSize: '0.75rem', color: '#64748b', fontStyle: 'italic', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
        <ShieldAlert size={14} />
        <span>{eligibility.disclaimer}</span>
      </div>
    </div>
  );
}
