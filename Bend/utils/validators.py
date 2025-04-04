import re
from datetime import datetime

class CardValidator:
    @staticmethod
    def validate_card_data(data):
        """Validează datele cardului"""
        errors = {}
        
        # Validează numele deținătorului cardului
        if not data.get('card_holder_name'):
            errors['card_holder_name'] = "Numele deținătorului cardului este obligatoriu"
        elif len(data.get('card_holder_name', '')) < 3:
            errors['card_holder_name'] = "Numele deținătorului trebuie să aibă cel puțin 3 caractere"
        elif len(data.get('card_holder_name', '')) > 100:
            errors['card_holder_name'] = "Numele deținătorului nu poate depăși 100 caractere"
        
        # Validează numărul cardului
        if not data.get('card_number'):
            errors['card_number'] = "Numărul cardului este obligatoriu"
        elif not CardValidator.is_valid_card_number(data.get('card_number', '')):
            errors['card_number'] = "Numărul cardului este invalid (trebuie să conțină 16 cifre)"
        
        # Validează data expirării
        if not data.get('expiry_date'):
            errors['expiry_date'] = "Data expirării este obligatorie"
        elif not CardValidator.is_valid_expiry_date(data.get('expiry_date', '')):
            errors['expiry_date'] = "Data expirării trebuie să fie în formatul MM/YYYY și să fie în viitor"
        
        # Validează CVV
        if not data.get('cvv'):
            errors['cvv'] = "CVV este obligatoriu"
        elif not CardValidator.is_valid_cvv(data.get('cvv', '')):
            errors['cvv'] = "CVV trebuie să conțină 3 sau 4 cifre"
        
        # Validează tipul cardului
        if not data.get('card_type'):
            errors['card_type'] = "Tipul cardului este obligatoriu"
        elif data.get('card_type') not in ['credit', 'debit']:
            errors['card_type'] = "Tipul cardului trebuie să fie credit sau debit"
        
        # Validează tipul criptării
        if not data.get('encryption_type'):
            errors['encryption_type'] = "Tipul criptării este obligatoriu"
        elif data.get('encryption_type') not in ['sync', 'async']:
            errors['encryption_type'] = "Tipul criptării trebuie să fie sync sau async"
        
        return errors
    
    @staticmethod
    def is_valid_card_number(card_number):
        """Validează numărul cardului"""
        # Elimină spațiile și verifică dacă sunt doar cifre și dacă lungimea este 16
        card_number = card_number.replace(' ', '')
        return card_number.isdigit() and len(card_number) == 16
    
    @staticmethod
    def is_valid_expiry_date(expiry_date):
        """Validează data expirării cardului"""
        # Verifică formatul MM/YYYY
        if not re.match(r'^(0[1-9]|1[0-2])/20[2-9]\d$', expiry_date):
            return False
        
        # Verifică dacă data este în viitor
        current_date = datetime.now()
        month, year = expiry_date.split('/')
        expiry_date = datetime(int(year), int(month), 1)
        
        return expiry_date > current_date
    
    @staticmethod
    def is_valid_cvv(cvv):
        """Validează codul CVV"""
        # CVV trebuie să conțină doar cifre și să aibă 3 sau 4 caractere
        return cvv.isdigit() and (len(cvv) == 3 or len(cvv) == 4)