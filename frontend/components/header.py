# pyrefly: ignore [missing-import]
import streamlit as st
from database.connection import is_db_connected

def render_top_header():
    """Renders the top application header bar with user profile info and bot connectivity badge."""
    connected = is_db_connected()
    status_label = "Online" if connected else "Local"

    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.markdown(f"""
        <div class="user-greeting">
            <div class="user-avatar">🧑‍💻</div>
            <div class="greeting-text">
                <h2>Hi, Explorer 👋</h2>
                <p>Domain: <strong>{st.session_state.target_domain}</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
            <div class="online-indicator">
                <div class="pulse-green"></div>
                <span>CareNex {status_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
