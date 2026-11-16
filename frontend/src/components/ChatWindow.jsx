import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import LoadingIndicator from './LoadingIndicator';
import { Trash2, MessageSquare, ShieldCheck } from 'lucide-react';

export default function ChatWindow({ messages, isLoading, onSendMessage, onClearHistory }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <MessageSquare size={20} color="#2563eb" />
          <span style={{ fontWeight: 700, fontSize: '1.05rem' }}>SevaAI Assistant</span>
          <span className="badge badge-match" style={{ fontSize: '0.7rem' }}>
            <ShieldCheck size={12} /> Source-Grounded
          </span>
        </div>

        {messages.length > 0 && (
          <button
            onClick={onClearHistory}
            className="btn btn-secondary"
            style={{ padding: '0.375rem 0.75rem', fontSize: '0.8rem' }}
          >
            <Trash2 size={14} />
            <span>Clear History</span>
          </button>
        )}
      </div>

      <div className="chat-messages-scroll" ref={scrollRef}>
        {messages.length === 0 ? (
          <div style={{ textAlign: 'center', margin: 'auto', padding: '2rem 1rem', color: '#64748b' }}>
            <div className="brand-logo-icon" style={{ margin: '0 auto 1rem', width: '56px', height: '56px', fontSize: '1.75rem' }}>
              S
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.5rem' }}>
              How can SevaAI help you today?
            </h3>
            <p style={{ fontSize: '0.9rem', maxWidth: '480px', margin: '0 auto 1.5rem' }}>
              Ask questions about government schemes, jobs, scholarships, notifications, or eligibility using indexed official source documents.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))
        )}

        {isLoading && <LoadingIndicator />}
      </div>

      <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} />
    </div>
  );
}
