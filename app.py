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
        url = "https://api.coingecko.com/api/v3/coins/m
