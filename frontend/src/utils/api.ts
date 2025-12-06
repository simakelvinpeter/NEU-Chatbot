import axios, { AxiosError } from 'axios';
import type { ChatRequest, ChatResponse, ApiError } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const sendMessage = async (
  message: string,
  sessionId?: string
): Promise<ChatResponse> => {
  try {
    const payload: ChatRequest = {
      message,
      session_id: sessionId,
    };

    const response = await apiClient.post<ChatResponse>('/api/chat', payload);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ApiError>;
      throw new Error(
        axiosError.response?.data?.detail || 'Failed to send message'
      );
    }
    throw new Error('An unexpected error occurred');
  }
};

export const uploadFile = async (file: File): Promise<{ url: string; id: string }> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<{ url: string; id: string }>(
      '/api/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ApiError>;
      throw new Error(
        axiosError.response?.data?.detail || 'Failed to upload file'
      );
    }
    throw new Error('An unexpected error occurred');
  }
};

export const healthCheck = async (): Promise<{ status: string }> => {
  try {
    const response = await apiClient.get<{ status: string }>('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('API is not available');
  }
};

export default apiClient;
