"""Test script: login as estudiante1 and submit a sample response via test_client."""
import os, sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / '.env')

from app import create_app
from app.extensions import db
from app.models import User, Examen

app = create_app()

with app.app_context():
    # Find an exam assigned to estudiante1
    user = User.query.filter_by(username='estudiante1').first()
    if not user:
        print('estudiante1 not found')
        sys.exit(1)

    # Get one assigned exam
    exam = None
    for e in user.examenes_asignados:
        exam = e
        break
    if not exam:
        print('No exam assigned to estudiante1')
        sys.exit(1)

    print(f'Found exam id={exam.id} title={exam.titulo}')

    client = app.test_client()
    # Login
    resp = client.post('/login', data={'username':'estudiante1','password':'Est1Pass!'}, follow_redirects=True)
    print('Login status:', resp.status_code)

    # Prepare sample responses: choose first options or true/false
    payload = {}
    for p in exam.preguntas:
        if p.tipo == 'opcion_multiple':
            try:
                opts = __import__('json').loads(p.opciones)
                payload[f'pregunta_{p.id}'] = opts[0]['texto'] if isinstance(opts, list) and opts else ''
            except Exception:
                payload[f'pregunta_{p.id}'] = ''
        elif p.tipo == 'verdadero_falso':
            # match template values "Verdadero"/"Falso"
            payload[f'pregunta_{p.id}'] = 'Verdadero'
        else:
            payload[f'pregunta_{p.id}'] = 'Respuesta de prueba'

    payload['tiempo_utilizado'] = 30

    print('Posting to enviar endpoint...')
    r = client.post(f'/estudiante/examen/{exam.id}/enviar', json=payload)
    print('Response status:', r.status_code)
    try:
        print('Response JSON:', r.get_json())
    except Exception as e:
        print('Error parsing JSON:', e)
        print('Raw data:', r.data)


