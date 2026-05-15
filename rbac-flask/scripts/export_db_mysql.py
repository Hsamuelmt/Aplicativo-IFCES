#!/usr/bin/env python
"""
Database Export Script - Convert SQLite to MySQL SQL format
Usage: python scripts/export_db_mysql.py
Output: database_export_sammor96_sammor96_.sql
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Database paths
SQLITE_DB = Path(__file__).parent.parent / "instance" / "app.db"
OUTPUT_FILE = Path(__file__).parent.parent / f"database_export_sammor96_sammor96_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
DB_NAME = "sammor96_sammor96_"

def sqlite_to_mysql_sql(sqlite_db_path, output_file_path, database_name):
    """Convert SQLite database to MySQL SQL format."""
    
    if not sqlite_db_path.exists():
        print(f"❌ Error: SQLite database not found at {sqlite_db_path}")
        return False
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️  No tables found in database")
            conn.close()
            return False
        
        sql_statements = []
        
        # Add header comments
        sql_statements.append(f"-- MySQL dump for {database_name}")
        sql_statements.append(f"-- Exported from SQLite on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sql_statements.append("-- MySQL Client version: 8.0")
        sql_statements.append("")
        sql_statements.append("SET NAMES utf8mb4;")
        sql_statements.append("SET FOREIGN_KEY_CHECKS=0;")
        sql_statements.append("")
        
        # Create database
        sql_statements.append(f"CREATE DATABASE IF NOT EXISTS `{database_name}`;")
        sql_statements.append(f"USE `{database_name}`;")
        sql_statements.append("")
        
        # Process each table
        for (table_name,) in tables:
            print(f"📋 Processing table: {table_name}")
            
            # Drop table if exists
            sql_statements.append(f"DROP TABLE IF EXISTS `{table_name}`;")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Get CREATE TABLE statement from SQLite and convert it
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            create_table = cursor.fetchone()[0]
            
            # Convert SQLite syntax to MySQL syntax
            create_table = create_table.replace("`", "`")  # Keep backticks
            create_table = create_table.replace("AUTOINCREMENT", "AUTO_INCREMENT")
            create_table = create_table.replace("TEXT", "TEXT")
            create_table = create_table.replace("REAL", "FLOAT")
            create_table = create_table.replace("BLOB", "BLOB")
            
            # Add ENGINE specification
            if "ENGINE=" not in create_table:
                create_table = create_table.rstrip(";") + " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
            
            sql_statements.append(create_table)
            sql_statements.append("")
            
            # Get all rows
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                # Build INSERT statements
                col_names = [col[1] for col in columns]
                col_names_str = ", ".join([f"`{col}`" for col in col_names])
                
                insert_values = []
                for row in rows:
                    # Format values for MySQL
                    values = []
                    for value in row:
                        if value is None:
                            values.append("NULL")
                        elif isinstance(value, str):
                            # Escape single quotes
                            escaped = value.replace("\\", "\\\\").replace("'", "\\'")
                            values.append(f"'{escaped}'")
                        elif isinstance(value, bool):
                            values.append("1" if value else "0")
                        else:
                            values.append(str(value))
                    
                    insert_values.append(f"({', '.join(values)})")
                
                # Create INSERT statement
                if insert_values:
                    insert_stmt = f"INSERT INTO `{table_name}` ({col_names_str}) VALUES\n"
                    insert_stmt += ",\n".join(insert_values) + ";"
                    sql_statements.append(insert_stmt)
                    sql_statements.append("")
            
            sql_statements.append("")
        
        # Add footer
        sql_statements.append("SET FOREIGN_KEY_CHECKS=1;")
        sql_statements.append("")
        
        # Write to file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(sql_statements))
        
        conn.close()
        
        file_size = output_file_path.stat().st_size / 1024  # Size in KB
        print(f"\n✅ Database export successful!")
        print(f"📄 Output file: {output_file_path}")
        print(f"📊 File size: {file_size:.2f} KB")
        print(f"\n📝 Next steps:")
        print(f"1. Go to FreeHostia control panel")
        print(f"2. Open phpMyAdmin")
        print(f"3. Create a new database named: {database_name}")
        print(f"4. Import this SQL file into the new database")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SQLite to MySQL Database Export")
    print(f"📍 Database: {SQLITE_DB}")
    print(f"📁 Output: {OUTPUT_FILE}")
    print("")
    
    success = sqlite_to_mysql_sql(SQLITE_DB, OUTPUT_FILE, DB_NAME)
    sys.exit(0 if success else 1)
