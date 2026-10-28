import os
import json
from dotenv import load_dotenv

class Config():
    def __init__(self, env_path):
        self.env_path = env_path

    def get_envConfig(self) -> json:

        load_dotenv(self.env_path)
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")

        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "access_key_id": access_key_id,
            "access_key_secret": access_key_secret
        }
