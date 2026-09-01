import os
from cryptography.fernet import Fernet


class TokenManager:
    def __init__(self):
        self.key = os.getenv("TOKEN_ENCRYPTION_KEY")
        self.cipher = Fernet(self.key.encode()) if self.key else None

    def encrypt(self, token: str) -> str:
        if not self.cipher:
            raise RuntimeError("TOKEN_ENCRYPTION_KEY is missing")
        return self.cipher.encrypt(token.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        if not self.cipher:
            raise RuntimeError("TOKEN_ENCRYPTION_KEY is missing")
        return self.cipher.decrypt(encrypted.encode()).decode()
