from kalshi_api import KalshiAPI

def print_all_market_titles():
    api = KalshiAPI()
    all_markets = api.get_all_markets()

    print(f"\n🧾 Found {len(all_markets)} total markets:\n")
    for m in all_markets:
        title = m.get("title", "[no title]")
        ticker = m.get("ticker", "[no ticker]")
        print(f"- {ticker}: {title}")

if __name__ == "__main__":
    print_all_market_titles()
