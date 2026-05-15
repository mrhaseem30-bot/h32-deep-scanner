import streamlit as st
import os

# --- 🎭 PREMIUM QUANTUM DARK INTERFACE ---
st.set_page_config(page_title="Aladdin Walkie-Talkie", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, label, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input {
        background-color: #1f293d !important;
        color: #ffffff !important;
        border: 2px solid #00ffd5 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN INSTANT AUDIO BRIDGE")
st.subheader("[ Pre-Stored Premium Human Voice Matrix ]")
st.write("---")

# --- 📥 TWO-WAY PRE-STORED DIALOGUE MAPPING ---
# Yahan hum saare basic dialogues aur unki files ka database lock kar rahe hain
dialogue_matrix = {
    "urdu_nodes": {
        "Aap ki baat bilkul theek hai, mein sun raha hoon.": {
            "translation": "您好，我完全理解您的意思。",
            "file": "voice_assets/chinese_1.mp3" # Pre-recorded high quality Chinese voice
        },
        "Shukriya bhai! Aap ki poori madad ki jayegi.": {
            "translation": "谢谢，非常感谢你的支持。",
            "file": "voice_assets/chinese_2.mp3"
        }
    },
    "chinese_nodes": {
        "您好，很高兴与您合作。": {
            "translation": "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai.",
            "file": "voice_assets/urdu_1.mp3" # Pre-recorded high quality Urdu voice
        },
        "这个价格可以再谈谈吗？": {
            "translation": "Kya is ke rate thode kam ho sakte hain bhai?",
            "file": "voice_assets/urdu_2.mp3"
        }
    }
}

# --- 🌐 LIVE TEXT CAPTURE WITH AUTO-DETECTION ---
user_input = st.text_input("✍️ ENTER TEXT OR DIALOGUE (Auto Matching Active):", 
                           value="Aap ki baat bilkul theek hai, mein sun raha hoon.")

if user_input:
    # Character verification to check if input is Chinese or Urdu
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in user_input)
    
    matched_file = None
    translated_text = ""
    
    if is_chinese:
        st.info("🔍 DETECTED: Chinese Mandarin Node")
        # Direct key mapping from database
        if user_input in dialogue_matrix["chinese_nodes"]:
            translated_text = dialogue_matrix["chinese_nodes"][user_input]["translation"]
            matched_file = dialogue_matrix["chinese_nodes"][user_input]["file"]
            st.success(f"🇵🇰 INSTANT URDU TARGET: {translated_text}")
    else:
        st.info("🔍 DETECTED: Urdu / Hindi Node")
        if user_input in dialogue_matrix["urdu_nodes"]:
            translated_text = dialogue_matrix["urdu_nodes"][user_input]["translation"]
            matched_file = dialogue_matrix["urdu_nodes"][user_input]["file"]
            st.success(f"🇨🇳 INSTANT MANDARIN TARGET: {translated_text}")

    # --- 🔊 INSTANT AUDIO FIRING MECHANISM ---
    if matched_file and os.path.exists(matched_file):
        with open(matched_file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            # Bypassing the visible timeline player to create a direct voice-note experience
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    elif matched_file:
        st.warning(f"⚠️ Audio asset active in matrix code but missing in repository folder: '{matched_file}'")
    else:
        st.error("❌ Audio mismatch: This specific phrase is not saved in the local voice dictionary yet.")
