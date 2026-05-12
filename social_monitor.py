def get_hype_score(symbol):
    """Scan Social Media Sentiment for the 21 Coins"""
    # Yahan Mistral AI ki logic use hogi news analyze karne ke liye
    hypes = {
        "BTC": "🏦 FED Decision Hype - High",
        "DOGE": "📱 TikTok Viral Trend - Extreme",
        "SOL": "🚀 Ecosystem Growth News - Strong"
    }
    return hypes.get(symbol, "⚖️ Normal Social Interest")
