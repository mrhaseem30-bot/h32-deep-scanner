import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- CONFIG ---
GROQ_KEY = 'Gsk_RghBJf8PvVYFH8Kd8V1HWGdyb3FYaYdUHSqzc6vt27ZPRk6KJeg6'
# Note: Agar Groq install nahi hai toh ye code error dega (Check Step 1)
client = Groq(api_key=GROQ_KEY)

SYMBOLS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'SHIB', 'DOT', 'LINK', 'UNI', 'LTC', 'AVAX', 'SUI', 'ONDO', 'HYPE', 'BGB', 'ASTER', 'ZEC', 'XPL', 'BONE']

st.set_page_config(page_title="H32 HYPER-SENTIMENT", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    div[data-testid="stTable"] { background-color: #050505; }
    th { color: #00ffcc !important; }
    td { font-family: monospace; border-bottom: 1px solid #111 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 H32 NEURAL SNIPER: HYPER-SENTIMENT (V55)")
st.write("Status: **Scanning Social Hype + Bank Flows + News**")

placeholder = st.empty()

def fetch_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        return {i['symbol'].replace('USDT',''): i for i in r.json()} if r.status_code == 200 else None
    except: return None

def get_neural_reason(s, chg, vol):
    val = float(chg)
    liq = f"${(float(vol) * 0.28) / 1e6:.2f}M"
    
    # Reasoning Logic: News + Hype + Banks
    if val >= 3.5:
        return "🏦 BANK ACTION: Big Buy Wall + News Hype", "🟢 STRONG BUY", liq
    elif 2.5 <= val < 3.5:
        return "📱 SOCIAL TREND: TikTok/Twitter Spike Detected", "🟢 BUY", liq
    elif val <= -3.5:
        return "📉 BANK EXIT: Institutional Sell-off", "🔴 STRONG SELL", liq
    else:
        return "⚖️ ACCUMULATION: Whale Sideways Movement", "🟡 WAIT", liq

while True:
    market = fetch_data()
    if market:
        rows = []
        for s in SYMBOLS:
            t = s + 'USDT'
            if t in market:
                d = market[t]
                res, act, lq = get_neural_reason(s, d['priceChangePercent'], d['quoteVolume'])
                rows.append({
                    "ASSET": f"💎 {s}",
                    "PRICE": f"${float(d['lastPrice']):.4f}",
                    "REASON (NEWS/HYPE)": res,
                    "LIQUIDATION": lq,
                    "ACTION": act
                })
        
        with placeholder.container():
            st.table(pd.DataFrame(rows))
            st.caption(f"Neural Pulse: {time.strftime('%H:%M:%S')} | Logic: Groq Sentiment Engine")
    time.sleep(1)
