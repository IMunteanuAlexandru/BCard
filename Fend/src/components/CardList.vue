<template>
    <div class="cards-container">
      <div class="cards-header">
        <button 
          class="btn-add"
          @click="$emit('add-card')"
        >
          Adaugă card nou
        </button>
      </div>
      
      <div v-if="loading" class="loading">
        Încărcare carduri...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-else-if="!cards.length" class="no-cards">
        Nu există carduri înregistrate. Adăugați primul card acum!
      </div>
      
      <div v-else class="cards-grid">
        <div 
          v-for="card in cards" 
          :key="card.id" 
          class="card-item"
          :class="{ 'credit': card.card_type === 'credit', 'debit': card.card_type === 'debit' }"
        >
          <div class="card-header">
            <div class="card-type">{{ card.card_type === 'credit' ? 'Credit' : 'Debit' }}</div>
            <div class="encryption-type">
              Criptare: {{ card.encryption_type === 'sync' ? 'Sincronă' : 'Asincronă' }}
            </div>
          </div>
          
          <div class="card-body">
            <div class="card-number">{{ card.card_number }}</div>
            <div class="card-details">
              <div class="card-holder">{{ card.card_holder_name }}</div>
              <div class="card-info">
                <div class="card-expiry">Exp: {{ card.expiry_date }}</div>
                <div class="card-cvv">CVV: {{ card.cvv }}</div>
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button 
              class="btn-edit"
              @click="$emit('edit-card', card)"
            >
              Editare
            </button>
            <button 
              class="btn-delete"
              @click="$emit('delete-card', card)"
            >
              Ștergere
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CardList',
    props: {
      cards: {
        type: Array,
        required: true
      },
      loading: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: ''
      }
    }
  }
  </script>
  
  <style scoped>
  .cards-container {
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
  }
  
  .cards-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    justify-content: center ;
  }

  .cards-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color);
    margin: 0;
  }
  
  .btn-add {
    background: var(--accent-color);
    color: var(--text-color);
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .btn-add:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
  }
  
  .loading, .error, .no-cards {
    text-align: center;
    padding: 2rem;
    border-radius: 1rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
  }
  
  .error {
    color: var(--danger-color);
    border-color: var(--danger-color);
  }
  
  .cards-grid {
    display: flex;
    flex-wrap: nowrap;
    gap: 1rem;
    padding: 1rem;
    margin: 0 auto;
    overflow-x: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--accent-color) var(--glass-bg);
    width: 400%;
  }
  
  .cards-grid::-webkit-scrollbar {
    height: 6px;
  }
  
  .cards-grid::-webkit-scrollbar-track {
    background: var(--glass-bg);
    border-radius: 3px;
  }
  
  .cards-grid::-webkit-scrollbar-thumb {
    background: var(--accent-color);
    border-radius: 3px;
  }
  
  .card-item {
    position: relative;
    border-radius: 1rem;
    padding: 1rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
    color: var(--text-color);
    transition: all 0.3s ease;
    overflow: hidden;
    flex: 0 0 300px;
    max-width: 300px;
  }
  
  .card-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(to right, var(--primary-color), var(--accent-color));
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .card-item:hover::before {
    opacity: 1;
  }
  
  .card-item:hover {
    transform: translateY(-4px);
    box-shadow: var(--card-shadow);
  }
  
  .card-item.credit::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.15), transparent);
  }
  
  .card-item.debit::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle at top right, rgba(16, 185, 129, 0.15), transparent);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .card-type {
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    color: var(--primary-color);
    letter-spacing: 0.05em;
    background: rgba(99, 102, 241, 0.1);
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
  }
  
  .encryption-type {
    font-size: 0.7rem;
    color: var(--text-color);
    background: rgba(156, 163, 175, 0.15);
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
  }
  
  .card-body {
    margin-bottom: 1.5rem;
  }
  
  .card-number {
    font-size: 1rem;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-color);
    background: rgba(255, 255, 255, 0.07);
    padding: 0.5rem;
    border-radius: 0.5rem;
    text-align: center;
  }
  
  .card-details {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .card-holder {
    text-transform: uppercase;
    font-size: 0.75rem;
    color: var(--text-color);
    max-width: 60%;
    letter-spacing: 0.05em;
  }
  
  .card-info {
    text-align: right;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .card-expiry, .card-cvv {
    font-size: 0.75rem;
    color: var(--text-color);
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    background: rgba(255, 255, 255, 0.07);
  }
  
  .card-cvv {
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-color);
    background: rgba(16, 185, 129, 0.15);
  }
  
  .card-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .btn-edit, .btn-delete {
    padding: 0.25rem 0.75rem;
    border: none;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.75rem;
  }
  
  .btn-edit {
    background: var(--primary-color);
    color: var(--text-color);
  }
  
  .btn-edit:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
  }
  
  .btn-delete {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger-color);
  }
  
  .btn-delete:hover {
    transform: translateY(-2px);
    background: var(--danger-color);
    color: var(--text-color);
  }
  </style>