"""Enrich Pregunta.opciones by ensuring each option dict has an 'explicacion' field.

Run: .venv/Scripts/python.exe scripts/enrich_preguntas_opciones.py
"""
import sys
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from app.extensions import db
from app.models import Pregunta


def enrich_option(option, pregunta_explicacion):
    # option is dict or other; ensure dict with keys texto, correcta, explicacion
    if not isinstance(option, dict):
        option = {"texto": str(option), "correcta": False}

    if 'texto' not in option:
        # attempt to find a text-like key
        for k in ('text', 'value', 'label'):
            if k in option:
                option['texto'] = option[k]
                break
        option.setdefault('texto', str(option))

    option.setdefault('correcta', bool(option.get('correcta') or option.get('correct')))

    # If pregunta_explicacion exists and option lacks explicacion, set it
    if 'explicacion' not in option or not option.get('explicacion'):
        option['explicacion'] = pregunta_explicacion or ''

    return option


def main():
    app = create_app()
    with app.app_context():
        preguntas = Pregunta.query.all()
        modified = 0
        for p in preguntas:
            if not p.opciones:
                continue
            try:
                parsed = json.loads(p.opciones)
            except Exception:
                # skip malformed
                continue

            changed = False
            new_opts = []
            if isinstance(parsed, list):
                for opt in parsed:
                    new_opt = enrich_option(opt, p.explicacion)
                    new_opts.append(new_opt)
                    if new_opt != opt:
                        changed = True
            elif isinstance(parsed, dict):
                new_opt = enrich_option(parsed, p.explicacion)
                new_opts = [new_opt]
                if new_opt != parsed:
                    changed = True
            else:
                # parsed is a primitive
                new_opts = [enrich_option(parsed, p.explicacion)]
                changed = True

            if changed:
                p.opciones = json.dumps(new_opts, ensure_ascii=False)
                modified += 1

        if modified:
            db.session.commit()
        print(f'Preguntas processed: {len(preguntas)}, modified: {modified}')


if __name__ == '__main__':
    main()
