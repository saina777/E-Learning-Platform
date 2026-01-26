import api, { USE_MOCK_API } from "./client";
import { mockApi } from "../mocks/mockApi";

export async function getDashboard(userId) {
  if (USE_MOCK_API) return mockApi.dashboard({ userId });
  const res = await api.get("/dashboard");
  return res.data;
}
