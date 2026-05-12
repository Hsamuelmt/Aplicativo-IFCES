"""Crear un usuario administrador localmente (SQLite).
Ejemplo de uso:
  .venv/Scripts/python.exe scripts/create_admin_user.py
"""
import os
import sys

# Asegurar que el directorio del proyecto esté en sys.path para importar `app`
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
  sys.path.insert(0, PROJECT_ROOT)
from dotenv import load_dotenv

# Cargar variables desde .env para que `config.Config` use los valores adecuados
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

from app import create_app
from app.extensions import db
from app.models import User

USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "Admin123!"
ROLE = "admin"

app = create_app()

with app.app_context():
  existing = User.query.filter((User.username == USERNAME) | (User.email == EMAIL)).first()
  if existing:
    print(f"Usuario existente: {existing.username} <{existing.email}>")
  else:
    u = User(username=USERNAME, email=EMAIL, role=ROLE)
    u.set_password(PASSWORD)
    db.session.add(u)
    db.session.commit()
    print(f"Usuario creado: {USERNAME} / {EMAIL} (rol: {ROLE})")
