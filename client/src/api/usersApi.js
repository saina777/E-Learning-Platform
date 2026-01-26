import apiClient from './client.js';

export const usersApi = {
  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  updateCurrentUser: async (userData) => {
    const response = await apiClient.put('/users/me', userData);
    return response.data;
  }
};