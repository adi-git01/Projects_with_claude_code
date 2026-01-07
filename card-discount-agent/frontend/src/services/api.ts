import axios from 'axios';
import type { SearchRequest, SearchResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for AI search
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
