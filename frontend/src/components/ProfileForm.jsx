import React, { useState, useEffect } from 'react';
import { Save, User, CheckCircle2 } from 'lucide-react';

export default function ProfileForm({ initialProfile, onSave, isSaving }) {
  const [formData, setFormData] = useState({
    name: 'Citizen',
    state: 'Unknown',
    district: 'Unknown',
    age: '',
    education: 'Graduate',
    category: 'General',
    gender: 'Prefer not to provide',
    employment_status: 'Unknown',
    annual_income: '',
    disability_status: 'No'
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (initialProfile) {
      setFormData({
        name: initialProfile.name || 'Citizen',
        state: initialProfile.state || 'Unknown',
        district: initialProfile.district || 'Unknown',
        age: initialProfile.age ?? '',
        education: initialProfile.education || 'Graduate',
        category: initialProfile.category || 'General',
        gender: initialProfile.gender || 'Prefer not to provide',
        employment_status: initialProfile.employment_status || 'Unknown',
        annual_income: initialProfile.annual_income ?? '',
        disability_status: initialProfile.disability_status || 'No'
      });
    }
  }, [initialProfile]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      age: formData.age !== '' ? parseInt(formData.age, 10) : null,
      annual_income: formData.annual_income !== '' ? parseFloat(formData.annual_income) : null
    };
    onSave(payload);
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="profile-form-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
        <User size={24} color="#2563eb" />
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700 }}>Personal Citizen Profile</h2>
      </div>
      <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
        This profile is used strictly locally to compare your criteria against government scheme requirements.
      </p>

      {savedSuccess && (
        <div style={{
          margin: '1rem 0',
          padding: '0.75rem 1rem',
          backgroundColor: '#ecfdf5',
          border: '1px solid #a7f3d0',
          color: '#065f46',
          borderRadius: '6px',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          fontSize: '0.9rem'
        }}>
          <CheckCircle2 size={18} /> Profile updated successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              name="name"
              className="form-control"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Ramesh Kumar"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Age (Years)</label>
            <input
              type="number"
              name="age"
              className="form-control"
              value={formData.age}
              onChange={handleChange}
              placeholder="e.g. 24"
              min="1"
              max="120"
            />
          </div>

          <div className="form-group">
            <label className="form-label">State</label>
            <input
              type="text"
              name="state"
              className="form-control"
              value={formData.state}
              onChange={handleChange}
              placeholder="e.g. Karnataka"
            />
          </div>

          <div className="form-group">
            <label className="form-label">District</label>
            <input
              type="text"
              name="district"
              className="form-control"
              value={formData.district}
              onChange={handleChange}
              placeholder="e.g. Bengaluru Urban"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Highest Education</label>
            <select name="education" className="form-control" value={formData.education} onChange={handleChange}>
              <option value="10th Pass / SSLC">10th Pass / SSLC</option>
              <option value="12th Pass / PUC">12th Pass / PUC</option>
              <option value="Diploma">Diploma</option>
              <option value="Graduate">Graduate / Bachelor's Degree</option>
              <option value="Postgraduate">Postgraduate / Master's Degree</option>

              <option value="Doctorate / PhD">Doctorate / PhD</option>
              <option value="Unknown">Prefer not to say</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Social Category</label>
            <select name="category" className="form-control" value={formData.category} onChange={handleChange}>
              <option value="General">General</option>
              <option value="OBC">OBC (Other Backward Classes)</option>
              <option value="SC">SC (Scheduled Caste)</option>
              <option value="ST">ST (Scheduled Tribe)</option>
              <option value="EWS">EWS (Economically Weaker Section)</option>
              <option value="Minority">Minority Community</option>
              <option value="Unknown">Prefer not to say</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Gender</label>
            <select name="gender" className="form-control" value={formData.gender} onChange={handleChange}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Transgender">Transgender</option>
              <option value="Prefer not to provide">Prefer not to provide</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Employment Status</label>
            <select name="employment_status" className="form-control" value={formData.employment_status} onChange={handleChange}>
              <option value="Student">Student</option>
              <option value="Unemployed">Unemployed / Jobseeker</option>
              <option value="Self-Employed">Self-Employed</option>
              <option value="Salaried">Salaried Employee</option>
              <option value="Farmer / Agriculturalist">Farmer / Agriculturalist</option>
              <option value="Unknown">Prefer not to say</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Annual Family Income (₹)</label>
            <input
              type="number"
              name="annual_income"
              className="form-control"
              value={formData.annual_income}
              onChange={handleChange}
              placeholder="e.g. 180000"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Disability Status (PwD)</label>
            <select name="disability_status" className="form-control" value={formData.disability_status} onChange={handleChange}>
              <option value="No">No</option>
              <option value="Yes (>= 40% Disability)">Yes (&gt;= 40% Disability)</option>
              <option value="Yes (< 40% Disability)">Yes (&lt; 40% Disability)</option>
              <option value="Prefer not to provide">Prefer not to provide</option>
            </select>
          </div>
        </div>

        <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn btn-primary" disabled={isSaving}>
            <Save size={18} />
            <span>{isSaving ? 'Saving...' : 'Save Profile'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
