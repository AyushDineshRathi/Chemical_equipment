import { useState } from "react";
import axios from "axios";
import Card from "./Card";

function Login({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    setError("");
    setMessage("");
    try {
      if (isLogin) {
        // Use the centralized Axios instance
        // Now that backend exposes /api/token/, this should work
        // NOTE: Standard DRF token view expects "username" and "password"
        const api = await import("../services/api");
        const res = await api.default.post("token/", { username, password });
        
        // DRF returns { "token": "..." }
        const token = res.data.token;
        if (token) {
            localStorage.setItem("token", token);
            onLogin(token);
        } else {
            setError("Login failed: No token received");
        }
      } else {
        const api = await import("../services/api");
        await api.register(username, password);
        setMessage("Registration successful! Please login.");
        setIsLogin(true);
        setPassword(""); 
      }
    } catch (err) {
      console.error(err);
      if (err.response && err.response.status === 404) {
        // This likely means the backend hasn't been redeployed with the new /api/token/ endpoint
        setError("Login service unavailable (404). Please redeploy the backend.");
      } else if (isLogin) {
        setError("Invalid credentials");
      } else {
        setError(err.response?.data?.error || "Registration failed");
      }
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "12px",
    marginBottom: "16px",
    borderRadius: "8px",
    border: "1px solid var(--border)",
    fontSize: "14px",
    outline: "none",
    transition: "border-color 0.2s"
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      display: "flex", 
      alignItems: "center", 
      justifyContent: "center", 
      background: "var(--bg)" 
    }}>
      <div style={{ maxWidth: "400px", width: "100%" }}>
        <Card title={isLogin ? "Welcome Back" : "Create Account"}>
          {message && <p style={{ color: "var(--success)", marginBottom: "16px", fontSize: "14px" }}>{message}</p>}
          {error && <p style={{ color: "#ef4444", marginBottom: "16px", fontSize: "14px" }}>{error}</p>}
          
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={inputStyle}
            onFocus={(e) => e.target.style.borderColor = "var(--primary)"}
            onBlur={(e) => e.target.style.borderColor = "var(--border)"}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
            onFocus={(e) => e.target.style.borderColor = "var(--primary)"}
            onBlur={(e) => e.target.style.borderColor = "var(--border)"}
          />
          
          <button 
            onClick={handleSubmit} 
            style={{
              width: "100%",
              padding: "12px",
              background: "var(--primary)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: "600",
              cursor: "pointer",
              marginBottom: "16px",
              transition: "background 0.2s"
            }}
            onMouseEnter={(e) => e.target.style.background = "var(--primary-hover)"}
            onMouseLeave={(e) => e.target.style.background = "var(--primary)"}
          >
            {isLogin ? "Login" : "Sign Up"}
          </button>

          <div style={{ textAlign: "center", fontSize: "14px", color: "var(--text-light)" }}>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span 
              onClick={() => { setIsLogin(!isLogin); setError(""); setMessage(""); }}
              style={{ color: "var(--primary)", fontWeight: "600", cursor: "pointer" }}
            >
              {isLogin ? "Sign Up" : "Login"}
            </span>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default Login;