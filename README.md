# CareNex-
> **⚡ CareNex — Next-Generation AI Career Counselor & Guidance Platform**

CareNex is an interactive, intelligent career counseling web application powered by **Google Gemini 3.6 Flash** and backed by **MongoDB**. Designed with a modern, mobile-first dark aesthetic, CareNex provides tailored career roadmaps, interview preparation, portfolio project recommendations, and automated PDF/Plaintext/Markdown report exports.

---

## ✨ Key Features

- **🎯 Personalized Career Roadmaps:** Tailors guidance dynamically based on your career stage (Student, Fresher, Working Professional, Career Switcher) and target domain.
- **⚡ Real-Time Streaming Mentorship:** Low-latency streaming advice with automatic multi-model fallback cascade (`gemini-3.6-flash` → `gemini-3.5-flash-lite` → `gemini-flash-latest`).
- **📥 3-in-1 Report Export:** Download your entire consultation report instantly as:
  - 📄 **PDF Document (`.pdf`)**: Formatted layout, clean headers, and sanitized typography.
  - 📝 **Plain Text (`.txt`)**: Clean ASCII text report.
  - 📑 **Markdown (`.md`)**: Structured Markdown file with roadmap phases and bullet points.
- **💾 Full MongoDB Persistence:** Automatic persistence of consultation sessions and messages with chronological history retrieval.
- **🚀 Interactive Quick Follow-Ups:** 1-tap follow-up chips (`📌 Next Steps`, `💼 Project Ideas`, `📄 Resume Tips`, `🎤 Interview Prep`) for an effortless chatting experience.
- **🎨 Modern Mobile-App UI:** Dark glassmorphism, animated 3D robot mascot, pulsing online status indicator, and interactive action cards.

---

## 🏗️ Modular Architecture

```text
CareNex/
│
├── .env.example                      # Environment variables template
├── requirements.txt                  # Python dependencies
├── AICareer.py                       # Lightweight Application Entry Point (~65 lines)
├── db.py                             # Backwards-compatible facade module
│
├── config/                           # Application Configurations
│   ├── __init__.py
│   └── settings.py                   # Canonical career domains, stages, models, and API key resolver
│
├── database/                         # Database Layer (MongoDB)
│   ├── __init__.py                   # Package exports
│   ├── connection.py                 # PyMongo client singleton with health check
│   └── session_repo.py               # Sessions & Messages CRUD operations
│
├── backend/                          # Backend Services Layer
│   ├── __init__.py                   # Package exports
│   ├── ai_service.py                 # Gemini client, dynamic persona & response streaming
│   └── export_service.py             # PDF, Plaintext (.txt), and Markdown (.md) generators
│
├── frontend/                         # Frontend UI Layer
│   ├── __init__.py
│   ├── styles.py                     # CSS design system, dark mode & animations
│   └── components/                   # Modular UI Components & Views
│       ├── __init__.py
│       ├── header.py                 # Top bar header, greeting & online badge
│       ├── home_view.py              # Home screen (Hero mascot, quick actions, history list)
│       ├── chat_view.py              # Chat view (Header, message history, follow-up chips, export)
│       └── settings_view.py          # Settings view (Profile stage, domain, model, DB status)
│
└── assets/                           # Media & brand assets
    └── mascot.jpg                    # CareNex 3D mascot avatar
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/honeyp11/CareNex-.git
cd CareNex-
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your **Google Gemini API Key**:
```env
GEMINI_API_KEY=your_actual_api_key_here
MONGO_URI=mongodb://localhost:27017
DB_NAME=career_guidance_db
```

### 5. Launch the Application
```bash
streamlit run AICareer.py
```
Open **`http://localhost:8501`** in your browser to start using CareNex!

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) with custom Vanilla CSS & Google Fonts (Outfit, Plus Jakarta Sans)
- **AI Engine:** [Google GenAI SDK](https://ai.google.dev/) (`gemini-3.6-flash`, `gemini-3.5-flash-lite`)
- **Database:** [MongoDB](https://www.mongodb.com/) via [PyMongo](https://pymongo.readthedocs.io/)
- **Document Generation:** [fpdf2](https://py-pdf.github.io/fpdf2/) (PDF generation with custom headers and footers)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
