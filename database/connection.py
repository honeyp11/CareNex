import os
# pyrefly: ignore [missing-import]
import pymongo
# pyrefly: ignore [missing-import]
from pymongo.errors import ServerSelectionTimeoutError
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "career_guidance_db")

_client = None
_db = None

def get_mongo_client():
    """Initializes and returns the PyMongo client singleton with 2-second timeout."""
    global _client
    if _client is None:
        try:
            _client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            _client.admin.command('ping')
        except (ServerSelectionTimeoutError, Exception) as e:
            print(f"[MongoDB Warning] Connection failed: {e}. Running in local memory mode.")
            _client = None
    return _client

def get_db():
    """Returns the MongoDB database instance, or None if offline."""
    global _db
    if _db is None:
        client = get_mongo_client()
        if client:
            _db = client[DB_NAME]
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
