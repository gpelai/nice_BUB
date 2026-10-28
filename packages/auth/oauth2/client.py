import httpx

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
