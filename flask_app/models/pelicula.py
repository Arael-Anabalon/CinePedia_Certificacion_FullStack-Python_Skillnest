from flask_app.config.pymysqlconnection import connectToMySQL

class Pelicula:
    def __init__(self, data):
        # Datos propios de la tabla
        self.id_pelicula = data['id_pelicula']
        self.titulo = data['titulo']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.publicador_id = data['publicador_id']
        # Datos del publicador obtenidos gracias a JOIN
        self.publicador_nombre = data.get('publicador_nombre', '')

    # Insertar una nueva película a la DB
    @classmethod
    def guardar_pelicula(cls, data):
        query = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, publicador_id, created_by)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(publicador_id)s, %(created_by)s);
        """
        return connectToMySQL().query_db(query, data)

    # Editar una película de la DB
    @classmethod
    def editar_pelicula(cls, data):
        query = """
            UPDATE peliculas
            SET titulo = %(titulo)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s, updated_by = %(updated_by)s
            WHERE id_pelicula = %(id_pelicula)s;
        """
        return connectToMySQL().query_db(query, data)

    # Eliminar una película de la DB
    @classmethod
    def eliminar_pelicula(cls, id_pelicula):
        query = "DELETE FROM peliculas WHERE id_pelicula = %(id)s;"
        return connectToMySQL().query_db(query, {'id': id_pelicula})

    # Traer todas las películas de la DB junto con queien la publicó
    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT peliculas.*, usuarios.nombre AS publicador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.publicador_id = usuarios.id_usuario;
        """
        resultados = connectToMySQL().query_db(query)
        peliculas = []
        if resultados:
            for fila in resultados:
                peliculas.append(cls(fila))
        return peliculas

    # Buscar una película en especifico por su ID
    @classmethod
    def obtener_por_id(cls, id_pelicula):
        query = """
            SELECT peliculas.*, usuarios.nombre AS publicador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.publicador_id = usuarios.id_usuario 
            WHERE peliculas.id_pelicula = %(id)s;
        """
        resultados = connectToMySQL().query_db(query, {'id': id_pelicula})
        if not resultados:
            return None
        return cls(resultados[0])

    # Buscar una película por su título (Validador)
    @classmethod
    def obtener_por_titulo(cls, titulo):
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s;"
        resultados = connectToMySQL().query_db(query, {'titulo': titulo})
        if not resultados:
            return None
        return cls(resultados[0])

    # Evitar títulos duplicados
    @classmethod
    def verificar_titulo_edicion(cls, titulo, id_pelicula):
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s AND id_pelicula != %(id)s;"
        resultados = connectToMySQL().query_db(query, {'titulo': titulo, 'id': id_pelicula})
        if not resultados:
            return None
        return cls(resultados[0])
