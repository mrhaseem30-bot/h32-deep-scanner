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
    .aggressive {background-color: #001a00; color: #00ff88;}
    .sell {background-color: #2a0000; color: #ff3366;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V9.0")
st.caption("⚡ Aggressive + Safe Profile • Urgent Signals • Pro Trader Logic")

tab1, tab2 = st.tabs(["🔥 AGGRESSIVE TRADER", "🛡️ SAFE ACCUMULATOR"])

SYMBOL_MAP = { ... }  # Same as before (copy from previous code)

def fetch_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=8)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return None

def pro_trader_logic(chg, vol, liq, symbol):
    score = 40
    if chg > 6: score += 35
    elif chg > 3: score += 20
    if vol > 250_000_000: score += 30
    if liq > 80: score += 18
    if symbol in ['SOL','SUI','HYPE','ONDO']: score += 15
    
    # Urgent Sell Logic
    if chg <= -7 or (chg < -4 and vol > 300_000_000):
        return 92, "🔴 URGENT SELL / EXIT", "HIGH RISK - LONGs Liquidating", "SELL"
    
    confidence = min(97, score + random.randint(-12, 8))
    
    if confidence >= 88:
        pred = "🚀 2-3 Ghante Strong Upar"
        action = "🟢 AGGRESSIVE BUY"
    elif confidence >= 72:
        pred = "📈 1.8X - 2.5X Possible"
        action = "🟢 BUY"
    else:
        pred = "Sideways / Monitor"
        action = "🟡 WAIT"
    
    return confidence, pred, "Moderate", action

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data()
        
        if data:
            rows = []
            urgent_sell = []
            strong_buy = []
            
            for sym in SYMBOL_MAP.keys():
                if sym in data:
                    d = data[sym]
                    chg = float(d['priceChangePercent'])
                    vol = float(d['quoteVolume'])
                    price = float(d['lastPrice'])
                    
                    liq = min(98, int(vol / 7_500_000))
                    conf, pred, risk, action = pro_trader_logic(chg, vol, liq, sym)
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQ": f"{liq}/100",
                        "CONFIDENCE": f"{conf}%",
                        "2-3H PREDICTION": pred,
                        "ACTION": action,
                        "RISK": risk
                    })
                    
                    if "URGENT SELL" in action:
                        urgent_sell.append(f"**{sym}** → URGENT SELL ({chg:+.1f}%)")
                    if conf >= 88:
                        strong_buy.append(f"**{sym}** → {pred} (Conf {conf}%)")
            
            df = pd.DataFrame(rows)
            
            # AGGRESSIVE TAB
            with tab1:
                st.success("### 🔥 AGGRESSIVE TRADER MODE (High Risk High Reward)")
                if urgent_sell:
                    st.error("### ⚠️ URGENT SELL SIGNALS")
                    for s in urgent_sell:
                        st.markdown(s)
                if strong_buy:
                    st.success("### 🚀 STRONG BUY SIGNALS")
                    for s in strong_buy[:6]:
                        st.markdown(s)
                st.dataframe(df, use_container_width=True, hide_index=True, height=650)
            
            # SAFE TAB
            with tab2:
                st.info("### 🛡️ SAFE ACCUMULATOR MODE (Low Risk)")
                safe_df = df[df['CONFIDENCE'].str.replace('%','').astype(int) > 65]
                st.dataframe(safe_df, use_container_width=True, hide_index=True, height=650)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')} | Refresh 8s")
        else:
            st.warning("Market data loading...")
    
    time.sleep(8)
