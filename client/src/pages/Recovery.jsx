import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function Recovery() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.post("/auth/recovery", { email });
      setSuccess(true);
    } catch (err) {
      setError(err?.response?.data?.detail || "Recovery request failed");
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="max-w-md space-y-4">
        <h1 className="text-2xl font-semibold">Check your email</h1>
        <p className="text-gray-600">
          We've sent a password reset link to {email}
        </p>
        <Link to="/login" className="text-blue-600 hover:underline">
          Back to login
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-md space-y-4">
      <h1 className="text-2xl font-semibold">Reset password</h1>
      <p className="text-gray-600">
        Enter your email address and we'll send you a link to reset your password.
      </p>

      {error && <div className="p-3 rounded border text-sm text-red-600">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          required
        />
        <button
          disabled={loading}
          className="w-full px-4 py-2 rounded bg-black text-white disabled:opacity-50"
        >
          {loading ? "Sending..." : "Send reset link"}
        </button>
      </form>

      <Link to="/login" className="text-sm text-blue-600 hover:underline">
        Back to login
      </Link>
    </div>
  );
}