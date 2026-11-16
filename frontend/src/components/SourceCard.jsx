import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, Calendar, Tag } from 'lucide-react';

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="source-card">
      <div 
        className="source-card-header" 
        onClick={() => setExpanded(!expanded)} 
        style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FileText size={16} color="#2563eb" />
          <span style={{ fontWeight: 600 }}>{source.document}</span>
          <span className="badge badge-unknown" style={{ textTransform: 'capitalize' }}>
            Page {source.page}
          </span>
          {source.category && (
            <span className="badge badge-unknown" style={{ textTransform: 'capitalize' }}>
              {source.category}
            </span>
          )}
        </div>
        <div>
          {expanded ? <ChevronUp size={16} color="#64748b" /> : <ChevronDown size={16} color="#64748b" />}
        </div>
      </div>

      {expanded && (
        <div style={{ marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px dashed #e2e8f0' }}>
          <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#64748b', marginBottom: '0.375rem' }}>
            <span>Category: <strong>{source.category || 'General'}</strong></span>
            {source.document_date && <span>Document Date: <strong>{source.document_date}</strong></span>}
            {source.score > 0 && <span>Relevance: <strong>{Math.round(source.score * 100)}%</strong></span>}
          </div>
          <div className="source-snippet">
            "{source.snippet}"
          </div>
        </div>
      )}
    </div>
  );
}
