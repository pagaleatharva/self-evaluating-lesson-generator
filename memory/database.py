
import sqlite3
import json
from pathlib import Path

from collections import Counter
# Database location
DB_PATH = Path(__file__).resolve().parent / "memory.db"


# 1. Create database and table
def initialize_database():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            topic TEXT NOT NULL,

            topic_key TEXT NOT NULL,

            lesson TEXT,

            evaluation TEXT,

            rejection_log TEXT,

            status TEXT,

            retry_count INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()
    connection.close()


# 2. Save workflow results
def save_lesson_run(result):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO lesson_history (
            topic,
            topic_key,
            lesson,
            evaluation,
            rejection_log,
            status,
            retry_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result["topic"],
        result["topic"].strip().lower(),
        result["lesson"],
        json.dumps(result["evaluation"]),
        json.dumps(result["rejection_log"]),
        result["status"],
        result["retry_count"]
    ))

    connection.commit()
    connection.close()


# 3. Retrieve previous failures
def get_learning_memory(topic, limit=5):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT rejection_log
        FROM lesson_history
        WHERE topic_key = ?
        AND rejection_log != '[]'
        ORDER BY id DESC
        LIMIT ?
    """, (topic.strip().lower(), limit))

    records = cursor.fetchall()

    connection.close()

    previous_failures = []

    for record in records:

        rejection_logs = json.loads(record[0])

        for log in rejection_logs:

            for failure in log["failed_checks"]:
                previous_failures.append(failure)

    # Remove duplicate feedback
    failure_counts = Counter(previous_failures)

    learning_insights = [
         f"{failure} (reported {count} times)"
        for failure, count in failure_counts.most_common()
]

    return learning_insights
