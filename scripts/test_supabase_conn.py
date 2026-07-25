"""
Supabase PostgreSQL Connection & Table Creation Verification Script
"""

import sys
import os

DB_URL = "postgresql://postgres:resume9878635@db.emkarnsfdneiqgmbnvit.supabase.co:5432/postgres"

def main():
    print(f"Connecting to Supabase PostgreSQL: {DB_URL[:30]}...")
    try:
        import psycopg2
        import psycopg2.extras

        conn = psycopg2.connect(DB_URL, sslmode="require", connect_timeout=10)
        conn.autocommit = True
        cursor = conn.cursor()

        print("✅ Connection successful!")

        # Create Users Table
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create Usage Limits Table
        print("Creating 'usage_limits' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_limits (
                id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                analysis_count INTEGER DEFAULT 0,
                analysis_limit INTEGER DEFAULT 3,
                last_analysis_at TIMESTAMP,
                reset_date TIMESTAMP,
                plan_tier TEXT DEFAULT 'free',
                extra_credits INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Create Analysis History Table
        print("Creating 'analysis_history' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id SERIAL PRIMARY KEY,
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
            );
        """)

        print("🎉 ALL 3 TABLES CREATED SUCCESSFULLY ON SUPABASE!")

        # Query existing tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [r[0] for r in cursor.fetchall()]
        print(f"Active tables in public schema: {tables}")

    except Exception as e:
        print(f"❌ Connection/Migration Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
