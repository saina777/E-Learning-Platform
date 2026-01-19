import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import { useAuthStore } from "../store/authStore";

export default function CourseDetails() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const { user } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const [courseRes, lessonsRes] = await Promise.all([
          api.get(`/courses/${courseId}`),
          user ? api.get(`/courses/${courseId}/lessons`) : Promise.resolve({ data: [] })
        ]);
        setCourse(courseRes.data);
        setLessons(lessonsRes.data);
      } catch (error) {
        console.error("Failed to fetch course", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCourse();
  }, [courseId, user]);

  const handleEnroll = async () => {
    if (!user) {
      navigate("/login");
      return;
    }
    setEnrolling(true);
    try {
      await api.post("/enrollments", { course_id: parseInt(courseId) });
      navigate(`/learn/${courseId}`);
    } catch (error) {
      console.error("Failed to enroll", error);
      alert("Failed to enroll in course");
    } finally {
      setEnrolling(false);
    }
  };

  const groupedLessons = lessons.reduce((acc, lesson) => {
    const section = lesson.section_title || "General";
    if (!acc[section]) acc[section] = [];
    acc[section].push(lesson);
    return acc;
  }, {});

  if (loading) {
    return <div className="text-center py-8">Loading course...</div>;
  }

  if (!course) {
    return <div className="text-center py-8">Course not found</div>;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Course Header */}
      <div className="bg-white rounded-lg shadow-sm p-8">
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-sm font-medium text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
                {course.category}
              </span>
              <span className="text-2xl font-bold text-gray-900">${course.price}</span>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">{course.title}</h1>
            <p className="text-xl text-gray-600 mb-6">{course.description}</p>
          </div>
          <div className="lg:w-80">
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Course Syllabus</h3>
              <div className="space-y-2">
                {Object.entries(groupedLessons).map(([section, sectionLessons]) => (
                  <div key={section}>
                    <h4 className="font-medium text-gray-900">{section}</h4>
                    <ul className="ml-4 mt-1 space-y-1">
                      {sectionLessons.map((lesson) => (
                        <li key={lesson.id} className="text-sm text-gray-600">
                          {lesson.lesson_title}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
              <button
                onClick={handleEnroll}
                disabled={enrolling}
                className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
              >
                {enrolling ? "Enrolling..." : "Enroll Now"}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Lessons Preview (if not enrolled) */}
      {!user && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold mb-6">Course Content Preview</h2>
          <div className="space-y-4">
            {Object.entries(groupedLessons).slice(0, 2).map(([section, sectionLessons]) => (
              <div key={section}>
                <h3 className="text-lg font-semibold mb-2">{section}</h3>
                <div className="space-y-2">
                  {sectionLessons.slice(0, 3).map((lesson) => (
                    <div key={lesson.id} className="flex items-center justify-between p-4 bg-gray-50 rounded">
                      <span className="font-medium">{lesson.lesson_title}</span>
                      <span className="text-sm text-gray-500">{lesson.duration_minutes} min</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 text-center">
            <Link
              to="/login"
              className="text-blue-600 font-medium hover:text-blue-800"
            >
              Login to access full course content
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
