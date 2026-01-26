import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import api from "../api/client";

export default function Landing() {
  const [courses, setCourses] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("/courses");
        setCourses(res.data.slice(0, 3)); // Show first 3 courses
        const uniqueCategories = [...new Set(res.data.map(c => c.category))];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error("Failed to fetch courses", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Learn Anything, Anytime
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Discover courses from expert instructors. Track your progress and achieve your goals with LearnFlow.
        </p>
        <div className="flex justify-center gap-4">
          <Link
            to="/catalog"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Browse Courses
          </Link>
          <Link
            to="/register"
            className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition"
          >
            Get Started
          </Link>
        </div>
      </section>

      {/* Categories */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">Popular Categories</h2>
        <div className="flex flex-wrap justify-center gap-4">
          {categories.map((category) => (
            <Link
              key={category}
              to={`/catalog?category=${category}`}
              className="bg-white border border-gray-200 px-6 py-3 rounded-full font-medium hover:shadow-md transition"
            >
              {category}
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Courses */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">Featured Courses</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {courses.map((course) => (
            <div key={course.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">Course Image</span>
              </div>
              <div className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded">
                    {course.category}
                  </span>
                  <span className="text-lg font-bold text-gray-900">${course.price}</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">{course.title}</h3>
                <p className="text-gray-600 mb-4 line-clamp-2">{course.description}</p>
                <Link
                  to={`/courses/${course.id}`}
                  className="text-blue-600 font-medium hover:text-blue-800"
                >
                  View Details →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
