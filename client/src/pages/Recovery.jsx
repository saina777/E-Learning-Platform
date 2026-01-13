import { useState } from "react";
import api from "../api/client";

export default function Recovery() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [token, setToken] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setMessage("");
    setToken("");
    try {
      const res = await api.post("/auth/request-password-reset", { email });
      setMessage("If the email exists, a reset token has been generated.");
      // MVP: backend may return token to display
      if (res.data?.token) setToken(res.data.token);
    } catch (err) {
      setError(err?.response?.data?.detail || "Request failed");
    }
  }

  return (
    <div className="max-w-md space-y-4">
      <h1 className="text-2xl font-semibold">Password Recovery</h1>
      {error && <div className="p-3 rounded border text-sm">{error}</div>}
      {message && <div className="p-3 rounded border text-sm">{message}</div>}
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          required
        />
        <button className="w-full px-4 py-2 rounded bg-black text-white">
          Send reset token
        </button>
      </form>

      {token && (
        <div className="text-sm p-3 rounded border">
          <p className="font-semibold">MVP Reset Token:</p>
          <code className="break-all">{token}</code>
        </div>
      )}
    </div>
  );
}
