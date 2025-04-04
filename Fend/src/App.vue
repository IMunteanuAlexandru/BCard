<template>
  <div id="app">
    <header class="app-header">
      <h1>Gestionare Carduri Bancare</h1>
    </header>
    <main class="app-content">
      <!-- Formular adăugare/editare card -->
      <card-form
        v-if="showForm"
        :cardData="currentCard"
        :isEdit="!!currentCard.id"
        :loading="formLoading"
        :error="formError"
        @submit="saveCard"
        @cancel="cancelForm"
      />
      <!-- Lista carduri -->
      <card-list
        v-else
        :cards="cards"
        :loading="cardsLoading"
        :error="cardsError"
        @add-card="addCard"
        @edit-card="editCard"
        @delete-card="openDeleteModal"
      />
      <!-- Modal confirmare ștergere -->
      <delete-modal
        v-if="showDeleteModal"
        :card="currentCard"
        :loading="deleteLoading"
        @confirm="deleteCard"
        @close="showDeleteModal = false"
      />
    </main>
  </div>
</template>

<script>
import CardList from './components/CardList.vue';
import CardForm from './components/CardForm.vue';
import DeleteModal from './components/DeleteModal.vue';
import ApiService from './services/api';

export default {
  name: 'App',
  components: {
    CardList,
    CardForm,
    DeleteModal
  },
  data() {
    return {
      cards: [],
      cardsLoading: false,
      cardsError: '',
      showForm: false,
      currentCard: {},
      formLoading: false,
      formError: '',
      showDeleteModal: false,
      deleteLoading: false
    };
  },
  created() {
    this.fetchCards();
  },
  methods: {
    // Obține lista de carduri
    async fetchCards() {
      this.cardsLoading = true;
      this.cardsError = '';
      try {
        const response = await ApiService.getCards();
        this.cards = response.data;
      } catch (error) {
        console.error('Eroare la obținerea cardurilor:', error);
        this.cardsError = 'Nu s-au putut încărca cardurile. Încercați din nou mai târziu.';
      } finally {
        this.cardsLoading = false;
      }
    },
    
    // Deschide formularul pentru adăugare card
    addCard() {
      this.currentCard = {
        card_holder_name: '',
        card_number: '',
        expiry_date: '',
        cvv: '',
        card_type: 'credit',
        encryption_type: 'sync'
      };
      this.showForm = true;
      this.formError = '';
    },
    
    // Deschide formularul pentru editare card
    editCard(card) {
      this.currentCard = { ...card };
      this.showForm = true;
      this.formError = '';
    },
    
    // Anulează operația de adăugare/editare
    cancelForm() {
      this.showForm = false;
      this.currentCard = {};
      this.formError = '';
    },
    
    // Salvează datele cardului (adăugare sau editare)
    async saveCard(cardData) {
      this.formLoading = true;
      this.formError = '';
      
      try {
        let response;
        if (cardData.id) {
          // Editare card existent
          response = await ApiService.updateCard(cardData.id, cardData);
          
          // Actualizează cardul în lista locală
          const index = this.cards.findIndex(card => card.id === cardData.id);
          if (index !== -1) {
            this.cards.splice(index, 1, response.data);
          }
        } else {
          // Adăugare card nou
          response = await ApiService.createCard(cardData);
          this.cards.push(response.data);
        }
        
        this.showForm = false;
        this.currentCard = {};
      } catch (error) {
        console.error('Eroare la salvarea cardului:', error);
        this.formError = 'Nu s-a putut salva cardul. Verificați datele și încercați din nou.';
      } finally {
        this.formLoading = false;
      }
    },
    
    // Deschide modalul de confirmare pentru ștergere
    openDeleteModal(card) {
      this.currentCard = { ...card };
      this.showDeleteModal = true;
    },
    
    // Șterge cardul confirmat
    async deleteCard() {
      this.deleteLoading = true;
      
      try {
        await ApiService.deleteCard(this.currentCard.id);
        
        // Elimină cardul din lista locală
        const index = this.cards.findIndex(card => card.id === this.currentCard.id);
        if (index !== -1) {
          this.cards.splice(index, 1);
        }
        
        this.showDeleteModal = false;
        this.currentCard = {};
      } catch (error) {
        console.error('Eroare la ștergerea cardului:', error);
        // Afișăm eroarea direct în modal
        this.currentCard.error = 'Nu s-a putut șterge cardul. Încercați din nou mai târziu.';
      } finally {
        this.deleteLoading = false;
      }
    }
  }
};
</script>

<style>
:root {
  --primary-color: #6366f1;
  --secondary-color: #4f46e5;
  --accent-color: #10b981;
  --danger-color: #ef4444;
  --text-color: #f3f4f6;
  --text-muted: #9ca3af;
  --dark-bg: #0f172a;
  --darker-bg: #070b14;
  --card-bg: rgba(30, 41, 59, 0.7);
  --border-color: rgba(148, 163, 184, 0.1);
  --success-color: #22c55e;
  --warning-color: #f59e0b;
  --glass-bg: rgba(15, 23, 42, 0.6);
  --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background: linear-gradient(135deg, var(--darker-bg), var(--dark-bg));
  min-height: 100vh;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.15), transparent 40%),
              radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.1), transparent 40%);
  width: 100%;
}

.app-header {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  padding: 2.5rem 0;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-color);
  font-weight: 700;
  letter-spacing: -0.025em;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}


.app-content {
  flex: 1;
  margin: 2rem auto;
  padding: 0 1.5rem;
  position: relative;
  width: 100%;
}

.app-footer {
  text-align: center;
  padding: 1.5rem;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid var(--border-color);
  font-size: 0.9rem;
  color: var(--text-muted);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  gap: 0.5rem;
  font-size: 0.95rem;
  background: var(--primary-color);
  color: var(--text-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  opacity: 0.95;
}

.btn:active {
  transform: translateY(0);
}

/* Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color);
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  background: var(--glass-bg);
  color: var(--text-color);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Card Container */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

/* Loading and Error States */
.loading, .error {
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
}

.loading {
  color: var(--text-muted);
}

.error {
  color: var(--danger-color);
  border-color: var(--danger-color);
}

/* Alerte și notificări */
.alert {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.alert-danger {
  background-color: #fbe9e7;
  color: var(--danger-color);
  border: 1px solid #fadbd8;
}

.alert-success {
  background-color: #e8f5e9;
  color: var(--success-color);
  border: 1px solid #d5f5d5;
}

/* Animații */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}
</style>