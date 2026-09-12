import os
import uuid
from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
import pymongo
# pyrefly: ignore [missing-import]
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv(override=True)

DEFAULT_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DEFAULT_DB_NAME = os.getenv("MONGO_DB_NAME", "career_guidance_db")

_client = None
_db = None

def get_db(uri=None, db_name=None):
    """
    Returns the MongoDB database instance.
    Uses short timeout (2s) so failures don't block the UI.
    """
    global _client, _db
    if _db is not None:
        return _db

    target_uri = uri or DEFAULT_MONGO_URI
    target_db_name = db_name or DEFAULT_DB_NAME

    try:
        _client = pymongo.MongoClient(
            target_uri,
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000
        )
        # Verify connection
        _client.admin.command('ping')
        _db = _client[target_db_name]
        
        # Ensure indexes for fast querying
        _db.sessions.create_index([("session_id", pymongo.ASCENDING)], unique=True)
        _db.sessions.create_index([("updated_at", pymongo.DESCENDING)])
        _db.messages.create_index([("session_id", pymongo.ASCENDING), ("timestamp", pymongo.ASCENDING)])
        return _db
    except (ConnectionFailure, ServerSelectionTimeoutError, Exception):
        _client = None
        _db = None
        return None

def is_db_connected():
    """Check if MongoDB is actively reachable."""
    try:
        db = get_db()
        return db is not None
    except Exception:
        return False

def create_session(session_id=None, user_stage="", target_domain="", title="New Career Consultation"):
    """Creates a new session record in MongoDB."""
    db = get_db()
    if db is None:
        return session_id or str(uuid.uuid4())

    sid = session_id or str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    doc = {
        "session_id": sid,
        "title": title,
        "user_stage": user_stage,
        "target_domain": target_domain,
        "created_at": now,
        "updated_at": now,
        "message_count": 0
    }
    try:
        db.sessions.update_one(
            {"session_id": sid},
            {"$setOnInsert": doc},
            upsert=True
        )
    except Exception as e:
        print(f"[MongoDB Error] create_session: {e}")
    return sid

def save_message(session_id, role, content):
    """Saves a message to the messages collection and updates session stats."""
    db = get_db()
    if db is None:
        return False

    now = datetime.now(timezone.utc)
    message_doc = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": now
    }
    try:
        db.messages.insert_one(message_doc)
        
        # Update session updated_at and message_count
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {"updated_at": now},
                "$inc": {"message_count": 1}
            }
        )
        return True
    except Exception as e:
        print(f"[MongoDB Error] save_message: {e}")
        return False

def update_session_title(session_id, title):
    """Updates session title (e.g. from first question)."""
    db = get_db()
    if db is None:
        return
    try:
        db.sessions.update_one(
            {"session_id": session_id},
            {"$set": {"title": title[:60] + ("..." if len(title) > 60 else "")}}
        )
    except Exception as e:
        print(f"[MongoDB Error] update_session_title: {e}")

def get_session_messages(session_id):
    """Retrieves all chat messages for a given session."""
    db = get_db()
    if db is None:
        return []

    try:
        cursor = db.messages.find(
            {"session_id": session_id}
        ).sort("timestamp", pymongo.ASCENDING)
        messages = []
        for doc in cursor:
            messages.append({
                "role": doc.get("role", "user"),
                "content": doc.get("content", "")
            })
        return messages
    except Exception as e:
        print(f"[MongoDB Error] get_session_messages: {e}")
        return []

def list_sessions(limit=25):
    """Returns list of recent sessions for the history drawer (excludes empty sessions)."""
    db = get_db()
    if db is None:
        return []

    try:
        cursor = db.sessions.find({"message_count": {"$gt": 0}}).sort("updated_at", pymongo.DESCENDING).limit(limit)
        sessions = []
        for doc in cursor:
            sessions.append({
                "session_id": doc.get("session_id"),
                "title": doc.get("title", "Career Consultation"),
                "user_stage": doc.get("user_stage", ""),
                "target_domain": doc.get("target_domain", ""),
                "updated_at": doc.get("updated_at"),
                "message_count": doc.get("message_count", 0)
            })
        return sessions
    except Exception as e:
        print(f"[MongoDB Error] list_sessions: {e}")
        return []

def delete_session(session_id):
    """Deletes a session and its associated messages."""
    db = get_db()
    if db is None:
        return False

    try:
        db.messages.delete_many({"session_id": session_id})
        db.sessions.delete_one({"session_id": session_id})
        return True
    except Exception as e:
        print(f"[MongoDB Error] delete_session: {e}")
        return False

