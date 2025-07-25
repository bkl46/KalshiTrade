import time
import base64
import yaml
import requests
from urllib.parse import urlparse
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class KalshiAPI:
    def __init__(self, config_path="config/settings.yaml"):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.load_credentials(config_path)
        self.load_private_key()

    def load_credentials(self, config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.key_id = config["kalshi"]["key_id"]
        self.private_key_path = config["kalshi"]["private_key_path"]

    def load_private_key(self):
        with open(self.private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def _sign_request(self, method, path):
        timestamp = str(int(time.time() * 1000))  
        sign_string = f"{timestamp}{method.upper()}{path}"
        
        print(f"Debug - Signing: '{sign_string}'")
        
        signature = self.private_key.sign(
            sign_string.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature_b64 = base64.b64encode(signature).decode()
        return timestamp, signature_b64

    def _request(self, method, endpoint, **kwargs):
        path = urlparse(endpoint).path
        timestamp, signature = self._sign_request(method, path)

        headers = {
            "KALSHI-ACCESS-KEY": self.key_id,
            "KALSHI-ACCESS-TIMESTAMP": timestamp,
            "KALSHI-ACCESS-SIGNATURE": signature
        }
        
        print(f"Debug - Headers: {headers}")
        
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        url = self.base_url + endpoint
        response = self.session.request(method, url, **kwargs)
        
        print(f"Response text: {response.text}")
        response.raise_for_status()
        return response.json()


    def get_all_markets(self):
        return self._request("GET", "/markets")["markets"]

    def get_market_details(self, ticker):
        return self._request("GET", f"/markets/{ticker}")

    def get_orderbook(self, ticker):
        return self._request("GET", f"/orderbooks/{ticker}")

    def get_contracts(self, ticker):
        return self._request("GET", f"/markets/{ticker}/contracts")["contracts"]

