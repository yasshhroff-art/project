/**
 * API service layer for communicating with the backend.
 * Centralized HTTP requests using Axios.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Campaign API methods
 */
export const campaignAPI = {
  /**
   * Get all campaigns
   */
  getAll: async () => {
    const response = await api.get('/campaigns');
    return response.data;
  },

  /**
   * Get a single campaign by ID
   */
  getById: async (id) => {
    const response = await api.get(`/campaigns/${id}`);
    return response.data;
  },

  /**
   * Create a new campaign
   */
  create: async (campaignData) => {
    const response = await api.post('/campaigns', campaignData);
    return response.data;
  },

  /**
   * Update an existing campaign
   */
  update: async (id, campaignData) => {
    const response = await api.put(`/campaigns/${id}`, campaignData);
    return response.data;
  },

  /**
   * Delete a campaign
   */
  delete: async (id) => {
    const response = await api.delete(`/campaigns/${id}`);
    return response.data;
  },

  /**
   * Publish a campaign to Google Ads
   */
  publish: async (id) => {
    const response = await api.post(`/campaigns/${id}/publish`);
    return response.data;
  },

  /**
   * Disable (pause) a campaign in Google Ads
   */
  disable: async (id) => {
    const response = await api.post(`/campaigns/${id}/disable`);
    return response.data;
  },
};

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
