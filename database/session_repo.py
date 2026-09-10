import uuid
from datetime import datetime
# pyrefly: ignore [missing-import]
import pymongo
from .connection import get_db

def create_session(user_stage="College Student", target_domain="General", title="New Career Consultation"):
    """Creates a new session record in MongoDB and returns its UUID string."""
    db = get_db()
    session_id = str(uuid.uuid4())
    now = datetime.now()

    session_doc = {
        "session_id": session_id,
        "title": title,
        "user_stage": user_stage,
        "target_domain": target_domain,
        "created_at": now,
        "updated_at": now,
        "message_count": 0
    }

    if db is not None:
        try:
            db.sessions.insert_one(session_doc)
        except Exception as e:
            print(f"[MongoDB Error] create_session: {e}")

    return session_id

def update_session_title(session_id, first_query):
    """Summarizes or sets the first user query as the session title."""
    db = get_db()
    if db is None:
        return

    clean_title = first_query.strip().replace("\n", " ")
    if len(clean_title) > 60:
        clean_title = clean_title[:57] + "..."

    try:
        db.sessions.update_one(
            {"session_id": session_id},
            {"$set": {"title": clean_title, "updated_at": datetime.now()}}
        )
    except Exception as e:
        print(f"[MongoDB Error] update_session_title: {e}")

def save_message(session_id, role, content):
    """Appends a chat message to MongoDB and updates session metadata."""
    db = get_db()
    if db is None:
        return False

    now = datetime.now()
    message_doc = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": now
    }

    try:
        db.messages.insert_one(message_doc)
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {"updated_at": now},
                "$inc": {"message_count": 1}
            },
            upsert=True
        )
        return True
    except Exception as e:
        print(f"[MongoDB Error] save_message: {e}")
        return False

def get_session_messages(session_id):
    """Retrieves all chat messages for a session ordered chronologically."""
    db = get_db()
    if db is None:
        return []

    try:
        cursor = db.messages.find({"session_id": session_id}).sort("timestamp", pymongo.ASCENDING)
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
