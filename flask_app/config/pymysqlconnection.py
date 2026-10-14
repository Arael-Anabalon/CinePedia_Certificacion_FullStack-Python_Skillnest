import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

# Clase conectora entre python y la DB
class MySQLConnection:
    def __init__(self):
        self.connection = pymysql.connect(
            # Variables de entorno guardadas en .env
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),  
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    # Función para las consultas
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Cursor para las querys
                cursor.execute(query, data)
                # Limpia las querys
                tipo_consulta = query.strip().lower()
                # Si es SELECT devuelve filas encontradas
                if tipo_consulta.startswith("select"):
                    return cursor.fetchall()
                # Si es INSERT devuelve el ID del nuevo registro
                if tipo_consulta.startswith("insert"):
                    return cursor.lastrowid
                # Si es DELETE o UPDATE devuelve cuantas filas afectó
                return cursor.rowcount
            except Exception as e:
                # Error en consola si algo falla
                print("Something went wrong:", e)
                raise e 
            # Cierra la conexión para no saturar la base de datos
            finally:
                self.connection.close()

# Funcion global para conectar de forma rápida
def connectToMySQL(db=None):
    return MySQLConnection()