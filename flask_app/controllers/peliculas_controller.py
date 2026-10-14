from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

# Inicialización del Blueprint de películas
peliculas_bp = Blueprint('peliculas', __name__)

# Ruta para el panel principal de películas (dashboard)
@peliculas_bp.route('/cine')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    todas_peliculas = Pelicula.obtener_todas()
    return render_template('peliculas.html', peliculas=todas_peliculas)

# Ruta para el formulario y la lógica de una nueva película
@peliculas_bp.route('/cine/nueva', methods=['GET', 'POST'])
def nueva_pelicula():
    if 'usuario_id' not in session:
        flash("El usuario debe haber iniciado sesión para ver esta página", "peli_error")
        return redirect('/')

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        director = request.form.get('director', '').strip()
        fecha_estreno = request.form.get('fecha_estreno', '').strip()
        sinopsis = request.form.get('sinopsis', '').strip()

        session['form_titulo'] = titulo
        session['form_director'] = director
        session['form_fecha'] = fecha_estreno
        session['form_sinopsis'] = sinopsis

        if not titulo or not director or not fecha_estreno or not sinopsis or len(titulo) < 3 or len(director) < 3 or len(sinopsis) < 3:
            flash("Todos los campos son obligatorios y deben tener al menos 3 caracteres", "peli_error")
            return redirect('/cine/nueva')

        if Pelicula.obtener_por_titulo(titulo):
            flash("El nombre de la película debe ser único", "peli_error")
            return redirect('/cine/nueva')

        data = {
            'titulo': titulo, 
            'director': director, 
            'fecha_estreno': fecha_estreno,
            'sinopsis': sinopsis, 
            'publicador_id': session['usuario_id'], 
            'created_by': session['usuario_nombre']
        }
        Pelicula.guardar_pelicula(data)

        session.pop('form_titulo', None)
        session.pop('form_director', None)
        session.pop('form_fecha', None)
        session.pop('form_sinopsis', None)
        return redirect('/cine')

    return render_template('nueva_pelicula.html')

# Ruta para ver el detalle de una película y sus respectivos comentarios
@peliculas_bp.route('/cine/<int:id_pelicula>')
def ver_pelicula(id_pelicula):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula_seleccionada = Pelicula.obtener_por_id(id_pelicula)
    if not pelicula_seleccionada:
        return redirect('/cine')
    lista_comentarios = Comentario.obtener_por_pelicula(id_pelicula)
    return render_template('ver_pelicula.html', pelicula=pelicula_seleccionada, comentarios=lista_comentarios)

# Ruta para el formulario y la lógica de edición de una película
@peliculas_bp.route('/cine/editar/<int:id_pelicula>', methods=['GET', 'POST'])
def editar_pelicula(id_pelicula):
    if 'usuario_id' not in session:
        flash("El usuario debe haber iniciado sesión para ver esta página", "edit_error")
        return redirect('/')

    pelicula_seleccionada = Pelicula.obtener_por_id(id_pelicula)
    if not pelicula_seleccionada or pelicula_seleccionada.publicador_id != session['usuario_id']:
        return redirect('/cine')

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        director = request.form.get('director', '').strip()
        fecha_estreno = request.form.get('fecha_estreno', '').strip()
        sinopsis = request.form.get('sinopsis', '').strip()

        if not fecha_estreno:
            flash("Fecha de Estreno no puede estar vacía", "edit_error")
            return redirect(f'/cine/editar/{id_pelicula}')

        if not titulo or not director or not sinopsis:
            flash("Todos los campos obligatorios deben completarse", "edit_error")
            return redirect(f'/cine/editar/{id_pelicula}')

        if Pelicula.verificar_titulo_edicion(titulo, id_pelicula):
            flash("El nombre de la película debe ser único", "edit_error")
            return redirect(f'/cine/editar/{id_pelicula}')

        data = {
            'id_pelicula': id_pelicula, 
            'titulo': titulo, 
            'director': director,
            'fecha_estreno': fecha_estreno, 
            'sinopsis': sinopsis, 
            'updated_by': session['usuario_nombre']
        }
        Pelicula.editar_pelicula(data)
        return redirect('/cine')

    return render_template('editar_pelicula.html', pelicula=pelicula_seleccionada)

# Ruta para borrar una película
@peliculas_bp.route('/cine/borrar/<int:id_pelicula>')
def borrar_pelicula(id_pelicula):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula_seleccionada = Pelicula.obtener_por_id(id_pelicula)
    if pelicula_seleccionada and pelicula_seleccionada.publicador_id == session['usuario_id']:
        Pelicula.eliminar_pelicula(id_pelicula)
    return redirect('/cine')

# Ruta para guardar un nuevo comentario en una película
@peliculas_bp.route('/comentario/guardar/<int:id_pelicula>', methods=['POST'])
def guardar_comentario(id_pelicula):
    if 'usuario_id' not in session:
        return redirect('/')
    contenido = request.form.get('contenido', '').strip()
    pelicula_seleccionada = Pelicula.obtener_por_id(id_pelicula)

    if not pelicula_seleccionada or pelicula_seleccionada.publicador_id == session['usuario_id']:
        return redirect(f'/cine/{id_pelicula}')

    if contenido:
        data = {
            'contenido': contenido, 
            'comentador_id': session['usuario_id'],
            'pelicula_id': id_pelicula, 
            'created_by': session['usuario_nombre']
        }
        Comentario.guardar_comentario(data)
    return redirect(f'/cine/{id_pelicula}')

# Ruta para eliminar un comentario
@peliculas_bp.route('/comentario/eliminar/<int:id_comentario>')
def eliminar_comentario(id_comentario):
    if 'usuario_id' not in session:
        return redirect('/')
    comentario = Comentario.obtener_por_id(id_comentario)
    if not comentario:
        return redirect('/cine')
    id_pelicula = comentario.pelicula_id
    if comentario.comentador_id == session['usuario_id']:
        Comentario.eliminar_comentario(id_comentario)
    return redirect(f'/cine/{id_pelicula}')
