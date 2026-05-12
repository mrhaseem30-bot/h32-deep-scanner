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
    .strong-buy {color: #00ff88; font-weight: bold;}
    .urgent-sell {color: #ff3366; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V10.2")
st.caption("⚡ Clean • Fast • Pro TradingView Style Analysis")

SYMBOLS = ['BTC','ETH','SOL','BNB','XRP','ADA','DOGE','SHIB','DOT','LINK','UNI','LTC','AVAX','SUI','ONDO','HYPE','BGB','ZEC','XPL','BONE']

@st.cache_data(ttl=6)
def get_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=6)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return {}

placeholder = st.empty()

while True:
    with placeholder.container():
        data = get_data() or {}
        
        rows = []
        strong_buy = []
        urgent_sell = []
        
        for sym in SYMBOLS:
            if sym in data:
                d = data[sym]
                chg = float(d['priceChangePercent'])
                vol = float(d['quoteVolume'])
                price = float(d['lastPrice'])
                
                liq = min(98, int(vol / 8000000))
                conf = max(42, min(96, int(48 + chg*4.5 + vol/12000000 + liq/3)))
                
                if chg <= -6.5:
                    action = "🔴 URGENT SELL"
                    outlook = "Strong Down Pressure"
                    urgent_sell.append(f"**{sym}** → Urgent Sell ({chg:+.2f}%)")
                elif conf >= 86 and chg > 3:
                    action = "🟢 AGGRESSIVE BUY"
                    outlook = "🚀 2-3 Ghante Strong Pump"
                    strong_buy.append(f"**{sym}** → Strong Pump ({conf}%)")
                elif conf >= 73:
                    action = "🟢 BUY"
                    outlook = "Good Upside Expected"
                else:
                    action = "🟡 MONITOR"
                    outlook = "Sideways Accumulation"
                
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
        
        # Top Signals
        if urgent_sell:
            st.error("### ⚠️ URGENT SELL ALERTS")
            for alert in urgent_sell[:6]:
                st.markdown(alert)
        
        if strong_buy:
            st.success("### 🚀 STRONG BUY SIGNALS")
            for signal in strong_buy[:8]:
                st.markdown(signal)
        
        # Main Clean Table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=680
        )
        
        st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')} | Refreshing every 6s")
    
    time.sleep(6)
