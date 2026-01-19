import { mockUsers, mockCourses, mockLessonsByCourseId } from "./mockData";

const sleep = (ms = 250) => new Promise((r) => setTimeout(r, ms));

const LS_ENROLLMENTS_KEY = "mock_enrollments";
const LS_PROGRESS_KEY = "mock_progress";

function loadJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function getEnrollments() {
  return loadJson(LS_ENROLLMENTS_KEY, []);
}

function setEnrollments(next) {
  saveJson(LS_ENROLLMENTS_KEY, next);
}

function getProgress() {
  return loadJson(LS_PROGRESS_KEY, {}); // { [courseId]: { completedLessonIds: [], lastLessonId: number|null } }
}

function setProgress(next) {
  saveJson(LS_PROGRESS_KEY, next);
}

export const mockApi = {
  async login({ email, password }) {
    await sleep();

    // demo passwords
    const okPassword = password === "Password123!";

    if (!okPassword) {
      throw new Error("Invalid credentials (mock)");
    }

    const isInstructor = email === "instructor@example.com";
    const isStudent = email === "student@example.com";

    if (!isInstructor && !isStudent) {
      throw new Error("Use student@example.com or instructor@example.com (mock)");
    }

    const user = isInstructor ? mockUsers.instructor : mockUsers.student;

    // Simple mock token
    const token = `mock-token-${user.id}-${Date.now()}`;

    return { access_token: token, token_type: "bearer" };
  },

  async me({ token }) {
    await sleep();
    if (!token?.startsWith("mock-token-")) throw new Error("Not authenticated (mock)");
    const isInstructor = token.includes("mock-token-1-");
    return isInstructor ? mockUsers.instructor : mockUsers.student;
  },

  async listCourses({ search = "", category = "" }) {
    await sleep();
    const s = search.trim().toLowerCase();
    return mockCourses.filter((c) => {
      const matchesSearch =
        !s ||
        c.title.toLowerCase().includes(s) ||
        c.description.toLowerCase().includes(s);
      const matchesCategory = !category || c.category === category;
      return matchesSearch && matchesCategory;
    });
  },

  async getCourse(courseId) {
    await sleep();
    const id = Number(courseId);
    const course = mockCourses.find((c) => c.id === id);
    if (!course) throw new Error("Course not found (mock)");
    return course;
  },

  async listLessons(courseId) {
    await sleep();
    const id = Number(courseId);
    return (mockLessonsByCourseId[id] || []).slice().sort((a, b) => a.order_sequence - b.order_sequence);
  },

  async enroll({ userId, courseId }) {
    await sleep();
    const enrollments = getEnrollments();
    const exists = enrollments.find((e) => e.user_id === userId && e.course_id === courseId);
    if (exists) return exists;

    const enrollment = {
      id: Date.now(),
      user_id: userId,
      course_id: courseId,
      enrollment_date: new Date().toISOString(),
      current_status: "active",
      completed_lesson_ids_json: "[]",
      last_lesson_id: null,
    };

    const next = [...enrollments, enrollment];
    setEnrollments(next);

    // initialize progress
    const prog = getProgress();
    if (!prog[courseId]) {
      prog[courseId] = { completedLessonIds: [], lastLessonId: null };
      setProgress(prog);
    }

    return enrollment;
  },

  async myEnrollments({ userId }) {
    await sleep();
    return getEnrollments().filter((e) => e.user_id === userId);
  },

  async updateProgress({ userId, enrollmentId, courseId, lessonId, completed }) {
    await sleep();

    // update progress store
    const prog = getProgress();
    const p = prog[courseId] || { completedLessonIds: [], lastLessonId: null };

    const set = new Set(p.completedLessonIds);
    if (completed) set.add(lessonId);
    else set.delete(lessonId);

    p.completedLessonIds = Array.from(set);
    p.lastLessonId = lessonId;
    prog[courseId] = p;
    setProgress(prog);

    // update enrollment record too (for dashboard)
    const enrollments = getEnrollments();
    const idx = enrollments.findIndex((e) => e.id === enrollmentId && e.user_id === userId);
    if (idx >= 0) {
      enrollments[idx] = {
        ...enrollments[idx],
        last_lesson_id: lessonId,
        completed_lesson_ids_json: JSON.stringify(p.completedLessonIds),
      };
      setEnrollments(enrollments);
      return enrollments[idx];
    }

    throw new Error("Enrollment not found (mock)");
  },

  async dashboard({ userId }) {
    await sleep();

    const enrollments = getEnrollments().filter((e) => e.user_id === userId);
    const prog = getProgress();

    const items = await Promise.all(
      enrollments.map(async (e) => {
        const course = mockCourses.find((c) => c.id === e.course_id);
        const lessons = (mockLessonsByCourseId[e.course_id] || []);
        const completedLessonIds = prog[e.course_id]?.completedLessonIds || [];
        const percent = lessons.length
          ? Math.round((completedLessonIds.length / lessons.length) * 100)
          : 0;

        return {
          enrollment: e,
          course,
          progress_percent: percent,
          last_lesson_id: prog[e.course_id]?.lastLessonId || null,
        };
      })
    );

    return {
      active: items.filter((i) => i.enrollment.current_status === "active"),
      completed: items.filter((i) => i.enrollment.current_status === "completed"),
    };
  },
};
