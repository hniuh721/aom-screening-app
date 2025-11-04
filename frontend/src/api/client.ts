// API client for backend communication
import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance (no authentication required)
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const api = {
  // Questionnaires (anonymous access)
  createQuestionnaire: (data: any) => apiClient.post('/questionnaires/anonymous', data),
  getQuestionnaire: (id: number) => apiClient.get(`/questionnaires/${id}`),
  submitQuestionnaire: (id: number) => apiClient.post(`/questionnaires/${id}/submit`),

  // Screening (anonymous access)
  runScreening: (questionnaireId: number) => apiClient.post(`/screening/run/${questionnaireId}`),
  getScreeningResults: (questionnaireId: number) => apiClient.get(`/screening/results/${questionnaireId}`),
};

export default apiClient;
