import React from 'react';
import { FileText, RefreshCw, Trash2, CheckCircle2 } from 'lucide-react';

export default function DocumentCard({ doc, onDelete, onReindex }) {
  return (
    <tr>
      <td>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 600 }}>
          <FileText size={18} color="#2563eb" />
          <span>{doc.filename}</span>
        </div>
      </td>
      <td>
        <span className="badge badge-unknown" style={{ textTransform: 'capitalize' }}>
          {doc.category || 'general'}
        </span>
      </td>
      <td>{doc.upload_date}</td>
      <td>{doc.page_count} pages ({doc.chunk_count} chunks)</td>
      <td>
        <span className="badge badge-match" style={{ fontSize: '0.7rem' }}>
          <CheckCircle2 size={12} /> {doc.status || 'Indexed'}
        </span>
      </td>
      <td>
        <div style={{ display: 'flex', gap: '0.375rem' }}>
          <button
            onClick={() => onReindex(doc.id)}
            className="btn btn-secondary"
            title="Re-index vector embeddings"
            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
          >
            <RefreshCw size={14} />
          </button>
          <button
            onClick={() => onDelete(doc.id)}
            className="btn btn-secondary"
            title="Delete document"
            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', color: '#dc2626' }}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </td>
    </tr>
  );
}
