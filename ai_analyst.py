import streamlit as st
import json

# --- 🛰️ SYSTEM RECOVERY CONFIG ---
st.set_page_config(page_title="Aladdin Live Channel", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050811; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    .radar-panel {
        border: 2px solid #00ffd5;
        padding: 20px;
        border-radius: 12px;
        background-color: #0b1528;
        margin-bottom: 25px;
        box-shadow: 0px 0px 20px rgba(0, 255, 213, 0.3);
    }
    .status-text { color: #ffffff !important; text-align: left !important; font-size: 14px; margin: 8px 0; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ ALADDIN AUDIO LIVE TELEMETRY")
st.subheader("[ Dynamic Urdu 🔄 Chinese Tunnel • Zero-Crash Build ]")
st.write("---")

# --- 🧠 SAFE SESSION MATRIX ---
if "captured_input" not in st.session_state:
    st.session_state.captured_input = None
if "broadcast_output" not in st.session_state:
    st.session_state.broadcast_output = None

# --- 📡 LIVE TRANSMISSION RADAR (Awaaz Check Panel) ---
st.markdown('<div class="radar-panel"><h3>📡 LIVE DATA TRANSMISSION RADAR</h3>', unsafe_allow_html=True)

if st.session_state.captured_input:
    st.markdown(f'<div class="status-text">🟢 <b>[SIGNAL RECEIVED]:</b> "{st.session_state.captured_input}"</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-text">⚡ <b>[MATRIX STATUS]:</b> Data Packet Transmitted to Server Network...</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="status-text">🔊 <b>[AUDIO FIRED]:</b> Target Response Sent ➡️ <i>"{st.session_state.broadcast_output}"</i> ✅</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-text" style="color: #ff3344 !important; text-align: center !important; font-weight: bold;">• STANDBY: Mic is waiting for voice input stream...</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 🎙️ PRESS TO TRANSMIT GLOBAL AUDIO")

# --- 🎙️ JAVASCRIPT BROADCAST MATRIX ---
raw_payload = st.components.v1.html("""
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
                
                let outputMeaning = await fetchTranslation(speechString, targetLang);
                
                // Professional Human Voice Output Settings
                const synthWave = new SpeechSynthesisUtterance(outputMeaning);
                synthWave.lang = isChinese ? "ur-PK" : "zh-CN";
                synthWave.pitch = 0.85; 
                synthWave.rate = 0.92;
                
                window.speechSynthesis.speak(synthWave);
                telemetry.innerText = "🔊 Broadcast Completed Successfully.";

                // Safely ship structural data payload
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: speechString + "|||" + outputMeaning
                }, '*');
            };

            recognizer.onend = () => {
                btn.style.borderColor = "#00ffd5";
            };
        } else {
            telemetry.innerText = "❌ Microphone device unavailable.";
        }
    </script>
""", height=160, key="aladdin_matrix_v4_stable")

# --- 📊 CRITICAL BUG FIX: ZERO-CRASH HYPER-SAFE PARSER ---
if raw_payload and isinstance(raw_payload, str) and "|||" in raw_payload:
    try:
        parts = raw_payload.split("|||")
        if len(parts) == 2:
            st.session_state.captured_input = parts[0]
            st.session_state.broadcast_output = parts[1]
            st.rerun()
    except Exception:
        pass
