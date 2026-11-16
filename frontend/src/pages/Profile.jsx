import React, { useState, useEffect } from 'react';
import ProfileForm from '../components/ProfileForm';
import { api } from '../api/api';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const data = await api.getProfile();
      setProfile(data);
    } catch (err) {
      console.error("Failed to fetch profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (profileData) => {
    setIsSaving(true);
    try {
      const updated = await api.updateProfile(profileData);
      setProfile(updated);
    } catch (err) {
      alert(`Error saving profile: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div className="loading-spinner" style={{ borderColor: 'rgba(37,99,235,0.2)', borderTopColor: '#2563eb' }}></div>
        <p style={{ marginTop: '0.5rem', color: '#64748b' }}>Loading citizen profile...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', width: '100%' }}>
      <ProfileForm
        initialProfile={profile}
        onSave={handleSaveProfile}
        isSaving={isSaving}
      />
    </div>
  );
}
