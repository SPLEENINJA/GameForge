import React from "react";
import { useParams } from "react-router-dom";

const GameDetails = () => {
  const { id } = useParams();

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Game Details - ID: {id}</h2>
      <p>This is where full game concept details will appear (title, story, characters, etc.).</p>
    </div>
  );
};

export default GameDetails;