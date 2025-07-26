import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add API key interceptor
api.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('gemini_api_key');
  if (apiKey) {
    config.headers['x-api-key'] = apiKey;
  }
  return config;
});

export const agentAPI = {
  runAgent: (data) => api.post('/agent', data),
  uploadFile: (formData) => api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getCase: (caseId) => api.get(`/case/${caseId}`),
  approveStep: (data) => api.post('/approve-step', data),
  getArtifact: (path) => api.get(`/artifact/${path}`, { responseType: 'blob' }),
};

export default api;