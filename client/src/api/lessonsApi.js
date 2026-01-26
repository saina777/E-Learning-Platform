import api, { USE_MOCK_API } from "./client";
import { mockApi } from "../mocks/mockApi";

export async function listLessons(courseId) {
  if (USE_MOCK_API) return mockApi.listLessons(courseId);
  const res = await api.get(`/courses/${courseId}/lessons`);
  return res.data;
}

export async function getLesson(lessonId) {
  
  const res = await api.get(`/lessons/${lessonId}`);
  return res.data;
}
