"""Script de ayuda para crear la base de datos MySQL definida en .env
Ejecutar con el Python del venv creado previamente:
  .\.venv\Scripts\python.exe scripts\create_mysql_db.py
"""
from dotenv import load_dotenv
import os
import sys
import pymysql

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

if not DB_NAME or not DB_USER:
    print('Faltan DB_NAME o DB_USER en .env')
    sys.exit(1)

print(f'Conectando a MySQL en {DB_HOST}:{DB_PORT} como {DB_USER}...')
try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD or None, port=DB_PORT)
except Exception as e:
    print('Error conectando a MySQL:', e)
    sys.exit(1)

try:
    with conn.cursor() as cur:
        sql = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cur.execute(sql)
    conn.commit()
    print(f'Base de datos `{DB_NAME}` creada (o ya existente).')
finally:
    conn.close()
