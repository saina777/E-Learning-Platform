import { useAuthStore } from "../store/authStore";
import { useEffect, useState } from "react";
import api from "../api/client";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const user = useAuthStore((s) => s.user);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleUnenroll = async (courseId) => {
    if (!confirm("Are you sure you want to unenroll from this course?")) return;

    try {
      await api.delete(`/courses/${courseId}/unenroll`);
      setCourses(courses.filter(c => c.id !== courseId));
    } catch (err) {
      alert("Failed to unenroll from course");
    }
  };

  useEffect(() => {
    async function fetchData() {
      try {
        if (user?.role === 'instructor') {
          // Fetch courses created by instructor
          const res = await api.get("/courses/");
          // TODO: Filter by instructor_id when auth is implemented
          setCourses(res.data);
        } else {
          // Fetch enrolled courses for students
          const res = await api.get("/courses/enrolled");
          setCourses(res.data);
        }
      } catch (err) {
        console.error("Failed to fetch courses:", err);
      } finally {
        setLoading(false);
      }
    }
    if (user) {
      fetchData();
    }
  }, [user]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Welcome back, {user?.full_name}!</h1>
        <p className="text-gray-600">
          {user?.role === 'instructor' ? 'Manage your courses and students' : 'Continue your learning journey'}
        </p>
      </div>

      {user?.role === 'instructor' ? (
        // Instructor Dashboard
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Instructor Dashboard</h2>
            <p className="text-gray-700 mb-2">Create and manage your courses, add lessons, and track student enrollments.</p>
            <p className="text-xs text-gray-600 mb-4">Note: Currently showing all courses. In production, only your courses will be shown.</p>
            <div className="flex gap-3">
              <Link
                to="/studio/courses/new"
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
              >
                Create New Course
              </Link>
              <Link
                to="/studio"
                className="border border-blue-600 text-blue-600 px-6 py-2 rounded hover:bg-blue-50"
              >
                Manage Courses
              </Link>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-medium mb-4">Your Courses</h2>
            {courses.length === 0 ? (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <p className="text-gray-600 mb-4">You haven't created any courses yet</p>
                <Link to="/studio/courses/new" className="text-blue-600 hover:underline">
                  Create your first course
                </Link>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {courses.map((course) => (
                  <div key={course.id} className="border rounded-lg p-4 hover:shadow-md">
                    <h3 className="font-medium">{course.title}</h3>
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">{course.description}</p>
                    <div className="mt-3 flex justify-between items-center">
                      <span className="text-xs text-gray-500">
                        {course.lessons_count || 0} lessons
                      </span>
                      <Link
                        to={`/studio/courses/${course.id}/edit`}
                        className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                      >
                        Edit
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        // Student Dashboard
        <div className="grid gap-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-medium">My Enrolled Courses</h2>
            <Link to="/catalog" className="text-blue-600 hover:underline">
              Browse catalog
            </Link>
          </div>

          {courses.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No courses enrolled yet</p>
              <Link to="/catalog" className="text-blue-600 hover:underline">
                Explore courses
              </Link>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {courses.map((course) => (
                <div key={course.id} className="border rounded-lg p-4 hover:shadow-md">
                  <h3 className="font-medium">{course.title}</h3>
                  <p className="text-sm text-gray-600 mt-1 line-clamp-2">{course.description}</p>
                  <div className="mt-3 flex justify-between items-center">
                    <span className="text-xs text-gray-500">
                      {course.lessons_count} lessons
                    </span>
                    <div className="flex gap-2">
                      <Link
                        to={`/learn/${course.id}`}
                        className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                      >
                        Continue
                      </Link>
                      <button
                        onClick={() => handleUnenroll(course.id)}
                        className="text-sm text-red-600 hover:text-red-700 px-2"
                        title="Unenroll from course"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
