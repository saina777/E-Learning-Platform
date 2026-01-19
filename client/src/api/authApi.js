import api, { USE_MOCK_API } from "./client";
import { mockApi } from "../mocks/mockApi";

export async function login(payload) {
  if (USE_MOCK_API) return mockApi.login(payload);
  const res = await api.post("/auth/login", payload);
  return res.data;
}

export async function register(payload) {
  if (USE_MOCK_API) return { message: "Registered (mock)" };
  const res = await api.post("/auth/register", payload);
  return res.data;
}

export async function requestPasswordReset(payload) {
  if (USE_MOCK_API) return { token: "mock-reset-token-123" };
  const res = await api.post("/auth/request-password-reset", payload);
  return res.data;
}

export async function resetPassword(payload) {
  if (USE_MOCK_API) return { message: "Password reset (mock)" };
  const res = await api.post("/auth/reset-password", payload);
  return res.data;
}
