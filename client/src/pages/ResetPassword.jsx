import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { requestPasswordReset, resetPassword } from "../api/authApi";

export default function ResetPassword() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (password !== confirm) return setError("Passwords do not match");
    try {
      const res = await authApi.resetPassword(token, password);
      setSuccess(res.message);
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError(err?.response?.data?.detail || "Reset failed");
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8 space-y-4">
      <h1 className="text-2xl font-semibold">Reset Password</h1>
      {error && <div className="p-3 rounded border bg-red-50 text-red-700">{error}</div>}
      {success && <div className="p-3 rounded border bg-green-50 text-green-700">{success}</div>}
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="New password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          minLength="6"
          required
        />
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Confirm password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          type="password"
          minLength="6"
          required
        />
        <button className="w-full px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
          Reset password
        </button>
      </form>
    </div>
  );
}
