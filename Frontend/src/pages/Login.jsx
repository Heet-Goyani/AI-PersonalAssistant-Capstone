import React, { useState } from "react";
import "../App.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:5001/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");
      localStorage.setItem("token", data.access_token);
      // Optionally redirect or show success
      window.location.href = "/";
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container" style={{ minHeight: "100vh", width: "100vw", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #1a0036 0%, #0a0a23 60%, #0a0023 100%)", position: "fixed", top: 0, left: 0 }}>
      <div className="auth-box" style={{ background: "#18182f", padding: 32, borderRadius: 16, boxShadow: "0 4px 32px rgba(0,0,0,0.18)", width: 350, maxWidth: "90%" }}>
        <h2 style={{ color: "#fff", marginBottom: 24, textAlign: "center" }}>Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{ width: "100%", padding: 12, marginBottom: 16, borderRadius: 8, border: "none", background: "#23234a", color: "#fff" }}
            autoComplete="username"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ width: "100%", padding: 12, marginBottom: 24, borderRadius: 8, border: "none", background: "#23234a", color: "#fff" }}
            autoComplete="current-password"
            required
          />
          <button
            type="submit"
            style={{ width: "100%", padding: 12, borderRadius: 8, background: "#7c3aed", color: "#fff", fontWeight: 600, border: "none", fontSize: 16, cursor: loading ? "not-allowed" : "pointer", marginBottom: 12, opacity: loading ? 0.7 : 1 }}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
          {error && <div style={{ color: "#ff6b6b", marginBottom: 12, textAlign: "center" }}>{error}</div>}
        </form>
        <p style={{ color: "#bdbdbd", marginTop: 16, textAlign: "center" }}>
          Don't have an account? <a href="/signup" style={{ color: "#7c3aed", textDecoration: "underline" }}>Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
