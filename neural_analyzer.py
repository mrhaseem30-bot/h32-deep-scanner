def get_neural_reason(change, volume):
    val = float(change)
    # Logic: Banks vs Hype vs News
    if val >= 3.0: return "🏦 BANK ENTRY: Institutional News + Hype"
    elif 1.5 <= val < 3.0: return "📱 SOCIAL TREND: Viral X/TikTok Activity"
    elif val <= -3.0: return "📉 BANK EXIT: Whale Sell-off / FUD"
    else: return "⚖️ NEUTRAL: Whale Accumulation"
