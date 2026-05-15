import streamlit as st
import os
import requests
import time
from openai import OpenAI
from elevenlabs import generate, save, set_api_key

# --- 🛰️ SYSTEM ENVIRONMENT SETUP ---
st.set_page_config(page_title="ALADDIN DUAL VOICE BRIDGE V58", layout="wide")

# --- 🎨 STUDIO DARK INTERFACE STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020610, #061129) !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    .studio-box {
        background: radial-gradient(circle at center, #0b1a3a, #030814);
        border: 2px solid #00ffcc;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    
    .direction-card {
        background: linear-gradient(145deg, #0d1b2a, #08111f);
        border: 1px solid #00ffcc;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .text-card {
        background-color: #0d1117;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 15px;
        min-height: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 📂 CONTROL SIDEBAR (KEYS DESK) ---
st.sidebar.markdown("### 🏛️ STUDIO CREDENTIALS CONTROL")
openai_key = st.sidebar.text_input("🔑 OPENAI API KEY", type="password", placeholder="sk-...")
elevenlabs_key = st.sidebar.text_input("🔑 ELEVENLABS API KEY", type="password", placeholder="Paste ElevenLabs Key...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗣️ HIGH-PERFECTION VOICE MODELS")
chinese_voice = st.sidebar.selectbox("🇨🇳 CHINESE VOICE CHARATER", ["Zhiyu (Native Mandarin)", "Bella (Studio Anchor)"])
urdu_voice = st.sidebar.selectbox("🇵🇰 URDU VOICE CHARACTER", ["Marcus (Deep Professional Urdu Accent)", "Adam (Solid Clear Tone)"])

# --- 👁️ MAIN INTERFACE HEADER ---
st.markdown("""
    <div class='studio-box'>
        <h2 style='color: #00ffcc; margin: 0; font-size: 1.6rem;'>👁️ ALADDIN TWO-WAY REAL-TIME VOICE BRIDGE</h2>
        <p style='color: #8b949e; margin: 5px 0 0 0;'>Automatic Translation Intercept | Urdu/Hindi ⇄ Chinese Mandarin (Studio Quality)</p>
    </div>
""", unsafe_allow_html=True)

# --- 🔄 DIRECTION SWITCHER ---
st.markdown("### 🔄 SELECT YOUR CONVERSATION FLOW")
direction = st.radio(
    "Choose who is speaking right now:",
    ["🎙️ I AM SPEAKING (Urdu/Hindi ➡️ Chinese Mandarin)", "🎙️ CHINESE CLIENT IS SPEAKING (Chinese Mandarin ➡️ Urdu)"],
    horizontal=True
)

st.write("---")

# --- 📂 AUDIO SOURCE INPUT ---
uploaded_audio = st.file_uploader("Upload or Record Voice Audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if uploaded_audio is not None:
    st.audio(uploaded_audio, format='audio/mp3')
    st.write("---")
    
    if st.button("🚀 TRANSMIT & TRANSLATE NOW"):
        if not openai_key or not elevenlabs_key:
            st.error("🚨 Galti! Please enter both OpenAI and ElevenLabs keys in the sidebar.")
        else:
            with st.spinner("⚡ Aladdin Quantum Core is processing voice channels..."):
                try:
                    # Save audio local cache
                    temp_input = "temp_voice_bridge.mp3"
                    with open(temp_input, "wb") as f:
                        f.write(uploaded_audio.read())
                        
                    openai_client = OpenAI(api_key=openai_key)
                    set_api_key(elevenlabs_key)
                    
                    # --- 🔴 PATH A: URDU TO CHINESE ---
                    if "Urdu/Hindi ➡️ Chinese" in direction:
                        # 1. Capture user Urdu speech
                        with open(temp_input, "rb") as f_audio:
                            transcription = openai_client.audio.transcriptions.create(model="whisper-1", file=f_audio)
                        input_text = transcription.text
                        
                        # 2. Perfect translate to Mandarin Text
                        translation = openai_client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are an elite native Chinese translator. Translate the input text directly into formal, professional Mandarin Chinese characters. Output ONLY the translation."},
                                {"role": "user", "content": input_text}
                            ]
                        )
                        output_text = translation.choices[0].message.content
                        selected_model_voice = chinese_voice.split(" ")[0]
                        success_msg = f"🔥 Successfully Translated into Chinese via `{selected_model_voice}` Studio Voice:"
                    
                    # --- 🔵 PATH B: CHINESE TO URDU ---
                    else:
                        # 1. Capture Chinese client speech
                        with open(temp_input, "rb") as f_audio:
                            transcription = openai_client.audio.transcriptions.create(model="whisper-1", file=f_audio)
                        input_text = transcription.text
                        
                        # 2. Perfect translate to Professional Urdu Text
                        translation = openai_client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are an elite Urdu linguist. Translate the Chinese text into perfectly natural, highly professional Urdu text. Use clean language, avoid robotic phrases. Output ONLY the translated Urdu text."},
                                {"role": "user", "content": input_text}
                            ]
                        )
                        output_text = translation.choices[0].message.content
                        selected_model_voice = urdu_voice.split(" ")[0]
                        success_msg = f"🔥 Successfully Translated into Professional Urdu via `{selected_model_voice}` Studio Voice:"

                    # 3. HIGH PERFECTION ELEVENLABS SOUND GENERATOR
                    high_quality_audio = generate(
                        text=output_text,
                        voice=selected_model_voice,
                        model="eleven_multilingual_v2"
                    )
                    
                    temp_output = "studio_bridge_output.mp3"
                    save(high_quality_audio, temp_output)
                    
                    # --- 📊 DISPLAY RESULTS SIDE-BY-SIDE ---
                    col_in, col_out = st.columns(2)
                    with col_in:
                        st.markdown(f"""
                            <div class='text-card' style='border-top: 3px solid #ff9b05;'>
                                <span style='color:#8b949e; font-size:11px;'>🎤 RECOGNIZED INCOMING AUDIO</span><br>
                                <p style='font-size:15px; margin-top:8px; color:#ffd699;'><b>{input_text}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_out:
                        st.markdown(f"""
                            <div class='text-card' style='border-top: 3px solid #00ffcc;'>
                                <span style='color:#8b949e; font-size:11px;'>🎯 TRANSLATED COMPOSITOR TARGET</span><br>
                                <p style='font-size:15px; margin-top:8px; color:#00ffcc;'><b>{output_text}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("---")
                    st.markdown(f"### 🔊 1-NUMBER PERFECT VOICE OUTPUT")
                    st.success(success_msg)
                    
                    with open(temp_output, "rb") as f_final:
                        st.audio(f_final.read(), format='audio/mp3')
                        
                    # Clean system cache files
                    if os.path.exists(temp_input): os.remove(temp_input)
                    if os.path.exists(temp_output): os.remove(temp_output)
                    
                except Exception as e:
                    st.error(f"Voice Bridge Processing Error: {str(e)}")
