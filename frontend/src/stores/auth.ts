import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: '',
    refreshToken: '',
    userName: '',
    userRoles: [] as string[],
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    setTokens(access: string, refresh: string, roles: string[]) {
      this.accessToken = access;
      this.refreshToken = refresh;
      this.userRoles = roles;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('userRoles', JSON.stringify(roles));
    },
    loadTokens() {
      this.accessToken = localStorage.getItem('accessToken') || '';
      this.refreshToken = localStorage.getItem('refreshToken') || '';
      this.userRoles = JSON.parse(localStorage.getItem('userRoles') || '[]');
    },
    clearTokens() {
      this.accessToken = '';
      this.refreshToken = '';
      this.userRoles = [];
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('userRoles');
    },
    clear() {
      this.clearTokens();
      this.userName = '';
    },
  },
});
