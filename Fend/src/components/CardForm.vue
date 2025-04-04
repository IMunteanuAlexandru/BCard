<template>
    <div class="card-form-container">
      <h2>{{ isEdit ? 'Editare card' : 'Adăugare card nou' }}</h2>
      
      <form @submit.prevent="submitForm" class="card-form">
        <!-- Numele deținătorului cardului -->
        <div class="form-group">
          <label for="cardHolderName">Numele deținătorului *</label>
          <input
            id="cardHolderName"
            v-model="form.card_holder_name"
            type="text"
            required
            placeholder="NUME PRENUME"
            class="form-control"
            :class="{ 'invalid': errors.card_holder_name }"
          />
          <div v-if="errors.card_holder_name" class="error-text">
            {{ errors.card_holder_name }}
          </div>
        </div>
        
        <!-- Numărul cardului -->
        <div class="form-group">
          <label for="cardNumber">Numărul cardului *</label>
          <input
            id="cardNumber"
            v-model="form.card_number"
            type="text"
            required
            placeholder="XXXX XXXX XXXX XXXX"
            maxlength="19"
            @input="formatCardNumber"
            class="form-control"
            :class="{ 'invalid': errors.card_number }"
          />
          <div v-if="errors.card_number" class="error-text">
            {{ errors.card_number }}
          </div>
        </div>
        
        <!-- Data expirării și CVV -->
        <div class="form-row">
          <div class="form-group half">
            <label for="expiryDate">Data expirării *</label>
            <input
              id="expiryDate"
              v-model="form.expiry_date"
              type="text"
              required
              placeholder="MM/YYYY"
              maxlength="7"
              @input="formatExpiryDate"
              class="form-control"
              :class="{ 'invalid': errors.expiry_date }"
            />
            <div v-if="errors.expiry_date" class="error-text">
              {{ errors.expiry_date }}
            </div>
          </div>
          
          <div class="form-group half">
            <label for="cvv">CVV *</label>
            <input
              id="cvv"
              v-model="form.cvv"
              type="text"
              required
              placeholder="123"
              maxlength="4"
              class="form-control"
              :class="{ 'invalid': errors.cvv }"
            />
            <div v-if="errors.cvv" class="error-text">
              {{ errors.cvv }}
            </div>
          </div>
        </div>
        
        <!-- Tipul cardului -->
        <div class="form-group">
          <label>Tipul cardului *</label>
          <div class="radio-group">
            <label class="radio-label">
              <input
                type="radio"
                v-model="form.card_type"
                value="credit"
                required
              />
              Credit
            </label>
            <label class="radio-label">
              <input
                type="radio"
                v-model="form.card_type"
                value="debit"
                required
              />
              Debit
            </label>
          </div>
          <div v-if="errors.card_type" class="error-text">
            {{ errors.card_type }}
          </div>
        </div>
        
        <!-- Tipul criptării -->
        <div class="form-group">
          <label>Tipul criptării *</label>
          <div class="radio-group">
            <label class="radio-label">
              <input
                type="radio"
                v-model="form.encryption_type"
                value="sync"
                required
              />
              Sincronă (AES)
            </label>
            <label class="radio-label">
              <input
                type="radio"
                v-model="form.encryption_type"
                value="async"
                required
              />
              Asincronă (RSA)
            </label>
          </div>
          <div v-if="errors.encryption_type" class="error-text">
            {{ errors.encryption_type }}
          </div>
        </div>
        
        <div v-if="error" class="form-error">
          {{ error }}
        </div>
        
        <div class="form-actions">
          <button 
            type="button" 
            class="btn-cancel"
            @click="$emit('cancel')"
          >
            Anulare
          </button>
          <button 
            type="submit" 
            class="btn-submit"
            :disabled="loading"
          >
            {{ loading ? 'Se procesează...' : (isEdit ? 'Salvează modificările' : 'Adaugă card') }}
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CardForm',
    props: {
      cardData: {
        type: Object,
        default: () => ({})
      },
      isEdit: {
        type: Boolean,
        default: false
      },
      loading: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: ''
      }
    },
    data() {
      return {
        form: {
          card_holder_name: '',
          card_number: '',
          expiry_date: '',
          cvv: '',
          card_type: 'credit',
          encryption_type: 'sync'
        },
        errors: {}
      };
    },
    created() {
      if (this.isEdit && this.cardData) {
        this.form = { ...this.cardData };
      }
    },
    methods: {
      formatCardNumber(event) {
        // Elimină orice caracter care nu este cifră
        let value = event.target.value.replace(/\D/g, '');
        
        // Adaugă spații după fiecare grup de 4 cifre
        let formatted = '';
        for (let i = 0; i < value.length; i++) {
          if (i > 0 && i % 4 === 0) {
            formatted += ' ';
          }
          formatted += value[i];
        }
        
        // Limitează la 16 cifre (19 caractere cu spații)
        this.form.card_number = formatted.substring(0, 19);
      },
      
      formatExpiryDate(event) {
        // Elimină orice caracter care nu este cifră
        let value = event.target.value.replace(/\D/g, '');
        
        // Adaugă '/' după primele 2 cifre
        if (value.length > 2) {
          value = value.substring(0, 2) + '/' + value.substring(2);
        }
        
        // Limitează la formatul MM/YYYY
        this.form.expiry_date = value.substring(0, 7);
      },
      
      validateForm() {
        this.errors = {};
        let isValid = true;
        
        // Validare nume deținător
        if (!this.form.card_holder_name.trim()) {
          this.errors.card_holder_name = 'Numele deținătorului este obligatoriu';
          isValid = false;
        } else if (this.form.card_holder_name.length < 3) {
          this.errors.card_holder_name = 'Numele trebuie să aibă cel puțin 3 caractere';
          isValid = false;
        }
        
        // Validare număr card
        const cardNumber = this.form.card_number.replace(/\s/g, '');
        if (!cardNumber) {
          this.errors.card_number = 'Numărul cardului este obligatoriu';
          isValid = false;
        } else if (!/^\d{16}$/.test(cardNumber)) {
          this.errors.card_number = 'Numărul cardului trebuie să conțină exact 16 cifre';
          isValid = false;
        }
        
        // Validare dată expirare
        if (!this.form.expiry_date) {
          this.errors.expiry_date = 'Data expirării este obligatorie';
          isValid = false;
        } else if (!/^(0[1-9]|1[0-2])\/20\d{2}$/.test(this.form.expiry_date)) {
          this.errors.expiry_date = 'Formatul datei trebuie să fie MM/YYYY';
          isValid = false;
        } else {
          // Verifică dacă data expirării este în viitor
          const [month, year] = this.form.expiry_date.split('/');
          const expiryDate = new Date(parseInt(year), parseInt(month) - 1);
          const currentDate = new Date();
          
          if (expiryDate <= currentDate) {
            this.errors.expiry_date = 'Data expirării trebuie să fie în viitor';
            isValid = false;
          }
        }
        
        // Validare CVV
        if (!this.form.cvv) {
          this.errors.cvv = 'CVV este obligatoriu';
          isValid = false;
        } else if (!/^\d{3,4}$/.test(this.form.cvv)) {
          this.errors.cvv = 'CVV trebuie să conțină 3 sau 4 cifre';
          isValid = false;
        }
        
        return isValid;
      },
      
      submitForm() {
        if (this.validateForm()) {
          this.$emit('submit', { ...this.form });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .card-form-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 1.5rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid var(--border-color);
    color: var(--text-color);
  }
  
  h2 {
    color: var(--text-color);
    margin-bottom: 1.5rem;
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  .card-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-row {
    display: flex;
    gap: 1.25rem;
  }
  
  .half {
    flex: 1;
  }
  
  label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-color);
  }
  
  .form-control {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    font-size: 0.875rem;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-color);
    transition: all 0.3s ease;
  }
  
  .form-control:focus {
    outline: none;
    border-color: var(--accent-color);
    background: rgba(255, 255, 255, 0.07);
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
  }
  
  .form-control.invalid {
    border-color: var(--danger-color);
    background: rgba(239, 68, 68, 0.1);
  }
  
  .error-text {
    color: var(--danger-color);
    font-size: 0.75rem;
  }
  
  .radio-group {
    display: flex;
    gap: 1.5rem;
  }
  
  .radio-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.875rem;
    color: var(--text-color);
  }
  
  .radio-label input[type="radio"] {
    width: 1rem;
    height: 1rem;
    border: 2px solid var(--border-color);
    border-radius: 50%;
    appearance: none;
    -webkit-appearance: none;
    outline: none;
    cursor: pointer;
    position: relative;
    background: rgba(255, 255, 255, 0.05);
  }

  .radio-label input[type="radio"]:checked {
    border-color: var(--accent-color);
    background: var(--accent-color);
  }

  .radio-label input[type="radio"]:checked::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 0.5rem;
    height: 0.5rem;
    background: var(--text-color);
    border-radius: 50%;
  }
  
  .form-error {
    color: var(--danger-color);
    padding: 0.75rem;
    background: rgba(239, 68, 68, 0.1);
    border-radius: 0.5rem;
    text-align: center;
    font-size: 0.875rem;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .btn-cancel, .btn-submit {
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
  
  .btn-submit {
    background: var(--accent-color);
    color: var(--text-color);
    border: none;
  }
  
  .btn-submit:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
  }
  
  .btn-submit:disabled {
    background: rgba(16, 185, 129, 0.5);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  </style>