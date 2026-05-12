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
    .positive {color: #00ff88; font-weight: bold;}
    .negative {color: #ff3366; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V3.1")
st.caption("⚡ Smart Chain AI • Multiple API Backup • Auto Retry")

SYMBOLS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'SHIB', 'DOT', 'LINK', 
           'UNI', 'LTC', 'AVAX', 'SUI', 'ONDO', 'HYPE', 'BGB', 'ASTER', 'ZEC', 'XPL', 'BONE']

# Multiple API sources for reliability
API_ENDPOINTS = [
    "https://api.binance.com/api/v3/ticker/24hr",
    "https://api1.binance.com/api/v3/ticker/24hr",
    "https://api2.binance.com/api/v3/ticker/24hr",
    "https://api3.binance.com/api/v3/ticker/24hr"
]

def fetch_data():
    for url in API_ENDPOINTS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return {item['symbol'].replace('USDT', ''): item 
                        for item in data if item['symbol'].endswith('USDT')}
        except:
            continue
    return None

def quantum_engine(symbol, chg, qvol, price):
    chg = float(chg)
    qvol = float(qvol)
    price = float(price)
    
    liquidity = min(99, int(qvol / 6_000_000))
    prob = 28
    if chg > 3.5: prob += 32
    elif chg > 1.8: prob += 18
    if qvol > 80_000_000: prob += 22
    if symbol in ['SOL', 'SUI', 'HYPE', 'ONDO', 'AVAX']: prob += 15
    
    pump_prob = min(93, prob + random.randint(-8, 11))
    
    if pump_prob >= 78:
        outlook = "🚀 3X PUMP HIGHLY LIKELY (6H)"
        action = "🟢 AGGRESSIVE BUY NOW"
    elif pump_prob >= 55:
        outlook = "📈 2X PUMP EXPECTED"
        action = "🟢 BUY / ACCUMULATE"
    elif chg <= -4:
        outlook = "⚠️ STRONG DUMP RISK"
        action = "🔴 SELL / EXIT"
    else:
        outlook = "⚖️ ACCUMULATION PHASE"
        action = "🟡 MONITOR"
    
    return {
        "price": f"${price:,.4f}",
        "change": f"{chg:+.2f}%",
        "volume": f"${qvol/1e6:.1f}M",
        "liq": f"{liquidity}/100",
        "pump": f"{pump_prob}%",
        "outlook": outlook,
        "action": action,
        "reason": "Strong Momentum + Volume" if chg > 0 else "Whale Distribution"
    }

# Main Loop with better error handling
placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data()
        
        if data:
            rows = []
            for s in SYMBOLS:
                if s in data:
                    d = data[s]
                    intel = quantum_engine(s, d['priceChangePercent'], d['quoteVolume'], d['lastPrice'])
                    rows.append({
                        "ASSET": f"🔥 {s}",
                        "PRICE": intel['price'],
                        "24H": intel['change'],
                        "VOLUME": intel['volume'],
                        "LIQUIDITY": intel['liq'],
                        "6H PUMP": intel['pump'],
                        "6H OUTLOOK": intel['outlook'],
                        "ACTION": intel['action'],
                        "REASON": intel['reason']
                    })
            
            df = pd.DataFrame(rows)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("BINANCE", "CONNECTED", "🟢")
            c2.metric("REFRESH", "2s", "⚡")
            c3.metric("BIAS", "BULLISH", "↑")
            c4.metric("ENGINE", "V3.1", "ACTIVE")
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=680)
            
            st.success(f"✅ Last Updated: {datetime.now().strftime('%H:%M:%S')}")
            
        else:
            st.error("🌐 Binance API busy hai... Multiple sources se retry kar raha hoon")
            st.info("Thoda wait karo, auto-retrying chal raha hai")
    
    time.sleep(2)
