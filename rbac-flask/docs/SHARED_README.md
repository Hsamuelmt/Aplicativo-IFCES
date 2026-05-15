Shared Materials & Messaging
=============================

Rutas principales
- `/compartir/materiales` — listar materiales (estudiantes ven públicos, con enlace o asignados a sus exámenes).
- `/compartir/materiales/subir` — subir material (solo `profesor`).
- `/compartir/uploads/<filename>` — descargar archivos subidos (requiere login).
- `/compartir/mensajes` — lista de mensajes.
- `/compartir/mensajes/enviar` — enviar mensaje (solo `profesor`).

Pruebas manuales
1. Activar virtualenv y arrancar la app:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

2. Login como profesor y subir material:
- Ir a `/compartir/materiales/subir`, completar título, archivo o enlace, opcionalmente asignar a un examen.

3. Login como estudiante y comprobar visibilidad:
- Ir a `/compartir/materiales` y verificar que aparecen los materiales públicos o asignados a exámenes asignados.

Scripts útiles
- `scripts/normalize_preguntas.py` — normaliza `Pregunta.opciones`.
- `scripts/add_material_examen_column.py` — asegura la columna `examen_id`.
- `scripts/test_shared_flow.py` — crea usuarios de prueba y verifica visibilidad.
- `scripts/cleanup_uploads.py [days]` — limpia archivos en `instance/uploads` mayores a `days` (30 por defecto).

Notas de despliegue
- Asegurar que `instance/uploads` exista y que el servicio web tenga permisos de escritura.
- En `config.py` se define `UPLOAD_FOLDER` apuntando a `instance/uploads` y `MAX_CONTENT_LENGTH`.
