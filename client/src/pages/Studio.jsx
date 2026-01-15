import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function Studio() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCourses() {
      try {
        const res = await api.get("/courses/");
        // TODO: Backend should filter by instructor_id from auth token
        // For now, showing all courses but in production this would be filtered
        setCourses(res.data);
      } catch (err) {
        console.error("Failed to fetch courses:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchCourses();
  }, []);

  const handleDelete = async (courseId) => {
    if (!confirm("Are you sure you want to delete this course?")) return;

    try {
      await api.delete(`/courses/${courseId}`);
      setCourses(courses.filter(c => c.id !== courseId));
    } catch (err) {
      alert("Failed to delete course");
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold">My Courses</h1>
          <p className="text-gray-600">Manage your courses and content</p>
          <p className="text-xs text-gray-500 mt-1">Note: Currently showing all courses. In production, only your courses will be shown.</p>
        </div>
        <Link
          to="/studio/courses/new"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Create New Course
        </Link>
      </div>

      {courses.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-600 mb-4">You haven't created any courses yet</p>
          <Link
            to="/studio/courses/new"
            className="text-blue-600 hover:underline"
          >
            Create your first course
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {courses.map((course) => (
            <div key={course.id} className="bg-white border rounded-lg p-6 hover:shadow-md transition">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">{course.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{course.description}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>{course.category}</span>
                    <span>•</span>
                    <span>${course.price}</span>
                    <span>•</span>
                    <span>{course.lessons_count || 0} lessons</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Link
                    to={`/studio/courses/${course.id}/edit`}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(course.id)}
                    className="text-red-600 hover:underline text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
