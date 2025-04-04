import os
from dotenv import load_dotenv
from Crypto.PublicKey import RSA

# Încarcă variabilele de mediu din fișierul .env
load_dotenv()

# Configurație bază
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    
    # Configurație bază de date
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', 'BCard')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'morbius')
    
    # Configurație pentru criptare
    # Cheie pentru criptare simetrică (AES)
    SYMMETRIC_KEY = os.environ.get('SYMMETRIC_KEY', 'default-symmetric-key-12345')
    
    # Căi pentru cheile de criptare asimetrică (RSA)
    RSA_PUBLIC_KEY_PATH = os.environ.get('RSA_PUBLIC_KEY_PATH', 'keys/public_key.pem')
    RSA_PRIVATE_KEY_PATH = os.environ.get('RSA_PRIVATE_KEY_PATH', 'keys/private_key.pem')

    # Conexiune PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Generare chei RSA dacă nu există
    @staticmethod
    def generate_rsa_keys():
        # Verifică și creează directorul pentru chei dacă nu există
        os.makedirs(os.path.dirname(Config.RSA_PUBLIC_KEY_PATH), exist_ok=True)
        
        # Generează pereche de chei RSA dacă nu există
        if not (os.path.exists(Config.RSA_PUBLIC_KEY_PATH) and 
                os.path.exists(Config.RSA_PRIVATE_KEY_PATH)):
            
            # Generează pereche de chei RSA
            key = RSA.generate(2048)
            
            # Salvează cheia privată
            private_key = key.export_key()
            with open(Config.RSA_PRIVATE_KEY_PATH, 'wb') as f:
                f.write(private_key)
            
            # Salvează cheia publică
            public_key = key.publickey().export_key()
            with open(Config.RSA_PUBLIC_KEY_PATH, 'wb') as f:
                f.write(public_key)
            
            print("Chei RSA generate cu succes")