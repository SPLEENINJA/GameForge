// src/components/Navbar.js
import React, { useContext } from "react";
import { AuthContext } from "../AuthContext";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="bg-gray-900 p-4 flex justify-between items-center">
      <h1 className="text-white font-bold text-2xl">🎮 GameForge</h1>
      {user && (
        <div className="flex gap-4 items-center">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? "text-blue-400 font-semibold" : "text-white"
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/favorites"
            className={({ isActive }) =>
              isActive ? "text-blue-400 font-semibold" : "text-white"
            }
          >
            Favorites
          </NavLink>
          <button
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white py-1 px-4 rounded-lg"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;



// import React, { useContext } from "react";
// import { Link } from "react-router-dom";
// import { AuthContext } from "../AuthContext";

// export default function Navbar() {
//   const { user, logout } = useContext(AuthContext);

//   return (
//     <nav className="navbar">
//       <h2>🎮 GameForge</h2>
//       <div>
//         <Link to="/">Home</Link>
//         {user ? (
//           <>
//             <Link to="/dashboard">Dashboard</Link>
//             <button onClick={logout}>Logout</button>
//           </>
//         ) : (
//           <>
//             <Link to="/login">Login</Link>
//             {/* <Link to="/register">Sign Up</Link> */}
//             <Link to="/signup">Sign Up</Link>
//           </>
//         )}
//       </div>
//     </nav>
//   );
// }
