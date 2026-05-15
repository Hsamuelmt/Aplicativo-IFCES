"""List users with roles and emails.
Run: python scripts/list_users.py
"""
import os, sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / '.env')
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.order_by(User.role, User.username).all()
    print(f"Total usuarios: {len(users)}\n")
    for u in users:
        print(f"{u.id:>3} | {u.username:<20} | {u.email:<30} | {u.role:<10} | active={u.is_active}")
