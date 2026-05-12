-- MySQL dump generated from local SQLite project data
-- Database: sammor96_sammor96_

SET FOREIGN_KEY_CHECKS=0;
CREATE DATABASE IF NOT EXISTS `sammor96_sammor96_` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `sammor96_sammor96_`;

DROP TABLE IF EXISTS `users`;

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	`role` VARCHAR(20) NOT NULL, 
	is_active BOOL NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)

;

DROP TABLE IF EXISTS `categorias`;

CREATE TABLE categorias (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	nombre VARCHAR(100) NOT NULL, 
	descripcion TEXT, 
	color VARCHAR(7), 
	icono VARCHAR(50), 
	activo BOOL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
)

;

DROP TABLE IF EXISTS `examenes`;

CREATE TABLE examenes (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	titulo VARCHAR(200) NOT NULL, 
	descripcion TEXT, 
	fecha_creacion DATETIME, 
	duracion_minutos INTEGER, 
	fecha_limite DATETIME, 
	publicado BOOL, 
	profesor_id INTEGER NOT NULL, 
	categoria_id INTEGER, 
	intentos_maximos INTEGER, 
	mostrar_respuestas BOOL, 
	barajar_preguntas BOOL, 
	calificacion_minima FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profesor_id) REFERENCES users (id), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id)
)

;

DROP TABLE IF EXISTS `preguntas`;

CREATE TABLE preguntas (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	examen_id INTEGER NOT NULL, 
	texto TEXT NOT NULL, 
	tipo VARCHAR(20) NOT NULL, 
	opciones TEXT, 
	respuesta_correcta TEXT, 
	puntos INTEGER, 
	orden INTEGER, 
	nivel_dificultad VARCHAR(20), 
	tiempo_estimado INTEGER, 
	explicacion TEXT, 
	imagen_url VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(examen_id) REFERENCES examenes (id)
)

;

DROP TABLE IF EXISTS `respuestas`;

CREATE TABLE respuestas (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	examen_id INTEGER NOT NULL, 
	estudiante_id INTEGER NOT NULL, 
	pregunta_id INTEGER NOT NULL, 
	respuesta_texto TEXT, 
	es_correcta BOOL, 
	puntos_obtenidos FLOAT, 
	fecha_respuesta DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(examen_id) REFERENCES examenes (id), 
	FOREIGN KEY(estudiante_id) REFERENCES users (id), 
	FOREIGN KEY(pregunta_id) REFERENCES preguntas (id)
)

;

DROP TABLE IF EXISTS `examenes_resultados`;

CREATE TABLE examenes_resultados (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	examen_id INTEGER NOT NULL, 
	estudiante_id INTEGER NOT NULL, 
	calificacion FLOAT, 
	total_puntos FLOAT, 
	fecha_inicio DATETIME, 
	fecha_fin DATETIME, 
	completado BOOL, 
	tiempo_utilizado INTEGER, 
	comentario_profesor TEXT, 
	recomendaciones TEXT, 
	fecha_presentacion DATETIME, 
	es_modo_practica BOOL, 
	solicitud_revision BOOL, 
	revision_completada BOOL, 
	fecha_solicitud_revision DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(examen_id) REFERENCES examenes (id), 
	FOREIGN KEY(estudiante_id) REFERENCES users (id)
)

;

DROP TABLE IF EXISTS `notificaciones`;

CREATE TABLE notificaciones (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	usuario_id INTEGER NOT NULL, 
	titulo VARCHAR(200) NOT NULL, 
	mensaje TEXT NOT NULL, 
	tipo VARCHAR(50), 
	leida BOOL, 
	fecha_creacion DATETIME, 
	url_destino VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES users (id)
)

;

DROP TABLE IF EXISTS `certificados`;

CREATE TABLE certificados (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	estudiante_id INTEGER NOT NULL, 
	examen_id INTEGER NOT NULL, 
	resultado_id INTEGER NOT NULL, 
	codigo_verificacion VARCHAR(100) NOT NULL, 
	fecha_emision DATETIME, 
	calificacion FLOAT NOT NULL, 
	archivo_pdf VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(estudiante_id) REFERENCES users (id), 
	FOREIGN KEY(examen_id) REFERENCES examenes (id), 
	FOREIGN KEY(resultado_id) REFERENCES examenes_resultados (id), 
	UNIQUE (codigo_verificacion)
)

;

DROP TABLE IF EXISTS `estudiante_examen`;

CREATE TABLE estudiante_examen (
	estudiante_id INTEGER NOT NULL, 
	examen_id INTEGER NOT NULL, 
	asignado_en DATETIME, 
	PRIMARY KEY (estudiante_id, examen_id), 
	FOREIGN KEY(estudiante_id) REFERENCES users (id), 
	FOREIGN KEY(examen_id) REFERENCES examenes (id)
)

