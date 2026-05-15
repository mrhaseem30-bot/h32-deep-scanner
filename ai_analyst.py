import streamlit as st
import os
import requests
import time
from openai import OpenAI
from elevenlabs import generate, save, set_api_key

# --- 🛰️ SYSTEM ENVIRONMENT SETUP ---
st.set_page_config(page_title="ALADDIN CHINESE VOICE V56", layout="wide")

if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1

# --- 🎨 STUDIO DARK INTERFACE STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020610, #070f24) !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    .studio-box {
        background: radial-gradient(circle at center, #0b1a3a, #030814);
        border: 2px solid #ff3333;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(255, 51, 51, 0.2);
    }
    
    .text-card {
        background-color: #0d1117;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 18px;
        min-height: 120px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 📂 CONTROL SIDEBAR (KEYS DESK) ---
st.sidebar.markdown("### 🏛️ CHINESE STUDIO KEY CONTROL")
st.sidebar.markdown("OpenAI aur ElevenLabs dono ki keys lagayein:")

openai_key = st.sidebar.text_input("🔑 OPENAI API KEY", type="password", placeholder="sk-...")
elevenlabs_key = st.sidebar.text_input("🔑 ELEVENLABS API KEY", type="password", placeholder="Paste ElevenLabs Key...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗣️ CHINESE AI VOICE CHARACTER")
# ElevenLabs ke multilingual v2 model ke sath yeh voices Chinese top-class bolti hain
voice_character = st.sidebar.selectbox("🎙️ SELECT CHINESE VOICE STYLE", ["Zhiyu (Professional Native Mandarin - Recommended)", "Marcus (Smooth Accent)", "Bella (Clear Female Anchor)"])

# --- 👁️ MAIN INTERFACE HEADER ---
st.markdown("""
    <div class='studio-box'>
        <h2 style='color: #ff3333; margin: 0; font-size: 1.6rem;'>👁️ ALADDIN PURE CHINESE TRANS-VOICE ENGINE V56</h2>
        <p style='color: #8b949e; margin: 5px 0 0 0;'>Perfect Urdu/Hindi-to-Chinese Audio Translation | Native Mandarin Studio Sound</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🎙️ STEP 1: UPLOAD YOUR AUDIO (Urdu / Hindi)")
uploaded_audio = st.file_uploader("Upload any rough/low-quality recording (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if uploaded_audio is not None:
    st.audio(uploaded_audio, format='audio/mp3')
    st.write("---")
    
    if st.button("🚀 EXECUTE PERFECT CHINESE TRANSLATION"):
        if not openai_key or not elevenlabs_key:
            st.error("🚨 Galti! Please check sidebar. OpenAI aur ElevenLabs dono ki API Keys dalna lazmi hai.")
        else:
            with st.spinner("⚡ Aladdin Engine is processing... Translating to Mandarin and generating premium voice..."):
                try:
                    # Save local temp cache file
                    temp_input_path = "temp_user_voice.mp3"
                    with open(temp_input_path, "wb") as f:
                        f.write(uploaded_audio.read())
                    
                    # 1. TRANSLATION TO CHINESE (Using GPT-4o-mini to perfectly translate the Urdu text)
                    openai_client = OpenAI(api_key=openai_key)
                    
                    # First get Urdu text from speech
                    with open(temp_input_path, "rb") as audio_file:
                        transcription = openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file
                        )
                    urdu_text = transcription.text
                    
                    # Convert that Urdu text into natural Chinese (Mandarin)
                    translation_data = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are an expert native Chinese translator. Translate the user's input text into natural, professional Mandarin Chinese text. Only output the translated Chinese characters."},
                            {"role": "user", "content": urdu_text}
                        ]
                    )
                    perfect_chinese_text = translation_data.choices[0].message.content
                    
                    # 2. HIGH-END CHINESE VOICE GENERATION (ElevenLabs Multilingual 1 Number Sound)
                    set_api_key(elevenlabs_key)
                    
                    # Using eleven_multilingual_v2 model which supports perfect native Chinese pronunciations
                    high_quality_audio = generate(
                        text=perfect_chinese_text,
                        voice=voice_character.split(" ")[0],
                        model="eleven_multilingual_v2"
                    )
                    
                    temp_output_path = "studio_chinese_output.mp3"
                    save(high_quality_audio, temp_output_path)
                    
                    # --- 📊 DISPLAY SYSTEM TEXT COMPARISON ---
                    col_view1, col_view2 = st.columns(2)
                    with col_view1:
                        st.markdown(f"""
                            <div class='text-card' style='border-top: 3px solid #ff9b05;'>
                                <span style='color:#8b949e; font-size:11px;'>ORIGINAL AUDIO RECOGNIZED</span><br>
                                <p style='font-size:14px; margin-top:8px; color:#ffd699;'><b>{urdu_text}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with col_view2:
                        st.markdown(f"""
                            <div class='text-card' style='border-top: 3px solid #ff3333;'>
                                <span style='color:#8b949e; font-size:11px;'>NATIVE CHINESE (MANDARIN) TEXT</span><br>
                                <p style='font-size:14px; margin-top:8px; color:#ff3333;'><b>{perfect_chinese_text}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("---")
                    st.markdown("### 🔊 STEP 2: PROFESSIONAL CHINESE SOUND OUTPUT")
                    st.success(f"🔥 Aladdin Audio successfully generated in Chinese using voice `{voice_character.split(' ')[0]}`:")
                    
                    # Stream the crystal clear audio to user
                    with open(temp_output_path, "rb") as final_audio:
                        st.audio(final_audio.read(), format='audio/mp3')
                    
                    # Clean cache from local directories
                    os.remove(temp_input_path)
                    os.remove(temp_output_path)
                    
                except Exception as e:
                    st.error(f"Chinese Voice Studio Error: {str(e)}")
