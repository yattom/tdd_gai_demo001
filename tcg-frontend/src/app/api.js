// src/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const startGame = (player1, player2) => {
    return axios.post(`${API_BASE_URL}/game/start`, { player1, player2 });
};

export const getGameState = (sessionId) => {
    return axios.get(`${API_BASE_URL}/game/${sessionId}/state`);
};

export const playCard = (sessionId, player, cardIndex) => {
    return axios.post(`${API_BASE_URL}/game/${sessionId}/play`, { player, cardIndex });
};

export const isGameFinished = (sessionId) => {
    return axios.get(`${API_BASE_URL}/game/${sessionId}/is_finished`);
};