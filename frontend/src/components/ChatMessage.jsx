import React from 'react';
import SourceCard from './SourceCard';
import EligibilityCard from './EligibilityCard';
import { Layers, ShieldCheck, AlertCircle } from 'lucide-react';

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';

  return (
    <div className={`chat-message-row ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-avatar ${isUser ? 'user-avatar' : 'assistant-avatar'}`}>
        {isUser ? 'U' : 'S'}
      </div>

      <div className="message-bubble">
        <div style={{ whiteSpace: 'pre-wrap' }}>
          {message.text}
        </div>

        {/* Eligibility Card display */}
        {!isUser && message.eligibility && (
          <EligibilityCard eligibility={message.eligibility} />
        )}

        {/* Source Cards display */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="source-section">
            <div className="source-section-header">
              <Layers size={14} />
              <span>Cited Official Government Sources ({message.sources.length})</span>
            </div>
            <div className="source-cards-list">
              {message.sources.map((src, idx) => (
                <SourceCard key={idx} source={src} />
              ))}
            </div>
          </div>
        )}

        {/* Grounding & Metadata footer */}
        {!isUser && (
          <div className="message-meta">
            {message.grounded ? (
              <span style={{ color: '#059669', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <ShieldCheck size={12} /> Grounded in Official Documents
              </span>
            ) : (
              <span style={{ color: '#d97706', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <AlertCircle size={12} /> Unverified / Document Not Found
              </span>
            )}
            <span>Confidence: {message.confidence || 'medium'}</span>
          </div>
        )}
      </div>
    </div>
  );
}
