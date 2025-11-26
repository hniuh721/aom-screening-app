#!/usr/bin/env python3
"""
Database Migration Script
Adds 'previous_aom_history' column to questionnaires table
"""
import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "aom_screening.db"

def migrate():
    """Add previous_aom_history column to questionnaires table"""
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🔄 Starting database migration...")
        print(f"📁 Database: {DB_PATH}")

        # Check if column already exists
        cursor.execute("PRAGMA table_info(questionnaires)")
        columns = [column[1] for column in cursor.fetchall()]

        if "previous_aom_history" in columns:
            print("✅ Column 'previous_aom_history' already exists. No migration needed.")
            conn.close()
            return True

        # Add the new column
        print("➕ Adding 'previous_aom_history' column...")
        cursor.execute("""
            ALTER TABLE questionnaires
            ADD COLUMN previous_aom_history TEXT
        """)

        # Commit changes
        conn.commit()
        print("✅ Migration completed successfully!")

        # Verify the column was added
        cursor.execute("PRAGMA table_info(questionnaires)")
        columns = [column[1] for column in cursor.fetchall()]

        if "previous_aom_history" in columns:
            print("✓ Verified: 'previous_aom_history' column exists")
        else:
            print("⚠️  Warning: Could not verify column was added")
            conn.close()
            return False

        # Close connection
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def rollback():
    """Remove previous_aom_history column (rollback migration)"""
    print("⚠️  SQLite does not support DROP COLUMN directly.")
    print("To rollback, you would need to:")
    print("1. Create a new table without the column")
    print("2. Copy data from old table")
    print("3. Drop old table and rename new table")
    print("\nFor safety, manual rollback is recommended.")
    return False

if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        print("Please make sure the database exists before running migration.")
        sys.exit(1)

    # Check for rollback flag
    if len(sys.argv) > 1 and sys.argv[1] == "--rollback":
        success = rollback()
    else:
        success = migrate()

    sys.exit(0 if success else 1)
