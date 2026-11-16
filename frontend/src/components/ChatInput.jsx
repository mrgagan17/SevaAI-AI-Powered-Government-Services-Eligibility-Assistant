import React, { useState } from 'react';
import { Send, UserCheck, HelpCircle } from 'lucide-react';

export default function ChatInput({ onSendMessage, isLoading }) {
  const [question, setQuestion] = useState('');
  const [checkEligibility, setCheckEligibility] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;
    onSendMessage(question, checkEligibility);
    setQuestion('');
  };

  const handleQuickQuestion = (sampleText) => {
    onSendMessage(sampleText, checkEligibility);
  };

  return (
    <div className="chat-input-container">
      {/* Sample Quick Prompts */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.75rem' }}>
        {[
          "What government jobs are available for graduates?",
          "What documents are required for this scheme?",
          "Am I eligible for this scholarship?",
          "What is the last date and age limit?"
        ].map((sample, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleQuickQuestion(sample)}
            disabled={isLoading}
            style={{
              padding: '0.25rem 0.625rem',
              borderRadius: '9999px',
              backgroundColor: '#f1f5f9',
              border: '1px solid #cbd5e1',
              fontSize: '0.75rem',
              color: '#334155',
              cursor: 'pointer',
              transition: 'background 0.15s'
            }}
          >
            {sample}
          </button>
        ))}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input-field"
          placeholder="Ask SevaAI about schemes, jobs, scholarships, eligibility..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !question.trim()}
          style={{ padding: '0.75rem 1.25rem' }}
        >
          <Send size={18} />
          <span>Ask</span>
        </button>
      </form>

      <div className="chat-input-options">
        <label style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={checkEligibility}
            onChange={(e) => setCheckEligibility(e.target.checked)}
          />
          <UserCheck size={14} color="#2563eb" />
          <span>Check personalized eligibility using My Profile</span>
        </label>
      </div>
    </div>
  );
}
