import React, { useState, useEffect } from 'react';
import DocumentUpload from '../components/DocumentUpload';
import DocumentCard from '../components/DocumentCard';
import { api } from '../api/api';
import { FileText, Database } from 'lucide-react';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await api.getDocuments();
      setDocuments(docs || []);
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = async (file, category) => {
    const result = await api.uploadDocument(file, category);
    await loadDocuments();
    return result;
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this document and remove its embeddings?")) return;
    try {
      await api.deleteDocument(id);
      await loadDocuments();
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleReindex = async (id) => {
    try {
      await api.reindexDocument(id);
      alert("Document re-indexed successfully.");
      await loadDocuments();
    } catch (err) {
      alert(`Re-indexing failed: ${err.message}`);
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      <DocumentUpload onUploadSuccess={handleUploadSuccess} />

      <div style={{ backgroundColor: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '12px', padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Database size={20} color="#2563eb" />
              Indexed Government Documents ({documents.length})
            </h3>
            <p style={{ fontSize: '0.85rem', color: '#64748b' }}>
              Documents available for SevaAI vector search and grounded retrieval.
            </p>
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div className="loading-spinner" style={{ borderColor: 'rgba(37,99,235,0.2)', borderTopColor: '#2563eb' }}></div>
          </div>
        ) : documents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', backgroundColor: '#f8fafc', borderRadius: '8px', color: '#64748b' }}>
            <FileText size={32} color="#94a3b8" style={{ margin: '0 auto 0.5rem' }} />
            <div>No government documents are currently indexed.</div>
            <div style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>
              Upload an official PDF above or add files to <code>data/documents/</code> and run <code>python scripts/ingest_documents.py</code>.
            </div>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="document-table">
              <thead>
                <tr>
                  <th>Document Name</th>
                  <th>Category</th>
                  <th>Upload Date</th>
                  <th>Pages / Chunks</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <DocumentCard
                    key={doc.id}
                    doc={doc}
                    onDelete={handleDelete}
                    onReindex={handleReindex}
                  />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
