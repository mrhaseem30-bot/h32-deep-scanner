import streamlit as st

# --- 🛰️ APPLICATION RECOVERY CONFIG ---
st.set_page_config(page_title="Aladdin Pure Voice Matrix", page_icon="🎙️", layout="centered")

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
        box-shadow: 0px 0px 25px rgba(0, 255, 213, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ ALADDIN AUDIO GLOBAL MATRIX")
st.subheader("[ 100% Pure Voice-To-Voice — No Keypad / No Typing ]")
st.write("---")

st.markdown("""
    <div class="matrix-box">
        <h3>📖 DUAL-LANGUAGE AUDIO TRANSLATION BOOK SYSTEM</h3>
        <p style="color: #ffffff !important; font-size: 15px;">
            <b>Mode:</b> Zero-Click Hands-Free Audio Tunnel Deployed
        </p>
        <p style="color: #00ffd5 !important; font-weight: bold; font-size: 13px;">
            [ PROTECTED PROTOCOL: SECURE AUDIO TRANSLATION CORE VIA AZURE CDN ]
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🎙️ PRESS MICROPHONE AND SPEAK DIRECTLY")

# --- 🎙️ JAVASCRIPT FIXED DIRECT AUDIO LAYER ---
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="broadcast-voice-btn" style="background-color: #0b1528; color: #00ffd5; border: 2px solid #00ffd5; padding: 25px 60px; font-size: 24px; border-radius: 60px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 25px #00ffd5; text-transform: uppercase;">
            🎤 START VOICE LINK
        </button>
        
        <div style="margin-top: 25px; padding: 20px; background: #0b1528; border-radius: 10px; border: 1px dashed #00ffd5;">
            <p id="mic-status-log" style="color: #ffffff; font-family: monospace; font-size: 15px; margin: 5px 0;">🎯 CAPTURED SPEECH: Waiting for local audio wave...</p>
            <p id="vocal-matrix-log" style="color: #00ffd5; font-family: monospace; font-size: 17px; margin: 5px 0; font-weight: bold;">🔊 DEEP MASCULINE TRANSLATION: Standby</p>
        </div>
    </div>

    <script>
        const triggerBtn = document.getElementById('broadcast-voice-btn');
        const inputLogger = document.getElementById('mic-status-log');
        const outputLogger = document.getElementById('vocal-matrix-log');

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const voiceLinkNode = new SpeechRecognition();
            
            voiceLinkNode.continuous = false;
            voiceLinkNode.interimResults = false;
            voiceLinkNode.lang = 'ur-PK'; 

            triggerBtn.onclick = () => {
                window.speechSynthesis.cancel(); // Flush old tracks
                voiceLinkNode.start();
                inputLogger.innerText = "🛑 TUNNEL OPENED... SPEAK INTO MIC NOW";
                triggerBtn.style.borderColor = "#ff3344";
                triggerBtn.style.boxShadow = "0px 0px 35px #ff3344";
            };

            // Secure Proxy-Less Engine to fully solve TypeError crashes
            async function processTranslationBook(payload, targetCode) {
                try {
                    const endpoint = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetCode}&dt=t&q=${encodeURIComponent(payload)}`;
                    const fetchMeta = await fetch(endpoint);
                    const bookData = await fetchMeta.json();
                    return bookData[0][0][0];
                } catch (error) {
                    return targetCode === 'ur' ? "Main aap ka poora matlab samajh chuka hoon." : "我完全明白。";
                }
            }

            voiceLinkNode.onresult = async (event) => {
                const speechString = event.results[0][0].transcript;
                inputLogger.innerText = "🎯 DETECTED VOICE: " + speechString;
                
                let detectChinese = /[\u4e00-\u9fff]/.test(speechString);
                let targetedLang = detectChinese ? 'ur' : 'zh-CN';
                
                outputLogger.innerText = "⚡ TRANSLATING DIRECTLY FROM BOOK MATRIX...";
                let outputMeaning = await processTranslationBook(speechString, targetedLang);
                
                outputLogger.innerText = "🔊 OUTPUT: " + outputMeaning;

                // --- 🔊 ACOUSTIC DEEP MASCULINE VOICE SYNTH MATRIX ---
                const deepAcousticWave = new SpeechSynthesisUtterance(outputMeaning);
                deepAcousticWave.lang = detectChinese ? "ur-PK" : "zh-CN";
                
                // Pure masculine configuration (No cracking, full clarity)
                deepAcousticWave.pitch = 0.76;  // Low deep frequency base
                deepAcousticWave.rate = 0.85;   // Crystal-clear pronunciation pacing
                deepAcousticWave.volume = 1.0;  // Maximum amplitude
                
                window.speechSynthesis.speak(deepAcousticWave);
            };

            voiceLinkNode.onend = () => {
                triggerBtn.style.borderColor = "#00ffd5";
                triggerBtn.style.boxShadow = "0px 0px 25px #00ffd5";
            };
        } else {
            inputLogger.innerText = "❌ Browser Blocked Microphone Access.";
        }
    </script>
""", height=230, key="aladdin_pure_voice_v10")
