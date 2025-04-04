<template>
    <div class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Confirmare ștergere</h3>
          <button class="btn-close" @click="$emit('close')">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Sunteți sigur că doriți să ștergeți acest card?</p>
          
          <div class="card-preview" v-if="card">
            <div class="preview-item">
              <span class="label">Deținător:</span>
              <span class="value">{{ card.card_holder_name }}</span>
            </div>
            <div class="preview-item">
              <span class="label">Număr card:</span>
              <span class="value">{{ card.card_number }}</span>
            </div>
            <div class="preview-item">
              <span class="label">Tip:</span>
              <span class="value">{{ card.card_type === 'credit' ? 'Credit' : 'Debit' }}</span>
            </div>
          </div>
          
          <p class="warning">Această acțiune nu poate fi anulată!</p>
        </div>
        
        <div class="modal-footer">
          <button class="btn-cancel" @click="$emit('close')">Anulare</button>
          <button 
            class="btn-delete" 
            @click="$emit('confirm')" 
            :disabled="loading"
          >
            {{ loading ? 'Se procesează...' : 'Șterge' }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DeleteModal',
    props: {
      card: {
        type: Object,
        required: true
      },
      loading: {
        type: Boolean,
        default: false
      }
    }
  }
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-container {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    width: 90%;
    max-width: 500px;
    border: 1px solid var(--border-color);
    color: var(--text-color);
    overflow: hidden;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .modal-header h3 {
    margin: 0;
    color: var(--danger-color);
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-color);
    opacity: 0.7;
    transition: opacity 0.3s ease;
    padding: 0.25rem;
    line-height: 1;
  }

  .btn-close:hover {
    opacity: 1;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .card-preview {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin: 1.25rem 0;
    border: 1px solid var(--border-color);
  }
  
  .preview-item {
    display: flex;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
  }
  
  .preview-item:last-child {
    margin-bottom: 0;
  }
  
  .preview-item .label {
    font-weight: 500;
    width: 100px;
    color: var(--text-muted);
  }

  .preview-item .value {
    color: var(--text-color);
  }
  
  .warning {
    color: var(--danger-color);
    font-weight: 500;
    text-align: center;
    font-size: 0.875rem;
    margin: 1rem 0 0;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.25rem;
    border-top: 1px solid var(--border-color);
  }
  
  .btn-cancel, .btn-delete {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.3s ease;
  }
  
  .btn-cancel {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    border: 1px solid var(--border-color);
  }
  
  .btn-cancel:hover {
    background: rgba(255, 255, 255, 0.15);
  }
  
  .btn-delete {
    background: var(--danger-color);
    color: var(--text-color);
    border: none;
  }
  
  .btn-delete:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
  }
  
  .btn-delete:disabled {
    background: rgba(239, 68, 68, 0.5);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  </style>