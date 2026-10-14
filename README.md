# CinePedia_Certificacion_FullStack-Python_Skillnest
Examen de Certificación FullStack Python, Skillnest 2026

## Datos del Estudiante
* **Nombre:** Arael Anabalón
* **Curso:** 4°C
* **Fecha:** 13/10/2026

## Descripción y Tecnologías
CinePedia es una aplicación web básica para la gestión y registro de películas desarrollada bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)**. El proyecto utiliza **Flask** como microframework principal, **Jinja2** para la renderización dinámica de datos, **Flask-Bcrypt** para la encriptación segura de contraseñas, y **PyMySQL** para la conexión con la base de datos MySQL. Para el diseño visual, se integró **Bootstrap 5 de forma local** con el objetivo de agilizar el desarrollo.

## Estructura de Carpetas
```text
C:.
│   .env
│   .gitattributes
│   .gitignore
│   LICENSE
│   Pipfile
│   Pipfile.lock
│   README.md
│   requirements.txt
│   server.py
│   
├───.vscode
│       settings.json
│       
└───flask_app
    │   __init__.py
    │   
    ├───config
    │       pymysqlconnection.py
    │       
    ├───controllers
    │       peliculas_controller.py
    │       usuarios_controller.py
    │       
    ├───db
    │       esquema_cinepedia.sql
    │       
    ├───models
    │       comentario.py
    │       pelicula.py
    │       usuario.py
    │       
    ├───static
    │   ├───css
    │   │       bootstrap.min.css
    │   │       
    │   └───js
    │           bootstrap.bundle.min.js
    │           
    └───templates
            base.html
            editar_pelicula.html
            iniciar_sesion.html
            nueva_pelicula.html
            peliculas.html
            registrarse.html
            ver_pelicula.html
```
