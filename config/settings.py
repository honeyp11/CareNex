import os
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
    """Resolves Gemini API key from environment variables or .env file."""
    load_dotenv(override=True)
    
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
