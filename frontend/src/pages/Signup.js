// src/pages/Signup.js


import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import { useNavigate, Link } from "react-router-dom";

const Signup = () => {
  const { handleRegister } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    const success = await handleRegister(username, email, password);
    if (success) {
      alert("Account created successfully!");
      navigate("/login");
    } else {
      alert("Signup failed. Check input.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-box">
        <h2>Register</h2>
        <form onSubmit={submit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input-field"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-field"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            required
          />
          <button type="submit" className="btn">
            Sign Up
          </button>
        </form>
        <p>
          Already have an account?{" "}
          <Link to="/login" className="link">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;



// import React, { useState } from "react";
// import { useNavigate, Link } from "react-router-dom";
// import api from "../api/axios";
// import "./Signup.css"; // 👈 We'll add a small CSS file below

// const Signup = () => {
//   const [email, setEmail] = useState("");
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       await api.post("register/", { username, email, password });
//       alert("🎉 Account created successfully!");
//       navigate("/login");
//     } catch (err) {
//       alert("Signup failed. Please check your input.");
//     }
//   };

//   return (
//     <div className="auth-page">
//       <div className="auth-box">
//         <h2>🧠 Create Your Account</h2>
//         <form onSubmit={handleSubmit}>
//           <input
//             type="text"
//             placeholder="Username"
//             onChange={(e) => setUsername(e.target.value)}
//             required
//             className="input-field"
//           />
//           <input
//             type="email"
//             placeholder="Email"
//             onChange={(e) => setEmail(e.target.value)}
//             required
//             className="input-field"
//           />
//           <input
//             type="password"
//             placeholder="Password"
//             onChange={(e) => setPassword(e.target.value)}
//             required
//             className="input-field"
//           />
//           <button type="submit" className="btn">Sign Up</button>
//         </form>
//         <p>
//           Already have an account? <Link to="/login" className="link">Login here</Link>
//         </p>
//       </div>
//     </div>
//   );
// };

// export default Signup;
