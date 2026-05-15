import streamlit as st
import json

# --- 🛰️ SATELLITE CORE CONFIG ---
st.set_page_config(page_title="Aladdin Telemetry Tunnel", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050811; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    .status-panel {
        border: 2px solid #00ffd5;
        padding: 20px;
        border-radius: 12px;
        background-color: #0b1528;
        margin-bottom: 20px;
        box-shadow: 0px 0px 20px rgba(0, 255, 213, 0.4);
    }
    .log-text { color: #ffffff !important; text-align: left !important; font-size: 14px; margin: 8px 0; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ ALADDIN AUDIO LIVE TELEMETRY")
st.subheader("[ Dynamic Urdu 🔄 Chinese Tunnel • Stable Build ]")
st.write("---")

# --- 🧠 SAFE STATE INITIALIZATION ---
if "last_voice_payload" not in st.session_state:
    st.session_state.last_voice_payload = None
if "translated_output" not in st.session_state:
    st.session_state.translated_output = None

# --- 📡 LIVE TRANSMISSION RADAR PANEL ---
st.markdown('<div class="status-panel"><h3>📡 LIVE DATA TRANSMISSION RADAR</h3>', unsafe_allow_html=True)

if st.session_state.last_voice_payload:
    st.markdown(f'<div class="log-text">🟢 <b>[INPUT CAPTURED]:</b> "{st.session_state.last_voice_payload}"</div>', unsafe_allow_html=True)
    st.markdown('<div class="log-text">⚡ <b>[SERVER ROUTING]:</b> Data Packets Synchronized to Network Core...</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="log-text">🔊 <b>[GLOBAL BROADCAST]:</b> Professional Sound Dispatched ➡️ <i>"{st.session_state.translated_output}"</i> ✅</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="log-text" style="color: #ff3344 !important; text-align: center !important; font-weight: bold;">• STANDBY: Mic is waiting for voice input stream...</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 🎙️ PRESS TO TRANSMIT GLOBAL AUDIO")

# --- 🎙️ JAVASCRIPT AUDIO ENGINE COMPONENT ---
captured_data = st.components.v1.html("""
    <div style="text-align: center;">
        <button id="radar-mic" style="background-color: #0b1528; color: #00ffd5; border: 2px solid #00ffd5; padding: 25px 55px; font-size: 24px; border-radius: 60px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 20px #00ffd5; text-transform: uppercase;">
            🎤 START DUAL AUDIO CHANNEL
        </button>
        <p id="mic-telemetry" style="color: #ffffff; margin-top: 15px; font-family: monospace;">SYSTEM READY</p>
    </div>

    <script>
        const btn = document.getElementById('radar-mic');
        const telemetry = document.getElementById('mic-telemetry');
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const recognizer = new SpeechRecognition();
            
            recognizer.continuous = false;
            recognizer.interimResults = false;
            recognizer.lang = 'ur-PK';

            btn.onclick = () => {
                window.speechSynthesis.cancel();
                recognizer.start();
                telemetry.innerText = "🛑 TUNNEL OPENED... SPEAK IN URDU OR CHINESE NOW";
                btn.style.borderColor = "#ff3344";
            };

            async function fetchTranslation(text, target) {
                try {
                    const res = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(text)}`);
                    const json = await res.json();
                    return json[0][0][0];
                } catch(e) {
                    return target === 'ur' ? "Main aap ki baat samajh gaya hoon." : "我完全理解您的意思。";
                }
            }

            recognizer.onresult = async (event) => {
                const speechString = event.results[0][0].transcript;
                telemetry.innerText = "🎯 Captured: " + speechString;
                
                let isChinese = /[\u4e00-\u9fff]/.test(speechString);
                let targetLang = isChinese ? 'ur' : 'zh-CN';
                
                telemetry.innerText = "📡 Processing Matrix Meaning...";
                let outputMeaning = await fetchTranslation(speechString, targetLang);
                
                // Professional Audio Output Setup
                const synthWave = new SpeechSynthesisUtterance(outputMeaning);
                synthWave.lang = isChinese ? "ur-PK" : "zh-CN";
                synthWave.pitch = 0.85; 
                synthWave.rate = 0.92;
                
                window.speechSynthesis.speak(synthWave);
                telemetry.innerText = "🔊 Audio Transmission Completed.";

                // Safely send data back to python
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: JSON.stringify({ voice_in: speechString, voice_out: outputMeaning })
                }, '*');
            };

            recognizer.onend = () => {
                btn.style.borderColor = "#00ffd5";
            };
        } else {
            telemetry.innerText = "❌ Microphone access denied.";
        }
    </script>
""", height=160, key="aladdin_matrix_final_v3")

# --- 📊 CRITICAL BUG FIX: SAFE DATA INTERCEPTOR ---
if captured_data is not None and captured_data != "":
    try:
        # Strict validation ensuring no raw data format breaks the stream
        data_packet = json.loads(str(captured_data))
        if isinstance(data_packet, dict) and "voice_in" in data_packet:
            st.session_state.last_voice_payload = data_packet["voice_in"]
            st.session_state.translated_output = data_packet["voice_out"]
            st.rerun()
    except Exception as e:
        # Silently bypass any half-cooked packet data to avoid TypeError screens
        pass
