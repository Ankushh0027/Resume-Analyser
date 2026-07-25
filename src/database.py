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


def _get_cloud_db_url() -> str:
    """Checks st.secrets and os.environ for SUPABASE_DB_URL, DATABASE_URL, or POSTGRES_URL."""
    raw_url = ""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets:
            for k in ["SUPABASE_DB_URL", "DATABASE_URL", "POSTGRES_URL"]:
                if k in st.secrets and st.secrets[k]:
                    raw_url = str(st.secrets[k]).strip()
                    break
    except Exception:
        pass
    if not raw_url:
        for k in ["SUPABASE_DB_URL", "DATABASE_URL", "POSTGRES_URL"]:
            val = os.getenv(k, "").strip()
            if val:
                raw_url = val
                break

    if raw_url:
        # Sanitize bracketed passwords from Supabase string (e.g., postgres:[pwd]@host)
        raw_url = raw_url.replace(":[", ":").replace("]@", "@")
    return raw_url


class DBCursorWrapper:
    """Normalizes query execution and dictionary row outputs across SQLite and PostgreSQL."""

    def __init__(self, raw_cursor, is_postgres: bool = False):
        self.raw_cursor = raw_cursor
        self.is_postgres = is_postgres
        self.last_inserted_id = None

    def execute(self, sql: str, params: tuple | list = ()):
        query = sql
        if self.is_postgres:
            query = query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            query = query.replace("?", "%s")
            if "INSERT INTO" in query and "RETURNING" not in query:
                query += " RETURNING id"
        
        self.raw_cursor.execute(query, params)
        if self.is_postgres and "INSERT INTO" in sql:
            try:
                res = self.raw_cursor.fetchone()
                if res:
                    row_dict = dict(res)
                    self.last_inserted_id = list(row_dict.values())[0]
            except Exception:
                pass
        return self

    def fetchone(self):
        res = self.raw_cursor.fetchone()
        if res:
            return dict(res)
        return None

    def fetchall(self):
        res = self.raw_cursor.fetchall()
        if res:
            return [dict(r) for r in res]
        return []

    @property
    def lastrowid(self):
        if self.is_postgres:
            return self.last_inserted_id or 1
        return self.raw_cursor.lastrowid


class DBWrapper:
    """Unified Database Connection Wrapper supporting both SQLite and PostgreSQL/Supabase."""

    def __init__(self, raw_conn, is_postgres: bool = False):
        self.raw_conn = raw_conn
        self.is_postgres = is_postgres

    def cursor(self):
        return DBCursorWrapper(self.raw_conn.cursor(), self.is_postgres)

    def commit(self):
        if not self.is_postgres:
            try:
                self.raw_conn.commit()
            except Exception:
                pass

    def close(self):
        try:
            self.raw_conn.close()
        except Exception:
            pass


def _get_connection() -> DBWrapper:
    """Returns a unified DBWrapper around SQLite or Cloud PostgreSQL/Supabase."""
    db_url = _get_cloud_db_url()
    if db_url.startswith(("postgres://", "postgresql://")):
        try:
            import psycopg2
            import psycopg2.extras
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            conn = psycopg2.connect(
                db_url,
                cursor_factory=psycopg2.extras.RealDictCursor,
                sslmode="require",
                connect_timeout=10,
            )
            conn.autocommit = True
            logger.info("Connected to Persistent Cloud PostgreSQL Database.")
            return DBWrapper(conn, is_postgres=True)
        except Exception as e:
            logger.error(f"Could not connect to Cloud PostgreSQL DB: {str(e)}. Falling back to local SQLite.")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception as e:
        logger.warning(f"Could not set WAL mode on SQLite: {str(e)}")
    return DBWrapper(conn, is_postgres=False)


