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
    .strong {background-color: #001a00; color: #00ff88; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM TERMINAL — V6.3")
st.caption("⚡ Stable Version • Realistic Signals • Rate Limit Protected")

SYMBOL_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 'BNB': 'binancecoin',
    'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu',
    'DOT': 'polkadot', 'LINK': 'chainlink', 'UNI': 'uniswap', 'LTC': 'litecoin',
    'AVAX': 'avalanche-2', 'SUI': 'sui', 'ONDO': 'ondo-finance', 'HYPE': 'hyperliquid',
    'BGB': 'bitget-token', 'ZEC': 'zcash', 'XPL': 'xpla', 'BONE': 'bone-shibaswap'
}

SYMBOLS = list(SYMBOL_MAP.keys())

@st.cache_data(ttl=10)
def fetch_coingecko_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 250}
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return {coin['id']: coin for coin in r.json()}
        else:
            st.error(f"API Error {r.status_code} - Retrying soon...")
            return None
    except:
        st.warning("🌐 Connecting to market data...")
        return None

def get_prediction(chg, confidence):
    if confidence >= 88 and chg > 3.5:
        return "🚀 1 GHANTA MARKET UPAR HI JAYEGI", "🟢 AGGRESSIVE BUY NOW"
    elif confidence >= 78 and chg > 2:
        return "📈 Strong Upar Move Expected", "🟢 BUY / ACCUMULATE"
    elif chg <= -5.5:
        return "⚠️ Downward Pressure", "🔴 SELL / EXIT"
    else:
        return "⚖️ Sideways Accumulation", "🟡 HOLD / MONITOR"

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_coingecko_data()
        
        if data:
            rows = []
            strong = []
            
            for sym in SYMBOLS:
                cg_id = SYMBOL_MAP.get(sym)
                if cg_id and cg_id in data:
                    coin = data[cg_id]
                    chg = coin.get('price_change_percentage_24h', 0) or 0
                    vol = coin.get('total_volume', 0) or 0
                    price = coin.get('current_price', 0)
                    
                    liq = min(99, int(vol / 8000000)) if vol > 0 else 45
                    confidence = max(38, min(93, int(48 + chg*3.2 + vol/11000000 + liq/5)))
                    
                    pred, action = get_prediction(chg, confidence)
                    
                    rows.append({
                        "ASSET": f"🔥 {sym}",
                        "PRICE": f"${price:,.4f}",
                        "24H": f"{chg:+.2f}%",
                        "VOLUME": f"${vol/1e6:.1f}M",
                        "LIQUIDITY": f"{liq}/100",
                        "CONFIDENCE": f"{confidence}%",
                        "1H PREDICTION": pred,
                        "ACTION": action
                    })m
                    
                    if confidence >= 85:
                        strong.append(f"**{sym}** → {pred}")
            
            df = pd.DataFrame(rows)
            
            if strong:
                st.success("### 🔥 STRONG 1H SIGNALS")
                for s in strong[:5]:
                    st.markdown(s)
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=650)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.info("Fetching market data...")
    
    time.sleep(10)
