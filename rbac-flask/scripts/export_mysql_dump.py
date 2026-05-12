"""Exporta la base local a un dump MySQL compatible para phpMyAdmin/Freehostia.

Salida por defecto:
  exports/sammor96_sammor96_.sql
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
import json
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from app import create_app
from app.extensions import db


OUTPUT_FILE = PROJECT_ROOT / "exports" / "sammor96_sammor96_.sql"
TARGET_DB_NAME = "sammor96_sammor96_"


def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return f"'{value.isoformat(sep=' ')}'" if isinstance(value, datetime) else f"'{value.isoformat()}'"
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    escaped = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def main():
    app = create_app()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        metadata = db.metadata

        # Orden simple para respetar dependencias comunes entre tablas.
        preferred_order = [
            "users",
            "categorias",
            "examenes",
            "preguntas",
            "respuestas",
            "examenes_resultados",
            "notificaciones",
            "certificados",
            "estudiante_examen",
        ]
        tables = [name for name in preferred_order if name in inspector.get_table_names()]

        with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write("-- MySQL dump generated from local SQLite project data\n")
            fh.write(f"-- Database: {TARGET_DB_NAME}\n\n")
            fh.write("SET FOREIGN_KEY_CHECKS=0;\n")
            fh.write(f"CREATE DATABASE IF NOT EXISTS `{TARGET_DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
            fh.write(f"USE `{TARGET_DB_NAME}`;\n\n")

            # DDL
            for table_name in tables:
                table = metadata.tables[table_name]
                ddl = str(CreateTable(table).compile(dialect=mysql.dialect()))
                fh.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                fh.write(f"{ddl};\n\n")

            # DML
            with engine.connect() as conn:
                for table_name in tables:
                    rows = conn.execute(text(f'SELECT * FROM `{table_name}`')).mappings().all()
                    if not rows:
                        continue
                    columns = list(rows[0].keys())
                    col_list = ", ".join(f"`{col}`" for col in columns)
                    for row in rows:
                        values = ", ".join(sql_value(row[col]) for col in columns)
                        fh.write(f"INSERT INTO `{table_name}` ({col_list}) VALUES ({values});\n")
                    fh.write("\n")

            fh.write("SET FOREIGN_KEY_CHECKS=1;\n")

    print(f"Dump generado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()