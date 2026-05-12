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
    .strong-buy {background-color: #001a00; color: #00ff88; font-weight: bold;}
    .urgent-sell {background-color: #2a0000; color: #ff3366; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V10.0")
st.caption("⚡ Never Stop • Always Running • Pro Logic")

tab1, tab2 = st.tabs(["🔥 AGGRESSIVE HIGH PROFIT", "🛡️ SAFE ACCUMULATOR"])

SYMBOLS = ['BTC','ETH','SOL','BNB','XRP','ADA','DOGE','SHIB','DOT','LINK','UNI','LTC','AVAX','SUI','ONDO','HYPE','BGB','ZEC','XPL','BONE']

# Mock Data (Kabhi API fail ho to yeh chalega)
def get_mock_data():
    mock = {}
    for sym in SYMBOLS:
        chg = random.uniform(-9, 10)
        vol = random.uniform(40_000_000, 1200_000_000)
        price = random.uniform(0.05, 12000) if sym != 'BTC' else random.uniform(60000, 110000)
        mock[sym] = {'priceChangePercent': chg, 'quoteVolume': vol, 'lastPrice': price}
    return mock

@st.cache_data(ttl=6)
def get_real_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=6)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return None

placeholder = st.empty()

while True:
    with placeholder.container():
        real_data = get_real_data()
        data = real_data if real_data else get_mock_data()
        source = "Binance LIVE" if real_data else "🔄 FALLBACK MODE"
        
        rows = []
        strong_buy = []
        urgent_sell = []
        
        for sym in SYMBOLS:
            if sym in data:
                d = data[sym]
                chg = float(d.get('priceChangePercent', random.uniform(-8,9)))
                vol = float(d.get('quoteVolume', random.uniform(50_000_000,800_000_000)))
                price = float(d.get('lastPrice', 100))
                
                liq = min(98, int(vol / 8000000))
                conf = max(40, min(96, int(45 + chg*4.5 + vol/14000000 + liq/3.5)))
                
                if chg <= -6.5:
                    action = "🔴 URGENT SELL"
                    outlook = "Strong Down Pressure"
                    urgent_sell.append(f"**{sym}** → Urgent Sell ({chg:+.1f}%)")
                elif conf >= 86 and chg > 3:
                    action = "🟢 AGGRESSIVE BUY"
                    outlook = "🚀 2-3 Ghante Strong Pump"
                    strong_buy.append(f"**{sym}** → {outlook} ({conf}%)")
                elif conf >= 73:
                    action = "🟢 BUY"
                    outlook = "Good Upside Expected"
                else:
                    action = "🟡 MONITOR"
                    outlook = "Accumulation Phase"
                
                rows.append({
                    "ASSET": f"🔥 {sym}",
                    "PRICE": f"${price:,.4f}",
                    "24H": f"{chg:+.2f}%",
                    "VOLUME": f"${vol/1e6:.1f}M",
                    "LIQUIDITY": f"{liq}/100",
                    "CONFIDENCE": f"{conf}%",
                    "2-3H OUTLOOK": outlook,
                    "ACTION": action
                })
        
        df = pd.DataFrame(rows)
        
        with tab1:
            st.success("### 🔥 AGGRESSIVE HIGH PROFIT MODE")
            if urgent_sell:
                st.error("### ⚠️ URGENT SELL ALERTS")
                for u in urgent_sell: st.markdown(u)
            if strong_buy:
                st.success("### 🚀 STRONG BUY SIGNALS")
                for s in strong_buy[:8]: st.markdown(s)
            st.dataframe(df, use_container_width=True, hide_index=True, height=680)
        
        with tab2:
            st.info("### 🛡️ SAFE ACCUMULATOR MODE")
            safe_df = df[df['CONFIDENCE'].str.replace('%','').astype(int) >= 70]
            st.dataframe(safe_df, use_container_width=True, hide_index=True, height=680)
        
        st.success(f"✅ {source} • Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    time.sleep(6)
