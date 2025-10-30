// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Favorites from "./pages/Favorites";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="*" element={<Login />} />
      </Routes>
    </>
  );
}

export default App;



// function App() {
//   return (
//     <div className="App" style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
//       <main style={{textAlign: 'center'}}>
//         <h1 style={{marginBottom: '0.5rem'}}>Bienvenue sur GameForge</h1>
//         <p style={{marginTop: 0}}>Page d'accueil</p>
//       </main>
//     </div>
//   );
// }

// export default App;
