// src/app/page.js
"use client";
import { useState } from 'react';
import { startGame, getGameState, playCard } from './api';

export default function Home() {
  const [sessionId, setSessionId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');

  const handleStartGame = async () => {
    const response = await startGame(player1, player2);
    setSessionId(response.data.session_id);
    fetchGameState(response.data.session_id);
  };

  const fetchGameState = async (sessionId) => {
    const response = await getGameState(sessionId);
    setGameState(response.data);
  };

  const handlePlayCard = async (cardIndex) => {
    await playCard(sessionId, gameState.current_player, cardIndex);
    fetchGameState(sessionId);
  };

  return (
      <div>
        {!sessionId ? (
            <div>
              <input
                  type="text"
                  placeholder="Player 1"
                  value={player1}
                  onChange={(e) => setPlayer1(e.target.value)}
              />
              <input
                  type="text"
                  placeholder="Player 2"
                  value={player2}
                  onChange={(e) => setPlayer2(e.target.value)}
              />
              <button onClick={handleStartGame}>Start Game</button>
            </div>
        ) : (
            <div>
              <h1>Turn: {gameState.turn_no}</h1>
              <h2>Current Player: {gameState.current_player}</h2>
              <h3>Life Points</h3>
              <ul>
                {Object.entries(gameState.life_points).map(([player, points]) => (
                    <li key={player}>{player}: {points}</li>
                ))}
              </ul>
              <h3>Hand</h3>
              <ul>
                {gameState.hand.map((card, index) => (
                    <li key={index} onClick={() => handlePlayCard(index)}>
                      {card}
                    </li>
                ))}
              </ul>
            </div>
        )}
      </div>
  );
}