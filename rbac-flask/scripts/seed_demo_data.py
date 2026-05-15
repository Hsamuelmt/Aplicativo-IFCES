"""Seed demo data: admin, profesores, estudiantes, categoria, examen, preguntas.
Run: python scripts/seed_demo_data.py
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / '.env')

from app import create_app
from app.extensions import db
from app.models import User, Categoria, Examen, Pregunta

app = create_app()

def create_user(username, email, password, role):
    u = User.query.filter((User.username==username)|(User.email==email)).first()
    if u:
        print(f"Existente: {username} ({u.role})")
        return u
    u = User(username=username, email=email, role=role)
    u.set_password(password)
    db.session.add(u)
    db.session.flush()
    print(f"Creado: {username} -> {role}")
    return u

def seed():
    with app.app_context():
        # Create admin
        admin = create_user('admin', 'admin@example.com', 'Admin123!', 'admin')

        # Create professors
        prof1 = create_user('prof_jose', 'jose@ifces.edu', 'Prof12345', 'profesor')
        prof2 = create_user('prof_maria', 'maria@ifces.edu', 'Prof12345', 'profesor')

        # Create students
        students = []
        for i in range(1,6):
            s = create_user(f'estudiante{i}', f'estudiante{i}@mail.com', f'Est{i}Pass!', 'estudiante')
            students.append(s)

        # Category
        cat = Categoria.query.filter_by(nombre='Matematicas').first()
        if not cat:
            cat = Categoria(nombre='Matematicas', descripcion='Pruebas de matematicas basicas')
            db.session.add(cat)
            print('Categoria creada: Matematicas')

        db.session.flush()

        # Create an exam by prof_jose
        examen = Examen.query.filter_by(titulo='Examen Demo ICFES').first()
        if not examen:
            examen = Examen(titulo='Examen Demo ICFES', descripcion='Examen de prueba', profesor_id=prof1.id, categoria_id=cat.id, publicado=True, duracion_minutos=60)
            db.session.add(examen)
            db.session.flush()
            print('Examen creado: Examen Demo ICFES')

            # Add sample questions
            q1 = Pregunta(examen_id=examen.id, texto='¿Cuánto es 2+2?', tipo='opcion_multiple', opciones='["3","4","5"]', respuesta_correcta='4', puntos=1)
            q2 = Pregunta(examen_id=examen.id, texto='¿Verdadero o falso: 5 es mayor que 3?', tipo='verdadero_falso', opciones='["True","False"]', respuesta_correcta='True', puntos=1)
            db.session.add_all([q1, q2])
            print('Preguntas añadidas al examen')

        db.session.commit()

        # Assign exam to students (many-to-many table via relationship)
        for s in students:
            if examen not in s.examenes_asignados:
                s.examenes_asignados.append(examen)
                print(f'Asignado examen a: {s.username}')

        db.session.commit()

        # Summary
        total_users = User.query.count()
        total_prof = User.query.filter_by(role='profesor').count()
        total_students = User.query.filter_by(role='estudiante').count()
        total_exams = Examen.query.count()
        total_questions = Pregunta.query.count()

        print('\n=== Resumen de semilla ===')
        print(f'Usuarios: {total_users} (Profesores: {total_prof}, Estudiantes: {total_students})')
        print(f'Examenes: {total_exams}, Preguntas: {total_questions}')

if __name__ == '__main__':
    seed()
