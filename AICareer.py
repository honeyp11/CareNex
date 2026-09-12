import os
import sys
import time
import base64
import warnings
from datetime import datetime
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv, dotenv_values
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
import importlib
import db
importlib.reload(db)

# Suppress minor runtime warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# Page Configuration & Assets
# ---------------------------------------------------------
st.set_page_config(
    page_title="CareNex • AI Career Guidance",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load Mascot Image as Base64 for instant, lossless rendering
def get_mascot_base64():
    path = os.path.join(os.path.dirname(__file__), "assets", "mascot.jpg")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

MASCOT_B64 = get_mascot_base64()

# ---------------------------------------------------------
# Modern Mobile-App UI Styling (GammaBot & Personal AI Buddy Style)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Global Dark Theme & Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #07090e !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 210, 180, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.06) 0px, transparent 50%) !important;
        background-attachment: fixed !important;
        color: #f1f5f9;
    }

    /* Constrain App Width to App-Like Dimension */
    .block-container {
        max-width: 820px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Top Bar Header */
    .app-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding: 4px 0;
    }
    .user-greeting {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d2b4 0%, #0077b6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 0 15px rgba(0, 210, 180, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.15);
    }
    .greeting-text h2 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
    }
    .greeting-text p {
        font-size: 0.8rem;
        color: #94a3b8;
        margin: 0;
    }
    .online-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 210, 180, 0.12);
        border: 1px solid rgba(0, 210, 180, 0.3);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        color: #00d2b4;
        font-weight: 600;
    }
    .pulse-green {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #00d2b4;
        box-shadow: 0 0 0 0 rgba(0, 210, 180, 0.7);
        animation: pulse-ring 2s infinite;
    }
    @keyframes pulse-ring {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 210, 180, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 7px rgba(0, 210, 180, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 210, 180, 0); }
    }

    /* Hero Mascot Banner (Like GammaBot / Personal AI Buddy) */
    .hero-card {
        background: linear-gradient(135deg, #0c2027 0%, #0d1627 50%, #09101d 100%);
        border: 1px solid rgba(0, 210, 180, 0.25);
        border-radius: 24px;
        padding: 24px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 15px 35px -10px rgba(0, 210, 180, 0.15), 0 20px 40px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    .hero-card::after {
        content: '';
        position: absolute;
        bottom: -30px; right: -30px;
        width: 140px; height: 140px;
        background: radial-gradient(circle, rgba(0, 210, 180, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-text-side {
        max-width: 60%;
    }
    .hero-tag {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #00d2b4;
        margin-bottom: 6px;
    }
    .hero-headline {
        font-family: 'Outfit', sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        margin: 0 0 10px 0;
    }
    .hero-subline {
        font-size: 0.86rem;
        color: #94a3b8;
        line-height: 1.4;
        margin-bottom: 16px;
    }
    .hero-img-side img {
        width: 155px;
        height: 155px;
        object-fit: cover;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 25px rgba(0, 210, 180, 0.3);
        border: 2px solid rgba(0, 210, 180, 0.3);
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    /* Section Titles */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 22px 0 12px 0;
    }
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-link {
        font-size: 0.8rem;
        color: #00d2b4;
        text-decoration: none;
        font-weight: 600;
    }

    /* Action Grid Cards (Mockup Style with ↗) */
    .action-card {
        background: #0f1523;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 115px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .action-card:hover {
        transform: translateY(-3px);
        border-color: #00d2b4;
        box-shadow: 0 10px 25px rgba(0, 210, 180, 0.15);
    }
    .action-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .action-card-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(0, 210, 180, 0.12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: #00d2b4;
    }
    .action-card-arrow {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 700;
        transition: color 0.2s;
    }
    .action-card:hover .action-card-arrow {
        color: #00d2b4;
        transform: translate(2px, -2px);
    }
    .action-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .action-card-sub {
        font-size: 0.72rem;
        color: #94a3b8;
        margin: 0;
    }

    /* History List Items (Mockup Style) */
    .history-card {
        background: #0f1523;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .history-card:hover {
        border-color: rgba(0, 210, 180, 0.4);
        background: #131b2d;
    }
    .history-left {
        display: flex;
        align-items: center;
        gap: 12px;
        overflow: hidden;
    }
    .history-icon-bubble {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(0, 210, 180, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .history-info h4 {
        margin: 0;
        font-size: 0.88rem;
        font-weight: 600;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 380px;
    }
    .history-info p {
        margin: 0;
        font-size: 0.72rem;
        color: #64748b;
    }

    /* Streamlit Button Overrides to Match Mockup */
    div.stButton > button {
        border-radius: 14px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: #0f1523 !important;
        color: #f1f5f9 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #00d2b4 !important;
        color: #00d2b4 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 210, 180, 0.2) !important;
    }

    /* Glowing Primary Action Button */
    .cta-neon-btn div.stButton > button {
        background: linear-gradient(135deg, #00d2b4 0%, #0096c7 100%) !important;
        color: #051318 !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 20px rgba(0, 210, 180, 0.4) !important;
    }
    .cta-neon-btn div.stButton > button:hover {
        box-shadow: 0 8px 30px rgba(0, 210, 180, 0.6) !important;
        transform: translateY(-2px) !important;
        color: #000000 !important;
    }

    /* Chat Screen Header Bar */
    .chat-header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 21, 35, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 20px;
    }
    .chat-header-bot {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .chat-header-bot img {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        border: 2px solid #00d2b4;
    }
    .chat-header-bot h3 {
        margin: 0;
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
    }
    .chat-header-bot p {
        margin: 0;
        font-size: 0.74rem;
        color: #00d2b4;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* GammaBot Chat Bubbles */
    div[data-testid="stChatMessage"] {
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 14px !important;
    }

    /* Bot Bubble - Signature GammaBot Mint/Teal Style */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(0, 210, 180, 0.15) 0%, rgba(12, 34, 38, 0.6) 100%) !important;
        border: 1px solid rgba(0, 210, 180, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    }

    /* User Bubble - Right Navy Pill */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #0f1c2e !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }

    /* Floating Rounded Chat Input (Like Mockups) */
    div[data-testid="stChatInput"] {
        background: #0f1523 !important;
        border: 1.5px solid rgba(0, 210, 180, 0.4) !important;
        border-radius: 9999px !important;
        padding: 4px 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 210, 180, 0.15) !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #00d2b4 !important;
        box-shadow: 0 0 0 2px rgba(0, 210, 180, 0.3), 0 12px 35px rgba(0, 0, 0, 0.6) !important;
    }
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #00d2b4 0%, #0096c7 100%) !important;
        color: #000000 !important;
        border-radius: 50% !important;
    }

    /* Bottom Floating App Navigation */
    .bottom-nav-bar {
        position: fixed;
        bottom: 16px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 21, 35, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 6px 18px;
        display: flex;
        align-items: center;
        gap: 28px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 210, 180, 0.15);
        z-index: 9999;
    }
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        color: #64748b;
        font-size: 0.72rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
    }
    .nav-item.active {
        color: #00d2b4;
    }
    .nav-item span {
        font-size: 1.15rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Environment & API Key Resolution
# ---------------------------------------------------------
load_dotenv(override=True)

def resolve_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()
    key = os.getenv("Career_Guidance_Chatbot")
    if key and key.strip():
        return key.strip()
    env_vals = dotenv_values(".env")
    if "GEMINI_API_KEY" in env_vals and env_vals["GEMINI_API_KEY"]:
        return env_vals["GEMINI_API_KEY"].strip()
    if "Career_Guidance_Chatbot" in env_vals and env_vals["Career_Guidance_Chatbot"]:
        return env_vals["Career_Guidance_Chatbot"].strip()
    return ""

detected_key = resolve_api_key()

# ---------------------------------------------------------
# Application State Initialization
# ---------------------------------------------------------
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"  # 'home', 'chat', 'settings'

if "user_stage" not in st.session_state:
    st.session_state.user_stage = "College Student / Undergraduate"

if "target_domain" not in st.session_state:
    st.session_state.target_domain = "Artificial Intelligence & Machine Learning"

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "gemini-3.6-flash"

if "session_id" not in st.session_state or not st.session_state.session_id:
    st.session_state.session_id = db.create_session(
        user_stage=st.session_state.user_stage,
        target_domain=st.session_state.target_domain,
        title="New Career Consultation"
    )

if "messages" not in st.session_state:
    st.session_state.messages = db.get_session_messages(st.session_state.session_id)

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ---------------------------------------------------------
# System Persona
# ---------------------------------------------------------
SYSTEM_INSTRUCTION = f"""
You are "CareNex", a world-class AI Career Counselor, Industry Mentor, and Strategic Advisor.
The user is: "{st.session_state.user_stage}" targeting: "{st.session_state.target_domain}".

Your Core Directives:
1. Provide structured, realistic, step-by-step career blueprints and actionable guidance.
2. Structure roadmaps with clear progressive milestones: Foundations → Practical Projects → Interview & Job Readiness.
3. Recommend top-tier, reputable free resources (official documentation, top GitHub roadmaps, industry certifications).
4. Emphasize actual industry standards, hiring demands, and portfolio proof.
5. If the user asks in Hindi or Hinglish, respond warmly in natural, fluent Hinglish. If in English, respond in crisp, professional English.
6. Use clean Markdown formatting: bullet points, bold keywords, comparison tables, and code snippets when appropriate.
7. Tone: Inspiring, approachable, friendly, and practical. Keep the user motivated and engaged.
"""

# =========================================================
# VIEW 1: HOME SCREEN (Mockup GammaBot / Personal AI Buddy)
# =========================================================
if st.session_state.current_view == "home":
    # 1. Top Bar Header
    is_connected = db.is_db_connected()
    status_label = "Online" if is_connected else "Local"

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

    # 2. Hero Mascot Card
    mascot_img_html = f'<img src="data:image/jpeg;base64,{MASCOT_B64}" alt="CareNex">' if MASCOT_B64 else '<div style="font-size: 5rem;">🤖</div>'
    
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-text-side">
            <div class="hero-tag">⚡ CareNex AI Mentor</div>
            <h1 class="hero-headline">Ask Your Career Question</h1>
            <p class="hero-subline">Meet CareNex! Your personalized AI counselor for customized roadmaps, skill audits, and interview preparation.</p>
        </div>
        <div class="hero-img-side">
            {mascot_img_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero CTA Button to Start Chatting
    c_btn1, c_btn2, c_btn3 = st.columns([0.05, 0.9, 0.05])
    with c_btn2:
        st.markdown('<div class="cta-neon-btn">', unsafe_allow_html=True)
        if st.button("💬 Chat with CareNex Now", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. Quick Action Grid (2x2 matching the reference mockups)
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">⚡ Quick Starters</h3>
    </div>
    """, unsafe_allow_html=True)

    q1, q2 = st.columns(2)
    with q1:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">🗺️</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Career Roadmap</p>
                <p class="action-card-sub">0 to job-ready milestone plan</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Roadmap ↗", key="home_btn_roadmap", use_container_width=True):
            st.session_state.pending_prompt = f"Please give me a realistic, step-by-step 6-month roadmap to become job-ready in {st.session_state.target_domain}. I am a {st.session_state.user_stage}."
            st.session_state.current_view = "chat"
            st.rerun()

    with q2:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">⚡</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Top Skills 2026</p>
                <p class="action-card-sub">Highest demand tools & technologies</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Skills ↗", key="home_btn_skills", use_container_width=True):
            st.session_state.pending_prompt = f"What are the top 5 highest paying and most demanded skills right now in {st.session_state.target_domain}? Give practical examples of how to learn them."
            st.session_state.current_view = "chat"
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    q3, q4 = st.columns(2)
    with q3:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">💼</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Resume & Projects</p>
                <p class="action-card-sub">Standout portfolio ideas</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Review Projects ↗", key="home_btn_resume", use_container_width=True):
            st.session_state.pending_prompt = f"What kind of portfolio projects and resume points will help me stand out to recruiters in {st.session_state.target_domain} as a {st.session_state.user_stage}?"
            st.session_state.current_view = "chat"
            st.rerun()

    with q4:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">🎤</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Mock Interview</p>
                <p class="action-card-sub">Technical & behavioral drills</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Interview Prep ↗", key="home_btn_interview", use_container_width=True):
            st.session_state.pending_prompt = f"What are the most common technical and behavioral interview questions asked for junior to mid roles in {st.session_state.target_domain}, and how should I answer them?"
            st.session_state.current_view = "chat"
            st.rerun()

    # 4. Trending Topics Tags (Mockup Style)
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">🔥 Trending Career Paths</h3>
    </div>
    """, unsafe_allow_html=True)

    t_cols = st.columns(4)
    topics = [
        ("🤖 AI Engineer", "Artificial Intelligence & Machine Learning"),
        ("🌐 Full Stack", "Software Development & Web Tech"),
        ("☁️ Cloud DevOps", "Cloud Computing & DevOps"),
        ("🛡️ Cybersecurity", "Cybersecurity & Ethical Hacking")
    ]
    for i, (tag_label, domain_name) in enumerate(topics):
        with t_cols[i]:
            if st.button(tag_label, key=f"topic_{i}", use_container_width=True):
                st.session_state.target_domain = domain_name
                st.session_state.pending_prompt = f"Give me an introductory roadmap and essential starter guide for becoming a {domain_name}."
                st.session_state.current_view = "chat"
                st.rerun()

    # 5. History Chat (Loaded from MongoDB)
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">🕒 Recent Consultations</h3>
        <span class="section-link">Stored in MongoDB</span>
    </div>
    """, unsafe_allow_html=True)

    recent_sessions = db.list_sessions(limit=5)
    if recent_sessions:
        for s in recent_sessions:
            sid = s["session_id"]
            title = s.get("title") or "Career Consultation"
            count = s.get("message_count", 0)
            
            c_hist_left, c_hist_btn, c_hist_dl = st.columns([0.68, 0.16, 0.16])
            with c_hist_left:
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-left">
                        <div class="history-icon-bubble">💬</div>
                        <div class="history-info">
                            <h4>{title}</h4>
                            <p>{count} messages • {s.get('target_domain', 'General')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_hist_btn:
                if st.button("Open >", key=f"hist_open_{sid}", use_container_width=True):
                    st.session_state.session_id = sid
                    st.session_state.messages = db.get_session_messages(sid)
                    st.session_state.current_view = "chat"
                    st.rerun()
            with c_hist_dl:
                with st.popover("📥", help="Export this chat in PDF, Text, or Markdown"):
                    st.caption(f"Export: {title[:20]}...")
                    try:
                        hist_pdf = db.export_session_as_pdf(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📄 PDF (.pdf)", data=hist_pdf, file_name=f"carenex_{sid[:8]}.pdf", mime="application/pdf", key=f"dl_pdf_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"PDF unavailable: {err}")
                    try:
                        hist_txt = db.export_session_as_text(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📝 Text (.txt)", data=hist_txt, file_name=f"carenex_{sid[:8]}.txt", mime="text/plain", key=f"dl_txt_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"Text unavailable: {err}")
                    try:
                        hist_md = db.export_session_as_markdown(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📑 Markdown (.md)", data=hist_md, file_name=f"carenex_{sid[:8]}.md", mime="text/markdown", key=f"dl_md_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"Markdown unavailable: {err}")
    else:
        st.caption("No past consultations found. Start your first session above!")

    # Top/Bottom navigation toggles
    st.markdown("---")
    nav_c1, nav_c2, nav_c3 = st.columns(3)
    with nav_c1:
        st.button("🏠 Home (Active)", disabled=True, use_container_width=True)
    with nav_c2:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
    with nav_c3:
        if st.button("⚙️ Settings / Profile", use_container_width=True):
            st.session_state.current_view = "settings"
            st.rerun()


# =========================================================
# VIEW 2: DEDICATED CHAT VIEW (GammaBot Mockup Style)
# =========================================================
elif st.session_state.current_view == "chat":
    # 1. Chat App Header Bar
    ch_col1, ch_col2, ch_col3, ch_col4 = st.columns([0.20, 0.46, 0.16, 0.18])
    with ch_col1:
        if st.button("← Home", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()
    with ch_col2:
        mascot_thumb_html = f'<img src="data:image/jpeg;base64,{MASCOT_B64}" alt="bot">' if MASCOT_B64 else '🤖'
        st.markdown(f"""
        <div class="chat-header-bot">
            {mascot_thumb_html}
            <div>
                <h3>CareNex</h3>
                <p><span class="pulse-green"></span> Online • {st.session_state.model_choice}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with ch_col3:
        if st.button("➕ New", help="Start new conversation", use_container_width=True):
            new_sid = db.create_session(user_stage=st.session_state.user_stage, target_domain=st.session_state.target_domain)
            st.session_state.session_id = new_sid
            st.session_state.messages = []
            st.rerun()
    with ch_col4:
        with st.popover("📥 Export", use_container_width=True):
            if not st.session_state.messages:
                st.info("💡 **Consultation is Empty**\n\nAsk CareNex a question or pick a starter prompt below. Once you start chatting, you can export your complete consultation report here.")
            else:
                msg_count = len(st.session_state.messages)
                st.markdown(f"<p style='font-size: 0.85rem; font-weight: 700; color: #00d2b4; margin-bottom: 6px;'>Export Consultation ({msg_count} messages):</p>", unsafe_allow_html=True)
                
                # PDF Download
                pdf_bytes = db.export_session_as_pdf(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📄 PDF Document (.pdf)",
                    data=pdf_bytes,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.pdf",
                    mime="application/pdf",
                    key=f"chat_export_pdf_{msg_count}",
                    use_container_width=True
                )

                # Plain Text Download
                txt_data = db.export_session_as_text(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📝 Plain Text (.txt)",
                    data=txt_data,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.txt",
                    mime="text/plain",
                    key=f"chat_export_txt_{msg_count}",
                    use_container_width=True
                )

                # Markdown Download
                md_data = db.export_session_as_markdown(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📑 Markdown (.md)",
                    data=md_data,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.md",
                    mime="text/markdown",
                    key=f"chat_export_md_{msg_count}",
                    use_container_width=True
                )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 2. Render Existing Messages or Interactive Empty Welcome Card
    if not st.session_state.messages and not st.session_state.pending_prompt:
        st.markdown(f"""
        <div style="text-align: center; padding: 28px 20px 20px 20px; background: rgba(15, 21, 35, 0.7); border-radius: 20px; border: 1px solid rgba(0, 210, 180, 0.25); margin-bottom: 20px;">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">⚡</div>
            <h3 style="color: #ffffff; margin: 0 0 6px 0; font-family: 'Outfit', sans-serif;">How can CareNex guide your career today?</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 480px; margin: 0 auto 16px auto;">
                Select a quick prompt below or type any question to begin personalized mentorship in <strong>{st.session_state.target_domain}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            if st.button("🗺️ Build My 6-Month Roadmap", key="chat_starter_roadmap", use_container_width=True):
                st.session_state.pending_prompt = f"Give me a step-by-step 6-month roadmap to become job-ready in {st.session_state.target_domain} as a {st.session_state.user_stage}."
                st.rerun()
            if st.button("💼 Best Portfolio Projects", key="chat_starter_projects", use_container_width=True):
                st.session_state.pending_prompt = f"What are 3 high-impact portfolio projects that recruiters love for {st.session_state.target_domain}?"
                st.rerun()
        with c_s2:
            if st.button("⚡ Top Skills to Learn First", key="chat_starter_skills", use_container_width=True):
                st.session_state.pending_prompt = f"What are the top 5 highest-paying and most demanded skills in {st.session_state.target_domain} right now?"
                st.rerun()
            if st.button("🎤 Practice Interview Q&A", key="chat_starter_interview", use_container_width=True):
                st.session_state.pending_prompt = f"Ask me the #1 most common interview question for {st.session_state.target_domain} and guide me on how to answer it."
                st.rerun()

    for msg in st.session_state.messages:
        is_user = (msg["role"] == "user")
        with st.chat_message(msg["role"], avatar="🧑‍💻" if is_user else "⚡"):
            st.markdown(msg["content"])

    # 3. Interactive Quick Follow-up Chips (When Conversation is Active)
    if st.session_state.messages:
        st.markdown("<div style='margin-top: 14px; margin-bottom: 6px;'><span style='font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;'>Quick Follow-Ups (Tap to Ask):</span></div>", unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            if st.button("📌 Next Steps", key="chip_next", use_container_width=True):
                st.session_state.pending_prompt = "What are my immediate next 3 action steps based on your advice above?"
                st.rerun()
        with fc2:
            if st.button("💼 Project Ideas", key="chip_proj", use_container_width=True):
                st.session_state.pending_prompt = "Give me 2 real-world hands-on project ideas to practice these skills."
                st.rerun()
        with fc3:
            if st.button("📄 Resume Tips", key="chip_res", use_container_width=True):
                st.session_state.pending_prompt = "How should I describe these skills and projects on my resume to pass ATS scanners?"
                st.rerun()
        with fc4:
            if st.button("🎤 Interview Prep", key="chip_int", use_container_width=True):
                st.session_state.pending_prompt = "What questions would an interviewer ask about this topic, and what is the ideal answer?"
                st.rerun()

    # 4. Handle Input (from chat_input or pending starter action)
    prompt_to_send = None
    if st.session_state.pending_prompt:
        prompt_to_send = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
    elif user_input := st.chat_input("Ask CareNex anything about your career roadmap, skills, resume..."):
        prompt_to_send = user_input

    if prompt_to_send:
        if not detected_key:
            st.error("⚠️ Please configure your Gemini API Key in `.env` or in Settings.")
            st.stop()

        # Save user turn to state and MongoDB
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        db.save_message(st.session_state.session_id, "user", prompt_to_send)

        if len(st.session_state.messages) == 1:
            db.update_session_title(st.session_state.session_id, prompt_to_send)

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt_to_send)

        # Stream Assistant turn
        with st.chat_message("assistant", avatar="⚡"):
            response_placeholder = st.empty()
            response_placeholder.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; color: #00d2b4; font-size: 0.88rem;">
                <span class="pulse-green"></span> <em>CareNex is thinking & preparing your guidance...</em>
            </div>
            """, unsafe_allow_html=True)

            try:
                client = genai.Client(api_key=detected_key)

                history_context = ""
                for prev in st.session_state.messages[-6:-1]:
                    history_context += f"{prev['role'].capitalize()}: {prev['content']}\n"

                full_prompt = f"{history_context}\nUser: {prompt_to_send}\n(Provide structured, practical advice with markdown formatting)"

                chat = client.chats.create(
                    model=st.session_state.model_choice,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )

                response_text = ""
                for chunk in chat.send_message_stream(full_prompt):
                    if chunk.text:
                        response_text += chunk.text
                        response_placeholder.markdown(response_text + "▌")

                response_placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                db.save_message(st.session_state.session_id, "assistant", response_text)
                st.rerun()

            except Exception as primary_err:
                # Fallback to backup models
                fallback_models = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]
                recovered = False
                for fb in fallback_models:
                    if fb == st.session_state.model_choice:
                        continue
                    try:
                        response_placeholder.markdown(f"🔄 *Optimizing response with {fb}...*")
                        client = genai.Client(api_key=detected_key)
                        chat = client.chats.create(
                            model=fb,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.7,
                            )
                        )
                        fallback_text = ""
                        for chunk in chat.send_message_stream(prompt_to_send):
                            if chunk.text:
                                fallback_text += chunk.text
                                response_placeholder.markdown(fallback_text + "▌")

                        if fallback_text:
                            response_placeholder.markdown(fallback_text)
                            st.session_state.messages.append({"role": "assistant", "content": fallback_text})
                            db.save_message(st.session_state.session_id, "assistant", fallback_text)
                            recovered = True
                            st.rerun()
                            break
                    except Exception:
                        continue

                if not recovered:
                    response_placeholder.error(f"Error: {str(primary_err)}")


# =========================================================
# VIEW 3: SETTINGS & PROFILE VIEW
# =========================================================
elif st.session_state.current_view == "settings":
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
        [
            "College Student / Undergraduate",
            "Recent Graduate / Fresher (Job Seeker)",
            "Working Professional (Upskilling)",
            "Career Switcher (Transitioning fields)",
            "High School / 12th Standard"
        ],
        index=[
            "College Student / Undergraduate",
            "Recent Graduate / Fresher (Job Seeker)",
            "Working Professional (Upskilling)",
            "Career Switcher (Transitioning fields)",
            "High School / 12th Standard"
        ].index(st.session_state.user_stage) if st.session_state.user_stage in [
            "College Student / Undergraduate",
            "Recent Graduate / Fresher (Job Seeker)",
            "Working Professional (Upskilling)",
            "Career Switcher (Transitioning fields)",
            "High School / 12th Standard"
        ] else 0
    )

    st.session_state.target_domain = st.selectbox(
        "Field of Interest:",
        [
            "Software Development & Web Tech",
            "Artificial Intelligence & Machine Learning",
            "Data Analytics & Business Intelligence",
            "Cloud Computing & DevOps",
            "Cybersecurity & Ethical Hacking",
            "UI/UX Design & Product Design",
            "Product Management & Business Strategy",
            "Finance, Investment Banking & Fintech",
            "Digital Marketing & Growth",
            "Government Exams & Public Sector",
            "Other / Undecided"
        ],
        index=[
            "Software Development & Web Tech",
            "Artificial Intelligence & Machine Learning",
            "Data Analytics & Business Intelligence",
            "Cloud Computing & DevOps",
            "Cybersecurity & Ethical Hacking",
            "UI/UX Design & Product Design",
            "Product Management & Business Strategy",
            "Finance, Investment Banking & Fintech",
            "Digital Marketing & Growth",
            "Government Exams & Public Sector",
            "Other / Undecided"
        ].index(st.session_state.target_domain) if st.session_state.target_domain in [
            "Software Development & Web Tech",
            "Artificial Intelligence & Machine Learning",
            "Data Analytics & Business Intelligence",
            "Cloud Computing & DevOps",
            "Cybersecurity & Ethical Hacking",
            "UI/UX Design & Product Design",
            "Product Management & Business Strategy",
            "Finance, Investment Banking & Fintech",
            "Digital Marketing & Growth",
            "Government Exams & Public Sector",
            "Other / Undecided"
        ] else 1
    )

    st.markdown("---")

    # Engine & Database
    st.markdown("#### 🤖 AI Engine & Database Status")
    st.session_state.model_choice = st.selectbox(
        "Gemini Model:",
        ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"],
        index=["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"].index(st.session_state.model_choice) if st.session_state.model_choice in ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"] else 0
    )

    mongo_ok = db.is_db_connected()
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
