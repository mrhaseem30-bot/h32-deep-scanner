import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import random

st.set_page_config(page_title="H32 QUANTUM TERMINAL", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    .main {background-color: #000000; color: #00ffcc;}
    th {color: #00ffcc !important; background: #111;}
    .buy {color: #00ff88; font-weight: bold;}
    .sell {color: #ff3366; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V9.3")
st.caption("⚡ Ultra Fast Version • Pro Logic")

# Fast Cache
@st.cache_data(ttl=5)
def get_market_data():
    try:
        # Binance - Fastest
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=6)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return {}

SYMBOLS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'SHIB', 'DOT', 'LINK', 
           'UNI', 'LTC', 'AVAX', 'SUI', 'ONDO', 'HYPE', 'BGB', 'ZEC', 'XPL', 'BONE']

data = get_market_data()

placeholder = st.empty()

while True:
    with placeholder.container():
        if data:
            rows = []
            strong = []
            
            for sym in SYMBOLS:
                if sym in data:
                    d = data[sym]
                    chg = float(d['priceChangePercent'])
                    vol = float(d['quoteVolume'])
                    price = float(d['lastPrice'])
                    
                    liq = min(98, int(vol / 8000000))
                    conf = min(96, 45 + int(chg*5) + int(vol/12000000) + liq//3)
                    
                    if chg <= -7:
                        action = "🔴 URGENT SELL"
                        outlook = "⚠️ Strong Down Move"
                    elif conf >= 85 and chg > 3:
                        action = "🟢 AGGRESSIVE BUY"
                        outlook = "🚀 2-3 Ghante Upar"
                        strong.append(f"**{sym}** → {outlook} ({conf}%)")
                    elif conf >= 72:
                        action = "🟢 BUY"
                        outlook = "📈 Good Move Expected"
                    else:
                        action = "🟡 MONITOR"
                        outlook = "Sideways"
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQ": f"{liq}/100",
                        "CONF": f"{conf}%",
                        "OUTLOOK": outlook,
                        "ACTION": action
                    })
            
            df = pd.DataFrame(rows)
            
            st.success("### 🌍 MARKET MOMENTUM BUILDING")
            
            if strong:
                st.success("### 🔥 HIGH PROFIT SIGNALS")
                for s in strong[:8]:
                    st.markdown(s)
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=720)
            
            st.success(f"✅ Fast Update: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.warning("Data loading... Please wait")
    
    time.sleep(6)
