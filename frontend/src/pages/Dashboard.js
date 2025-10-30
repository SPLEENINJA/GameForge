// src/pages/Dashboard.js
import React, { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import api from "../api/axios";

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);

  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("");
  const [theme, setTheme] = useState("");
  const [inspiration, setInspiration] = useState("");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await api.post("/generate-game/", {
        title,
        genre,
        theme,
        inspiration,
      });
      setResult(res.data);
    } catch (err) {
      alert("Failed to generate game concept.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <div className="w-full max-w-4xl">
        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-blue-400">🎮 Welcome, {user?.username}!</h2>
          {/* <button
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white py-1 px-4 rounded-lg"
          >
            Logout
          </button> */}
        </header>

        {/* Game Concept Form */}
        <div className="bg-gray-800 rounded-2xl p-6 shadow-lg mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-blue-300">
            Generate a New Game Concept
          </h2>
          <form
            onSubmit={handleGenerate}
            className="grid grid-cols-1 gap-4 md:grid-cols-2"
          >
            <input
              type="text"
              placeholder="Game Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
              required
            />
            <input
              type="text"
              placeholder="Genre"
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
              required
            />
            <input
              type="text"
              placeholder="Theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
              required
            />
            <input
              type="text"
              placeholder="Inspiration"
              value={inspiration}
              onChange={(e) => setInspiration(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
              required
            />
            <button
              type="submit"
              className="col-span-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Game Concept"}
            </button>
          </form>
        </div>

        {/* Result Display */}
        {result && (
          <div className="bg-gray-800 rounded-2xl p-6 shadow-lg mt-6">
            <h3 className="text-xl font-semibold text-green-400 mb-2">
              {result.title}
            </h3>
            <p className="text-gray-300">
              <strong>Genre:</strong> {result.genre} | <strong>Theme:</strong>{" "}
              {result.theme}
            </p>
            <p className="mt-3 text-gray-400 italic">
              Inspiration: {result.inspiration}
            </p>
            <p className="mt-4">{result.story}</p>

            {/* Characters */}
            <div className="mt-4 grid grid-cols-2 gap-4">
              {result.characters?.map((char, idx) => (
                <div
                  key={idx}
                  className="bg-gray-700 p-3 rounded-lg text-center shadow-md"
                >
                  <strong>{char.name}</strong>
                  <p className="text-sm text-gray-300">{char.role}</p>
                </div>
              ))}
            </div>

            {/* Concept Art */}
            {result.image && (
              <img
                src={result.image}
                alt="Concept"
                className="rounded-lg mt-6 mx-auto w-full max-w-sm"
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;




// import React, { useContext, useState } from "react";
// import "./Dashboard.css";
// import api from "../api/axios"; // Axios instance pointing to your backend
// import { AuthContext } from "../AuthContext";
// import { useNavigate } from "react-router-dom";




// const Dashboard = () => {
//   const { user, handleLogout } = useContext(AuthContext);
//   const navigate = useNavigate();

//   const logout = async () => {
//     await handleLogout();
//     navigate("/login");
//   };
//   const [title, setTitle] = useState("");
//   const [genre, setGenre] = useState("");
//   const [theme, setTheme] = useState("");
//   const [inspiration, setInspiration] = useState("");
//   const [concepts, setConcepts] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const handleGenerate = async () => {
//     if (!title || !genre) {
//       alert("Please fill at least Title and Genre.");
//       return;
//     }

//     setLoading(true);
//     try {
//       const response = await api.post("/generate-game/", {
//         title,
//         genre,
//         theme,
//         inspiration,
//       });

//       const newConcept = response.data;

//       setConcepts([newConcept, ...concepts]);

//       // Clear inputs
//       setTitle("");
//       setGenre("");
//       setTheme("");
//       setInspiration("");
//     } catch (err) {
//       console.error(err);
//       alert("Failed to generate concept. Try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="dashboard-page">
//       <h2>Welcome, {user?.username}!</h2>
//       <div className="input-box">
//         <h2>🎮 Create a New Game Concept</h2>
//         <input
//           type="text"
//           placeholder="Title"
//           value={title}
//           onChange={(e) => setTitle(e.target.value)}
//         />
//         <input
//           type="text"
//           placeholder="Genre"
//           value={genre}
//           onChange={(e) => setGenre(e.target.value)}
//         />
//         <input
//           type="text"
//           placeholder="Theme"
//           value={theme}
//           onChange={(e) => setTheme(e.target.value)}
//         />
//         <input
//           type="text"
//           placeholder="Inspiration / Keywords"
//           value={inspiration}
//           onChange={(e) => setInspiration(e.target.value)}
//         />
//         <button onClick={handleGenerate} disabled={loading}>
//           {loading ? "Generating..." : "Generate Concept"}
//         </button>
//       </div>

//       <div className="concept-gallery">
//         {concepts.map((c) => (
//           <div key={c.id || c.title} className="concept-card">
//             <img src={c.image || "https://via.placeholder.com/200x150.png?text=Concept"} alt="concept" />
//             <h3>{c.title}</h3>
//             <p><strong>Genre:</strong> {c.genre}</p>
//             <p><strong>Theme:</strong> {c.theme}</p>
//             <p><strong>Inspiration:</strong> {c.inspiration}</p>
//             {c.story && <p><strong>Story:</strong> {c.story}</p>}
//             {c.characters && (
//               <div>
//                 <strong>Characters:</strong>
//                 <ul>
//                   {c.characters.map((char, index) => (
//                     <li key={index}>{char.name} - {char.role}</li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         ))}
//       </div>
//       <button onClick={logout}>Logout</button>
//     </div>
//   );
// };

// export default Dashboard;



// import React, { useContext } from "react";
// import { AuthContext } from "../AuthContext";
// import { useNavigate } from "react-router-dom";

// const Dashboard = () => {
//   const { user, handleLogout } = useContext(AuthContext);
//   const navigate = useNavigate();

//   const logout = async () => {
//     await handleLogout();
//     navigate("/login");
//   };

//   return (
//     <div className="dashboard">
//       <h2>Welcome, {user?.username}!</h2>
//       <p>Email: {user?.email}</p>
//       <button onClick={logout}>Logout</button>
//     </div>
//   );
// };

// export default Dashboard;
