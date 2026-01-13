import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/client";

export default function ResetPassword() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (password !== confirm) return setError("Passwords do not match");
    try {
      await api.post("/auth/reset-password", { token, new_password: password });
      navigate("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Reset failed");
    }
  }

  return (
    <div className="max-w-md space-y-4">
      <h1 className="text-2xl font-semibold">Reset Password</h1>
      {error && <div className="p-3 rounded border text-sm">{error}</div>}
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
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          type="password"
          required
        />
        <button className="w-full px-4 py-2 rounded bg-black text-white">
          Reset password
        </button>
      </form>
    </div>
  );
}
