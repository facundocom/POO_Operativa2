# Control de Registro de Horarios - Flask + SQLAlchemy

Aplicación web para registrar entradas y salidas de trabajadores, consultar registros y gestionar dependencias, desarrollada con Flask y SQLAlchemy.
Realizada para la cátedra de Programacióin Orientada a Objetos, diseñada siguiendo dicho paradigma.

## Estructura del Proyecto

```
aplicacionSQLAlchemy/
│   app.py
│   config.py
│   datos.sqlite3
│   models.py
│
├── static/
│   ├── otros.txt
│   └── css/
│       └── estilos.css
│
├── templates/
│   ├── aviso.html
│   ├── base_template.html
│   ├── confirmar_salida.html
│   ├── consultar.html
│   ├── error.html
│   ├── inicio.html
│   ├── registrar_entrada.html
│   └── registrar_salida.html
│
└── __pycache__/
```

## Requisitos

- Python 3.10+
- Flask
- Flask-SQLAlchemy

Instala las dependencias con:

```sh
pip install flask flask_sqlalchemy
```

## Uso

1. Clona este repositorio.
2. Ejecuta la aplicación:

```sh
cd aplicacionSQLAlchemy
python app.py
```

3. Accede a [http://localhost:5000](http://localhost:5000) en tu navegador.

## Funcionalidades

- Registrar entrada de trabajadores.
- Registrar salida (con confirmación).
- Consultar registros por rango de fechas.
- Mensajes de error y confirmación amigables.
- Interfaz responsiva y moderna.

## Configuración

La configuración principal está en [`config.py`](aplicacionSQLAlchemy/config.py). La base de datos SQLite se almacena en `datos.sqlite3`.

## Estructura de la Base de Datos

- **trabajador**: id, nombre, apellido, dni, correo, legajo, horas, funcion
- **registrohorario**: id, fecha, horaentrada, horasalida, dependencia, idtrabajador

## Créditos

Desarrollado por Facundo Coria para la práctica de la materia POO, UNSJ - FCEFyN.

---
