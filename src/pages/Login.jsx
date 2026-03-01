import { useState } from "react";
import API from "../api/api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await API.post("/login", formData);

    localStorage.setItem("token", res.data.access_token);

    alert("Logged in!");
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button>Login</button>
    </form>
  );
}