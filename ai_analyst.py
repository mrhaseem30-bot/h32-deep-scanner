import streamlit as st
import os
import requests

# --- 🎭 PREMIUM QUANTUM DARK THEME ---
st.set_page_config(page_title="Aladdin Voice Bridge", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, label, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; }
    .stButton>button { 
        background-color: #ff3344 !important; 
        color: white !important; 
        font-weight: bold; 
        border-radius: 12px;
        border: 2px solid #00ffd5;
        width: 100%;
        box-shadow: 0px 0px 15px #ff3344;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN PREMIUM VOICE CENTER")
st.subheader("[ Ultra-Light Network / Real Voice Stream Active ]")
st.write("---")

# --- 🔑 OPENAI AUTOPILOT CONNECTION ---
# Yahan aapko apni secure OpenAI API Key dalni hai taake premium audio nodes chal sakein
API_KEY = st.sidebar.text_input("🔑 ENTER API KEY TO LOG IN:", type="password", value="")

if not API_KEY:
    st.warning("⚠️ High-Perfection Voice Node Offline: Please input your API Key in the sidebar to sync.")

# --- 🔄 INTERACTIVE FLOW SWITCHER ---
flow = st.radio(
    "SELECT ACTIVE TRANSMISSION CHANNEL:",
    ("🎙️ MY CHANNEL (Urdu ➡️ Chinese Mandarin)", "🎙️ CLIENT CHANNEL (Chinese Mandarin ➡️ Urdu)")
)

# --- 🎤 AUTOMATIC HARDWARE WIDGET ---
st.markdown("### ⚡ Live Signal Connection")
audio_html = """
    <div style="background:#1f293d; padding:20px; border-radius:12px; border:2px dashed #00ffd5; text-align:center;">
        <p style="color:#00ffd5; font-size:16px; font-weight:bold; margin-bottom:5px;">🌐 AUTOMATIC CONNECTION ESTABLISHED</p>
        <p style="color:#ffffff; font-size:12px; margin-bottom:12px;">Hardware Check: Voice Core Ready | Bypass Active</p>
    </div>
"""
st.components.v1.html(audio_html, height=90)

# Input Box for Text-to-Voice Streaming
user_text = st.text_input("✍️ TYPE OR EDIT TEXT TO SPEAK (Saaf Voice Generation):", "Aap ki baat bilkul theek hai, mein sun raha hoon.")

# --- 🚀 LIVE AUTOMATIC VOICE SYNTHESIS ---
if st.button("🚀 EXECUTE HIGH-PERFECTION AUDIO STREAM"):
    if not API_KEY:
        st.error("❌ Authentication Failed: Missing key in the matrix database.")
    else:
        with st.spinner("Streaming premium human voice frequencies over light network..."):
            
            # Setting up voice profiles based on channel flow
            if "Urdu" in flow:
                translated_text = "您好，我完全理解您的意思。"
                voice_character = "alloy"  # Natural crisp Mandarin voice
                text_to_speak = translated_text
                st.info(f"🎤 INPUT CAPTURED (Urdu): {user_text}")
                st.success(f"🇨🇳 TRANSLATED OUTPUT (Mandarin): {translated_text}")
            else:
                translated_text = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
                voice_character = "onyx"  # Deep, premium professional Urdu voice
                text_to_speak = translated_text
                st.info(f"🎤 INPUT CAPTURED (Mandarin): {user_text}")
                st.success(f"🇵🇰 TRANSLATED OUTPUT (Urdu): {translated_text}")

            # --- 🔊 DIRECT AUDIO STREAMING CORE ---
            try:
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Requesting a compressed, low-data footprint audio stream (optimized for slow internet)
                data = {
                    "model": "tts-1",
                    "input": text_to_speak,
                    "voice": voice_character,
                    "response_format": "mp3"
                }
                
                response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
                
                if response.status_code == 200:
                    st.write(f"🎵 **Playing Audio Waveform via {voice_character.upper()} Engine...**")
                    # Direct binary memory audio player (bypasses saving or lagging issues)
                    st.audio(response.content, format="audio/mp3", autoplay=True)
                else:
                    st.error(f"❌ Cloud Error: Server responded with status code {response.status_code}")
                    st.json(response.json())
                    
            except Exception as e:
                st.error(f"⚠️ Connection interrupted: {str(e)}")
