from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app, abort
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Material, Mensaje, User
from ..models import Examen
from ..decorators import role_required

shared_bp = Blueprint('compartir', __name__, url_prefix='/compartir')


@shared_bp.route('/materiales')
@login_required
def listar_materiales():
    # Mostrar materiales públicos y los subidos por el usuario (si es profesor)
    if current_user.is_profesor:
        materiales = Material.query.order_by(Material.created_at.desc()).all()
    else:
        # Estudiante: ver materiales públicos, con enlace, o asignados a exámenes del estudiante
        examenes_ids = [e.id for e in current_user.examenes_asignados]
        materiales = Material.query.filter(
            (Material.publico == True) |
            (Material.enlace_externo != None) |
            (Material.examen_id.in_(examenes_ids) if examenes_ids else False)
        ).order_by(Material.created_at.desc()).all()
    return render_template('shared/materiales.html', materiales=materiales)


@shared_bp.route('/materiales/subir', methods=['GET', 'POST'])
@login_required
@role_required('profesor')
def subir_material():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        publico = request.form.get('publico') == 'on'
        enlace = request.form.get('enlace', '').strip() or None

        examen_id = request.form.get('examen_id')
        archivo = request.files.get('archivo')
        filename = None
        if archivo and archivo.filename:
            filename = secure_filename(archivo.filename)
            upload_dir = os.path.join(current_app.instance_path, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            archivo.save(os.path.join(upload_dir, filename))

        examen_ref = int(examen_id) if examen_id else None
        material = Material(titulo=titulo or 'Sin título', descripcion=descripcion, archivo=filename, enlace_externo=enlace, publico=publico, uploader_id=current_user.id, examen_id=examen_ref)
        db.session.add(material)
        db.session.commit()
        flash('Material subido correctamente', 'success')
        return redirect(url_for('compartir.listar_materiales'))

    # Mostrar exámenes del profesor para asignación
    examenes = Examen.query.filter_by(profesor_id=current_user.id).all()
    return render_template('shared/subir_material.html', examenes=examenes)


@shared_bp.route('/uploads/<path:filename>')
@login_required
def descargar_archivo(filename):
    upload_dir = os.path.join(current_app.instance_path, 'uploads')
    return send_from_directory(upload_dir, filename, as_attachment=True)


@shared_bp.route('/mensajes')
@login_required
def listar_mensajes():
    # Mostrar mensajes donde current_user es destinatario o broadcasts (destinatario_id is NULL)
    mensajes = Mensaje.query.filter((Mensaje.destinatario_id == current_user.id) | (Mensaje.destinatario_id == None)).order_by(Mensaje.fecha_creacion.desc()).all()
    usuarios = User.query.filter(User.role.in_(['profesor', 'estudiante'])).all()
    return render_template('shared/mensajes.html', mensajes=mensajes, usuarios=usuarios)


@shared_bp.route('/mensajes/enviar', methods=['GET', 'POST'])
@login_required
@role_required('profesor')
def enviar_mensaje():
    if request.method == 'POST':
        destinatario_id = request.form.get('destinatario')
        asunto = request.form.get('asunto', '').strip()
        cuerpo = request.form.get('cuerpo', '').strip()
        enlace = request.form.get('enlace', '').strip() or None

        dest = None
        if destinatario_id and destinatario_id != 'broadcast':
            try:
                dest = int(destinatario_id)
            except ValueError:
                dest = None

        msg = Mensaje(remitente_id=current_user.id, destinatario_id=dest, asunto=asunto, cuerpo=cuerpo, enlace=enlace)
        db.session.add(msg)
        db.session.commit()
        flash('Mensaje enviado', 'success')
        return redirect(url_for('compartir.listar_mensajes'))

    usuarios = User.query.filter(User.role == 'estudiante', User.is_active == True).all()
    return render_template('shared/enviar_mensaje.html', usuarios=usuarios)
