import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/client";
import { useAuthStore } from "../store/authStore";

export default function CoursePlayer() {
  const { courseId } = useParams();
  const [lessons, setLessons] = useState([]);
  const [currentLesson, setCurrentLesson] = useState(null);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuthStore();

  // Initialize completed lessons from localStorage
  useEffect(() => {
    const stored = localStorage.getItem(`course-progress-${courseId}`);
    if (stored) {
      try {
        setCompletedLessons(JSON.parse(stored));
      } catch (e) {
        console.error("Failed to parse stored progress", e);
      }
    }
  }, [courseId]);

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const res = await api.get(`/courses/${courseId}/lessons`);
        setLessons(res.data || []);
        if (res.data && res.data.length > 0) {
          setCurrentLesson(res.data[0]);
        }
      } catch (error) {
        console.error("Failed to fetch lessons", error);
        setLessons([]);
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, [courseId]);

  const handleLessonClick = (lesson) => {
    setCurrentLesson(lesson);
  };

  const handleMarkComplete = async () => {
    if (!currentLesson) return;

    // Simple dummy progress - just mark as complete
    const updated = completedLessons.includes(currentLesson.id)
      ? completedLessons.filter(id => id !== currentLesson.id)
      : [...completedLessons, currentLesson.id];

    setCompletedLessons(updated);
    // Persist to localStorage
    localStorage.setItem(`course-progress-${courseId}`, JSON.stringify(updated));
  };

  const groupedLessons = lessons.reduce((acc, lesson) => {
    const section = lesson.section_title || "General";
    if (!acc[section]) acc[section] = [];
    acc[section].push(lesson);
    return acc;
  }, {});

  const progress = lessons.length > 0 ? Math.round((completedLessons.length / lessons.length) * 100) : 0;

  if (loading) {
    return <div className="text-center py-8">Loading course...</div>;
  }

  if (!user) {
    return (
      <div className="text-center py-16">
        <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
        <p className="text-gray-600 mb-8">Please log in to access course content.</p>
        <Link to="/login" className="bg-blue-600 text-white px-6 py-3 rounded-lg">
          Login
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Progress Bar */}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-semibold">Course Progress</h2>
          <span className="text-lg font-bold text-blue-600">{progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-blue-600 h-3 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <p className="text-sm text-gray-600 mt-2">{completedLessons.length} of {lessons.length} lessons completed</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar */}
        <div className="lg:w-80 bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-6">Course Content</h2>
          <div className="space-y-4">
            {Object.entries(groupedLessons).map(([section, sectionLessons]) => (
              <div key={section}>
                <h3 className="font-medium text-gray-900 mb-2">{section}</h3>
                <div className="space-y-2">
                  {sectionLessons.map((lesson) => (
                    <button
                      key={lesson.id}
                      onClick={() => handleLessonClick(lesson)}
                      className={`w-full text-left p-3 rounded flex items-center gap-3 transition-colors ${
                        currentLesson?.id === lesson.id
                          ? "bg-blue-50 border border-blue-200"
                          : "hover:bg-gray-50"
                      }`}
                    >
                      <div className={`w-5 h-5 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold ${
                        completedLessons.includes(lesson.id)
                          ? "bg-green-500 text-white"
                          : "bg-gray-300 text-gray-600"
                      }`}>
                        {completedLessons.includes(lesson.id) ? "✓" : "•"}
                      </div>
                      <span className="text-sm font-medium flex-1">{lesson.lesson_title}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {currentLesson ? (
            <div className="bg-white p-8 rounded-lg shadow-sm">
              <h1 className="text-3xl font-bold mb-6">{currentLesson.lesson_title}</h1>

              {/* Video Placeholder */}
              <div className="mb-8">
                <div className="aspect-video bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
                  <div className="text-white text-center">
                    <div className="text-5xl mb-2">▶</div>
                    <p className="text-lg font-semibold">Video Content</p>
                    <p className="text-sm opacity-75">Click "Mark Complete" to continue</p>
                  </div>
                </div>
              </div>

              {/* Lesson Content */}
              <div className="prose max-w-none mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Lesson Content</h2>
                <p className="text-gray-700 leading-relaxed">{currentLesson.content_body}</p>
              </div>

              {/* Mark Complete Button */}
              <button
                onClick={handleMarkComplete}
                className={`w-full py-3 px-6 rounded-lg font-semibold text-lg transition-colors ${
                  completedLessons.includes(currentLesson.id)
                    ? "bg-green-600 text-white hover:bg-green-700"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {completedLessons.includes(currentLesson.id) ? "✓ Completed" : "Mark Complete"}
              </button>
            </div>
          ) : (
            <div className="bg-white p-8 rounded-lg shadow-sm text-center">
              <p className="text-gray-600 text-lg">Select a lesson to begin</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
