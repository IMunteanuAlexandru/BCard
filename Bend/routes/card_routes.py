from flask import Blueprint, request, jsonify, current_app
from services.encryption_service import EncryptionService
from services.db_service import DatabaseService
from utils.validators import CardValidator
import logging
import traceback

# Creare blueprint pentru API carduri
card_bp = Blueprint('cards', __name__)

def init_routes(app):
    # Inițializare servicii cu configurație
    try:
        global db_service, encryption_service
        db_service = DatabaseService(app.config)
        encryption_service = EncryptionService(app.config)
    except Exception as e:
        logging.error(f"Eroare la inițializarea serviciilor: {str(e)}\n{traceback.format_exc()}")
        raise
    
    @card_bp.route('', methods=['GET'])
    def get_cards():
        """Obține toate cardurile"""
        try:
            logging.info("Attempting to fetch all cards")
            # Obține cardurile din baza de date
            cards = db_service.get_cards()
            if not cards:
                logging.info("No cards found in database")
                return jsonify([]), 200
            
            # Decriptează datele sensibile
            decrypted_cards = []
            for card in cards:
                try:
                    decrypted_card = dict(card)
                    if card.get('card_number'):
                        decrypted_card['card_number'] = encryption_service.decrypt(
                            card['card_number'], card['encryption_type']
                        )
                        # Adaugă spații pentru lizibilitate (XXXX XXXX XXXX XXXX)
                        decrypted_card['card_number'] = ' '.join([
                            decrypted_card['card_number'][i:i+4] 
                            for i in range(0, len(decrypted_card['card_number']), 4)
                        ])
                    
                    if card.get('cvv'):
                        decrypted_card['cvv'] = encryption_service.decrypt(
                            card['cvv'], card['encryption_type']
                        )
                    
                    # Convertește timestamp-urile la string pentru JSON
                    if isinstance(card.get('created_at'), str):
                        decrypted_card['created_at'] = card['created_at']
                    else:
                        decrypted_card['created_at'] = card['created_at'].isoformat() if card.get('created_at') else None
                    
                    if isinstance(card.get('updated_at'), str):
                        decrypted_card['updated_at'] = card['updated_at']
                    else:
                        decrypted_card['updated_at'] = card['updated_at'].isoformat() if card.get('updated_at') else None
                    
                    decrypted_cards.append(decrypted_card)
                except Exception as e:
                    logging.error(f"Error decrypting card {card.get('id')}: {str(e)}\n{traceback.format_exc()}")
                    continue
            
            logging.info(f"Successfully fetched and decrypted {len(decrypted_cards)} cards")
            return jsonify(decrypted_cards), 200
            
        except Exception as e:
            logging.error(f"Error fetching cards: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": "Error fetching cards", "details": str(e)}), 500
    
    @card_bp.route('/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        """Obține un card după ID"""
        try:
            # Obține cardul din baza de date
            card = db_service.get_card_by_id(card_id)
            
            if not card:
                return jsonify({"error": "Card negăsit"}), 404
            
            # Decriptează datele sensibile
            card['card_number'] = encryption_service.decrypt(
                card['card_number'], card['encryption_type']
            )
            card['cvv'] = encryption_service.decrypt(
                card['cvv'], card['encryption_type']
            )
            
            # Formatează timestamp-urile pentru JSON
            card['created_at'] = card['created_at'].isoformat() if card['created_at'] else None
            card['updated_at'] = card['updated_at'].isoformat() if card['updated_at'] else None
            
            return jsonify(card), 200
            
        except Exception as e:
            app.logger.error(f"Eroare la obținerea cardului: {str(e)}")
            return jsonify({"error": "Eroare la obținerea cardului"}), 500
    
    @card_bp.route('', methods=['POST'])
    def create_card():
        """Crează un nou card"""
        try:
            # Obține datele din cerere
            data = request.get_json()
            logging.info(f"Received POST request with data: {data}")
            
            if not data:
                logging.error("No data received in request")
                return jsonify({
                    "error": "No data received",
                    "details": "Request body is required"
                }), 400
            
            # Validează datele
            validation_errors = CardValidator.validate_card_data(data)
            if validation_errors:
                logging.error(f"Validation errors: {validation_errors}")
                return jsonify({
                    "error": "Validation failed",
                    "details": validation_errors
                }), 400
            
            # După validare, criptează datele sensibile
            try:
                # Curăță datele de intrare
                card_data = {
                    'card_holder_name': data['card_holder_name'].strip(),
                    'card_number': data['card_number'].replace(' ', ''),
                    'expiry_date': data['expiry_date'].strip(),
                    'cvv': str(data['cvv']).strip(),
                    'card_type': data['card_type'].lower().strip(),
                    'encryption_type': data['encryption_type'].lower().strip()
                }
                
                # Criptează datele sensibile
                card_data['card_number'] = encryption_service.encrypt(
                    card_data['card_number'],
                    card_data['encryption_type']
                )
                card_data['cvv'] = encryption_service.encrypt(
                    card_data['cvv'],
                    card_data['encryption_type']
                )
                
                logging.info("Data validated and encrypted successfully")
            except Exception as e:
                logging.error(f"Error encrypting data: {str(e)}\n{traceback.format_exc()}")
                return jsonify({
                    "error": "Error encrypting data",
                    "details": str(e)
                }), 500
            
            # Adaugă cardul în baza de date
            try:
                new_card = db_service.create_card(card_data)
                if not new_card:
                    logging.error("Database returned None after card creation")
                    return jsonify({
                        "error": "Error creating card",
                        "details": "Database operation failed"
                    }), 500
                
                # Decriptează pentru răspuns
                result = dict(new_card)
                result['card_number'] = encryption_service.decrypt(
                    result['card_number'],
                    result['encryption_type']
                )
                result['cvv'] = encryption_service.decrypt(
                    result['cvv'],
                    result['encryption_type']
                )
                
                # Format card number for display (add spaces)
                result['card_number'] = ' '.join([
                    result['card_number'][i:i+4]
                    for i in range(0, len(result['card_number']), 4)
                ])
                
                # Formatează timestamp-urile pentru JSON
                if isinstance(result.get('created_at'), str):
                    result['created_at'] = result['created_at']
                else:
                    result['created_at'] = result['created_at'].isoformat() if result.get('created_at') else None
                
                if isinstance(result.get('updated_at'), str):
                    result['updated_at'] = result['updated_at']
                else:
                    result['updated_at'] = result['updated_at'].isoformat() if result.get('updated_at') else None
                
                logging.info(f"Successfully created card with ID: {result.get('id')}")
                return jsonify(result), 201
                
            except Exception as e:
                logging.error(f"Error saving to database: {str(e)}\n{traceback.format_exc()}")
                return jsonify({
                    "error": "Error saving card",
                    "details": str(e)
                }), 500
            
        except Exception as e:
            logging.error(f"Error creating card: {str(e)}\n{traceback.format_exc()}")
            return jsonify({
                "error": "Error creating card",
                "details": str(e)
            }), 500
    
    @card_bp.route('/<int:card_id>', methods=['PUT'])
    def update_card(card_id):
        """Actualizează un card existent"""
        try:
            # Verifică dacă cardul există
            existing_card = db_service.get_card_by_id(card_id)
            if not existing_card:
                return jsonify({"error": "Card negăsit"}), 404
            
            # Obține datele din cerere
            data = request.get_json()
            
            # Validează datele
            validation_errors = CardValidator.validate_card_data(data)
            if validation_errors:
                return jsonify({"errors": validation_errors}), 400
            
            # După validare, criptează datele sensibile
            card_data = {
                'card_holder_name': data['card_holder_name'],
                'card_number': encryption_service.encrypt(
                    data['card_number'].replace(' ', ''), data['encryption_type']
                ),
                'expiry_date': data['expiry_date'],
                'cvv': encryption_service.encrypt(data['cvv'], data['encryption_type']),
                'card_type': data['card_type'],
                'encryption_type': data['encryption_type']
            }
            
            # Actualizează cardul în baza de date
            updated_card = db_service.update_card(card_id, card_data)
            
            if not updated_card:
                return jsonify({"error": "Eroare la actualizarea cardului"}), 500
            
            # Decriptează pentru răspuns
            result = dict(updated_card)
            result['card_number'] = encryption_service.decrypt(
                result['card_number'], result['encryption_type']
            )
            result['cvv'] = encryption_service.decrypt(
                result['cvv'], result['encryption_type']
            )
            
            # Formatează timestamp-urile pentru JSON
            result['created_at'] = result['created_at'].isoformat() if result['created_at'] else None
            result['updated_at'] = result['updated_at'].isoformat() if result['updated_at'] else None
            
            return jsonify(result), 200
            
        except Exception as e:
            app.logger.error(f"Eroare la actualizarea cardului: {str(e)}")
            return jsonify({"error": "Eroare la actualizarea cardului"}), 500
    
    @card_bp.route('/<int:card_id>', methods=['DELETE'])
    def delete_card(card_id):
        """Șterge un card"""
        try:
            # Verifică dacă cardul există
            existing_card = db_service.get_card_by_id(card_id)
            if not existing_card:
                return jsonify({"error": "Card negăsit"}), 404
            
            # Șterge cardul din baza de date
            success = db_service.delete_card(card_id)
            
            if not success:
                return jsonify({"error": "Eroare la ștergerea cardului"}), 500
            
            return jsonify({"message": "Card șters cu succes"}), 200
            
        except Exception as e:
            app.logger.error(f"Eroare la ștergerea cardului: {str(e)}")
            return jsonify({"error": "Eroare la ștergerea cardului"}), 500
    
    # Înregistrează blueprint-ul
    app.register_blueprint(card_bp, url_prefix='/api/cards')