import requests
import yaml
import os

class KalshiAPI:
    def __init__(self, config_path="config/settings.yaml"):
        self.base_url = "https://trading-api.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.load_credentials(config_path)
        self.authenticate()

    def load_credentials(self, config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.email = config["kalshi"]["email"]
        self.password = config["kalshi"]["password"]

    def authenticate(self):
        url = f"{self.base_url}/login"
        response = self.session.post(url, json={
            "email": self.email,
            "password": self.password
        })
        response.raise_for_status()
        token = response.json()["token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_all_markets(self, category=None):
        url = f"{self.base_url}/markets"
        params = {}
        if category:
            params["category"] = category
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()["markets"]

    def get_market_details(self, market_ticker):
        url = f"{self.base_url}/markets/{market_ticker}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_orderbook(self, market_ticker):
        url = f"{self.base_url}/orderbooks/{market_ticker}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_contracts(self, market_ticker):
        url = f"{self.base_url}/markets/{market_ticker}/contracts"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()["contracts"]

    # Placeholder for future:
    def place_order(self, contract_id, side, quantity, price):
        pass  # We’ll fill this in later

