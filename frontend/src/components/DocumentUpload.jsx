import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

export default function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('general');
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      if (selected.type !== 'application/pdf') {
        setMessage({ type: 'error', text: 'Only PDF documents (.pdf) are supported.' });
        setFile(null);
        return;
      }
      setFile(selected);
      setMessage(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || isUploading) return;

    setIsUploading(true);
    setMessage(null);

    try {
      const res = await onUploadSuccess(file, category);
      setMessage({ type: 'success', text: res.message || 'PDF uploaded and indexed successfully!' });
      setFile(null);
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Upload failed.' });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '12px', padding: '1.5rem', marginBottom: '2rem' }}>
      <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <UploadCloud size={20} color="#2563eb" />
        Upload Official Government Document (PDF)
      </h3>
      <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '1.25rem' }}>
        Upload official notification gazettes, recruitment guidelines, or scholarship PDFs. Text will be automatically extracted, chunked, and indexed into local vector database.
      </p>

      {message && (
        <div style={{
          padding: '0.75rem 1rem',
          borderRadius: '6px',
          marginBottom: '1rem',
          fontSize: '0.875rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          backgroundColor: message.type === 'success' ? '#ecfdf5' : '#fef2f2',
          border: `1px solid ${message.type === 'success' ? '#a7f3d0' : '#fecaca'}`,
          color: message.type === 'success' ? '#065f46' : '#991b1b'
        }}>
          {message.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
          <span>{message.text}</span>
        </div>
      )}

      <form onSubmit={handleUpload}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 200px', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <label className="form-label">Category</label>
            <select
              className="form-control"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="general">General Notification</option>
              <option value="scholarships">Scholarship Scheme</option>
              <option value="recruitment">Government Job / Recruitment</option>
              <option value="schemes">Welfare Scheme / Benefits</option>
            </select>
          </div>

          <div>
            <label className="form-label">Selected File</label>
            <div style={{ fontSize: '0.85rem', color: file ? '#0f172a' : '#94a3b8', paddingTop: '0.5rem' }}>
              {file ? file.name : 'No file chosen'}
            </div>
          </div>
        </div>

        <div className="dropzone" onClick={() => document.getElementById('pdf-file-input').click()}>
          <input
            id="pdf-file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <FileText size={36} color="#2563eb" style={{ margin: '0 auto 0.5rem' }} />
          <div style={{ fontWeight: 600, color: '#1e293b' }}>
            {file ? file.name : 'Click to select or drag and drop official PDF file'}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
            Maximum allowed file size: 20 MB
          </div>
        </div>

        <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn btn-primary" disabled={!file || isUploading}>
            <UploadCloud size={18} />
            <span>{isUploading ? 'Extracting & Indexing...' : 'Upload & Index PDF'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
