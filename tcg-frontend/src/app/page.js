// src/app/page.js
"use client";
import {useState} from 'react';
import {startGame, getGameState, playCard, isGameFinished} from './api';

export default function Home() {
    const [sessionId, setSessionId] = useState(null);
    const [gameState, setGameState] = useState(null);
    const [player1, setPlayer1] = useState('');
    const [player2, setPlayer2] = useState('');
    const [gameFinished, setGameFinished] = useState(false);
    const [winner, setWinner] = useState(null);

    const handleStartGame = async () => {
        const response = await startGame(player1, player2);
        await fetchGameState(response.data.session_id);
        setSessionId(response.data.session_id);
    };

    const fetchGameState = async (sessionId) => {
        const response = await getGameState(sessionId);
        setGameState(response.data);
        const finishedResponse = await isGameFinished(sessionId);
        setGameFinished(finishedResponse.data.is_finished);
        setWinner(finishedResponse.data.winner);
    };

    const handlePlayCard = async (cardIndex) => {
        await playCard(sessionId, gameState.current_player, cardIndex);
        fetchGameState(sessionId);
    };

    const handlePlayAgain = () => {
        setSessionId(null);
        setGameState(null);
        setGameFinished(false);
        setWinner(null);
        setPlayer1('');
        setPlayer2('');
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
            ) : gameFinished ? (
                <div>
                    <h1>Game Over</h1>
                    <h2>Winner: {winner}</h2>
                    <button onClick={handlePlayAgain}>Play Again</button>
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