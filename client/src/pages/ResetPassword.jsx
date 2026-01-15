import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from "../api/client";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }
  }, [token, navigate]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }
    
    setError("");
    setLoading(true);
    try {
      await api.post("/auth/reset", { token, password });
      navigate("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Password reset failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md space-y-4">
      <h1 className="text-2xl font-semibold">Set new password</h1>

      {error && <div className="p-3 rounded border text-sm text-red-600">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="New password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          required
        />
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Confirm password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          type="password"
          required
        />
        <button
          disabled={loading}
          className="w-full px-4 py-2 rounded bg-black text-white disabled:opacity-50"
        >
          {loading ? "Updating..." : "Update password"}
        </button>
      </form>
    </div>
  );
}