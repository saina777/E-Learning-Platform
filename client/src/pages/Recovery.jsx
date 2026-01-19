import { useState } from "react";
import { requestPasswordReset, resetPassword } from "../api/authApi";
import { Link } from "react-router-dom";

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
      const res = await authApi.requestPasswordReset(email);
      setMessage(res.message);
      if (res.token) setToken(res.token);
    } catch (err) {
      setError(err?.response?.data?.detail || "Request failed");
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8 space-y-4">
      <h1 className="text-2xl font-semibold">Password Recovery</h1>
      {error && <div className="p-3 rounded border bg-red-50 text-red-700">{error}</div>}
      {message && <div className="p-3 rounded border bg-green-50 text-green-700">{message}</div>}
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          required
        />
        <button className="w-full px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
          Send reset token
        </button>
      </form>

      {token && (
        <div className="text-sm p-3 rounded border bg-yellow-50">
          <p className="font-semibold mb-2">MVP Reset Token (click to use):</p>
          <Link 
            to={`/account/reset/${token}`}
            className="text-blue-600 hover:underline break-all"
          >
            Reset Password with this token
          </Link>
        </div>
      )}
      
      <Link to="/login" className="text-blue-600 hover:underline">
        Back to Login
      </Link>
    </div>
  );
}
