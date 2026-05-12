import requests

def get_top_21_assets():
    # Only the 21 coins you requested
    return ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'SHIB', 'DOT', 'LINK', 'UNI', 'LTC', 'AVAX', 'SUI', 'ONDO', 'HYPE', 'BGB', 'ASTER', 'ZEC', 'XPL', 'BONE']

def analyze_market_cap(key):
    # Groq Logic to analyze overall market health
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': key}
    try:
        r = requests.get(url, headers=headers)
        return r.json()['data'] if r.status_code == 200 else None
    except: return None
