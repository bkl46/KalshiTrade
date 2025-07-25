from kalshi_api import KalshiAPI
import json

api = KalshiAPI()
markets = api.get_all_markets()

for m in markets[:5]:
    print(f"{m['ticker']}: {m['title']} (Ends: {m['close_time']})")
    
print("**************************************************")
print(json.dumps(markets[0], indent=2))