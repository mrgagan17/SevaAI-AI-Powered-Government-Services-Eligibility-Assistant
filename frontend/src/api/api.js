const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

function getAuthHeaders(extraHeaders = {}) {
  const headers = { ...extraHeaders };
  const token = localStorage.getItem('sevaai_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server returned status ${response.status}`);
  }
  return response.json();
}

export const api = {
  // Authentication Endpoints
  async register(fullName, email, password) {
    const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full_name: fullName, email, password }),
    });
    return handleResponse(res);
  },

  async login(email, password) {
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return handleResponse(res);
  },

  async getMe() {
    const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  // System Health
  async getHealth() {
    const res = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(res);
  },

  // Chat & Grounded QA
  async sendChatMessage(question, checkEligibility = false) {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ question, check_eligibility: checkEligibility }),
    });
    return handleResponse(res);
  },

  async getChatHistory() {
    const res = await fetch(`${API_BASE_URL}/api/chat/history`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  async clearChatHistory() {
    const res = await fetch(`${API_BASE_URL}/api/chat/history`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  // Document Management
  async getDocuments() {
    const res = await fetch(`${API_BASE_URL}/api/documents`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  async uploadDocument(file, category = 'general') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);

    const res = await fetch(`${API_BASE_URL}/api/documents/upload`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
    return handleResponse(res);
  },

  async deleteDocument(id) {
    const res = await fetch(`${API_BASE_URL}/api/documents/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  async reindexDocument(id) {
    const res = await fetch(`${API_BASE_URL}/api/documents/${id}/reindex`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  // Citizen Profile
  async getProfile() {
    const res = await fetch(`${API_BASE_URL}/api/profile`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  async updateProfile(profileData) {
    const res = await fetch(`${API_BASE_URL}/api/profile`, {
      method: 'POST',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(profileData),
    });
    return handleResponse(res);
  },
};
