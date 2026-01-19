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

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const res = await api.get(`/courses/${courseId}/lessons`);
        setLessons(res.data);
        if (res.data.length > 0) {
          setCurrentLesson(res.data[0]);
        }
      } catch (error) {
        console.error("Failed to fetch lessons", error);
      } finally {
        setLoading(false);
      }
    };

    const fetchProgress = async () => {
      try {
        const res = await api.get("/enrollments/me");
        const enrollment = res.data.find(e => e.course_id === parseInt(courseId));
        if (enrollment) {
          setCompletedLessons(JSON.parse(enrollment.completed_lesson_ids_json || "[]"));
        }
      } catch (error) {
        console.error("Failed to fetch progress", error);
      }
    };

    if (user) {
      fetchLessons();
      fetchProgress();
    }
  }, [courseId, user]);

  const handleLessonClick = (lesson) => {
    setCurrentLesson(lesson);
  };

  const handleMarkComplete = async () => {
    if (!currentLesson) return;

    try {
      await api.patch(`/enrollments/me/progress`, {
        lesson_id: currentLesson.id,
        completed: !completedLessons.includes(currentLesson.id)
      });

      setCompletedLessons(prev =>
        prev.includes(currentLesson.id)
          ? prev.filter(id => id !== currentLesson.id)
          : [...prev, currentLesson.id]
      );
    } catch (error) {
      console.error("Failed to update progress", error);
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
    <div className="flex flex-col lg:flex-row gap-8">
      {/* Sidebar */}
      <div className="lg:w-80 bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Course Content</h2>
        <div className="space-y-4">
          {Object.entries(groupedLessons).map(([section, sectionLessons]) => (
            <div key={section}>
              <h3 className="font-medium text-gray-900 mb-2">{section}</h3>
              <div className="space-y-1">
                {sectionLessons.map((lesson) => (
                  <button
                    key={lesson.id}
                    onClick={() => handleLessonClick(lesson)}
                    className={`w-full text-left p-3 rounded flex items-center gap-3 ${
                      currentLesson?.id === lesson.id
                        ? "bg-blue-50 border border-blue-200"
                        : "hover:bg-gray-50"
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      completedLessons.includes(lesson.id)
                        ? "bg-green-500 border-green-500"
                        : "border-gray-300"
                    }`}>
                      {completedLessons.includes(lesson.id) && (
                        <div className="w-full h-full flex items-center justify-center">
                          <span className="text-white text-xs">✓</span>
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">{lesson.lesson_title}</p>
                      {lesson.duration_minutes && (
                        <p className="text-xs text-gray-500">{lesson.duration_minutes} min</p>
                      )}
                    </div>
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
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h1 className="text-2xl font-bold mb-4">{currentLesson.lesson_title}</h1>

            {currentLesson.video_link && (
              <div className="mb-6">
                <div className="aspect-video bg-gray-200 rounded-lg flex items-center justify-center">
                  <iframe
                    src={currentLesson.video_link}
                    className="w-full h-full rounded-lg"
                    allowFullScreen
                  ></iframe>
                </div>
              </div>
            )}

            <div className="prose max-w-none mb-6">
              <p className="text-gray-700">{currentLesson.content_body}</p>
            </div>

            <div className="flex items-center justify-between">
              <button
                onClick={handleMarkComplete}
                className={`px-6 py-2 rounded-lg font-medium ${
                  completedLessons.includes(currentLesson.id)
                    ? "bg-green-600 text-white hover:bg-green-700"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {completedLessons.includes(currentLesson.id) ? "Mark Incomplete" : "Mark Complete"}
              </button>

              <div className="text-sm text-gray-500">
                {currentLesson.duration_minutes && `${currentLesson.duration_minutes} minutes`}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white p-6 rounded-lg shadow-sm text-center">
            <p className="text-gray-600">Select a lesson to begin</p>
          </div>
        )}
      </div>
    </div>
  );
}
