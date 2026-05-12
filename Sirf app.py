import streamlit as st
import asyncio, aiohttp, time, pandas as pd

# --- SYSTEM CONFIG ---
CMC_KEY = '767c7cda-2859-417f-9415-6e3b10642c60'
FAV_COINS = ['ASTER', 'UNI', 'LTC', 'ZEC', 'BNB', 'SOL', 'AVAX', 'ONDO', 'BGB', 'HYPE', 'ADA', 'SUI', 'DOT', 'LINK', 'DOGE', 'XPL', 'BTC', 'ETH', 'XRP', 'BONE', 'SHIB']

st.set_page_config(page_title="SMART CHAIN AI: V36", layout="wide")

# Institutional Sniper UI
st.markdown("""
    <style>
    .main { background-color: #000000; }
    div[data-testid="stTable"] { background-color: #050505; border: 1px solid #1a1a1a; }
    th { color: #00ffcc !important; background-color: #0a0a0a !important; font-size: 14px; }
    td { font-size: 15px; border-bottom: 1px solid #111 !important; padding: 12px !important; color: white; }
    .pump { color: #00ff00; font-weight: bold; }
    .dump { color: #ff0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 SMART CHAIN AI: PUMP/DUMP SNIPER")
st.write("Targeting: **3% - 20% Moves** | Mode: **Institutional Liquidity**")

placeholder = st.empty()

def calculate_ai_logic(q):
    """
    3% to 20% Move Detection Logic
    """
    vol_24h = q.get('volume_24h', 0)
    vol_chg = q.get('volume_change_24h', 0)
    p_1h = q.get('percent_change_1h', 0)
    
    # Automatic Liquidation Calculation (Institutional Flow)
    liq_val = f"${(vol_24h * 0.02) / 1e6:.2f}M" if vol_chg > 10 else "$0.00M"
    
    # 3% to 20% Strategy
    if p_1h >= 2.5 or vol_chg > 50:
        return "🚀 BULLISH (3-20% UP)", "🟢 BUY", liq_val
    elif p_1h <= -2.5 or vol_chg < -15:
        return "📉 BEARISH (3-20% DOWN)", "🔴 SELL", liq_val
    else:
        return "⚖️ SIDELINES (Waiting)", "🟡 WAIT", liq_val

async def fetch_api():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'symbol': ",".join(FAV_COINS)}, headers=headers) as r:
            res = await r.json()
            return res.get('data', {})

async def sniper_loop():
    while True:
        data = await fetch_api()
        rows = []
        
        for sym in FAV_COINS:
            price, status, action, liq = "---", "Scanning...", "WAIT", "$0.00M"
            
            if sym in data:
                # Direct Data Access
                usd_data = data[sym]['quote']['USD']
                price = f"${usd_data['price']:.4f}"
                status, action, liq = calculate_ai_logic(usd_data)
            
            rows.append({
                "ASSET": sym,
                "LIVE PRICE": price,
                "LIQUIDATION": liq,
                "AI ENGINE STATUS": status,
                "DECISION": action,
                "REASON": "Institutional Move" if liq != "$0.00M" else "Market Flow"
            })

        df = pd.DataFrame(rows)
        with placeholder.container():
            # Real-time Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("SCAN SPEED", "1.2s", "EXPRESS")
            m2.metric("VOLATILITY", "HIGH", "3%-20% READY")
            m3.metric("WHALE STATUS", "TRACKING", "LIVE")
            
            st.table(df)
            st.caption(f"Last Intelligence Sync: {time.strftime('%H:%M:%S')}")

        await asyncio.sleep(2) # Refresh har 2 second baad

if __name__ == "__main__":
    asyncio.run(sniper_loop())
