import httpx

class NiceClient():
    def __init__(self, client_id, client_secret, access_key_id, access_key_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def get_accessToken(self):
        headers = {
            "Content-Type":"application/x-www-form-urlencoded"
        }

        body = {
            "grant_type":"password",
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "username":self.access_key_id,
            "password":self.access_key_secret,
        }


        try:
            response = httpx.post(
                url= "https://cxone.niceincontact.com/auth/token",
                headers=headers,
                data=body
            )

            return response.json()["access_token"]
        except Exception as exc:
            print(f"Error: {exc}")
            return None