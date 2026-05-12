import streamlit as st
import pandas as pd
import time
from assets_config import get_my_21_coins
from market_logic import analyze_market_cap
from neural_signals import get_neural_reason
from social_monitor import get_hype_score

st.set_page_config(page_title="H32 MODULAR QUANTUM", layout="wide")

st.markdown("<style>.main {background-color: #000; color: #00ffcc;}</style>", unsafe_allow_html=True)
st.title("🔱 H32 QUANTUM TERMINAL: MODULAR V1")

def load_terminal():
    coins = get_my_21_coins()
    rows = []
    
    # Fast Processing Loop
    for sym in coins:
        reason = get_neural_reason(3.5, 5000000) # Example inputs
        hype = get_hype_score(sym)
        
        rows.append({
            "ASSET": sym,
            "REASON": reason,
            "HYPE STATUS": hype,
            "ACTION": "🟢 BUY" if "BANK" in reason else "🟡 WAIT"
        })
    
    st.table(pd.DataFrame(rows))

if st.button("🚀 ACTIVATE NEURAL CORES"):
    while True:
        load_terminal()
        time.sleep(2)
