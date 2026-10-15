from nice_auth.config import NiceConfig
from nice_auth.client import NiceClient

config = NiceConfig()
client_id, client_secret, access_key_id, access_key_secret = config.get_credentials()

client = NiceClient(client_id, client_secret, access_key_id, access_key_secret)

access_token = client.get_accessToken()

