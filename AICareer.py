import warnings
# pyrefly: ignore [missing-import]
import streamlit as st
from config.settings import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    DEFAULT_STAGE,
    DEFAULT_DOMAIN,
    DEFAULT_MODEL,
    resolve_api_key
)
from database.session_repo import create_session, get_session_messages
from frontend.styles import apply_app_styles
from frontend.components import (
    render_home_view,
    render_chat_view,
    render_settings_view
)

# Suppress minor runtime warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# Page Configuration & Modern Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="collapsed"
)

apply_app_styles()

# ---------------------------------------------------------
# API Key & State Initialization
# ---------------------------------------------------------
detected_key = resolve_api_key()

if "current_view" not in st.session_state:
    st.session_state.current_view = "home"

if "user_stage" not in st.session_state:
    st.session_state.user_stage = DEFAULT_STAGE

if "target_domain" not in st.session_state:
    st.session_state.target_domain = DEFAULT_DOMAIN

if "model_choice" not in st.session_state:
    st.session_state.model_choice = DEFAULT_MODEL

if "session_id" not in st.session_state or not st.session_state.session_id:
    st.session_state.session_id = create_session(
        user_stage=st.session_state.user_stage,
        target_domain=st.session_state.target_domain,
        title="New Career Consultation"
    )

if "messages" not in st.session_state:
    st.session_state.messages = get_session_messages(st.session_state.session_id)

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ---------------------------------------------------------
# View Router
# ---------------------------------------------------------
if st.session_state.current_view == "home":
    render_home_view()
elif st.session_state.current_view == "chat":
    render_chat_view(detected_key=detected_key)
elif st.session_state.current_view == "settings":
    render_settings_view()
