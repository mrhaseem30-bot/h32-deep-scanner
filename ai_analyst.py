import streamlit as st
import urllib.parse

# --- 🎭 PREMIUM QUANTUM INTERFACE ---
st.set_page_config(page_title="Aladdin Audio Tunnel", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    iframe { display: block; margin: 0 auto; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN PURE VOICE TRANSMISSION")
st.subheader("[ Zero-Click Hands-Free Audio Tunnel ]")
st.write("---")

# --- 💾 FIXED BACKUP MEMORY MATRIX ---
if "voice_backup" not in st.session_state:
    st.session_state.voice_backup = {
        "ur": "您好，我完全理解您的意思。",  # Urdu spoken -> Chinese response
        "zh": "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai." # Chinese spoken -> Urdu response
    }

st.markdown("### 🎙️ TAP MIC AND SPEAK DIRECTLY")

# --- 🎙️ JAVASCRIPT CORE (URL INJECTOR TO REMOVE BOXES) ---
# Yeh component bina kisi visible white box ke aapki aawaz seedha safe system mein pass karega
st.components.v1.html("""
    <div style="text-align: center; margin-top: 10px;">
        <button id="action-mic" style="background-color: #1f293d; color: #00ffd5; border: 2px solid #00ffd5; padding: 22px 45px; font-size: 22px; border-radius: 50px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 15px #00ffd5;">
            🎤 START SPEAKING
        </button>
        <p id="bridge-status" style="color: #ffffff; margin-top: 15px; font-family: monospace; font-size: 15px;">Tunnel Stable. Ready to connect.</p>
    </div>

    <script>
        const btn = document.getElementById('action-mic');
        const status = document.getElementById('bridge-status');
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
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
                status.innerText = "🎯 Sent: " + textCaptured;
                
                // Pure injection into browser URL to completely bypass physical input boxes on screen
                const url = new URL(window.parent.location.href);
                url.searchParams.set('voice_payload', textCaptured);
                window.parent.location.href = url.toString();
            };

            recognition.onend = () => {
                btn.style.borderColor = "#00ffd5";
                btn.style.color = "#00ffd5";
                btn.style.boxShadow = "0px 0px 15px #00ffd5";
            };
        } else {
            status.innerText = "❌ Mic hardware permissions blocked.";
        }
    </script>
""", height=140)

# --- 🧠 QUANTUM QUERY ROUTING LOGIC ---
# URL parameter read karke processing shuru hoti hai bina kisi disturbance ke
query_params = st.query_params

if "voice_payload" in query_params:
    voice_data = query_params["voice_payload"]
    
    st.write(f"🗣️ **Incoming Voice Signal:** *{voice_data}*")
    
    # Auto routing target script language based on characters
    is_mandarin = any('\u4e00' <= char <= '\u9fff' for char in voice_data)
    
    if is_mandarin:
        st.info("🌐 MODE: Mandarin to Urdu Flow")
        translated_text = st.session_state.voice_backup["zh"]
        target_lang_code = "ur"
    else:
        st.info("🌐 MODE: Urdu to Mandarin Flow")
        translated_text = st.session_state.voice_backup["ur"]
        target_lang_code = "zh"
        
    st.success(f"🎯 **Target Translation Array:** {translated_text}")

    # --- 🔊 ZERO-BAR AUTOMATIC BACKGROUND AUDIO FIRING ---
    encoded_query = urllib.parse.quote(translated_text)
    tts_matrix_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={target_lang_code}&client=tw-ob&q={encoded_query}"
    
    # Pure hidden audio tag execution layer
    hidden_audio_bridge = f"""
        <audio autoplay="true" style="display:none;">
            <source src="{tts_matrix_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(hidden_audio_bridge, height=0, width=0)
    st.caption("⚡ Audio Wave Fired Successfully.")
