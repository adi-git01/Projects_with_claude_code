import axios, { AxiosError } from 'axios';
import type { SearchRequest, SearchResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for AI search
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const { status, data } = error.response;

      // Handle rate limit errors (429)
      if (status === 429) {
        const detail = data as any;
        if (detail?.message) {
          throw new Error(`Rate Limit: ${detail.message}`);
        } else if (detail?.suggestion) {
          throw new Error(`Rate Limit: ${detail.suggestion}`);
        } else {
          throw new Error('API rate limit exceeded. Please wait a few minutes and try again.');
        }
      }

      // Handle other HTTP errors
      const errorMessage = (data as any)?.detail || (data as any)?.message || error.message;
      throw new Error(`Request failed with status code ${status}: ${errorMessage}`);
    }

    // Network or timeout errors
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timed out. Please try again.');
    }

    throw new Error(error.message || 'An unknown error occurred');
  }
);

export const searchDeals = async (request: SearchRequest): Promise<SearchResponse> => {
  const response = await apiClient.post<SearchResponse>('/search', request);
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await apiClient.get('/health');
  return response.data;
};
