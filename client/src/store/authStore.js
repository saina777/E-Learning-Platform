import { create } from "zustand";
import { login as loginApi } from "../api/authApi";
import api, { USE_MOCK_API } from "../api/client";
import { mockApi } from "../mocks/mockApi";

const LS_TOKEN = "learnflow_token";

export const useAuthStore = create((set, get) => ({
  token: localStorage.getItem(LS_TOKEN) || null,
  user: null,

  async login(email, password) {
    const res = await loginApi({ email, password });
    localStorage.setItem(LS_TOKEN, res.access_token);
    set({ token: res.access_token });

    // fetch user
    const user = USE_MOCK_API
      ? await mockApi.me({ token: res.access_token })
      : (await api.get("/users/me")).data;

    set({ user });
    return user;
  },

  logout() {
    localStorage.removeItem(LS_TOKEN);
    set({ token: null, user: null });
  },

  async hydrate() {
    const token = localStorage.getItem(LS_TOKEN);
    if (!token) return;

    set({ token });

    try {
      const user = USE_MOCK_API
        ? await mockApi.me({ token })
        : (await api.get("/users/me")).data;

      set({ user });
    } catch {
      get().logout();
    }
  },
}));
