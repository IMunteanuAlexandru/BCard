import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging
import traceback

class DatabaseService:
    def __init__(self, config):
        self.config = config
        # Test connection on initialization
        self.test_connection()
        
    def test_connection(self):
        """Testează conexiunea la baza de date"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT 1')
            logging.info("Database connection successful")
        except Exception as e:
            logging.error(f"Database connection failed: {str(e)}\n{traceback.format_exc()}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager pentru conexiunea la baza de date"""
        connection = None
        try:
            connection = psycopg2.connect(
                host=self.config['DB_HOST'],
                port=self.config['DB_PORT'],
                dbname=self.config['DB_NAME'],
                user=self.config['DB_USER'],
                password=self.config['DB_PASSWORD']
            )
            yield connection
        except Exception as e:
            logging.error(f"Database connection error: {str(e)}\n{traceback.format_exc()}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                try:
                    connection.close()
                except Exception as e:
                    logging.error(f"Error closing connection: {str(e)}")
    
    def get_cards(self):
        """Obține toate cardurile din baza de date"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT 
                            id, card_holder_name, card_number, expiry_date, 
                            cvv, card_type, encryption_type, 
                            created_at, updated_at
                        FROM cards
                        ORDER BY created_at DESC
                    """)
                    results = cursor.fetchall()
                    logging.info(f"Successfully fetched {len(results)} cards from database")
                    return results
        except Exception as e:
            logging.error(f"Error fetching cards: {str(e)}\n{traceback.format_exc()}")
            raise
    
    def get_card_by_id(self, card_id):
        """Obține un card după ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT 
                            id, card_holder_name, card_number, expiry_date, 
                            cvv, card_type, encryption_type, 
                            created_at, updated_at
                        FROM cards
                        WHERE id = %s
                    """, (card_id,))
                    result = cursor.fetchone()
                    if result:
                        logging.info(f"Successfully fetched card with ID {card_id}")
                    else:
                        logging.info(f"No card found with ID {card_id}")
                    return result
        except Exception as e:
            logging.error(f"Error fetching card {card_id}: {str(e)}\n{traceback.format_exc()}")
            raise
    
    def create_card(self, card_data):
        """Crează un nou card în baza de date"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        INSERT INTO cards (
                            card_holder_name, card_number, expiry_date, 
                            cvv, card_type, encryption_type
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING 
                            id, card_holder_name, card_number, expiry_date, 
                            cvv, card_type, encryption_type, 
                            created_at, updated_at
                    """, (
                        card_data['card_holder_name'],
                        card_data['card_number'],
                        card_data['expiry_date'],
                        card_data['cvv'],
                        card_data['card_type'],
                        card_data['encryption_type']
                    ))
                    conn.commit()
                    result = cursor.fetchone()
                    if result:
                        logging.info(f"Successfully created new card with ID {result['id']}")
                    return result
        except Exception as e:
            logging.error(f"Error creating card: {str(e)}\n{traceback.format_exc()}")
            raise
    
    def update_card(self, card_id, card_data):
        """Actualizează un card existent"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        UPDATE cards
                        SET 
                            card_holder_name = %s,
                            card_number = %s,
                            expiry_date = %s,
                            cvv = %s,
                            card_type = %s,
                            encryption_type = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        RETURNING 
                            id, card_holder_name, card_number, expiry_date, 
                            cvv, card_type, encryption_type, 
                            created_at, updated_at
                    """, (
                        card_data['card_holder_name'],
                        card_data['card_number'],
                        card_data['expiry_date'],
                        card_data['cvv'],
                        card_data['card_type'],
                        card_data['encryption_type'],
                        card_id
                    ))
                    conn.commit()
                    result = cursor.fetchone()
                    if result:
                        logging.info(f"Successfully updated card with ID {card_id}")
                    else:
                        logging.warning(f"No card found to update with ID {card_id}")
                    return result
        except Exception as e:
            logging.error(f"Error updating card {card_id}: {str(e)}\n{traceback.format_exc()}")
            raise
    
    def delete_card(self, card_id):
        """Șterge un card din baza de date"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM cards WHERE id = %s", (card_id,))
                    conn.commit()
                    deleted = cursor.rowcount > 0
                    if deleted:
                        logging.info(f"Successfully deleted card with ID {card_id}")
                    else:
                        logging.warning(f"No card found to delete with ID {card_id}")
                    return deleted
        except Exception as e:
            logging.error(f"Error deleting card {card_id}: {str(e)}\n{traceback.format_exc()}")
            raise