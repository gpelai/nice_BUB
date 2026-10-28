from config import Config
from client import Client

def return_authAccessToken():
    config = Config("packages/auth/oauth2/.env")
    config_info = config.get_envConfig()

    client = Client(
        client_id = config_info["client_id"],
        client_secret = config_info["client_secret"],
        access_key_id = config_info["access_key_id"],
        access_key_secret = config_info["access_key_secret"]
    )

    return client.get_accessToken()



if __name__ == "__main__":
    # access_token = return_authAccessToken()
    # print(access_token)
    pass