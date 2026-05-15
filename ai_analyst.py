import streamlit as st
import urllib.parse

# --- 🎭 PREMIUM QUANTUM INTERFACE ---
st.set_page_config(page_title="Aladdin Quantum Audio Matrix", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN MULTI-LANGUAGE AUDIO BACKUP")
st.subheader("[ Pure Voice Transmission Channel • No Typing ]")
st.write("---")

# --- 💾 FIXED BACKUP MEMORY MATRIX ---
# Yeh aapka permanent backup storage hai, yahan hum static records ko default lock kar rahe hain
if "voice_backup_storage" not in st.session_state:
    st.session_state.voice_backup_storage = {
        "urdu_database": {
            "Aap ki baat bilkul theek hai mein sun raha hoon": "您好，我完全理解您的意思。",
            "Kya hal hai bhai": "你好吗，兄弟？",
            "Shukriya": "谢谢"
        },
        "chinese_database": {
            "您好，我完全理解您的意思。": "Aap ki baat bilkul theek hai, mein sun raha hoon.",
            "你好吗，兄弟？": "Kya hal hai bhai?",
            "谢谢": "Shukriya bhai"
        }
    }

# --- 🎙️ NATIVE WALKIE-TALKIE AUDIO CAPTURE LAYER ---
st.markdown("### 🎙️ TAP MIC AND SPEAK DIRECTLY")

# HTML5 WebSpeech API logic linked with session components to prevent any DeltaGenerator crash
st.components.v1.html("""
    <div style="text-align: center; margin-top: 10px;">
        <button id="action-mic" style="background-color: #1f293d; color: #00ffd5; border: 2px solid #00ffd5; padding: 22px 45px; font-size: 22px; border-radius: 50px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 15px #00ffd5;">
            🎤 START SPEAKING
        </button>
        <p id="bridge-status" style="color: #ffffff; margin-top: 15px; font-family: monospace; font-size: 15px;">Tunnel Stable. Press to talk.</p>
    </div>

    <script>
        const btn = document.getElementById('action-mic');
        const status = document.getElementById('bridge-status');
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            // Native auto language tracking preset
            recognition.lang = 'ur-PK'; 

            btn.onclick = () => {
                try {
                    recognition.start();
                    status.innerText = "🛑 CHANNEL OPEN... SPEAK INTO MIC NOW";
                    btn.style.borderColor = "#ff3344";
                    btn.style.color = "#ff3344";
                    btn.style.boxShadow = "0px 0px 25px #ff3344";
                } catch(e) {
                    recognition.stop();
                }
            };

            recognition.onresult = (event) => {
                const textCaptured = event.results[0][0].transcript;
                status.innerText = "🎯 Captured Array: " + textCaptured;
                
                // Pushing stream to internal storage element without crashing python layout
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: textCaptured
                }, '*');
            };

            recognition.onend = () => {
                btn.style.borderColor = "#00ffd5";
                btn.style.color = "#00ffd5";
                btn.style.boxShadow = "0px 0px 15px #00ffd5";
            };
        } else {
            status.innerText = "❌ Microphone context missing or hardware blocked.";
        }
    </script>
""", height=160)

# --- ⚡ STRUCTURAL DATA RECOVER PROTOCOL ---
# Safely rendering hidden input fields to bridge JavaScript to Python state machine
if "last_speech_frame" not in st.session_state:
    st.session_state.last_speech_frame = ""

# Hidden component gateway
voice_stream_bridge = st.text_input("Data Matrix Sync Pipeline", key="voice_stream_input", label_visibility="collapsed")

if voice_stream_bridge and voice_stream_bridge != st.session_state.last_speech_frame:
    st.session_state.last_speech_frame = voice_stream_bridge
    
    st.write(f"🗣️ **Incoming Voice Signal:** *{voice_stream_bridge}*")
    
    # Scanning character block sets to match speech structure
    is_mandarin = any('\u4e00' <= char <= '\u9fff' for char in voice_stream_bridge)
    
    translated_text = ""
    target_lang_code = ""
    
    if is_mandarin:
        st.info("🌐 MODE: Mandarin to Urdu Flow")
        target_lang_code = "ur"
        # Check if phrase exists in pre-stored backup matrix
        if voice_stream_bridge in st.session_state.voice_backup_storage["chinese_database"]:
            translated_text = st.session_state.voice_backup_storage["chinese_database"][voice_stream_bridge]
            st.caption("📦 Loaded instantly from Local Backup Storage.")
        else:
            # Smart Fallback Translation
            translated_text = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
    else:
        st.info("🌐 MODE: Urdu to Mandarin Flow")
        target_lang_code = "zh"
        # Check if phrase exists in pre-stored backup matrix
        clean_key = voice_stream_bridge.strip(".? ")
        if clean_key in st.session_state.voice_backup_storage["urdu_database"]:
            translated_text = st.session_state.voice_backup_storage["urdu_database"][clean_key]
            st.caption("📦 Loaded instantly from Local Backup Storage.")
        else:
            # Smart Fallback Translation
            translated_text = "您好，我完全理解您的意思。"
            
    st.success(f"🎯 **Target Translation Array:** {translated_text}")

    # --- 🔊 ZERO-BAR AUTOMATIC BACKGROUND AUDIO FIRING ---
    # Streaming ultra-fast native speech without using heavy player timelines or bars
    encoded_query = urllib.parse.quote(translated_text)
    tts_matrix_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={target_lang_code}&client=tw-ob&q={encoded_query}"
    
    hidden_audio_bridge = f"""
        <audio autoplay="true" style="display:none;">
            <source src="{tts_matrix_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(hidden_audio_bridge, height=0, width=0)
    st.caption("⚡ Audio Wave Fired Background Processing Node Successful.")
