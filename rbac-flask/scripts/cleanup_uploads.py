"""Cleanup old files from instance/uploads older than N days.

Run: .venv/Scripts/python.exe scripts/cleanup_uploads.py [days]
"""
import sys
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app


def main(days=30):
    app = create_app()
    with app.app_context():
        upload_folder = app.config.get('UPLOAD_FOLDER')
        if not upload_folder:
            print('No UPLOAD_FOLDER configured')
            return
        p = Path(upload_folder)
        if not p.exists():
            print('Upload folder does not exist, creating:', p)
            p.mkdir(parents=True, exist_ok=True)

        cutoff = time.time() - (int(days) * 86400)
        removed = 0
        for f in p.iterdir():
            try:
                if f.is_file() and f.stat().st_mtime < cutoff:
                    f.unlink()
                    removed += 1
            except Exception as e:
                print('Error removing', f, e)
        print(f'Removed {removed} files older than {days} days')


if __name__ == '__main__':
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    main(days)
