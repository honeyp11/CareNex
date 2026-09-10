import os
import base64
# pyrefly: ignore [missing-import]
import streamlit as st

def get_mascot_base64() -> str:
    """Loads the 3D robot mascot image as base64 for instant, lossless rendering."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "assets", "mascot.jpg")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def apply_app_styles():
    """Injects the complete modern mobile-app UI CSS design system."""
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

        /* Hero Mascot Banner */
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

        /* Action Grid Cards */
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

        /* History List Items */
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
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
        }
        .history-info {
            overflow: hidden;
        }
        .history-info h4 {
            font-family: 'Outfit', sans-serif;
            font-size: 0.88rem;
            font-weight: 600;
            color: #f1f5f9;
            margin: 0 0 2px 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .history-info p {
            font-size: 0.72rem;
            color: #64748b;
            margin: 0;
        }

        /* CTA Neon Button */
        .cta-neon-btn .stButton > button {
            background: linear-gradient(135deg, #00d2b4 0%, #008be3 100%) !important;
            color: #050b14 !important;
            font-weight: 700 !important;
            font-size: 1.02rem !important;
            border-radius: 16px !important;
            border: none !important;
            padding: 14px 24px !important;
            box-shadow: 0 8px 25px rgba(0, 210, 180, 0.35) !important;
            transition: all 0.25s ease !important;
        }
        .cta-neon-btn .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 30px rgba(0, 210, 180, 0.5) !important;
        }

        /* Chat View Elements */
        .chat-header-bot {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 4px 0 14px 0;
        }
        .chat-header-bot img {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            border: 2px solid #00d2b4;
            box-shadow: 0 0 12px rgba(0, 210, 180, 0.4);
            object-fit: cover;
        }
        .chat-header-bot h3 {
            font-family: 'Outfit', sans-serif;
            margin: 0;
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
            gap: 6px;
        }

        /* Floating Bottom Tab Bar */
        .app-bottom-nav {
            position: fixed;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 32px);
            max-width: 460px;
            background: rgba(15, 21, 35, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 9999px;
            padding: 10px 24px;
            display: flex;
            justify-content: space-around;
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
