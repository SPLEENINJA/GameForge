// GameForge/frontend/src/pages/Dashboard.js
import React, { useContext, useState } from "react";
import api from "../api/axios";
import { AuthContext } from "../AuthContext";

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);

  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("");
  const [theme, setTheme] = useState("");
  const [inspiration, setInspiration] = useState("");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  // console.log(result);
  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      // create placeholders for story and characters
      const payload = {
        title,
        genre,
        main_story: "This is a placeholder story for your game.", //result.main_story,
        atmosphere: theme || "",       // maps to Game.atmosphere
        visual_style: inspiration || "", // maps to Game.visual_style
        characters: [
          { name: "Character 1", role: "Hero" },
          { name: "Character 2", role: "Villain" },
        ], // optional field
        is_public: true,
      };

      console.log("📤 Sending game data: ", payload);
      const res = await api.post("/generate-game/", payload);
      console.log("IMAGE URL:", res.data.image);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to generate game concept. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <div className="w-full max-w-4xl">
        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-blue-400">🎮 GameForge</h1>
          {/* <button
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 py-1 px-4 rounded-lg"
          >
            Logout
          </button> */}
        </header>

        {/* Input Form */}
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
            />
            <input
              type="text"
              placeholder="Genre"
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
            />
            <input
              type="text"
              placeholder="Theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
            />
            <input
              type="text"
              placeholder="Inspiration"
              value={inspiration}
              onChange={(e) => setInspiration(e.target.value)}
              className="p-3 rounded-lg bg-gray-700 text-white"
            />
            <button
              type="submit"
              className="col-span-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold"
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Game Concept"}
            </button>
          </form>
        </div>

        {/* Generated Game Display */}
        {result && (
          <div className="bg-gray-800 rounded-2xl p-6 shadow-lg mt-6">
            <h3 className="text-2xl font-bold text-green-400 mb-2">
              {result.title}
            </h3>
            <p className="text-gray-300">
              <strong>Genre:</strong> {result.genre} | <strong>Theme:</strong>{" "}
              {result.atmosphere} | <strong>Inspiration:</strong> {result.visual_style}
            </p>
            <p className="mt-3 text-gray-400 italic">{result.main_story}</p>

            {/* Characters */}
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              {result.characters?.map((char, idx) => (
                <div
                  key={idx}
                  className="bg-gray-700 p-3 rounded-lg text-center shadow-md"
                >
                  <strong>{char.name}</strong>
                  <p className="text-sm text-gray-300">{char.role}</p>
                  {char.class && <p className="text-sm text-gray-300">{char.class}</p>}
                </div>
              ))}
            </div>

            {/* Concept Art */}
            {result.image && (
              <img
                src={`http://localhost:8000${result.image}`}
                alt="Concept Art"
                className="rounded-lg mt-6 mx-auto w-full max-w-md shadow-lg"
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

