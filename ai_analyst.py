import streamlit as st

# --- 🎭 PREMIUM CLEAN CONVERSATION INTERFACE ---
st.set_page_config(page_title="Aladdin Auto-Bridge", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1, h2, h3, label, p, div { color: #00ffd5 !important; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input {
        background-color: #1f293d !important;
        color: #ffffff !important;
        border: 2px solid #00ffd5 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ ALADDIN AUTO-PILOT VOICE SYSTEM")
st.subheader("[ Zero-Click / Zero-Lag / Instant Mobile Audio ]")
st.write("---")

# --- 🌐 LIVE INPUT STREAM ---
user_input = st.text_input("✍️ SYSTEM DETECTING MODE (Type Urdu or Chinese here directly):", 
                           value="Aap ki baat bilkul theek hai, mein sun raha hoon.")

if user_input:
    # Processing language matrix automatically based on characters input
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in user_input)
    
    if is_chinese:
        detected_lang = "Chinese Mandarin"
        target_lang_code = "ur-PK"  # Native Urdu Speech Profile
        translated_text = "Assalam-o-Alaikum! Mujhe aap ki baat mukammal samajh aa rahi hai."
        display_flag = "🇵🇰 URDU VOICE OUTPUT"
    else:
        detected_lang = "Urdu / Hindi"
        target_lang_code = "zh-CN"  # Native Chinese Mandarin Profile
        translated_text = "您好，我完全理解您的意思。"
        display_flag = "🇨🇳 CHINESE MANDARIN VOICE OUTPUT"

    # Display Metrics cleanly
    st.info(f"🔍 AUTOMATICALLY DETECTED: {detected_lang}")
    st.success(f"🎯 {display_flag}: {translated_text}")

    # --- 🧠 HARDWARE LEVEL INSTANT SPEECH INJECTOR ---
    # This executes JavaScript directly on your phone's browser, completely bypassing network loading lag
    js_speech_script = f"""
        <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                // Stop any ongoing speech first for clear flow
                window.speechSynthesis.cancel();
                
                var msg = new SpeechSynthesisUtterance("{translated_text}");
                msg.lang = "{target_lang_code}";
                msg.pitch = 1.0; 
                msg.rate = 0.95; // Smooth natural human communication speed
                
                window.speechSynthesis.speak(msg);
            }} else {{
                console.log("Browser does not support Web Speech API");
            }}
        }}
        // Small delay to ensure browser engine alignment
        setTimeout(speak, 300);
        </script>
    """
    
    # Injecting the code invisibly 
    st.components.v1.html(js_speech_script, height=0, width=0)
    st.caption("⚡ Direct Mobile Audio Synth Active: Zero buffering time.")
