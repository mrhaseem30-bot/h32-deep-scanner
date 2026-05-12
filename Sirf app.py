import streamlit as st
import asyncio
import aiohttp
import time
import requests

# --- CONFIGURATION ---
CMC_KEY = '767c7cda-2859-417f-9415-6e3b10642c60'
GROQ_KEY = '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'

# Aapki Favorites List (From Screenshot)
FAV_COINS = ['ASTER', 'UNI', 'LTC', 'ZEC', 'BNB', 'SOL', 'AVAX', 'ONDO', 'BGB', 'HYPE', 'ADA', 'SUI', 'DOT', 'LINK', 'DOGE', 'XPL', 'BTC', 'ETH', 'XRP']

st.set_page_config(page_title="H32 X200 Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stMetric { background: #111; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    .signal-box { border-left: 5px solid #00ff00; background: #0a0a0a; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 H32 X200 HYPER-DRIVE DASHBOARD")
st.write("Target: **21 Elite Coins** | Speed: **Mili-seconds** | Accuracy: **X200 AI**")

placeholder = st.empty()

async def get_ai_prediction(sym, data):
    prompt = f"Predict {sym} 1h lead. Data: {data}. Confirm pump, target, and duration. Reply: CONFIRMED | Target: X | Duration: Y."
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mixtral-8x7b-32768", "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers) as r:
                res = await r.json()
                return res['choices'][0]['message']['content'].upper()
    except: return "SCANNING..."

async def main():
    while True:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'symbol': ",".join(FAV_COINS)}, headers=headers) as r:
                res = await r.json()
                data = res.get('data', {})
                
                with placeholder.container():
                    c1, c2, c3 = st.columns(3)
                    c1.metric("System Speed", f"{(time.time()-start_time):.3f}s")
                    c2.metric("Scan Mode", "X200 Parallel")
                    c3.metric("Lead Time", "60 Mins Advance")

                    st.subheader("🎯 Live Sniper Signals")
                    for sym in FAV_COINS:
                        if sym in data:
                            q = data[sym]['quote']['USD']
                            if abs(q['percent_change_1h']) > 0.05:
                                pred = await get_ai_prediction(sym, q['price'])
                                st.markdown(f"""
                                <div class="signal-box">
                                    <h3 style='margin:0;'>💎 {sym} | Price: ${q['price']:.4f}</h3>
                                    <p style='color:#00ff00;'>🚀 <b>AI Forecast:</b> {pred}</p>
                                    <small>Vol: {q['volume_change_24h']:.1f}% | 1h Change: {q['percent_change_1h']:+.2f}%</small>
                                </div>
                                """, unsafe_allow_html=True)
        await asyncio.sleep(2) # Refresh every 2 seconds

if __name__ == "__main__":
    try: asyncio.run(main())
    except: pass
