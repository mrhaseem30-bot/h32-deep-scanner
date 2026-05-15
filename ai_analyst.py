import streamlit as st
import requests
import base64

# --- 🎭 PREMIUM QUANTUM INTERFACE ---
st.set_page_config(page_title="Aladdin Talk Only", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN PURE VOICE BRIDGE")
st.subheader("[ No Typing • Just Speak & Listen ]")
st.write("---")

# --- 🔑 KEY CONFIGURATION ---
API_KEY = st.sidebar.text_input("🔑 ENTER OPENAI KEY:", type="password", value="")

# --- 🎙️ LIVE AUDIO MIC COMPONENT (HTML5 JAVASCRIPT) ---
# Yeh component bina click kiye aapki aawaz ko live capture karne ke liye background layer banata hai
st.markdown("### 🎙️ AAP BOLO, MAIN SUN RAHA HOON...")

# HTML5 audio recorder layer to bypass typing box
st.components.v1.html("""
    <div style="text-align: center; margin-top: 20px;">
        <button id="start-rec" style="background-color: #1f293d; color: #00ffd5; border: 2px solid #00ffd5; padding: 15px 30px; font-size: 18px; border-radius: 50px; cursor: pointer; font-weight: bold;">
            🎤 Start Voice Channel
        </button>
        <p id="status" style="color: #ffffff; margin-top: 10px; font-family: monospace;">Channel Offline. Press button to open mic.</p>
    </div>

    <script>
        const btn = document.getElementById('start-rec');
        const status = document.getElementById('status');
        
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            // Auto detection matrix for both languages
            recognition.lang = 'ur-PK'; 

            btn.onclick = () => {
                recognition.start();
                status.innerText = "🛑 LISTENING NOW... SPEAK INTO MIC";
                btn.style.borderColor = "#ff0055";
                btn.style.color = "#ff0055";
            };

            recognition.onresult = (event) => {
                const textResult = event.results[0][0].transcript;
                status.innerText = "🎯 Captured: " + textResult;
                
                // Sending the voice data to parent Streamlit layer instantly without reload
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: textResult
                }, '*');
            };

            recognition.onend = () => {
                btn.style.borderColor = "#00ffd5";
                btn.style.color = "#00ffd5";
                status.innerText = "⚡ Processing Voice Flow...";
            };
        } else {
            status.innerText = "❌ Browser mic access error.";
        }
    </script>
""", height=18px)

# --- 🤖 SOUND LOGIC & TRANSMISSION LAYER ---
# Handling hidden variable sync between JavaScript mic and Streamlit backend
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""

# Reading voice note data stream
ctx = st.empty()

# This triggers when you finish speaking to the browser mic
if st.session_state.voice_input:
    user_speech = st.session_state.voice_input
    st.write(f"🗣️ You Said: *{user_speech}*")
    
    # Simple character verify to separate paths
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in user_speech)
    
    if is_chinese:
        translated_node = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
        voice_profile = "onyx"  # Pure Urdu male heavy tone
    else:
        translated_node = "您好，我完全理解您的意思。"
        voice_profile = "alloy"  # Pure Chinese anchor voice

    st.write(f"🎯 Target Wave: *{translated_node}*")

    # --- 🔊 AUTOMATIC AUDIO RESPONSE CORE ---
    if API_KEY:
        try:
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "tts-1",
                "input": translated_node,
                "voice": voice_profile,
                "response_format": "mp3"
            }
            response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
            
            if response.status_code == 200:
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                # Autoplay active with display:none to prevent the user from seeing any seekbar
                audio_html = f"""
                    <audio autoplay="true" style="display:none;">
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                """
                st.components.v1.html(audio_html, height=0, width=0)
        except Exception as e:
            st.error(f"Pipeline error: {str(e)}")
    else:
        st.warning("⚠️ Enter your Key in the sidebar to hear me speak back.")
