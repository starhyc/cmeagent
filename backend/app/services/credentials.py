from cryptography.fernet import Fernet
from app.core.config import settings

class CredentialManager:
    def __init__(self):
        self.cipher = Fernet(settings.FERNET_KEY.encode())

    def encrypt(self, password: str) -> str:
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password.encode()).decode()

credential_manager = CredentialManager()
