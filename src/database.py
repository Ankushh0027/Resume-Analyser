"""
Database Module for AI Resume Analyzer SaaS
Handles SQLite database initialization, user accounts, free tier usage limits, and analysis history persistence.
"""

import json
import os
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from typing import Any
from src.logger import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "data", "saas_resume_analyzer.db"))


def _get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with WAL mode, extended timeout, and row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception as e:
        logger.warning(f"Could not set WAL mode on SQLite: {str(e)}")
    return conn


def init_db() -> None:
    """Initializes SQLite database tables for users, usage limits, and analysis history."""
    conn = _get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Free Tier Usage Limits Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            analysis_count INTEGER DEFAULT 0,
            analysis_limit INTEGER DEFAULT 3,
            last_analysis_at TIMESTAMP,
            reset_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    # Persistent Analysis History Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            request_id TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            target_role TEXT,
            has_jd BOOLEAN,
            extracted_text TEXT,
            ats_score INTEGER,
            result_json TEXT NOT NULL,
            ai_provider_used TEXT,
            model_used TEXT,
            execution_time_ms INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()
    logger.info("Database schema initialized successfully.")

    # Seed default demo user if empty
    seed_demo_user()


def hash_password(password: str) -> str:
    """Hashes password with SHA256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def seed_demo_user() -> dict[str, Any]:
    """Creates default demo user (demo@resumeai.com / demo123) if not present."""
    conn = _get_connection()
    cursor = conn.cursor()

    email = "demo@resumeai.com"
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        pwd_hash = hash_password("demo123")
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email, "Demo User", pwd_hash),
        )
        user_id = cursor.lastrowid

        reset_date = (datetime.now() + timedelta(days=30)).isoformat()
        cursor.execute(
            """
            INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date)
            VALUES (?, 0, 3, ?)
            """,
            (user_id, reset_date),
        )
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        logger.info("Seeded default demo user (demo@resumeai.com / demo123)")

    conn.close()
    return dict(user)


def register_user(email: str, name: str, password: str) -> dict[str, Any]:
    """Registers a new user account and initializes free usage limits."""
    conn = _get_connection()
    cursor = conn.cursor()

    email_clean = email.strip().lower()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("An account with this email already exists.")

    pwd_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (email_clean, name.strip(), pwd_hash),
    )
    user_id = cursor.lastrowid

    reset_date = (datetime.now() + timedelta(days=30)).isoformat()
    cursor.execute(
        """
        INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date)
        VALUES (?, 0, 3, ?)
        """,
        (user_id, reset_date),
    )
    conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user)


def reset_user_usage(user_id: int) -> None:
    """Resets user analysis_count back to 0 for testing/demo purposes."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usage_limits SET analysis_count = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    logger.info(f"Reset usage count to 0 for user ID #{user_id}")


def authenticate_user(email: str, password: str) -> dict[str, Any] | None:
    """Authenticates user with email and password."""
    conn = _get_connection()
    cursor = conn.cursor()

    email_clean = email.strip().lower()
    pwd_hash = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (email_clean, pwd_hash),
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None


def get_user_usage(user_id: int) -> dict[str, Any]:
    """Retrieves usage statistics and auto-resets count if reset date has passed."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usage_limits WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if not row:
        reset_date = (datetime.now() + timedelta(days=30)).isoformat()
        cursor.execute(
            """
            INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date)
            VALUES (?, 0, 3, ?)
            """,
            (user_id, reset_date),
        )
        conn.commit()
        cursor.execute("SELECT * FROM usage_limits WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

    usage_dict = dict(row)

    # Check for monthly reset
    if usage_dict.get("reset_date"):
        try:
            reset_dt = datetime.fromisoformat(usage_dict["reset_date"])
            if datetime.now() >= reset_dt:
                new_reset = (datetime.now() + timedelta(days=30)).isoformat()
                cursor.execute(
                    "UPDATE usage_limits SET analysis_count = 0, reset_date = ? WHERE user_id = ?",
                    (new_reset, user_id),
                )
                conn.commit()
                usage_dict["analysis_count"] = 0
                usage_dict["reset_date"] = new_reset
        except Exception:
            pass

    conn.close()
    return usage_dict


def check_and_increment_usage(user_id: int) -> tuple[bool, int, int, str]:
    """
    Checks if user is within free monthly analysis limit.
    Increments count if allowed.

    Returns:
        tuple[bool, int, int, str]: (can_proceed, count, limit, message)
    """
    conn = _get_connection()
    cursor = conn.cursor()

    usage = get_user_usage(user_id)
    count = usage["analysis_count"]
    limit = usage["analysis_limit"]

    if count >= limit:
        conn.close()
        return False, count, limit, f"You've reached your free monthly limit of {limit} resume analyses."

    new_count = count + 1
    now_str = datetime.now().isoformat()
    cursor.execute(
        "UPDATE usage_limits SET analysis_count = ?, last_analysis_at = ? WHERE user_id = ?",
        (new_count, now_str, user_id),
    )
    conn.commit()
    conn.close()

    return True, new_count, limit, "Success"


def save_analysis_history(
    user_id: int,
    request_id: str,
    filename: str,
    target_role: str,
    has_jd: bool,
    extracted_text: str,
    result_dict: dict,
    provider_used: str,
    model_used: str,
    execution_time_ms: int,
) -> int:
    """Saves completed analysis record into database for user history tracking."""
    conn = _get_connection()
    cursor = conn.cursor()

    result_json = json.dumps(result_dict, ensure_ascii=False)
    ats_score = result_dict.get("ats_score", 0)

    cursor.execute(
        """
        INSERT INTO analysis_history (
            user_id, request_id, filename, target_role, has_jd, extracted_text,
            ats_score, result_json, ai_provider_used, model_used, execution_time_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            request_id,
            filename,
            target_role,
            has_jd,
            extracted_text,
            ats_score,
            result_json,
            provider_used,
            model_used,
            execution_time_ms,
        ),
    )
    conn.commit()
    history_id = cursor.lastrowid
    conn.close()
    logger.info(f"Saved analysis history ID #{history_id} for user ID #{user_id}")
    return history_id


def get_user_analysis_history(user_id: int) -> list[dict[str, Any]]:
    """Retrieves all past saved resume analysis records for a user."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, request_id, filename, target_role, has_jd, ats_score, result_json,
               ai_provider_used, model_used, execution_time_ms, created_at
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        item = dict(r)
        try:
            item["result"] = json.loads(item["result_json"])
        except Exception:
            item["result"] = {}
        history.append(item)

    return history


def get_system_stats() -> dict[str, Any]:
    """Queries live SQLite database for authentic system statistics."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    total_audits = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(ats_score) FROM analysis_history WHERE ats_score > 0")
    avg_score_row = cursor.fetchone()[0]
    avg_score = round(avg_score_row, 1) if avg_score_row else None

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    conn.close()

    return {
        "total_audits": total_audits,
        "avg_score": avg_score,
        "total_users": total_users,
    }


def get_all_users_admin() -> list[dict[str, Any]]:
    """Retrieves all registered users and their usage statistics for admin overview."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT u.id, u.email, u.name, u.created_at,
               COALESCE(l.analysis_count, 0) as analysis_count,
               COALESCE(l.analysis_limit, 3) as analysis_limit,
               COUNT(h.id) as total_audits_logged
        FROM users u
        LEFT JOIN usage_limits l ON u.id = l.user_id
        LEFT JOIN analysis_history h ON u.id = h.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Automatically run DB initialization on module load
init_db()
