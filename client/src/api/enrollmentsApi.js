import api, { USE_MOCK_API } from "./client";
import { mockApi } from "../mocks/mockApi";

export async function enroll(courseId, userId) {
  if (USE_MOCK_API) return mockApi.enroll({ userId, courseId: Number(courseId) });
  const res = await api.post("/enrollments", { course_id: Number(courseId) });
  return res.data;
}

export async function myEnrollments(userId) {
  if (USE_MOCK_API) return mockApi.myEnrollments({ userId });
  const res = await api.get("/enrollments/me");
  return res.data;
}

export async function updateProgress({ enrollmentId, courseId, lessonId, completed, userId }) {
  if (USE_MOCK_API) {
    return mockApi.updateProgress({
      userId,
      enrollmentId,
      courseId: Number(courseId),
      lessonId: Number(lessonId),
      completed: Boolean(completed),
    });
  }
  const res = await api.patch(`/enrollments/${enrollmentId}/progress`, {
    lesson_id: Number(lessonId),
    completed: Boolean(completed),
  });
  return res.data;
}
