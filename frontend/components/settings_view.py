# pyrefly: ignore [missing-import]
import streamlit as st
from config.settings import CAREER_STAGES, CAREER_DOMAINS, SUPPORTED_MODELS, resolve_api_key
from database.connection import is_db_connected

def render_settings_view():
    """Renders the Profile and System Settings View."""
    col_set_top, col_set_back = st.columns([0.8, 0.2])
    with col_set_top:
        st.markdown("<h2 style='font-family: Outfit; margin: 0;'>⚙️ Profile & System Settings</h2>", unsafe_allow_html=True)
    with col_set_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()

    st.markdown("---")

    # 1. API Key Configuration
    st.markdown("#### 🔑 Gemini API Key Configuration")
    active_key = resolve_api_key()
    if active_key:
        masked_key = active_key[:6] + "..." + active_key[-4:] if len(active_key) > 12 else "******"
        st.success(f"🟢 Active API Key Connected: `{masked_key}`")
    else:
        st.warning("⚠️ No Gemini API key detected. Paste your key below to activate CareNex.")

    user_key_input = st.text_input(
        "Enter or Update Gemini API Key:",
        type="password",
        value=st.session_state.get("custom_api_key", ""),
        placeholder="Paste your key here (e.g. AIzaSy...)",
        help="Free API keys available at https://aistudio.google.com/apikey"
    )
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        if st.button("Save API Key 🔑", use_container_width=True):
            if user_key_input and user_key_input.strip():
                st.session_state.custom_api_key = user_key_input.strip()
                st.success("API key saved for this session!")
                st.rerun()
    with col_k2:
        if st.button("Clear Custom Key", use_container_width=True):
            st.session_state.custom_api_key = ""
            st.rerun()

    st.caption("💡 For Streamlit Cloud deployment: add `GEMINI_API_KEY = 'your_key'` to App Settings → Secrets to enable it permanently for all users.")

    st.markdown("---")

    # 2. Career Context
    st.markdown("#### 🎯 Career Profile")
    st.session_state.user_stage = st.selectbox(
        "Current Stage:",
        CAREER_STAGES,
        index=CAREER_STAGES.index(st.session_state.user_stage) if st.session_state.user_stage in CAREER_STAGES else 0
    )

    st.session_state.target_domain = st.selectbox(
        "Field of Interest:",
        CAREER_DOMAINS,
        index=CAREER_DOMAINS.index(st.session_state.target_domain) if st.session_state.target_domain in CAREER_DOMAINS else 1
    )

    st.markdown("---")

    # 3. Engine & Database
    st.markdown("#### 🤖 AI Engine & Database Status")
    st.session_state.model_choice = st.selectbox(
        "Gemini Model:",
        SUPPORTED_MODELS,
        index=SUPPORTED_MODELS.index(st.session_state.model_choice) if st.session_state.model_choice in SUPPORTED_MODELS else 0
    )

    mongo_ok = is_db_connected()
    if mongo_ok:
        st.success("🟢 MongoDB is Connected (`localhost:27017` / `career_guidance_db`)")
    else:
        st.info("🟡 MongoDB is running in In-Memory mode. (To enable cloud database on Streamlit Cloud, add `MONGO_URI` to Secrets).")

    st.markdown("---")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Return to Home", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()
    with col_cancel:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
