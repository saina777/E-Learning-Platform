import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/client";

export default function EditCourse() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [course, setCourse] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    price: 0
  });

  useEffect(() => {
    async function fetchCourse() {
      try {
        const res = await api.get(`/courses/${courseId}`);
        setCourse(res.data);
        setFormData({
          title: res.data.title,
          description: res.data.description,
          category: res.data.category,
          price: res.data.price
        });
      } catch (err) {
        setError("Failed to load course");
      } finally {
        setLoading(false);
      }
    }
    fetchCourse();
  }, [courseId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'price' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);

    try {
      await api.patch(`/courses/${courseId}`, formData);
      navigate("/studio");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update course");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error && !course) return <div className="text-red-600">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Edit Course</h1>
        <button
          onClick={() => navigate("/studio")}
          className="text-gray-600 hover:text-gray-800"
        >
          Back to Studio
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow">
        <div>
          <label className="block text-sm font-medium mb-1">Course Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows={4}
            className="w-full border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Category</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          >
            <option>Programming</option>
            <option>Web Development</option>
            <option>Data Science</option>
            <option>Mobile Development</option>
            <option>Database</option>
            <option>Cloud</option>
            <option>Security</option>
            <option>Other</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Price ($)</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            min="0"
            step="0.01"
            className="w-full border rounded px-3 py-2"
          />
        </div>

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/studio")}
            className="border px-6 py-2 rounded hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
      </form>

      <div className="bg-gray-50 p-6 rounded-lg">
        <h2 className="text-lg font-semibold mb-2">Course Lessons</h2>
        <p className="text-gray-600 text-sm mb-4">
          Lesson management coming soon. You can add and edit lessons for this course.
        </p>
        <div className="text-sm text-gray-500">
          Current lessons: {course?.lessons?.length || 0}
        </div>
      </div>
    </div>
  );
}
