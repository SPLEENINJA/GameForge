// src/pages/Login.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/login/", { username, password });
      login(res.data);
      navigate("/dashboard"); 
    } catch {
      alert("Login failed. Check credentials.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <form
        onSubmit={submit}
        className="bg-gray-800 p-8 rounded-2xl shadow-lg w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-6 text-blue-400">Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 mb-4 rounded-lg bg-gray-700 text-white"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 mb-4 rounded-lg bg-gray-700 text-white"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold"
        >
          Login
        </button>
        <p className="mt-4">
          No account? <Link to="/register" className="text-blue-400">Register here</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;


// import React, { useState, useContext } from "react";
// import { AuthContext } from "../AuthContext";
// import { useNavigate, Link } from "react-router-dom";

// const Login = () => {
//   const { handleLogin } = useContext(AuthContext);
//   const navigate = useNavigate();
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const submit = async (e) => {
//     e.preventDefault();
//     const success = await handleLogin(username, password);
//     if (success) navigate("/dashboard");
//   };

//   return (
//     <div className="auth-page">
//       <div className="auth-box">
//         <h2>🎮 GameForge Login</h2>
//         <form onSubmit={submit}>
//           <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} className="input-field" />
//           <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="input-field" />
//           <button type="submit" className="btn">Login</button>
//         </form>
//         <p>No account? <Link to="/register" className="link">Register here</Link></p>
//       </div>
//     </div>
//   );
// };

// export default Login;



// import React, { useState, useContext } from "react";
// import { AuthContext } from "../AuthContext";
// import { useNavigate } from "react-router-dom";

// export default function Login() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const { login } = useContext(AuthContext);
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     await login(username, password);
//     navigate("/dashboard");
//   };

//   return (
//     <div className="auth-form">
//       <h2>Login</h2>
//       <form onSubmit={handleSubmit}>
//         <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
//         <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
//         <button type="submit">Login</button>
//       </form>
//     </div>
//   );
// }
