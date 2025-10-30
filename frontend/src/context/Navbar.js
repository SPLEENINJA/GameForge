import React from "react";
import { NavLink } from "react-router-dom";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={{ padding: "10px", backgroundColor: "#282c34", color: "white" }}>
      <Link to="/" style={{ color: "white", marginRight: "15px" }}>
        GameForge
      </Link>
      {user ? (
        <>
          <Link to="/dashboard" style={{ color: "white", marginRight: "15px" }}>
            Dashboard
          </Link>
          <button onClick={handleLogout} style={{ background: "none", color: "white", border: "none", cursor: "pointer" }}>
            Logout
          </button>
        </>
      ) : (
        <>
          <Link to="/login" style={{ color: "white", marginRight: "15px" }}>
            Login
          </Link>
          <Link to="/signup" style={{ color: "white" }}>
            Signup
          </Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;
