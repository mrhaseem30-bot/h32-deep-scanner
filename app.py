import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import random

st.set_page_config(page_title="H32 QUANTUM TERMINAL", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    .main {background-color: #0a0a0a; color: #00ffcc;}
    th {color: #00ffcc !important; background: #1a1a1a; text-transform: uppercase;}
    .green {color: #00ff88 !important; font-weight: bold;}
    .red {color: #ff3366 !important; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V7.1")
st.caption("⚡ Backtrader Logic + Global Situation + Liquidation Scanner")

# ================== SYMBOLS ==================
SYMBOL_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 'BNB': 'binancecoin',
    'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu',
    'DOT': 'polkadot', 'LINK': 'chainlink', 'UNI': 'uniswap', 'LTC': 'litecoin',
    'AVAX': 'avalanche-2', 'SUI': 'sui', 'ONDO': 'ondo-finance', 'HYPE': 'hyperliquid',
    'BGB': 'bitget-token', 'ZEC': 'zcash', 'XPL': 'xpla', 'BONE': 'bone-shibaswap'
}

@st.cache_data(ttl=8)
def fetch_data():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                         params={'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 250}, timeout=12)
        if r.status_code == 200:
            return {coin['id']: coin for coin in r.json()}
    except:
        return None

def global_situation_analysis(coins_data):
    total_chg = sum(c.get('price_change_percentage_24h', 0) or 0 for c in coins_data.values())
    avg_chg = total_chg / len(coins_data)
    high_vol = sum(1 for c in coins_data.values() if (c.get('total_volume', 0) or 0) > 100_000_000)
    
    if avg_chg > 2.5 and high_vol > 8:
        sentiment = "🔥 STRONG BULLISH"
        risk = "High Risk Appetite"
        greed = "Extreme Greed"
    elif avg_chg > 0.8:
        sentiment = "📈 BULLISH"
        risk = "Moderate Bullish"
        greed = "Greed"
    elif avg_chg < -2:
        sentiment = "📉 BEARISH"
        risk = "Risk Off"
        greed = "Fear"
    else:
        sentiment = "⚖️ NEUTRAL / ACCUMULATION"
        risk = "Cautious"
        greed = "Neutral"
    
    return sentiment, risk, greed, round(avg_chg, 2)

def backtrader_logic(chg, vol, liq_score):
    score = 0
    if chg > 4: score += 35
    elif chg > 2: score += 20
    if vol > 150_000_000: score += 30
    if liq_score > 75: score += 20
    
    if vol > 250_000_000 and chg > 12 and liq_score < 60:
        score -= 35
        fake = "HIGH"
    else:
        fake = "LOW"
    
    confidence = max(35, min(95, score + random.randint(-8,8)))
    
    if confidence >= 88 and fake == "LOW":
        action = "🟢 AGGRESSIVE LONG"
        liq = "HIGH LONG LIQUIDATION RISK ↑"
    elif confidence >= 75:
        action = "🟢 BUY"
        liq = "Moderate Liquidation"
    elif chg <= -6:
        action = "🔴 SHORT / EXIT"
        liq = "LONGs Getting Liquidated"
    else:
        action = "🟡 WAIT"
        liq = "Low Risk"
    
    return confidence, action, liq, fake

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data()
        
        if data:
            # Global Situation
            global_sentiment, risk, greed, avg_chg = global_situation_analysis(data)
            
            st.markdown(f"### 🌍 GLOBAL MARKET SITUATION")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("OVERALL SENTIMENT", global_sentiment, f"{avg_chg:+.2f}%")
            col2.metric("RISK APPETITE", risk)
            col3.metric("FEAR & GREED", greed)
            col4.metric("MARKET MODE", "CRYPTO", "LIVE")
            
            # Main Table
            rows = []
            for sym, cg_id in SYMBOL_MAP.items():
                if cg_id in data:
                    c = data[cg_id]
                    chg = c.get('price_change_percentage_24h', 0) or 0
                    vol = c.get('total_volume', 0) or 0
                    price = c.get('current_price', 0)
                    
                    liq_score = min(98, int(vol / 7_500_000)) if vol else 40
                    conf, action, liq_potential, fake = backtrader_logic(chg, vol, liq_score)
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQUIDITY": f"{liq_score}/100",
                        "CONFIDENCE": f"{conf}%",
                        "ACTION": action,
                        "LIQUIDATION": liq_potential,
                        "FAKE PUMP": fake
                    })
            
            df = pd.DataFrame(rows)
            
            # Strong Signals
            strong = [row for row in rows if int(row['CONFIDENCE'].replace('%','')) >= 85]
            if strong:
                st.success("### 🔥 BACKTRADER STRONG SIGNALS")
                st.dataframe(pd.DataFrame(strong), use_container_width=True, hide_index=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=680)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')} | Refresh 8s")
        else:
            st.warning("🌐 Fetching Global Market Data...")
    
    time.sleep(8)
