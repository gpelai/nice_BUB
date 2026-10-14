import os
from dotenv import load_dotenv

load_dotenv()

class NiceConfig():
    def __init__(self):
        self.client_id = os.getenv("NICE_CLIENT_ID")
        self.client_secret = os.getenv("NICE_CLIENT_SECRET")
        self.access_key_id = os.getenv("NICE_ACCESS_KEY_ID")
        self.access_key_secret = os.getenv("NICE_ACCESS_KEY_SECRET")



    def get_credentials(self):
        """
        This method returns:
            - client_id
            - client_secret
            - access_key_id
            - access_key_secret
        """
        return self.client_id, self.client_secret, self.access_key_id, self.access_key_secret
