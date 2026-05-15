"""Add `examen_id` column to `materiales` table if missing."""
import sys
import os
from sqlalchemy import text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from app.extensions import db


def column_exists_sqlite(conn):
    res = conn.execute(text("PRAGMA table_info('materiales')")).fetchall()
    cols = [r[1] for r in res]
    return 'examen_id' in cols


def column_exists_generic(conn):
    # Try information_schema
    try:
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='materiales' LIMIT 1")).fetchall()
        cols = [r[0] for r in res]
        return 'examen_id' in cols
    except Exception:
        return False


def main():
    app = create_app()
    with app.app_context():
        # Ensure tables exist according to models (will create missing tables)
        db.create_all()
        engine = db.engine
        conn = engine.connect()
        try:
            exists = False
            if engine.dialect.name == 'sqlite':
                exists = column_exists_sqlite(conn)
            else:
                exists = column_exists_generic(conn)

            if exists:
                print('Column examen_id already exists; nothing to do.')
                return

            # Add column
            print('Adding examen_id column to materiales...')
            try:
                conn.execute(text('ALTER TABLE materiales ADD COLUMN examen_id INTEGER'))
                print('Column added.')
            except Exception as e:
                print('Failed to add column:', e)
        finally:
            conn.close()


if __name__ == '__main__':
    main()
