import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";

export default function CoursePlayer() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [currentLesson, setCurrentLesson] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCourse() {
      try {
        const res = await api.get(`/courses/${courseId}`);
        setCourse(res.data);
      } catch (err) {
        console.error("Failed to fetch course:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchCourse();
  }, [courseId]);

  if (loading) return <div>Loading course...</div>;
  if (!course) return <div>Course not found</div>;

  const lessons = course.lessons || [];
  const lesson = lessons[currentLesson];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg p-6 mb-6">
        <h1 className="text-2xl font-bold mb-4">{course.title}</h1>
        <p className="text-gray-600 mb-4">{course.description}</p>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1 bg-white rounded-lg p-4">
          <h2 className="font-semibold mb-4">Lessons</h2>
          <div className="space-y-2">
            {lessons.map((lessonItem, index) => (
              <button
                key={lessonItem.id}
                onClick={() => setCurrentLesson(index)}
                className={`w-full text-left p-3 rounded border transition ${
                  index === currentLesson
                    ? "bg-blue-50 border-blue-200"
                    : "hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 w-8">{index + 1}.</span>
                  <span className="flex-1 text-sm">{lessonItem.lesson_title}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="lg:col-span-3">
          {lesson && (
            <div className="bg-white rounded-lg p-6">
              <h2 className="text-xl font-bold mb-4">{lesson.lesson_title}</h2>
              <div className="prose max-w-none">
                <p className="text-gray-700 whitespace-pre-wrap">{lesson.content_body}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}