import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AuthModal from './components/AuthModal';
import AuthGate from './components/AuthGate';
import { AuthProvider, useAuth } from './context/AuthContext';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Profile from './pages/Profile';
import Documents from './pages/Documents';
import About from './pages/About';
import PrivacyPolicy from './pages/PrivacyPolicy';
import { api } from './api/api';

function AppContent() {
  const [activeTab, setActiveTab] = useState('home');
  const [healthInfo, setHealthInfo] = useState(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    fetchHealthStatus();
  }, []);

  const fetchHealthStatus = async () => {
    try {
      const info = await api.getHealth();
      setHealthInfo(info);
    } catch (err) {
      console.warn("Backend health check failed:", err);
    }
  };

  return (
    <div className="app-container">
      {/* Official Government Disclaimer Banner */}
      <div className="app-disclaimer-banner">
        <strong>Disclaimer:</strong> SevaAI is an independent AI assistance project. Information is provided for guidance and should be verified with the official government source before taking action.
      </div>

      {/* Top Navigation Bar (Primary Site Navigation) */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="app-body">
        <main className="main-content">
          {activeTab === 'home' && <Home setActiveTab={setActiveTab} healthInfo={healthInfo} />}

          {/* Ask Assistant - Protected (Requires Login/Signup) */}
          {activeTab === 'chat' && (
            isAuthenticated ? <Chat /> : <AuthGate type="chat" setActiveTab={setActiveTab} />
          )}

          {/* Citizen Profile - Strictly Private to Logged-in User */}
          {activeTab === 'profile' && (
            isAuthenticated ? <Profile /> : <AuthGate type="profile" setActiveTab={setActiveTab} />
          )}

          {/* Official Documents - Protected (Requires Login/Signup) */}
          {activeTab === 'documents' && (
            isAuthenticated ? <Documents /> : <AuthGate type="documents" setActiveTab={setActiveTab} />
          )}

          {/* Transparency & Legal */}
          {activeTab === 'about' && <About setActiveTab={setActiveTab} />}
          {activeTab === 'privacy' && <PrivacyPolicy />}

          {/* Cohesive Footer */}
          <Footer setActiveTab={setActiveTab} />
        </main>
      </div>

      {/* Global Authentication Modal (Login / Signup) */}
      <AuthModal />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
