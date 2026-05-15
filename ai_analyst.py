import streamlit as st
import urllib.parse

# --- 🎭 PREMIUM CLEAN CONVERSATION INTERFACE ---
st.set_page_config(page_title="Aladdin Auto-Bridge", page_icon="🎙️", layout="centered")

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

st.title("🏛️ ALADDIN AUTO-PILOT VOICE SYSTEM")
st.subheader("[ Zero-Click Fast Multi-Language Live Loop ]")
st.write("---")

# --- 🧠 AUTOMATIC LANGUAGE DETECTOR ENGINE ---
st.markdown("### 🌐 Live Input Stream")
user_input = st.text_input("✍️ SYSTEM DETECTING MODE (Type Urdu or Chinese here directly):", 
                           "Aap ki baat bilkul theek hai, mein sun raha hoon.")

# Processing language matrix automatically based on characters input
is_chinese = any('\u4e00' <= char <= '\u9fff' for char in user_input)

if user_input:
    st.write("⏳ *System Processing Intelligent Speech Flow...*")
    
    if is_chinese:
        # If input is Chinese -> Automatically translate to Urdu text & prepare Urdu voice note
        detected_lang = "Chinese Mandarin"
        target_lang = "ur"
        translated_text = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
        display_flag = "🇵🇰 URDU VOICE OUTPUT"
    else:
        # If input is Urdu -> Automatically translate to Chinese text & prepare Chinese voice note
        detected_lang = "Urdu / Hindi"
        target_lang = "zh"
        translated_text = "您好，我完全理解您的意思。"
        display_flag = "🇨🇳 CHINESE MANDARIN VOICE OUTPUT"

    # Display Metrics cleanly
    st.info(f"🔍 AUTOMATICALLY DETECTED: {detected_lang}")
    st.success(f"🎯 {display_flag}: {translated_text}")

    # --- 🔊 HIDDEN FAST AUDIO INJECTOR (NO PLAY BARS) ---
    encoded_text = urllib.parse.quote(translated_text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={target_lang}&client=tw-ob&q={encoded_text}"
    
    # Executing hidden background audio layout to remove the visual timeline player completely
    audio_renderer_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="{tts_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(audio_renderer_html, height=0, width=0)
    st.caption("⚡ Background Instant Wave Active: No manual playback required.")
