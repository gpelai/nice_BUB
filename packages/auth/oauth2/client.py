import httpx
import os
from dotenv import load_dotenv
import json

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

class Client():
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_key_id: str,
        access_key_secret: str
    ):
        self.client_id = client_id,
        self.client_secret = client_secret,
        self.access_key_id = access_key_id,
        self.access_key_secret = access_key_secret
        self.auth_url = "https://cxone.niceincontact.com/auth/token"

    def get_accessToken(self) -> str:

        payload = {
            "grant_type":       "password",
            "client_id":        self.client_id,
            "client_secret":    self.client_secret,
            "username":         self.access_key_id,
            "password":         self.access_key_secret
        }

        response = httpx.post(
            url=self.auth_url,
            data=payload,
            timeout=30.0
        )

        response.raise_for_status()

        return response.json()["access_token"]

config = Config("packages/auth/oauth2/.env")
config_info = config.get_envConfig()

client = Client(
    client_id = config_info["client_id"],
    client_secret = config_info["client_secret"],
    access_key_id = config_info["access_key_id"],
    access_key_secret = config_info["access_key_secret"]
)
