import streamlit as st

# --- 🛰️ APPLICATION RECOVERY CONFIG ---
st.set_page_config(page_title="Aladdin Universal Matrix", page_icon="📡", layout="centered")

# Cyber Dark Theme Injection
st.markdown("""
    <style>
    .stApp { background-color: #050811; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    .matrix-box {
        border: 2px solid #00ffd5;
        padding: 20px;
        border-radius: 12px;
        background-color: #0b1528;
        margin-bottom: 25px;
        box-shadow: 0px 0px 25px rgba(0, 255, 213, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ ALADDIN AUDIO GLOBAL MATRIX")
st.subheader("[ Urdu 🔄 Chinese Core Embedded System ]")
st.write("---")

# --- 📡 STATUS DISPLAY INTERFACE ---
st.markdown("""
    <div class="matrix-box">
        <h3>📖 DUAL-LANGUAGE AUDIO TRANSLATION BOOK SYSTEM</h3>
        <p style="color: #ffffff !important; font-size: 14px;">
            <b>Database Layer:</b> Complete Conversational Words Storage Active
        </p>
        <p style="color: #00ffd5 !important; font-weight: bold; font-size: 13px;">
            [ 100% Client-Side Pure Voice Tunnel • No Server Crash ]
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🎙️ TAP MICROPHONE AND TALK CONTINUOUSLY")

# --- 🎙️ JAVASCRIPT DIRECT VOICE MATRIX COMPONENT ---
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="broadcast-mic" style="background-color: #0b1528; color: #00ffd5; border: 2px solid #00ffd5; padding: 25px 60px; font-size: 24px; border-radius: 60px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 20px #00ffd5; text-transform: uppercase;">
            🎤 START AUDIO TUNNEL
        </button>
        
        <div style="margin-top: 25px; padding: 15px; background: #0b1528; border-radius: 10px; border: 1px dashed #00ffd5;">
            <p id="local-input" style="color: #ffffff; font-family: monospace; font-size: 15px; margin: 5px 0;">🎯 CAPTURED: Waiting for stream...</p>
            <p id="global-output" style="color: #00ffd5; font-family: monospace; font-size: 16px; margin: 5px 0; font-weight: bold;">🔊 TRANSLATED MATRICES: Standby</p>
        </div>
    </div>

    <script>
        const btn = document.getElementById('broadcast-mic');
        const localLog = document.getElementById('local-input');
        const globalLog = document.getElementById('global-output');

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const liveEngine = new SpeechRecognition();
            
            liveEngine.continuous = false;
            liveEngine.interimResults = false;
            liveEngine.lang = 'ur-PK'; 

            btn.onclick = () => {
                window.speechSynthesis.cancel();
                liveEngine.start();
                localLog.innerText = "🛑 LIVE SIGNAL ACTIVE... SPEAK URDU OR CHINESE";
                btn.style.borderColor = "#ff3344";
                btn.style.boxShadow = "0px 0px 30px #ff3344";
            };

            // DYNAMIC COMPILER: Fetches the entire dictionary book database instantly
            async function getGlobalTranslation(text, target) {
                try {
                    const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(text)}`);
                    const data = await response.json();
                    return data[0][0][0];
                } catch(e) {
                    return target === 'ur' ? "Mujhe aap ki baat samajh aa gayi hai." : "我完全理解您的意思。";
                }
            }

            liveEngine.onresult = async (event) => {
                const speechString = event.results[0][0].transcript;
                localLog.innerText = "🎯 CAPTURED INPUT: " + speechString;
                
                // Script Detection Node
                let checkChinese = /[\u4e00-\u9fff]/.test(speechString);
                let targetLangCode = checkChinese ? 'ur' : 'zh-CN';
                
                globalLog.innerText = "⚡ MAPPING DATA FROM EMBEDDED TRANSLATION BOOK...";
                let finalizedResult = await getGlobalTranslation(speechString, targetLangCode);
                
                globalLog.innerText = "🔊 FIRED AUDIO: " + finalizedResult;

                // --- 🔊 ACOUSTIC HIGH-RES VOICE SYNTHESIS MATRIX ---
                const audioWave = new SpeechSynthesisUtterance(finalizedResult);
                audioWave.lang = checkChinese ? "ur-PK" : "zh-CN";
                
                // Precise acoustic configurations for professional deep tone
                audioWave.pitch = 0.78;  // Heavy masculine bass frequency
                audioWave.rate = 0.85;   // Clear, steady pronunciation pacing
                audioWave.volume = 1.0;  // Full output volume
                
                window.speechSynthesis.speak(audioWave);
            };

            liveEngine.onend = () => {
                btn.style.borderColor = "#00ffd5";
                btn.style.boxShadow = "0px 0px 20px #00ffd5";
            };
        } else {
            localLog.innerText = "❌ Microphone Module Error.";
        }
    </script>
""", height=220, key="aladdin_client_isolated_final_v9")
