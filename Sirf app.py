import streamlit as st
import asyncio, aiohttp, time, pandas as pd

# --- REFRESH THESE KEYS (Nayi Keys Generate Karein) ---
CMC_KEY = '767c7cda-2859-417f-9415-6e3b10642c60' # Isay check karein
ARKHAM_KEY = '1b87c73f-6b44-4871-b857-bed5e17b676c' # Isay check karein

FAV_COINS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'SHIB', 'DOT', 'LINK', 'UNI', 'LTC', 'AVAX', 'SUI', 'ONDO', 'HYPE', 'BGB', 'ASTER', 'ZEC', 'XPL', 'BONE']

st.set_page_config(page_title="H32 FINAL RESOLUTION", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    div[data-testid="stTable"] { background-color: #050505; border: 1px solid #1a1a1a; }
    th { color: #00ffcc !important; background-color: #111 !important; }
    td { font-size: 16px; color: white; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 H32 ARKHAM-OVERLORD: THE 401 RESOLUTION")
st.write("Engine Status: **Checking Key Authorization...**")

placeholder = st.empty()

async def fetch_validated_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY, 'Accept': 'application/json'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params={'symbol': ",".join(FAV_COINS)}, headers=headers) as r:
                if r.status == 200:
                    res = await r.json()
                    return res.get('data', {}), "🟢 Key Active"
                elif r.status == 401:
                    return {}, "🔴 Key Blocked (Status 401)"
                else:
                    return {}, f"⚠️ Error {r.status}"
        except:
            return {}, "❌ Connection Failed"

def trader_brain(q):
    p_1h = q.get('percent_change_1h', 0)
    vol_24h = q.get('volume_24h', 0)
    # Institutional Logic
    liq = f"🐋 ${(vol_24h * 0.25) / 1e6:.2f}M"
    if p_1h >= 2.8: return "🚀 PUMP ALERT", "🟢 BUY", liq
    elif p_1h <= -2.8: return "📉 DUMP ALERT", "🔴 SELL", liq
    else: return "⚖️ ACCUMULATION", "🟡 WAIT", liq

async def main_loop():
    while True:
        data, status_msg = await fetch_validated_data()
        rows = []
        
        for sym in FAV_COINS:
            p, intel, act, liq = "---", "Calculating...", "WAIT", "$0.00M"
            if sym in data:
                usd = data[sym]['quote']['USD']
                p = f"${usd['price']:.4f}"
                intel, act, liq = trader_brain(usd)
            
            rows.append({"ASSET": sym, "PRICE": p, "LIQUIDITY": liq, "WHALE ANALYSIS": intel, "DECISION": act})

        df = pd.DataFrame(rows)
        with placeholder.container():
            st.warning(f"System Check: {status_msg}")
            st.table(df)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main_loop())
