import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [courseProgress, setCourseProgress] = useState({});

  // Load progress from localStorage
  useEffect(() => {
    const progress = {};
    if (dashboardData?.enrollments) {
      dashboardData.enrollments.forEach(enrollment => {
        const stored = localStorage.getItem(`course-progress-${enrollment.course_id}`);
        if (stored) {
          try {
            const completedIds = JSON.parse(stored);
            // Calculate progress percentage (we'll get total lessons count from the API)
            progress[enrollment.course_id] = completedIds;
          } catch (e) {
            console.error("Failed to parse stored progress", e);
          }
        }
      });
    }
    setCourseProgress(progress);
  }, [dashboardData]);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get("/dashboard");
        setDashboardData(res.data);
      } catch (error) {
        console.error("Failed to fetch dashboard", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  const handleDeleteCourse = async (enrollmentId) => {
    try {
      await api.delete(`/enrollments/${enrollmentId}`);
      // Refresh dashboard
      const res = await api.get("/dashboard");
      setDashboardData(res.data);
    } catch (error) {
      console.error("Failed to delete enrollment", error);
    }
  };

  const getProgressPercent = (enrollment) => {
    const completedIds = courseProgress[enrollment.course_id] || [];
    if (!enrollment.total_lessons || enrollment.total_lessons === 0) {
      return 0;
    }
    return Math.round((completedIds.length / enrollment.total_lessons) * 100);
  };

  if (loading) {
    return <div className="text-center py-8">Loading dashboard...</div>;
  }

  const { enrollments } = dashboardData || { enrollments: [] };
  const activeEnrollments = enrollments.filter(e => e.current_status === "Active");
  const completedEnrollments = enrollments.filter(e => e.current_status === "Completed");

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Track your learning progress</p>
      </div>

      {/* Continue Learning */}
      {activeEnrollments.length > 0 && (
        <section>
          <h2 className="text-2xl font-semibold mb-6">Continue Learning</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {activeEnrollments.map((enrollment) => (
              <div key={enrollment.enrollment_id} className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-2">{enrollment.course_title}</h3>
                <p className="text-gray-600 mb-4">{enrollment.course_category}</p>
                <div className="mb-4">
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{getProgressPercent(enrollment)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${getProgressPercent(enrollment)}%` }}
                    ></div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Link
                    to={`/learn/${enrollment.course_id}`}
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-center"
                  >
                    Continue Course
                  </Link>
                  <button
                    onClick={() => handleDeleteCourse(enrollment.enrollment_id)}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                    title="Remove course from dashboard"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Completed Courses */}
      {completedEnrollments.length > 0 && (
        <section>
          <h2 className="text-2xl font-semibold mb-6">Completed Courses</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {completedEnrollments.map((enrollment) => (
              <div key={enrollment.enrollment_id} className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-green-500">
                <h3 className="text-xl font-semibold mb-2">{enrollment.course_title}</h3>
                <p className="text-gray-600 mb-4">{enrollment.course_category}</p>
                <div className="flex items-center">
                  <span className="text-green-600 font-medium">✓ Completed</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Empty State */}
      {enrollments.length === 0 && (
        <div className="text-center py-16">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">No courses yet</h2>
          <p className="text-gray-600 mb-8">Start your learning journey by enrolling in a course.</p>
          <Link
            to="/catalog"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
          >
            Browse Courses
          </Link>
        </div>
      )}
    </div>
  );
}
