from flask_app.config.pymysqlconnection import connectToMySQL

class Usuario:
    def __init__(self, data):
        # Datos propios de la tabla
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.contrasena = data['contrasena']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Inserar un nuevo usuario a la DB
    @classmethod
    def registrar_usuario(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, created_by)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s, 'Registro');
        """
        return connectToMySQL().query_db(query, data)

    # Buscar usuarios por su email (V>alidador)
    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        resultados = connectToMySQL().query_db(query, data)
        if resultados:
            return cls(resultados[0])
        return None

    # Buscar usuario específico por ID (Manejador de la sesión activa)
    @classmethod
    def obtener_por_id(cls, id_usuario):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id)s;"
        data = {'id': id_usuario}
        resultados = connectToMySQL().query_db(query, data)
        if resultados:
            return cls(resultados[0])
        return None
