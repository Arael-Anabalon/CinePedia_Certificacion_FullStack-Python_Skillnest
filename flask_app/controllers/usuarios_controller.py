from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.usuario import Usuario
from flask_app import bcrypt
import re

usuarios_bp = Blueprint('usuarios', __name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@usuarios_bp.route('/')
def iniciar_sesion():
    if 'usuario_id' in session:
        return redirect('/cine') 
    return render_template('iniciar_sesion.html')

@usuarios_bp.route('/registrarse')
def registrarse():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('registrarse.html')

@usuarios_bp.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    email = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '')
    confirmar = request.form.get('confirmar_contrasena', '')

    session['reg_nombre'] = nombre
    session['reg_apellido'] = apellido
    session['reg_email'] = email

    errores = False
    if len(nombre) < 2 or len(apellido) < 2:
        flash("Nombre y apellido deben de tener al menos 2 caracteres", "registro")
        errores = True
    if not EMAIL_REGEX.match(email):
        flash("Email debe de tener un formato válido", "registro")
        errores = True
    if contrasena != confirmar:
        flash("Contraseña y Confirmación deben de ser iguales", "registro")
        errores = True
    if Usuario.obtener_por_email(email):
        flash("El email no puede repetirse en la BD", "registro")
        errores = True

    if errores:
        return redirect('/registrarse')

    password_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    data = {
        'nombre': nombre, 
        'apellido': apellido, 
        'email': email, 
        'contrasena': password_hash
    }
    id_nuevo_usuario = Usuario.registrar_usuario(data)
    
    session.pop('reg_nombre', None)
    session.pop('reg_apellido', None)
    session.pop('reg_email', None)

    session['usuario_id'] = id_nuevo_usuario
    session['usuario_nombre'] = nombre
    return redirect('/cine')

@usuarios_bp.route('/procesar_inicio_sesion', methods=['POST'])
def procesar_inicio_sesion():
    email = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '')

    usuario_encontrado = Usuario.obtener_por_email(email)
    if not usuario_encontrado:
        flash("El email debe estar registrado en BD", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario_encontrado.contrasena, contrasena):
        flash("La contraseña debe ser la correspondiente a la BD", "login")
        return redirect('/')

    session['usuario_id'] = usuario_encontrado.id_usuario
    session['usuario_nombre'] = usuario_encontrado.nombre
    return redirect('/cine')

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
