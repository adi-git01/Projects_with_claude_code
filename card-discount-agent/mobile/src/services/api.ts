import axios from 'axios';
import type { SearchRequest, SearchResponse } from '../types';

// Change this to your backend URL
// For local development on Android emulator: use 10.0.2.2
// For local development on physical device: use your computer's IP
const API_BASE_URL = __DEV__
  ? 'http://10.0.2.2:8000/api'  // Android emulator
  : 'https://your-production-api.com/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchDeals = async (request: SearchRequest): Promise<SearchResponse> => {
  const response = await apiClient.post<SearchResponse>('/search', request);
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await apiClient.get('/health');
  return response.data;
};

export { API_BASE_URL };
