import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function Catalog() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function fetchCourses() {
      try {
        console.log('Fetching courses from:', '/courses');
        const res = await api.get("/courses/");
        console.log('Courses response:', res.data);
        
        // Ensure we have an array
        if (Array.isArray(res.data)) {
          setCourses(res.data);
        } else {
          console.error('Expected array but got:', typeof res.data, res.data);
          setCourses([]);
        }
      } catch (err) {
        console.error("Failed to fetch courses:", err);
        console.error("Error response:", err.response?.data);
        setCourses([]);
      } finally {
        setLoading(false);
      }
    }
    fetchCourses();
  }, []);

  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(search.toLowerCase()) ||
    course.description.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div>Loading courses...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Course Catalog</h1>
        <p className="text-gray-600">Discover new skills and advance your career</p>
      </div>

      <div className="max-w-md">
        <input
          type="text"
          placeholder="Search courses..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full border rounded-lg px-4 py-2"
        />
      </div>

      {filteredCourses.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No courses found</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <div key={course.id} className="bg-white border rounded-lg p-6 hover:shadow-md transition">
              <h3 className="text-lg font-semibold mb-2">{course.title}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                {course.description}
              </p>
              
              <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
                <span>{course.lessons_count || 0} lessons</span>
                <span>By {course.instructor?.full_name || 'Unknown'}</span>
              </div>
              
              <Link
                to={`/courses/${course.id}`}
                className="block w-full text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
              >
                View Course
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}