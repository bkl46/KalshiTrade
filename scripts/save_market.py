# scripts/download_market_data.py

import json
import os
from kalshi_api import KalshiAPI

def download_market_data(ticker):
    api = KalshiAPI()

    try:
        print(f"📥 Downloading data for market: {ticker}")

        market_details = api.get_market_details(ticker)
        contracts = api.get_contracts(ticker)
        orderbook = api.get_orderbook(ticker)

        # Enrich the market dictionary
        market_details["contracts"] = contracts
        market_details["orderbook"] = orderbook

        os.makedirs("data", exist_ok=True)
        file_path = f"data/market_{ticker}.json"
        with open(file_path, "w") as f:
            json.dump(market_details, f, indent=2)

        print(f"✅ Saved market data to {file_path}")

    except Exception as e:
        print(f"❌ Error fetching market {ticker}: {e}")

if __name__ == "__main__":
    TICKER = "KXHIGHNY-25JUL27-B83.5"  
    download_market_data(TICKER)
