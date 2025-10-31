import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Welcome to GameForge</h1>
      <p>Generate and explore AI-powered video game concepts.</p>
      <Link to="/dashboard">
        <button>Go to Dashboard</button>
      </Link>
    </div>
  );
};

export default Home;


// import React, { useEffect, useState } from "react";
// import api from "../api/axios";
// import { Link } from "react-router-dom";

// export default function Home() {
//   const [games, setGames] = useState([]);

//   useEffect(() => {
//     api.get("/games/").then((res) => setGames(res.data));
//   }, []);

//   return (
//     <div className="home">
//       <h1>🎮 Community Game Creations</h1>
//       <div className="game-list">
//         {games.map((game) => (
//           <div key={game.id} className="game-card">
//             <h3>{game.title}</h3>
//             <p><strong>By:</strong> {game.creator_username}</p>
//             <Link to={`/game/${game.id}`}>View Details</Link>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
