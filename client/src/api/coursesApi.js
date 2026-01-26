import api, { USE_MOCK_API } from "./client";
import { mockApi } from "../mocks/mockApi";

export async function listCourses(params = {}) {
  if (USE_MOCK_API) return mockApi.listCourses(params);
  const res = await api.get("/courses", { params });
  return res.data;
}

export async function getCourse(courseId) {
  if (USE_MOCK_API) return mockApi.getCourse(courseId);
  const res = await api.get(`/courses/${courseId}`);
  return res.data;
}
