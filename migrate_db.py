#!/usr/bin/env python
"""Database migration script to add category column to user_blogs table."""

import sqlite3
import os

# Database is located in instance folder
db_path = os.path.join('instance', 'blogs_app.db')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if category column exists
        cursor.execute("PRAGMA table_info(user_blogs)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'category' not in columns:
            # Add category column
            cursor.execute("ALTER TABLE user_blogs ADD COLUMN category VARCHAR(50) DEFAULT 'General'")
            conn.commit()
            print("✓ Successfully added category column to user_blogs table")
            print(f"✓ All existing blogs defaulted to 'General' category")
        else:
            print("✓ Category column already exists in user_blogs table")
    except Exception as e:
        print(f"✗ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()
else:
    print(f"✗ Database file '{db_path}' not found")
    print("The database will be created on first application run")
