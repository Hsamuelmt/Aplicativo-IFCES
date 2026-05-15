"""Normalize Pregunta.opciones to a JSON list of dicts: {"texto": str, "correcta": bool}

Run with: .venv/Scripts/python.exe scripts/normalize_preguntas.py
"""
import sys
import os
import json

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from app.extensions import db
from app.models import Pregunta


def normalize_opciones(opciones_raw, respuesta_correcta):
    # Return list of dicts {texto, correcta}
    if not opciones_raw:
        if respuesta_correcta:
            return [{"texto": respuesta_correcta, "correcta": True}]
        return []

    # Try to load JSON
    try:
        parsed = json.loads(opciones_raw)
    except Exception:
        # Fallback: split by newline or comma
        parts = [p.strip() for p in opciones_raw.split('\n') if p.strip()]
        if len(parts) == 1 and ',' in parts[0]:
            parts = [p.strip() for p in parts[0].split(',') if p.strip()]
        parsed = parts

    normalized = []
    # If parsed is list
    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict):
                texto = item.get('texto') or item.get('text') or item.get('value') or item.get('label') or str(item)
                correcta = bool(item.get('correcta') or item.get('correct') or item.get('is_correct'))
                # If respuesta_correcta equals texto, mark correct
                if respuesta_correcta and texto == respuesta_correcta:
                    correcta = True
                normalized.append({"texto": texto, "correcta": correcta})
            else:
                texto = str(item)
                correcta = (respuesta_correcta is not None and texto == respuesta_correcta)
                normalized.append({"texto": texto, "correcta": correcta})
    elif isinstance(parsed, dict):
        # Single dict -> try to pull options from keys
        # Treat as single option
        texto = parsed.get('texto') or parsed.get('text') or str(parsed)
        correcta = bool(parsed.get('correcta') or parsed.get('correct'))
        if respuesta_correcta and texto == respuesta_correcta:
            correcta = True
        normalized.append({"texto": texto, "correcta": correcta})
    else:
        # Other types -> fallback
        texto = str(parsed)
        correcta = (respuesta_correcta is not None and texto == respuesta_correcta)
        normalized.append({"texto": texto, "correcta": correcta})

    return normalized


def main():
    app = create_app()
    with app.app_context():
        preguntas = Pregunta.query.all()
        modified = 0
        for p in preguntas:
            orig = p.opciones
            try:
                norm = normalize_opciones(orig, p.respuesta_correcta)
            except Exception as e:
                print(f'Error normalizing pregunta {p.id}: {e}')
                continue

            # If normalized differs, update
            try:
                norm_json = json.dumps(norm, ensure_ascii=False)
            except Exception:
                norm_json = json.dumps([], ensure_ascii=False)

            if orig != norm_json:
                p.opciones = norm_json
                modified += 1
        if modified:
            db.session.commit()
        print(f'Preguntas checked: {len(preguntas)}, modified: {modified}')


if __name__ == '__main__':
    main()
