from flask import Flask
from .db import init_db
from .routes import main_bp
from config import SECRET_KEY, OPENAI_API_KEY

def create_app():
    print("==> Entrando a create_app()")  # esto debería aparecer en los logs

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['OPENAI_API_KEY'] = OPENAI_API_KEY
    app.register_blueprint(main_bp)
    init_db(app)
    return app

