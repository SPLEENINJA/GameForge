// src/AuthContext.js

import React, { createContext, useState } from "react";
import api from "./api/axios";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const navigate = useNavigate();

  const login = (data) => {
    if (data?.tokens?.access) {
      localStorage.setItem("access", data.tokens.access);
      localStorage.setItem("refresh", data.tokens.refresh);
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
      console.log("✅ Login success:", data.user);
    } else {
      console.error("⚠️ No access token found in login response:", data);
      alert("Login failed. Invalid response from server.");
    }
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setUser(null);
     // Redirect to login page
     navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};




// import React, { createContext, useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";
// import api from "./api/axios"; 

// export const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const navigate = useNavigate();
//   const [user, setUser] = useState(null);

//   // Load user from localStorage on mount
//   useEffect(() => {
//     const savedUser = localStorage.getItem("user");
//     if (savedUser) setUser(JSON.parse(savedUser));
//   }, []);

//   const login = async (username, password) => {
//     try {
//       const res = await api.post("/token/", { username, password });
//       const token = res.data.access;
//       const userData = { username, token };
//       localStorage.setItem("user", JSON.stringify(userData));
//       setUser(userData);
//       return true;
//     } catch {
//       return false;
//     }
//   };
  
//   const logout = () => {
//     localStorage.removeItem("user");
//     setUser(null);
//   };
//   // Login function
//   // const login = (userData) => {
//   //   setUser(userData);
//   //   localStorage.setItem("user", JSON.stringify(userData));
//   //   navigate("/dashboard");
//   // };

//   // Logout function
//   // const logout = () => {
//   //   setUser(null);
//   //   localStorage.removeItem("user");
//   //   navigate("/login");
//   // };

//   return (
//     <AuthContext.Provider value={{ user, login, logout }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };


// import React, { createContext, useState, useEffect } from "react";
// import axios from "axios";

// export const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null);
//   const [accessToken, setAccessToken] = useState(localStorage.getItem("accessToken") || null);
//   const [refreshToken, setRefreshToken] = useState(localStorage.getItem("refreshToken") || null);

//   // Fetch user info when logged in
//   useEffect(() => {
//     if (accessToken) {
//       axios.get("http://127.0.0.1:8000/api/user/", {
//         headers: { Authorization: `Bearer ${accessToken}` },
//       })
//       .then(res => setUser(res.data))
//       .catch(() => handleLogout());
//     }
//   }, [accessToken]);

//   // ✅ Register
//   const handleRegister = async (username, email, password) => {
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/api/register/", {
//         username, email, password
//       });
//       alert("Registration successful! You can now log in.");
//       return response.data;
//     } catch (err) {
//       console.error(err);
//       alert("Registration failed. Try again.");
//     }
//   };

//   // ✅ Login
//   const handleLogin = async (username, password) => {
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/api/login/", {
//         username, password
//       });
//       const data = response.data;
//       setAccessToken(data.tokens.access);
//       setRefreshToken(data.tokens.refresh);
//       setUser(data.user);
//       localStorage.setItem("accessToken", data.tokens.access);
//       localStorage.setItem("refreshToken", data.tokens.refresh);
//       return true;
//     } catch (err) {
//       console.error(err);
//       alert("Invalid credentials. Try again.");
//       return false;
//     }
//   };

//   // ✅ Logout
//   const handleLogout = async () => {
//     try {
//       await axios.post("http://127.0.0.1:8000/api/logout/", {
//         refresh: refreshToken
//       }, {
//         headers: { Authorization: `Bearer ${accessToken}` }
//       });
//     } catch (err) {
//       console.error("Logout failed (ignored).");
//     }
//     setUser(null);
//     setAccessToken(null);
//     setRefreshToken(null);
//     localStorage.removeItem("accessToken");
//     localStorage.removeItem("refreshToken");
//   };

//   return (
//     <AuthContext.Provider value={{
//       user, accessToken, handleLogin, handleLogout, handleRegister
//     }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };


// import React, { createContext, useState, useEffect } from "react";
// import api from "./api/axios";

// export const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(
//     JSON.parse(localStorage.getItem("user")) || null
//   );

//   const login = async (username, password) => {
//     const res = await api.post("/auth/login/", { username, password });
//     if (res.status === 200) {
//       setUser(res.data);
//       localStorage.setItem("user", JSON.stringify(res.data));
//     }
//   };

//   const logout = async () => {
//     await api.post("/auth/logout/");
//     setUser(null);
//     localStorage.removeItem("user");
//   };

//   const register = async (username, password) => {
//     const res = await api.post("/auth/register/", { username, password });
//     if (res.status === 201) {
//       setUser(res.data);
//       localStorage.setItem("user", JSON.stringify(res.data));
//     }
//   };

//   return (
//     <AuthContext.Provider value={{ user, login, logout, register }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
