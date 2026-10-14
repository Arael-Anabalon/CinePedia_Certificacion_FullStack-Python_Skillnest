from flask_app.config.pymysqlconnection import connectToMySQL

class Comentario:
    def __init__(self, data):
        self.id_comentario = data['id_comentario']
        self.contenido = data['contenido']
        self.comentador_id = data['comentador_id']
        self.pelicula_id = data['pelicula_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comentador_nombre = data.get('comentador_nombre', '')

    @classmethod
    def guardar_comentario(cls, data):
        query = """
            INSERT INTO comentarios (contenido, comentador_id, pelicula_id, created_by)
            VALUES (%(contenido)s, %(comentador_id)s, %(pelicula_id)s, %(created_by)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_por_pelicula(cls, id_pelicula):
        query = """
            SELECT comentarios.*, usuarios.nombre AS comentador_nombre 
            FROM comentarios 
            JOIN usuarios ON comentarios.comentador_id = usuarios.id_usuario 
            WHERE comentarios.pelicula_id = %(id)s 
            ORDER BY comentarios.created_at DESC;
        """
        resultados = connectToMySQL().query_db(query, {'id': id_pelicula})
        comentarios = []
        if resultados:
            for fila in resultados:
                comentarios.append(cls(fila))
        return comentarios

    @classmethod
    def obtener_por_id(cls, id_comentario):
        query = "SELECT * FROM comentarios WHERE id_comentario = %(id)s;"
        resultados = connectToMySQL().query_db(query, {'id': id_comentario})
        if not resultados:
            return None
        return cls(resultados[0])

    @classmethod
    def eliminar_comentario(cls, id_comentario):
        query = "DELETE FROM comentarios WHERE id_comentario = %(id)s;"
        return connectToMySQL().query_db(query, {'id': id_comentario})