def get_db_type_info() -> dict[str, Any]:
    """Returns information about active database engine (PostgreSQL Cloud vs Local SQLite)."""
    db_url = _get_cloud_db_url()
    if db_url.startswith(("postgres://", "postgresql://")):
        try:
            conn = _get_connection()
            if conn.is_postgres:
                conn.close()
                return {"is_cloud": True, "type": "Supabase PostgreSQL Cloud DB", "status": "Connected (SSL Mode)"}
        except Exception as e:
            return {"is_cloud": False, "type": "Local SQLite Fallback", "status": f"Cloud Error: {str(e)}"}
    return {"is_cloud": False, "type": "Local SQLite Database", "status": "Active (Local File)"}


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

    # Migration: Add plan_tier and extra_credits if missing
    try:
        cursor.execute("ALTER TABLE usage_limits ADD COLUMN plan_tier TEXT DEFAULT 'free'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usage_limits ADD COLUMN extra_credits INTEGER DEFAULT 0")
    except Exception:
        pass

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
            INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date, plan_tier, extra_credits)
            VALUES (?, 0, 3, ?, 'free', 0)
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
        INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date, plan_tier, extra_credits)
        VALUES (?, 0, 3, ?, 'free', 0)
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
    cursor.execute("UPDATE usage_limits SET analysis_count = 0, extra_credits = 0, plan_tier = 'free' WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    logger.info(f"Reset usage count to 0 for user ID #{user_id}")


def add_user_credits(user_id: int, credits_to_add: int) -> dict[str, Any]:
    """Adds purchased credit pack to user account."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usage_limits SET extra_credits = COALESCE(extra_credits, 0) + ?, plan_tier = 'starter' WHERE user_id = ?",
        (credits_to_add, user_id),
    )
    conn.commit()
    conn.close()
    logger.info(f"Added {credits_to_add} extra credits to user ID #{user_id}")
    return get_user_usage(user_id)


def set_user_pro_plan(user_id: int) -> dict[str, Any]:
    """Upgrades user to Pro Monthly Pass (Unlimited)."""
    conn = _get_connection()
    cursor = conn.cursor()
    reset_date = (datetime.now() + timedelta(days=30)).isoformat()
    cursor.execute(
        "UPDATE usage_limits SET plan_tier = 'pro_monthly', reset_date = ? WHERE user_id = ?",
        (reset_date, user_id),
    )
    conn.commit()
    conn.close()
    logger.info(f"Upgraded user ID #{user_id} to Pro Monthly Pass")
    return get_user_usage(user_id)


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
            INSERT INTO usage_limits (user_id, analysis_count, analysis_limit, reset_date, plan_tier, extra_credits)
            VALUES (?, 0, 3, ?, 'free', 0)
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
    Checks user credit tier and remaining balance.
    Consumes credits or checks free limits.

    Returns:
        tuple[bool, int, int, str]: (can_proceed, remaining_or_count, limit, message)
    """
    conn = _get_connection()
    cursor = conn.cursor()

    usage = get_user_usage(user_id)
    plan_tier = usage.get("plan_tier", "free")
    extra_credits = usage.get("extra_credits", 0) or 0
    count = usage.get("analysis_count", 0) or 0
    limit = usage.get("analysis_limit", 3) or 3
    now_str = datetime.now().isoformat()

    # 1. Pro Unlimited Plan
    if plan_tier == "pro_monthly":
        cursor.execute(
            "UPDATE usage_limits SET last_analysis_at = ? WHERE user_id = ?",
            (now_str, user_id),
        )
        conn.commit()
        conn.close()
        return True, 999, 999, "Pro Unlimited Active"

    # 2. Use Extra Purchased Credits
    if extra_credits > 0:
        new_extra = extra_credits - 1
        cursor.execute(
            "UPDATE usage_limits SET extra_credits = ?, last_analysis_at = ? WHERE user_id = ?",
            (new_extra, now_str, user_id),
        )
        conn.commit()
        conn.close()
        return True, new_extra, limit, "Credit Used"

    # 3. Standard Free Quota
    if count >= limit:
        conn.close()
        return False, count, limit, f"You've used all {limit} free monthly credits."

    new_count = count + 1
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


def _safe_val(row: Any, default: Any = 0) -> Any:
    """Extracts first column value safely from dict, tuple, or Row."""
    if not row:
        return default
    if isinstance(row, dict):
        vals = list(row.values())
        return vals[0] if vals and vals[0] is not None else default
    try:
        return row[0] if row[0] is not None else default
    except Exception:
        return default


def get_system_stats() -> dict[str, Any]:
    """Queries database for authentic system statistics."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    total_audits = _safe_val(cursor.fetchone(), 0)

    cursor.execute("SELECT AVG(ats_score) FROM analysis_history WHERE ats_score > 0")
    avg_score_row = _safe_val(cursor.fetchone(), None)
    avg_score = round(float(avg_score_row), 1) if avg_score_row is not None else None

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = _safe_val(cursor.fetchone(), 0)

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
        GROUP BY u.id, u.email, u.name, u.created_at, l.analysis_count, l.analysis_limit
        ORDER BY u.created_at DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Automatically run DB initialization on module load
init_db()
