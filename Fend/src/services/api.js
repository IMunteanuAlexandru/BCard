import axios from 'axios';

// Configurare de bază pentru Axios
const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000
});

// Serviciul pentru operațiunile cu carduri
export default {
  // Obține toate cardurile
  getCards() {
    return apiClient.get('/cards');
  },
  
  // Obține un card după ID
  getCard(id) {
    return apiClient.get(`/cards/${id}`);
  },
  
  // Crează un card nou
  createCard(card) {
    return apiClient.post('/cards', card);
  },
  
  // Actualizează un card existent
  updateCard(id, card) {
    return apiClient.put(`/cards/${id}`, card);
  },
  
  // Șterge un card
  deleteCard(id) {
    return apiClient.delete(`/cards/${id}`);
  }
};