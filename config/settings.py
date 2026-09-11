import os
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv, dotenv_values

# Page Metadata
PAGE_TITLE = "CareNex • AI Career Guidance"
PAGE_ICON = "⚡"
LAYOUT = "centered"

# Default Preferences
DEFAULT_STAGE = "College Student / Undergraduate"
DEFAULT_DOMAIN = "Artificial Intelligence & Machine Learning"
DEFAULT_MODEL = "gemini-3.6-flash"

# Selection Choices
CAREER_STAGES = [
    "College Student / Undergraduate",
    "Recent Graduate / Fresher (Job Seeker)",
    "Working Professional (Upskilling)",
    "Career Switcher (Transitioning fields)",
    "High School / 12th Standard"
]

CAREER_DOMAINS = [
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
]

SUPPORTED_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest"
]

def resolve_api_key():
    """
    Resolves Gemini API key with priority:
    1. Runtime custom key entered in UI (st.session_state.custom_api_key)
    2. Streamlit Cloud Secrets (st.secrets["GEMINI_API_KEY"])
    3. OS Environment variables (GEMINI_API_KEY or Career_Guidance_Chatbot)
    4. Local .env file
    """
    # 1. Runtime UI Session Key
    try:
        if hasattr(st, "session_state") and st.session_state.get("custom_api_key"):
            key = st.session_state.custom_api_key.strip()
            if key:
                return key
    except Exception:
        pass

    # 2. Streamlit Cloud Secrets (for deployed apps on streamlit.app)
    try:
        if hasattr(st, "secrets"):
            if "GEMINI_API_KEY" in st.secrets and str(st.secrets["GEMINI_API_KEY"]).strip():
                return str(st.secrets["GEMINI_API_KEY"]).strip()
            if "Career_Guidance_Chatbot" in st.secrets and str(st.secrets["Career_Guidance_Chatbot"]).strip():
                return str(st.secrets["Career_Guidance_Chatbot"]).strip()
    except Exception:
        pass

    # 3. Environment Variables
    key = os.getenv("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()
        
    key = os.getenv("Career_Guidance_Chatbot")
    if key and key.strip():
        return key.strip()

    # 4. Local .env file
    try:
        load_dotenv(override=True)
        env_vals = dotenv_values(".env")
        if "GEMINI_API_KEY" in env_vals and env_vals["GEMINI_API_KEY"]:
            return env_vals["GEMINI_API_KEY"].strip()
            
        if "Career_Guidance_Chatbot" in env_vals and env_vals["Career_Guidance_Chatbot"]:
            return env_vals["Career_Guidance_Chatbot"].strip()
    except Exception:
        pass
        
    return ""
