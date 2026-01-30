import { useState } from "react";
import axios from "axios";
import Card from "./Card";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/token/",
        { username, password }
      );

      localStorage.setItem("token", res.data.token);
      onLogin(res.data.token);
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <Card title="Login">
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <br /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </Card>
  );
}

export default Login;