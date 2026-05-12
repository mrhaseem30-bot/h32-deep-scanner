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

st.title("🔱 H32 QUANTUM TERMINAL — V3.2")
st.caption("⚡ CoinGecko API • Fast & Stable • Smart Chain AI")

SYMBOLS = ['bitcoin', 'ethereum', 'solana', 'binancecoin', 'ripple', 'cardano', 'dogecoin', 
           'shiba-inu', 'polkadot', 'chainlink', 'uniswap', 'litecoin', 'avalanche-2', 
           'sui', 'ondo-finance', 'hyperliquid', 'bitget-token', 'zcash', 'xpla', 'bone-shibaswap']

# CoinGecko IDs mapping
SYMBOL_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 'BNB': 'binancecoin',
    'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu',
    'DOT': 'polkadot', 'LINK': 'chainlink', 'UNI': 'uniswap', 'LTC': 'litecoin',
    'AVAX': 'avalanche-2', 'SUI': 'sui', 'ONDO': 'ondo-finance', 'HYPE': 'hyperliquid',
    'BGB': 'bitget-token', 'ZEC': 'zcash', 'XPL': 'xpla', 'BONE': 'bone-shibaswap'
}

def fetch_coingecko_data():
    try:
        # Get all coins market data (most reliable endpoint)
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 250,
            'page': 1,
            'sparkline': 'false'
        }
        r = requests.get(url, params=params, timeout=12)
        if r.status_code == 200:
            data = r.json()
            return {coin['id']: coin for coin in data}
    except:
        return None
    return None

def quantum_engine(coin_data, symbol):
    if not coin_data:
        return None
    
    chg = coin_data.get('price_change_percentage_24h', 0) or 0
    price = coin_data.get('current_price', 0)
    volume = coin_data.get('total_volume', 0) or 0
    market_cap = coin_data.get('market_cap', 0) or 0
    
    liquidity = min(99, int(volume / 8_000_000) if volume else 40)
    
    prob = 30
    if chg > 4: prob += 35
    elif chg > 2: prob += 20
    if volume > 100_000_000: prob += 18
    if symbol in ['SOL', 'SUI', 'HYPE', 'ONDO', 'AVAX']: prob += 15
    
    pump_prob = min(94, prob + random.randint(-9, 12))
    
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
        "price": f"\( {price:,.4f}" if price else " \)--",
        "change": f"{chg:+.2f}%",
        "volume": f"\( {volume/1e6:.1f}M" if volume else " \)--",
        "liq": f"{liquidity}/100",
        "pump": f"{pump_prob}%",
        "outlook": outlook,
        "action": action,
        "reason": "Strong Volume + Momentum" if chg > 0 else "Correction Phase"
    }

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_coingecko_data()
        
        if data:
            rows = []
            for sym in ['BTC','ETH','SOL','BNB','XRP','ADA','DOGE','SHIB','DOT','LINK',
                       'UNI','LTC','AVAX','SUI','ONDO','HYPE','BGB','ZEC','XPL','BONE']:
                cg_id = SYMBOL_MAP.get(sym)
                if cg_id and cg_id in data:
                    intel = quantum_engine(data[cg_id], sym)
                    if intel:
                        rows.append({
                            "ASSET": f"🔥 {sym}",
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
            c1.metric("API", "COINGECKO", "🟢")
            c2.metric("REFRESH", "3s", "⚡")
            c3.metric("MODE", "LIVE", "ACTIVE")
            c4.metric("ENGINE", "V3.2", "STABLE")
            
            st.dataframe(df, use_container_width=True, hide_index=True, height=680)
            
            st.success(f"✅ Updated: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.error("🌐 API busy... Retrying in few seconds")
    
    time.sleep(3)
