"""
Migration script to add condition_control_status column to questionnaires table
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "aom_screening.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Add condition_control_status column
        cursor.execute("""
            ALTER TABLE questionnaires
            ADD COLUMN condition_control_status TEXT
        """)
        print("✅ Added 'condition_control_status' column to questionnaires table")

        conn.commit()
        print("✅ Migration completed successfully!")

    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("ℹ️ Column 'condition_control_status' already exists, skipping")
        else:
            raise e
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
