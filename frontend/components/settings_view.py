# pyrefly: ignore [missing-import]
import streamlit as st
from config.settings import CAREER_STAGES, CAREER_DOMAINS, SUPPORTED_MODELS
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

    # Career Context
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

    # Engine & Database
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
        st.warning("🟡 MongoDB is in In-Memory fallback mode")

    st.markdown("---")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Save & Return to Home", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()
    with col_cancel:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
