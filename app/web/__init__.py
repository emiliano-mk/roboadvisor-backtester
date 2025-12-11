from flask import Flask
from app.routes.main import main
from app.routes.transactions import transactions_bp
from app.routes.portfolio import portfolio_bp
from app.extensions import db
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    # Configuración de DB (archivo sqlite dentro de la carpeta principal `data/`)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(portfolio_bp)

    return app
