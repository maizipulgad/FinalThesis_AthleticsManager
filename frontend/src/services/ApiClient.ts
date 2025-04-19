import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const ApiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

ApiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  const accessToken = authStore.accessToken;

  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`;
  }
  return config;
});

export default ApiClient;

// Refresh Token Handling
ApiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      const authStore = useAuthStore();
      try {
        const refreshResponse = await axios.post(`${ApiClient.defaults.baseURL}token/refresh/`, {
          refresh: authStore.refreshToken,
        });

        authStore.setTokens(refreshResponse.data.access, authStore.refreshToken, authStore.userRoles);
        error.config.headers['Authorization'] = `Bearer ${refreshResponse.data.access}`;
        return axios.request(error.config);
      } catch (refreshError) {
        authStore.clearTokens();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
