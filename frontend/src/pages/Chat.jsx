import React, { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow';
import { api } from '../api/api';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const history = await api.getChatHistory();
      if (Array.isArray(history)) {
        const formatted = history.map(item => [
          { sender: 'user', text: item.question },
          {
            sender: 'assistant',
            text: item.answer,
            sources: item.sources || [],
            confidence: item.confidence,
            grounded: item.grounded
          }
        ]).flat();
        setMessages(formatted);
      }
    } catch (err) {
      console.warn("Chat history fetch error:", err);
    }
  };

  const handleSendMessage = async (question, checkEligibility) => {
    // Append user message immediately
    const newMessages = [...messages, { sender: 'user', text: question }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(question, checkEligibility);
      setMessages([
        ...newMessages,
        {
          sender: 'assistant',
          text: response.answer,
          sources: response.sources || [],
          confidence: response.confidence || 'medium',
          grounded: response.grounded,
          eligibility: response.eligibility
        }
      ]);
    } catch (err) {
      setMessages([
        ...newMessages,
        {
          sender: 'assistant',
          text: `Error processing query: ${err.message || 'Server error'}`,
          sources: [],
          confidence: 'low',
          grounded: false
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await api.clearChatHistory();
      setMessages([]);
    } catch (err) {
      console.error("Failed to clear chat history:", err);
    }
  };

  return (
    <div className="chat-page">
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        onClearHistory={handleClearHistory}
      />
    </div>
  );
}
