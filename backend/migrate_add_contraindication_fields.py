#!/usr/bin/env python3
"""
Database Migration Script
Adds 'absolute_exclusions' and 'relative_warnings' columns to screening_results table
"""
import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "aom_screening.db"

def migrate():
    """Add new columns to screening_results table"""
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🔄 Starting database migration...")
        print(f"📁 Database: {DB_PATH}")

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(screening_results)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add absolute_exclusions column
        if "absolute_exclusions" not in columns:
            print("➕ Adding 'absolute_exclusions' column...")
            cursor.execute("""
                ALTER TABLE screening_results
                ADD COLUMN absolute_exclusions JSON
            """)
            print("✅ Added 'absolute_exclusions' column")
        else:
            print("✓ Column 'absolute_exclusions' already exists")

        # Add relative_warnings column
        if "relative_warnings" not in columns:
            print("➕ Adding 'relative_warnings' column...")
            cursor.execute("""
                ALTER TABLE screening_results
                ADD COLUMN relative_warnings JSON
            """)
            print("✅ Added 'relative_warnings' column")
        else:
            print("✓ Column 'relative_warnings' already exists")

        # Commit changes
        conn.commit()
        print("✅ Migration completed successfully!")

        # Verify columns were added
        cursor.execute("PRAGMA table_info(screening_results)")
        columns = [column[1] for column in cursor.fetchall()]

        if "absolute_exclusions" in columns and "relative_warnings" in columns:
            print("✓ Verified: New columns exist")
        else:
            print("⚠️  Warning: Could not verify all columns were added")
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

if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        print("Please make sure the database exists before running migration.")
        sys.exit(1)

    success = migrate()
    sys.exit(0 if success else 1)
