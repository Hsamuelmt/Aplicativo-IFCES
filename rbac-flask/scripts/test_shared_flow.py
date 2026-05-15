"""Test shared materials flow: create profesor, estudiante, examen, assign, material, verify visibility."""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from app.extensions import db
from app.models import User, Examen, Material


def main():
    app = create_app()
    with app.app_context():
        # Create users
        prof = User.query.filter_by(username='test_prof').first()
        if not prof:
            prof = User(username='test_prof', email='prof@example.com', role='profesor')
            prof.set_password('ProfPass1!')
            db.session.add(prof)
            db.session.commit()

        student = User.query.filter_by(username='test_student').first()
        if not student:
            student = User(username='test_student', email='student@example.com', role='estudiante')
            student.set_password('StudPass1!')
            db.session.add(student)
            db.session.commit()

        # Create exam by professor
        exam = Examen.query.filter_by(titulo='Test Exam Shared').first()
        if not exam:
            exam = Examen(titulo='Test Exam Shared', descripcion='Exam for material assignment', profesor_id=prof.id)
            db.session.add(exam)
            db.session.commit()

        # Assign student to exam
        if student not in exam.estudiantes:
            exam.estudiantes.append(student)
            db.session.commit()

        # Create material assigned to exam (not public)
        mat = Material.query.filter_by(titulo='Material Test Shared').first()
        if not mat:
            mat = Material(titulo='Material Test Shared', descripcion='Material assigned to exam', publico=False, uploader_id=prof.id, examen_id=exam.id)
            db.session.add(mat)
            db.session.commit()

        # Now emulate listing for student
        exam_ids = [e.id for e in student.examenes_asignados]
        visible = Material.query.filter(
            (Material.publico == True) |
            (Material.enlace_externo != None) |
            (Material.examen_id.in_(exam_ids) if exam_ids else False)
        ).all()

        print('Visible materials for student:', [m.titulo for m in visible])


if __name__ == '__main__':
    main()
