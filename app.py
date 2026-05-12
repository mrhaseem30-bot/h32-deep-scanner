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
    th {color: #00ffcc !important; background: #111111;}
    .sell-alert {background-color: #2a0000; color: #ff3366; padding: 10px; border-radius: 8px;}
    .buy-signal {background-color: #001a00; color: #00ff88; padding: 10px; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V10.1")
st.caption("⚡ Clean • Only 2 Important Sections • Fast")

SYMBOLS = ['BTC','ETH','SOL','BNB','XRP','ADA','DOGE','SHIB','DOT','LINK','UNI','LTC','AVAX','SUI','ONDO','HYPE','BGB','ZEC','XPL','BONE']

@st.cache_data(ttl=6)
def get_data():
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
        data = get_data() or {}
        
        rows = []
        urgent_sell = []
        strong_buy = []
        
        for sym in SYMBOLS:
            if sym in data:
                d = data[sym]
                chg = float(d['priceChangePercent'])
                vol = float(d['quoteVolume'])
                price = float(d['lastPrice'])
                
                liq = min(98, int(vol / 8000000))
                conf = max(40, min(96, int(45 + chg*4.8 + vol/13000000 + liq/3)))
                
                if chg <= -6:
                    action = "🔴 URGENT SELL"
                    outlook = "Strong Down Pressure"
                    urgent_sell.append(f"**{sym}** → Urgent Sell ({chg:+.2f}%)")
                elif conf >= 85 and chg > 2.5:
                    action = "🟢 AGGRESSIVE BUY"
                    outlook = "🚀 2-3 Ghante Strong Pump"
                    strong_buy.append(f"**{sym}** → Strong Pump ({conf}%)")
                elif conf >= 72:
                    action = "🟢 BUY"
                    outlook = "Good Upside"
                else:
                    action = "🟡 MONITOR"
                    outlook = "Sideways"
                
                rows.append({
                    "ASSET": f"🔥 {sym}",
                    "PRICE": f"${price:,.4f}",
                    "24H": f"{chg:+.2f}%",
                    "VOLUME": f"${vol/1e6:.1f}M",
                    "CONFIDENCE": f"{conf}%",
                    "OUTLOOK": outlook,
                    "ACTION": action
                })
        
        df = pd.DataFrame(rows)
        
        # ================== TWO MAIN SECTIONS ==================
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("### ⚠️ URGENT SELL ALERTS")
            if urgent_sell:
                for alert in urgent_sell[:8]:
                    st.markdown(f"<div class='sell-alert'>{alert}</div>", unsafe_allow_html=True)
            else:
                st.success("No Urgent Sell right now")
        
        with col2:
            st.success("### 🚀 STRONG BUY SIGNALS")
            if strong_buy:
                for signal in strong_buy[:8]:
                    st.markdown(f"<div class='buy-signal'>{signal}</div>", unsafe_allow_html=True)
            else:
                st.info("Waiting for strong momentum...")
        
        # Main Table
        st.dataframe(df, use_container_width=True, hide_index=True, height=650)
        
        st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    time.sleep(7)
