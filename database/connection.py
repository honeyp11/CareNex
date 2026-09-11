import os
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import pymongo
# pyrefly: ignore [missing-import]
from pymongo.errors import ServerSelectionTimeoutError
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv(override=True)

def get_mongo_uri() -> str:
    """Resolves MongoDB URI from Streamlit Secrets or Environment."""
    try:
        if hasattr(st, "secrets") and "MONGO_URI" in st.secrets:
            val = str(st.secrets["MONGO_URI"]).strip()
            if val:
                return val
    except Exception:
        pass
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_db_name() -> str:
    """Resolves Database name from Streamlit Secrets or Environment."""
    try:
        if hasattr(st, "secrets") and "DB_NAME" in st.secrets:
            val = str(st.secrets["DB_NAME"]).strip()
            if val:
                return val
        if hasattr(st, "secrets") and "MONGO_DB_NAME" in st.secrets:
            val = str(st.secrets["MONGO_DB_NAME"]).strip()
            if val:
                return val
    except Exception:
        pass
    return os.getenv("DB_NAME", os.getenv("MONGO_DB_NAME", "career_guidance_db"))

_client = None
_db = None

def get_mongo_client():
    """Initializes and returns the PyMongo client singleton with 2-second timeout."""
    global _client
    if _client is None:
        uri = get_mongo_uri()
        try:
            _client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
            _client.admin.command('ping')
        except (ServerSelectionTimeoutError, Exception) as e:
            print(f"[MongoDB Warning] Connection to {uri} failed: {e}. Running in local memory mode.")
            _client = None
    return _client

def get_db():
    """Returns the MongoDB database instance, or None if offline."""
    global _db
    if _db is None:
        client = get_mongo_client()
        if client:
            db_name = get_db_name()
            _db = client[db_name]
    return _db

def is_db_connected():
    """Quick boolean check to see if MongoDB is actively reachable."""
    try:
        client = get_mongo_client()
        if client:
            client.admin.command('ping')
            return True
        return False
    except Exception:
        return False
