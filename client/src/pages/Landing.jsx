import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <h1 className="text-6xl font-bold text-gray-900">
            LearnFlow
          </h1>
          <p className="text-2xl text-gray-600">
            Your gateway to knowledge
          </p>
          
          <div className="flex gap-4 justify-center pt-8">
            <Link
              to="/register"
              className="bg-black text-white px-8 py-3 rounded-lg text-lg hover:bg-gray-800 transition"
            >
              Get Started
            </Link>
            <Link
              to="/catalog"
              className="border-2 border-black text-black px-8 py-3 rounded-lg text-lg hover:bg-gray-50 transition"
            >
              Browse Courses
            </Link>
          </div>

          <div className="pt-16 grid grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-black">8+</div>
              <div className="text-gray-600 mt-2">Courses</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-black">36+</div>
              <div className="text-gray-600 mt-2">Lessons</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-black">3+</div>
              <div className="text-gray-600 mt-2">Instructors</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}