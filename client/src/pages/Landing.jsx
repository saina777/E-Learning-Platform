import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">LearnFlow</h1>
      <p className="text-gray-600">
        A clean, focused e-learning platform with progress tracking and private lessons.
      </p>
      <div className="flex gap-3">
        <Link className="px-4 py-2 rounded bg-black text-white" to="/catalog">Browse Courses</Link>
        <Link className="px-4 py-2 rounded border" to="/login">Login</Link>
      </div>
    </div>
  );
}