;

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (1, 'smoreno', 'guest1234@gmail.com', 'scrypt:32768:8:1$PTl0ggS0Z9ay5eQS$c4821feff9fe768cd9461e96c2c230e4606357fe99fd033356fe77e2536a8c7e11afaf9a2aba99a1c74d6bd319c5f30f10f3fd3c1399d11877efc47638f37dd0', 'estudiante', '2025-11-10 19:20:25.958598', 1);
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (2, 'profesor', 'guestprofesor@gmail.com', 'scrypt:32768:8:1$vO9gqFuzj2ydU0ly$8a9296c810ace6eb57442b6752968348b2745930c63d849ecaac20585cfe7daa36406fbf4f6198c17d0fd536c43af401d7532e25de995f1476ce59809586f677', 'profesor', '2025-11-10 19:25:58.638206', 1);
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (3, 'felipe', 'estudiante25@gmail.com', 'scrypt:32768:8:1$79D76lC9aHNsXOOp$83342bb1bd05368790d5202555c94abc966eb3b8a03199a13385eb4b9bb6f4928c177f71d1aeac67bb6f758ea30e1d1b291ae79359e38e06b89241b6301ae595', 'estudiante', '2025-11-10 20:37:31.624716', 1);
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (4, 'juliansito', 'julian@gmail.com', 'scrypt:32768:8:1$JmSgoCwfhLY0EZpz$d6ad5bfd787d3ac2ad6961ccba0e7189e2602d43fd25ad5c6cb6c4c85abd7ae7cdaee84159a74f0a656ac416f4837b5377ec4145a5c801ba6c9d5910dfacbf63', 'estudiante', '2025-11-15 08:14:45.843884', 1);
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (5, 'profesor carlos', 'profesor@gmail.com', 'scrypt:32768:8:1$QuP0HVYdm3j0X47G$e1bb5ff6966e568354128e7136322c7147ad33f1bbcda0b55fdd5bc9a6908fc2288e408a31127f60be42f46e42b98b1b7b64d7ab5a5ceb9f83b921cf94b21043', 'profesor', '2025-11-15 08:16:04.621213', 1);
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `is_active`) VALUES (6, 'admin', 'admin@example.com', 'scrypt:32768:8:1$6kE9kN0EVMBRW3NW$7997cff05f71c26cd22949b844d4f595f4b336ea5b02cd17a94194bf6d02091e481295f0696f833f827eefe9130749600fb3c5bc7aab7c53c4829ed379f84ec7', 'admin', '2026-05-11 21:50:21.321831', 1);

INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (1, 'Matemáticas', 'Razonamiento matemático y cuantitativo', '#1976d2', '🔢', 1, '2025-11-10 20:01:20');
INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (2, 'Lectura Crítica', 'Comprensión lectora y análisis textual', '#388e3c', '📖', 1, '2025-11-10 20:01:20');
INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (3, 'Ciencias Naturales', 'Biología, Física y Química', '#7b1fa2', '🔬', 1, '2025-11-10 20:01:20');
INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (4, 'Ciencias Sociales', 'Historia, Geografía y Política', '#f57c00', '🌍', 1, '2025-11-10 20:01:20');
INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (5, 'Inglés', 'Comprensión y uso del idioma inglés', '#0097a7', '🌐', 1, '2025-11-10 20:01:20');
INSERT INTO `categorias` (`id`, `nombre`, `descripcion`, `color`, `icono`, `activo`, `created_at`) VALUES (6, 'General', 'Conocimientos generales y misceláneos', '#00695c', '📚', 1, '2025-11-10 20:01:20');

INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (1, 'matematicas', 'duppler', '2025-11-10 20:10:33.150406', 2, 1, 1, 0, 60.0, NULL, 60, NULL, 0);
INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (3, 'ingles', 'prubas', '2025-11-10 20:15:34.726431', 2, 1, 1, 0, 60.0, NULL, 60, NULL, 1);
INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (4, 'Español', 'lenguaje castellana', '2025-11-10 20:22:42.060038', 2, 1, 0, 1, 60.0, 2, 60, '2025-11-10 21:21:00.000000', 1);
INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (5, 'PHRASAL VERBS', 'Phrasal verbs are very common in English, especially in more informal contexts. They are made up of a verb and a particle or, sometimes, two particles', '2025-11-15 08:18:58.558292', 5, 1, 1, 1, 60.0, 5, 60, '2025-11-16 04:19:00.000000', 1);
INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (6, 'VERB TO BE', 'El verbo "to be" se utiliza para expresar estados, cualidades, características o ubicaciones de personas, animales o cosas. Por ejemplo:
Estado: "I am happy." (Yo estoy feliz.)
Ubicación: "They are in Europe." (Ellos están en Europa.)', '2025-11-15 08:31:13.558273', 5, 2, 1, 1, 60.0, 5, 60, '2025-11-15 06:34:00.000000', 1);
INSERT INTO `examenes` (`id`, `titulo`, `descripcion`, `fecha_creacion`, `profesor_id`, `intentos_maximos`, `mostrar_respuestas`, `barajar_preguntas`, `calificacion_minima`, `categoria_id`, `duracion_minutos`, `fecha_limite`, `publicado`) VALUES (7, 'VERB TO BE (Only One Attemp)', 'Ejemplo: Sally is leaving tomorrow and coming back on Saturday. (Sally se va mañana y vuelve el sábado.)', '2025-11-15 08:41:43.604398', 5, 2, 1, 0, 60.0, 5, 60, '2025-11-15 06:44:00.000000', 1);

INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (1, 1, 'prueba', 'verdadero_falso', '["Verdadero", "Falso"]', '', 5, 1, 'avanzado', 60, 'recetra', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (2, 4, 'pregunta 1', 'abierta', NULL, '', 5, 1, 'basico', 60, 'si', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (3, 3, 'prueba', 'verdadero_falso', '["Verdadero", "Falso"]', '', 5, 1, 'basico', 60, 's', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (4, 5, 'Subir/montarse
Get on - Subir/montarse', 'verdadero_falso', '["Verdadero", "Falso"]', '', 6, 1, 'intermedio', 70, 'Ejemplo: The bus was full. We couldn’t get on. (El autobús estaba completo, no pudimos subirnos.)', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (5, 5, 'Drive off - Marcharse (en un vehículo)', 'verdadero_falso', '["Verdadero", "Falso"]', '', 6, 2, 'basico', 70, 'Ejemplo: A woman got into the car and drove off. (Una mujer se subió al coche y se marchó.)', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (6, 5, 'Come back - Contra Ataque', 'verdadero_falso', '["Verdadero", "Falso"]', '', 6, 3, 'basico', 55, 'Ejemplo: Sally is leaving tomorrow and coming back on Saturday. (Sally se va mañana y vuelve el sábado.) 
Come back - Volver', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (7, 6, 'He ___ smart', 'opcion_multiple', '["are", "is", "it", "isnt"]', 'is', 6, 1, 'basico', 55, 'He is smart = Él es inteligente', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (8, 6, '__ is cold today (Hoy está hacienda frío)', 'opcion_multiple', '["It", "He", "She", "Are"]', 'It', 6, 2, 'basico', 55, 'Estar = It is cold today = Hoy está hacienda frío', NULL);
INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `opciones`, `respuesta_correcta`, `puntos`, `orden`, `nivel_dificultad`, `tiempo_estimado`, `explicacion`, `imagen_url`) VALUES (9, 7, 'there anybody inside? = ¿Hay alguien adentro?', 'opcion_multiple', '["Is", "Are", "It", "He"]', 'Is', 6, 1, 'basico', 70, '', NULL);

INSERT INTO `respuestas` (`id`, `examen_id`, `estudiante_id`, `pregunta_id`, `respuesta_texto`, `puntos_obtenidos`, `fecha_respuesta`, `es_correcta`) VALUES (1, 5, 4, 4, 'Verdadero', 0.0, '2025-11-15 08:23:21.374399', 0);
INSERT INTO `respuestas` (`id`, `examen_id`, `estudiante_id`, `pregunta_id`, `respuesta_texto`, `puntos_obtenidos`, `fecha_respuesta`, `es_correcta`) VALUES (2, 5, 4, 5, 'Verdadero', 0.0, '2025-11-15 08:23:21.374402', 0);
INSERT INTO `respuestas` (`id`, `examen_id`, `estudiante_id`, `pregunta_id`, `respuesta_texto`, `puntos_obtenidos`, `fecha_respuesta`, `es_correcta`) VALUES (3, 5, 4, 6, 'Falso', 0.0, '2025-11-15 08:23:21.374403', 0);

INSERT INTO `examenes_resultados` (`id`, `examen_id`, `estudiante_id`, `calificacion`, `total_puntos`, `fecha_inicio`, `fecha_fin`, `completado`, `comentario_profesor`, `recomendaciones`, `fecha_presentacion`, `tiempo_utilizado`, `es_modo_practica`, `solicitud_revision`, `revision_completada`, `fecha_solicitud_revision`) VALUES (1, 5, 4, 0.0, 0.0, '2025-11-15 08:23:21.371702', NULL, 1, NULL, NULL, '2025-11-15 03:23:21.370578', 10, 0, 0, 0, NULL);

INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (1, 1, '2025-11-10 20:20:36.342113');
INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (1, 4, '2025-11-10 21:46:13.766894');
INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (3, 4, '2025-11-10 21:46:13.766898');
INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (4, 5, '2025-11-15 08:30:13.050285');
INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (4, 6, '2025-11-15 08:33:54.886129');
INSERT INTO `estudiante_examen` (`estudiante_id`, `examen_id`, `asignado_en`) VALUES (4, 7, '2025-11-15 08:42:35.336233');

SET FOREIGN_KEY_CHECKS=1;
