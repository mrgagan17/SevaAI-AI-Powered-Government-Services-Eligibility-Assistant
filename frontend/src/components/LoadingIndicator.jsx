import React from 'react';
import { Bot } from 'lucide-react';

export default function LoadingIndicator({ message = 'Retrieving official context & generating grounded response...' }) {
  return (
    <div className="chat-message-row assistant">
      <div className="message-avatar assistant-avatar">S</div>
      <div className="message-bubble" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div className="loading-spinner" style={{ borderColor: 'rgba(37,99,235,0.2)', borderTopColor: '#2563eb' }}></div>
        <span style={{ fontSize: '0.875rem', color: '#475569' }}>{message}</span>
      </div>
    </div>
  );
}
