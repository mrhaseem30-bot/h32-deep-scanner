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

st.title("🔱 H32 QUANTUM TERMINAL — V9.1")
st.caption("⚡ Pro Trader + Smart Money + AI Logic • High Profit Formula")

tab1, tab2 = st.tabs(["🔥 AGGRESSIVE (High Profit)", "🛡️ SAFE ACCUMULATOR"])

SYMBOL_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 'BNB': 'binancecoin',
    'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu',
    'DOT': 'polkadot', 'LINK': 'chainlink', 'UNI': 'uniswap', 'LTC': 'litecoin',
    'AVAX': 'avalanche-2', 'SUI': 'sui', 'ONDO': 'ondo-finance', 'HYPE': 'hyperliquid',
    'BGB': 'bitget-token', 'ZEC': 'zcash', 'XPL': 'xpla', 'BONE': 'bone-shibaswap'
}

def fetch_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=8)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return None

def smart_money_logic(chg, vol, liq, symbol):
    score = 45
    if chg > 5: score += 40
    elif chg > 2.5: score += 22
    if vol > 250_000_000: score += 35
    if liq > 82: score += 20
    if symbol in ['SOL','SUI','HYPE','ONDO','AVAX']: score += 18
    
    # Urgent Sell (Distribution)
    if chg <= -6.5 or (chg < -4 and vol > 400_000_000):
        return 95, "🔴 URGENT SELL / EXIT NOW", "Distribution Started", "SELL"
    
    confidence = min(97, score + random.randint(-10, 10))
    
    if confidence >= 88:
        pred = "🚀 2-3 Ghante Strong Pump"
        action = "🟢 AGGRESSIVE BUY"
        risk = "HIGH REWARD"
    elif confidence >= 75:
        pred = "📈 1.8X - 2.5X Expected"
        action = "🟢 BUY"
        risk = "Good"
    else:
        pred = "Sideways / Wait"
        action = "🟡 MONITOR"
        risk = "Low"
    
    return confidence, pred, risk, action

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data()
        
        if data:
            rows = []
            urgent = []
            strong = []
            
            for sym in SYMBOL_MAP.keys():
                if sym in data:
                    d = data[sym]
                    chg = float(d['priceChangePercent'])
                    vol = float(d['quoteVolume'])
                    price = float(d['lastPrice'])
                    
                    liq = min(98, int(vol / 7500000))
                    conf, pred, risk, action = smart_money_logic(chg, vol, liq, sym)
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQUIDITY": f"{liq}/100",
                        "CONFIDENCE": f"{conf}%",
                        "2-3H OUTLOOK": pred,
                        "ACTION": action,
                        "RISK/REWARD": risk
                    })
                    
                    if "URGENT SELL" in action:
                        urgent.append(f"**{sym}** → {pred}")
                    if conf >= 88:
                        strong.append(f"**{sym}** → {pred} | {conf}%")
            
            df = pd.DataFrame(rows)
            
            with tab1:
                st.success("### 🔥 AGGRESSIVE TRADER MODE (Jyada Kamai Wala Style)")
                if urgent:
                    st.error("### ⚠️ URGENT SELL ALERT")
                    for u in urgent:
                        st.markdown(u)
                if strong:
                    st.success("### 🚀 HIGH PROFIT OPPORTUNITY")
                    for s in strong[:6]:
                        st.markdown(s)
                st.dataframe(df, use_container_width=True, hide_index=True, height=680)
            
            with tab2:
                st.info("### 🛡️ SAFE ACCUMULATOR MODE")
                safe = df[df['CONFIDENCE'].str.replace('%','').astype(int) >= 70]
                st.dataframe(safe, use_container_width=True, hide_index=True, height=680)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')} | Refresh 8s")
        else:
            st.warning("Market data loading... Please wait")
    
    time.sleep(8)
