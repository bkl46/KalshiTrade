import json
from kalshi_api import KalshiAPI

KEYWORDS = ["CPI", "inflation", "consumer price", "core CPI"]

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
        print(f"Error fetching contracts/orderbook for {ticker}: {e}")
    return market

def save_to_file(markets, filename="data/cpi_markets.json"):
    with open(filename, "w") as f:
        json.dump(markets, f, indent=2)
    print(f"Saved {len(markets)} CPI markets to {filename}")

def main():
    api = KalshiAPI()
    print("Fetching all markets...")
    all_markets = api.get_all_markets()

    print("Filtering CPI-related markets...")
    cpi_markets = filter_markets_by_keywords(all_markets, KEYWORDS)

    print(f"Found {len(cpi_markets)} CPI markets. Enriching...")
    enriched = [enrich_market_data(api, m) for m in cpi_markets]

    save_to_file(enriched)

if __name__ == "__main__":
    main()
