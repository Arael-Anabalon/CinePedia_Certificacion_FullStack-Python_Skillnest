import os
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

from flask_app.controllers.usuarios_controller import usuarios_bp
from flask_app.controllers.peliculas_controller import peliculas_bp

app.register_blueprint(usuarios_bp)
app.register_blueprint(peliculas_bp)
