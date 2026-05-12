import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import random

st.set_page_config(page_title="H32 QUANTUM TERMINAL", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    .main {background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace;}
    th {color: #00ffcc !important; background: #111111; text-transform: uppercase;}
    .high-confidence {color: #00ff88; font-weight: bold;}
    .fake-pump {color: #ffaa00; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V4.0")
st.caption("⚡ Fake Pump Detector + 100 IQ Confidence Score + Enhanced Profile")

SYMBOLS = ['BTC','ETH','SOL','BNB','XRP','ADA','DOGE','SHIB','DOT','LINK','UNI','LTC',
           'AVAX','SUI','ONDO','HYPE','BGB','ZEC','XPL','BONE']

SYMBOL_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 'BNB': 'binancecoin',
    'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu',
    'DOT': 'polkadot', 'LINK': 'chainlink', 'UNI': 'uniswap', 'LTC': 'litecoin',
    'AVAX': 'avalanche-2', 'SUI': 'sui', 'ONDO': 'ondo-finance', 'HYPE': 'hyperliquid',
    'BGB': 'bitget-token', 'ZEC': 'zcash', 'XPL': 'xpla', 'BONE': 'bone-shibaswap'
}

def fetch_coingecko_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 250, 'page': 1}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return {coin['id']: coin for coin in r.json()}
    except:
        return None

def advanced_quantum_analysis(coin, symbol):
    chg_24h = coin.get('price_change_percentage_24h', 0) or 0
    volume = coin.get('total_volume', 0) or 0
    price = coin.get('current_price', 0)
    mcap = coin.get('market_cap', 0) or 0
    
    # Liquidity Score
    liquidity = min(99, int(volume / 7_000_000)) if volume else 45
    
    # Fake Pump Detector (100 IQ)
    fake_pump_risk = "LOW"
    if volume > 150_000_000 and chg_24h > 8 and liquidity < 65:
        fake_pump_risk = "HIGH ⚠️"
    elif volume > 80_000_000 and chg_24h > 12:
        fake_pump_risk = "MEDIUM"
    
    # Bullish Confidence Score (0-100)
    confidence = 40
    if chg_24h > 3: confidence += 25
    if chg_24h > 6: confidence += 20
    if volume > 100_000_000: confidence += 18
    if liquidity > 70: confidence += 12
    if symbol in ['SOL', 'SUI', 'HYPE', 'ONDO']: confidence += 10
    confidence = min(98, confidence + random.randint(-8, 8))
    
    # Final Action
    if confidence >= 82 and fake_pump_risk == "LOW":
        action = "🟢 AGGRESSIVE BUY (STRONG)"
        outlook = "🚀 HIGH PROBABILITY UPAR MOVE"
    elif confidence >= 65:
        action = "🟢 BUY / ACCUMULATE"
        outlook = "📈 2X-3X POTENTIAL"
    elif chg_24h <= -5:
        action = "🔴 SELL / EXIT"
        outlook = "⚠️ DOWNWARD PRESSURE"
    else:
        action = "🟡 MONITOR"
        outlook = "⚖️ ACCUMULATION PHASE"
    
    return {
        "price": f"\( {price:,.4f}" if price else " \)--",
        "change": f"{chg_24h:+.2f}%",
        "volume": f"${volume/1e6:.1f}M",
        "liq": f"{liquidity}/100",
        "confidence": f"{confidence}%",
        "fake_risk": fake_pump_risk,
        "action": action,
        "outlook": outlook,
        "mcap": f"${mcap/1e9:.2f}B" if mcap else "--"
    }

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_coingecko_data()
        
        if data:
            rows = []
            for sym in SYMBOLS:
                cg_id = SYMBOL_MAP.get(sym)
                if cg_id and cg_id in data:
                    intel = advanced_quantum_analysis(data[cg_id], sym)
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": intel['price'],
                        "24H": intel['change'],
                        "VOLUME": intel['volume'],
                        "LIQUIDITY": intel['liq'],
                        "CONFIDENCE": intel['confidence'],
                        "FAKE PUMP": intel['fake_risk'],
                        "6H OUTLOOK": intel['outlook'],
                        "ACTION": intel['action'],
                        "MCAP": intel['mcap']
                    })
            
            df = pd.DataFrame(rows)
            
            # Top Bar
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("API STATUS", "COINGECKO LIVE", "🟢")
            c2.metric("FAKE PUMP FILTER", "ACTIVE", "🛡️")
            c3.metric("CONFIDENCE ENGINE", "100 IQ", "🔥")
            c4.metric("VERSION", "V4.0", "ENHANCED")
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=720
            )
            
            st.success(f"✅ Last Updated: {datetime.now().strftime('%H:%M:%S')} | Auto-refresh every 3s")
            
        else:
            st.error("API busy... Retrying")
    
    time.sleep(3)
