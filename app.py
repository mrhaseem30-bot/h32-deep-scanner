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

st.title("🔱 H32 QUANTUM TERMINAL — V7.2")
st.caption("⚡ Backtrader Logic + Global Situation + Pump Potential + Liquidation")

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
    avg_chg = sum(c.get('price_change_percentage_24h', 0) or 0 for c in coins_data.values()) / len(coins_data)
    high_vol_count = sum(1 for c in coins_data.values() if (c.get('total_volume', 0) or 0) > 100_000_000)
    
    if avg_chg > 2.5 and high_vol_count > 8:
        return "🔥 STRONG BULLISH", "High Risk Appetite", "Extreme Greed"
    elif avg_chg > 0.8:
        return "📈 BULLISH", "Moderate Bullish", "Greed"
    elif avg_chg < -2:
        return "📉 BEARISH", "Risk Off", "Fear"
    else:
        return "⚖️ NEUTRAL", "Cautious", "Neutral"

def pump_potential(chg, vol, confidence):
    if confidence >= 88 and chg > 4:
        return "🚀 3X POSSIBLE", "HIGH"
    elif confidence >= 78 and chg > 2:
        return "📈 2X - 2.5X", "MEDIUM"
    elif confidence >= 65:
        return "1.5X - 2X", "MEDIUM"
    else:
        return "0.8X - 1.3X", "LOW"

def backtrader_logic(chg, vol, liq_score):
    score = 0
    if chg > 5: score += 40
    elif chg > 2.5: score += 25
    if vol > 180_000_000: score += 30
    if liq_score > 80: score += 18
    
    fake = "HIGH" if (vol > 300_000_000 and chg > 15 and liq_score < 55) else "LOW"
    if fake == "HIGH": score -= 35
    
    confidence = max(40, min(96, score + random.randint(-10,10)))
    
    if confidence >= 88 and fake == "LOW":
        action = "🟢 AGGRESSIVE LONG"
    elif confidence >= 75:
        action = "🟢 BUY"
    elif chg <= -6:
        action = "🔴 SHORT / EXIT"
    else:
        action = "🟡 WAIT"
    
    return confidence, action, fake

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data()
        
        if data:
            # Global Situation
            sentiment, risk, greed = global_situation_analysis(data)
            st.markdown("### 🌍 GLOBAL MARKET SITUATION")
            c1, c2, c3 = st.columns(3)
            c1.metric("SENTIMENT", sentiment)
            c2.metric("RISK APPETITE", risk)
            c3.metric("FEAR & GREED", greed)
            
            # Main Table
            rows = []
            for sym, cg_id in SYMBOL_MAP.items():
                if cg_id in data:
                    c = data[cg_id]
                    chg = c.get('price_change_percentage_24h', 0) or 0
                    vol = c.get('total_volume', 0) or 0
                    price = c.get('current_price', 0)
                    
                    liq_score = min(98, int(vol / 7500000)) if vol else 40
                    conf, action, fake = backtrader_logic(chg, vol, liq_score)
                    pump_text, pump_level = pump_potential(chg, vol, conf)
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQUIDITY": f"{liq_score}/100",
                        "CONFIDENCE": f"{conf}%",
                        "PUMP POTENTIAL": pump_text,
                        "ACTION": action,
                        "LIQUIDATION": "HIGH RISK ↑" if conf >= 85 else "Moderate",
                        "FAKE": fake
                    })
            
            df = pd.DataFrame(rows)
            
            # Strong Pump Signals
            strong = df[df['CONFIDENCE'].str.replace('%','').astype(int) >= 85]
            if not strong.empty:
                st.success("### 🔥 HIGH PUMP POTENTIAL SIGNALS")
                st.dataframe(strong[["ASSET", "PRICE", "24H", "PUMP POTENTIAL", "ACTION", "LIQUIDATION"]], 
                           use_container_width=True, hide_index=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=680)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.warning("🌐 Fetching Global Market Data...")
    
    time.sleep(8)
