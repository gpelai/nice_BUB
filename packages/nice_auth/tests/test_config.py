import pytest

from nice_auth.config import NiceConfig

def test_getCredentials_complete(monkeypatch):
    monkeypatch.setenv("NICE_CLIENT_ID", "clientid_test")
    monkeypatch.setenv("NICE_CLIENT_SECRET", "clientsecret_test")
    monkeypatch.setenv("NICE_ACCESS_KEY_ID", "accesskeyid_test")
    monkeypatch.setenv("NICE_ACCESS_KEY_SECRET", "accesskeysecret_test")
    
    config = NiceConfig()
    client_id, client_secret, access_key_id, access_key_secret = config.get_credentials()
    
    assert client_id == "clientid_test"
    assert client_secret == "clientsecret_test"
    assert access_key_id == "accesskeyid_test"
    assert access_key_secret == "accesskeysecret_test"

def test_getCredentials_incomplete(monkeypatch):
    monkeypatch.delenv("NICE_CLIENT_ID", raising=False)
    
    with pytest.raises(
        ValueError,
        match="NICE Credencials incomplete"
    ):
        NiceConfig()