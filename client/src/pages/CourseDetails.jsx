import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/client";
import { useAuthStore } from "../store/authStore";

export default function CourseDetails() {
  const { courseId } = useParams();
  const user = useAuthStore((s) => s.user);
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [enrolled, setEnrolled] = useState(false);

  useEffect(() => {
    async function fetchCourse() {
      try {
        const res = await api.get(`/courses/${courseId}`);
        setCourse(res.data);
        setEnrolled(res.data.is_enrolled);
      } catch (err) {
        console.error("Failed to fetch course:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchCourse();
  }, [courseId]);

  async function handleEnroll() {
    setEnrolling(true);
    try {
      await api.post(`/courses/${courseId}/enroll`);
      setEnrolled(true);
    } catch (err) {
      console.error("Enrollment failed:", err);
    } finally {
      setEnrolling(false);
    }
  }

  if (loading) return <div>Loading course...</div>;
  if (!course) return <div>Course not found</div>;

  return (
    <div className="max-w-4xl space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h1 className="text-3xl font-bold mb-4">{course.title}</h1>
        <p className="text-gray-600 mb-6">{course.description}</p>
        
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>{course.lessons?.length || 0} lessons</span>
            <span>•</span>
            <span>By {course.instructor?.full_name}</span>
          </div>
          
          {user?.role !== 'instructor' && (
            enrolled ? (
              <Link
                to={`/learn/${courseId}`}
                className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
              >
                Continue Learning
              </Link>
            ) : (
              <button
                onClick={handleEnroll}
                disabled={enrolling}
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {enrolling ? "Enrolling..." : "Enroll Now"}
              </button>
            )
          )}
        </div>
      </div>

      {course.lessons && course.lessons.length > 0 && (
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Course Content</h2>
          <div className="space-y-2">
            {course.lessons.map((lesson, index) => (
              <div key={lesson.id} className="flex items-center p-3 border rounded">
                <span className="text-sm text-gray-500 w-8">{index + 1}.</span>
                <span className="flex-1">{lesson.title}</span>
                {enrolled && (
                  <span className="text-xs text-gray-400">
                    {lesson.duration || "5 min"}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}