import base64
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from config import Config

class EncryptionService:
    def __init__(self, config):
        self.config = config
        self.symmetric_key = config.get('SYMMETRIC_KEY', 'cheie-secreta-default').encode('utf-8')
        # Ensure the key is 32 bytes (256 bits)
        self.symmetric_key = self.symmetric_key.ljust(32)[:32]
        
        # Asigură existența cheilor RSA
        Config.generate_rsa_keys()
        
        # Salvează căile pentru chei
        self.rsa_public_key_path = config['RSA_PUBLIC_KEY_PATH']
        self.rsa_private_key_path = config['RSA_PRIVATE_KEY_PATH']
        
        # Încarcă cheile RSA
        self.rsa_public_key = self._load_public_key()
        self.rsa_private_key = self._load_private_key()
    
    def _load_public_key(self):
        with open(self.rsa_public_key_path, "rb") as key_file:
            return RSA.import_key(key_file.read())
    
    def _load_private_key(self):
        with open(self.rsa_private_key_path, "rb") as key_file:
            return RSA.import_key(key_file.read())
    
    # Criptare sincronă (AES)
    def encrypt_sync(self, data):
        if not data:
            return None
            
        # Convertește datele în bytes
        data_bytes = data.encode('utf-8')
        
        # Generează un IV aleatoriu
        iv = get_random_bytes(16)
        
        # Adaugă padding
        padded_data = pad(data_bytes, AES.block_size)
        
        # Inițializează cifrul
        cipher = AES.new(self.symmetric_key, AES.MODE_CBC, iv)
        
        # Criptează datele
        encrypted_data = cipher.encrypt(padded_data)
        
        # Combină IV cu datele criptate și encodează în base64
        result = base64.b64encode(iv + encrypted_data).decode('utf-8')
        return result
    
    # Decriptare sincronă (AES)
    def decrypt_sync(self, encrypted_data):
        if not encrypted_data:
            return None
            
        # Decodează din base64
        binary_data = base64.b64decode(encrypted_data)
        
        # Separă IV de datele criptate
        iv = binary_data[:16]
        ciphertext = binary_data[16:]
        
        # Inițializează cifrul pentru decriptare
        cipher = AES.new(self.symmetric_key, AES.MODE_CBC, iv)
        
        # Decriptează datele
        padded_data = cipher.decrypt(ciphertext)
        
        # Elimină padding
        data = unpad(padded_data, AES.block_size)
        
        return data.decode('utf-8')
    
    # Criptare asincronă (RSA)
    def encrypt_async(self, data):
        if not data:
            return None
            
        # Convertește datele în bytes
        data_bytes = data.encode('utf-8')
        
        # Creează un cifru PKCS1_OAEP
        cipher = PKCS1_OAEP.new(self.rsa_public_key)
        
        # Criptează datele
        encrypted = cipher.encrypt(data_bytes)
        
        # Encodează rezultatul în base64
        return base64.b64encode(encrypted).decode('utf-8')
    
    # Decriptare asincronă (RSA)
    def decrypt_async(self, encrypted_data):
        if not encrypted_data:
            return None
            
        # Decodează din base64
        binary_data = base64.b64decode(encrypted_data)
        
        # Creează un cifru PKCS1_OAEP
        cipher = PKCS1_OAEP.new(self.rsa_private_key)
        
        # Decriptează datele
        decrypted = cipher.decrypt(binary_data)
        
        return decrypted.decode('utf-8')
    
    # Metodă generică pentru criptare bazată pe tipul specificat
    def encrypt(self, data, encryption_type):
        if encryption_type == 'sync':
            return self.encrypt_sync(data)
        elif encryption_type == 'async':
            return self.encrypt_async(data)
        else:
            raise ValueError("Tip de criptare necunoscut")
    
    # Metodă generică pentru decriptare bazată pe tipul specificat
    def decrypt(self, data, encryption_type):
        if encryption_type == 'sync':
            return self.decrypt_sync(data)
        elif encryption_type == 'async':
            return self.decrypt_async(data)
        else:
            raise ValueError("Tip de criptare necunoscut")