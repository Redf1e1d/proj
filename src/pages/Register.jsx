import { useState } from "react";
import API from "../api/api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    await API.post("/register", {
      username,
      password,
    });

    alert("User created!");
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button>Register</button>
    </form>
  );
}