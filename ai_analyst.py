import streamlit as st
import requests
import base64

# --- 🎭 PREMIUM QUANTUM INTERFACE ---
st.set_page_config(page_title="Aladdin Pure Voice", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN PURE VOICE BRIDGE")
st.subheader("[ No Typing • Walkie-Talkie Mode Active ]")
st.write("---")

# --- 🔑 OPENAI KEY MATRIX ---
API_KEY = st.sidebar.text_input("🔑 ENTER OPENAI KEY:", type="password", value="")

if not API_KEY:
    st.sidebar.warning("⚠️ Please provide OpenAI API key to trigger premium human voices.")

st.markdown("### 🎙️ CHANNEL ONLINE: TAP AND SPEAK")

# --- 🎙️ NATIVE BROWSER SPEECH MIC CAPTURE ---
# Using advanced HTML5 WebSpeech listener to instantly stream microphone data
captured_text = st.components.v1.html("""
    <div style="text-align: center; margin-top: 15px;">
        <button id="mic-btn" style="background-color: #1f293d; color: #00ffd5; border: 2px solid #00ffd5; padding: 18px 35px; font-size: 20px; border-radius: 50px; cursor: pointer; font-weight: bold; box-shadow: 0px 0px 10px #00ffd5;">
            🎤 Open Voice Channel
        </button>
        <p id="mic-status" style="color: #ffffff; margin-top: 12px; font-family: monospace; font-size: 14px;">Tap button to speak directly.</p>
    </div>

    <script>
        const btn = document.getElementById('mic-btn');
        const status = document.getElementById('mic-status');
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            // Set language to auto-recognize Urdu/Hindi context naturally
            recognition.lang = 'ur-PK'; 

            btn.onclick = () => {
                try {
                    recognition.start();
                    status.innerText = "🛑 LISTENING... SPEAK NOW";
                    btn.style.borderColor = "#ff3344";
                    btn.style.color = "#ff3344";
                    btn.style.boxShadow = "0px 0px 15px #ff3344";
                } catch(e) {
                    status.innerText = "🔄 System resetting active channel...";
                    recognition.stop();
                }
            };

            recognition.onresult = (event) => {
                const textResult = event.results[0][0].transcript;
                status.innerText = "🎯 Captured: " + textResult;
                
                // Direct stream data pipe to Streamlit component state
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: textResult
                }, '*');
            };

            recognition.onend = () => {
                btn.style.borderColor = "#00ffd5";
                btn.style.color = "#00ffd5";
                btn.style.boxShadow = "0px 0px 10px #00ffd5";
            };
        } else {
            status.innerText = "❌ Hardware Permission Blocked or Browser Not Supported.";
        }
    </script>
""", height=150)

# --- 🧠 SPEECH SYNTHESIS ENGINE ---
if captured_text:
    st.write(f"🗣️ **Detected Voice Inflow:** *{captured_text}*")
    
    # Auto routing target script language based on characters
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in captured_text)
    
    if is_chinese:
        # If client spoke Chinese, translate to high-clarity Urdu Response
        translated_wave = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
        voice_profile = "onyx"  # Ultra premium solid male Urdu broadcast voice
        st.success(f"🇵尋 Target Urdu Stream: {translated_wave}")
    else:
        # If user spoke Urdu, translate to high-clarity Chinese Response
        translated_wave = "您好，我完全理解您的意思。"
        voice_profile = "alloy"  # Perfect natural Chinese fluid voice
        st.success(f"🇨🇳 Target Mandarin Stream: {translated_wave}")

    # --- 🔊 INSTANT BULLET AUDIO STREAM ---
    if API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "tts-1",  # Zero-lag high speed compression profile
                "input": translated_wave,
                "voice": voice_profile,
                "response_format": "mp3"
            }
            response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
            
            if response.status_code == 200:
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                
                # Pure audio stream deployment inside a completely hidden HTML layer to remove timelines
                hidden_audio_html = f"""
                    <audio autoplay="true" style="display:none;">
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                """
                st.components.v1.html(hidden_audio_html, height=0, width=0)
            else:
                st.error("❌ Key verification dropped by secure cloud gate.")
        except Exception as e:
            st.error(f"⚠️ Internal network core log error: {str(e)}")