def export_session_as_markdown(session_id, user_stage="", target_domain="", messages=None):
    """Compiles a session into a structured Markdown report."""
    if messages is None:
        messages = get_session_messages(session_id)
    if not messages:
        return "# CareNex AI Career Guidance Report\n\nNo messages in this session."

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"# 🎓 CareNex AI Career Guidance Report\n\n"
    md += f"**Date:** {now_str}  \n"
    if user_stage:
        md += f"**Profile:** {user_stage}  \n"
    if target_domain:
        md += f"**Domain:** {target_domain}  \n"
    md += f"**Session ID:** `{session_id}`  \n"
    md += "\n---\n\n"

    for i, msg in enumerate(messages, 1):
        role_title = "🧑‍💻 User" if msg["role"] == "user" else "⚡ CareNex"
        md += f"### {role_title}\n\n"
        md += f"{msg['content']}\n\n"
        md += "---\n\n"

    return md

def export_session_as_text(session_id, user_stage="", target_domain="", messages=None):
    """Compiles a session into a clean Plaintext (.txt) document."""
    if messages is None:
        messages = get_session_messages(session_id)
    if not messages:
        return "CARENEX CAREER GUIDANCE REPORT\nNo messages in this session."

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sep = "=" * 70
    sub_sep = "-" * 70

    lines = [
        sep,
        "CARENEX - AI CAREER GUIDANCE CONSULTATION REPORT",
        sep,
        f"Date:           {now_str}",
        f"Career Stage:   {user_stage or 'General'}",
        f"Target Domain:  {target_domain or 'All Domains'}",
        f"Session ID:     {session_id}",
        sep,
        ""
    ]

    for i, msg in enumerate(messages, 1):
        sender = "USER" if msg["role"] == "user" else "CARENEX"
        lines.append(f"[{sender}]:")
        lines.append(msg["content"].strip())
        lines.append("")
        lines.append(sub_sep)
        lines.append("")

    return "\n".join(lines)

def export_session_as_pdf(session_id, user_stage="", target_domain="", messages=None):
    """Compiles a session into a formatted PDF Document (.pdf) bytes."""
    from fpdf import FPDF

    if messages is None:
        messages = get_session_messages(session_id)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    class CareerPDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(0, 180, 160)
            self.cell(0, 8, 'CareNex AI - Career Guidance Report', new_x='LMARGIN', new_y='NEXT')
            self.set_draw_color(220, 225, 230)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(140, 150, 160)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}  |  Generated by CareNex AI Career Platform', align='C')

    def sanitize(text):
        if not text:
            return ""
        rep = {
            '🤖': '[CareNex]', '🧑‍💻': '[User]', '⚡': '[CareNex]', '🗺️': '[Roadmap]',
            '💼': '[Career]', '🎤': '[Interview]', '•': '-', '—': '--', '–': '-',
            '’': "'", '“': '"', '”': '"', '‘': "'", '👉': '->', '✅': '[OK]',
            '⚠️': '[Warning]', '💡': '[Tip]', '🔥': '[Trending]', '🚀': '[Launch]',
            '🎯': '[Goal]', '🌟': '[Star]', '⭐': '[Star]', '📌': '[Action]',
            '🔍': '[Search]', '📊': '[Data]', '🛠️': '[Tools]', '🛠': '[Tools]',
            '📚': '[Study]', '🎓': '[Edu]', '📈': '[Growth]', '✨': '[Key]'
        }
        for k, v in rep.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf = CareerPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title & Metadata Banner
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, 'CareNex Career Guidance Consultation', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('Helvetica', size=9)
    pdf.set_text_color(90, 105, 125)
    meta_info = f"Date: {now_str}  |  Stage: {user_stage or 'General'}  |  Domain: {target_domain or 'All Domains'}"
    pdf.cell(0, 6, sanitize(meta_info), new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)

    if not messages:
        pdf.set_font('Helvetica', 'I', 11)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 8, 'No messages recorded in this consultation session.', new_x='LMARGIN', new_y='NEXT')
    else:
        for msg in messages:
            is_user = (msg["role"] == "user")
            
            # Role Header
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Helvetica', 'B', 10)
            if is_user:
                pdf.set_text_color(0, 102, 204)
                pdf.cell(0, 7, 'User Query:', new_x='LMARGIN', new_y='NEXT')
            else:
                pdf.set_text_color(0, 150, 120)
                pdf.cell(0, 7, 'CareNex Mentorship:', new_x='LMARGIN', new_y='NEXT')

            # Message Content
            pdf.set_font('Helvetica', size=9.5)
            pdf.set_text_color(30, 41, 59)
            clean_body = sanitize(msg["content"].strip())
            
            # Render using epw width safely
            pdf.set_x(pdf.l_margin)
            try:
                pdf.multi_cell(w=pdf.epw, h=5.5, text=clean_body, markdown=True)
            except Exception:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(w=pdf.epw, h=5.5, text=clean_body, markdown=False)
            pdf.ln(4)

            # Divider line
            pdf.set_draw_color(230, 235, 240)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)

    return bytes(pdf.output())


