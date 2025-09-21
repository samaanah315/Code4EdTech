# db_utils.py
import sqlite3

DB_FILE = "results.db"  # SQLite database file

# Initialize the database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_file TEXT,
        jd_file TEXT,
        role_title TEXT,
        score REAL,
        verdict TEXT,
        missing_skills TEXT,
        location TEXT
    )
    """)
    conn.commit()
    conn.close()

# Save a result row into the database
def save_result(resume_file, jd_file, role_title, score, verdict, missing_skills, location="Unknown"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO results (resume_file, jd_file, role_title, score, verdict, missing_skills, location)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (resume_file, jd_file, role_title, score, verdict, ", ".join(missing_skills), location))
    conn.commit()
    conn.close()

# Fetch results with optional filters
def fetch_results(filters={}):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM results WHERE 1=1"
    params = []

    # Apply filters
    if "role_title" in filters and filters["role_title"]:
        query += " AND role_title LIKE ?"
        params.append(f"%{filters['role_title']}%")
    if "min_score" in filters:
        query += " AND score >= ?"
        params.append(filters["min_score"])
    if "max_score" in filters:
        query += " AND score <= ?"
        params.append(filters["max_score"])
    if "location" in filters and filters["location"]:
        query += " AND location LIKE ?"
        params.append(f"%{filters['location']}%")

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    return results
