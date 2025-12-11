from app.web import create_app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)