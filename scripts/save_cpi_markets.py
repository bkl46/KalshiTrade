# scripts/filter_markets.py

import json
from kalshi_api import KalshiAPI

FILTER_KEYWORDS = ["ECB", "interest", "rate", "Sep", "2025", "temperature", "weather"]

def filter_markets_by_keywords(markets, keywords):
    def contains_keyword(text):
        return any(kw.lower() in text.lower() for kw in keywords)

    filtered = []
    for market in markets:
        if contains_keyword(market.get("title", "")) or contains_keyword(market.get("event_ticker", "")):
            filtered.append(market)
    return filtered

def enrich_market_data(api, market):
    ticker = market["ticker"]
    try:
        contracts = api.get_contracts(ticker)
        orderbook = api.get_orderbook(ticker)
        market["contracts"] = contracts
        market["orderbook"] = orderbook
    except Exception as e:
        print(f"Error enriching {ticker}: {e}")
    return market

def save_to_file(markets, filename="data/filtered_markets.json"):
    with open(filename, "w") as f:
        json.dump(markets, f, indent=2)
    print(f" Saved {len(markets)} markets to {filename}")

def main():
    api = KalshiAPI()
    print(" Fetching all markets...")
    all_markets = api.get_all_markets()

    print(" Filtering markets by keywords:", FILTER_KEYWORDS)
    filtered_markets = filter_markets_by_keywords(all_markets, FILTER_KEYWORDS)

    print(f" Enriching {len(filtered_markets)} markets with contract/orderbook data...")
    enriched = [enrich_market_data(api, m) for m in filtered_markets]

    save_to_file(enriched)

if __name__ == "__main__":
    main()
