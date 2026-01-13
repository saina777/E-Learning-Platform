import { create } from "zustand";

const STORAGE_KEY = "learnflow_auth";

function loadAuth() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { token: null, user: null };
  } catch {
    return { token: null, user: null };
  }
}

export const useAuthStore = create((set, get) => ({
  token: loadAuth().token,
  user: loadAuth().user,

  setAuth: ({ token, user }) => {
    const data = { token, user };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    set(data);
  },

  setUser: (user) => {
    const { token } = get();
    const data = { token, user };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    set({ user });
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEY);
    set({ token: null, user: null });
  },
}));
