"""
Backwards-compatible facade module for legacy imports.
Re-exports database operations from 'database' package and export services from 'backend' package.
"""

from database.connection import (
    get_mongo_client,
    get_db,
    is_db_connected
)
from database.session_repo import (
    create_session,
    update_session_title,
    save_message,
    get_session_messages,
    list_sessions,
    delete_session
)
from backend.export_service import (
    export_session_as_pdf,
    export_session_as_text,
    export_session_as_markdown
)

__all__ = [
    "get_mongo_client",
    "get_db",
    "is_db_connected",
    "create_session",
    "update_session_title",
    "save_message",
    "get_session_messages",
    "list_sessions",
    "delete_session",
    "export_session_as_pdf",
    "export_session_as_text",
    "export_session_as_markdown"
]
