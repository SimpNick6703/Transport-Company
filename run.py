from app import create_app, db
from app.models import Vehicle, Customer, Rental
import os

app = create_app()

# Create database directory if it doesn't exist
with app.app_context():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database', 'transport.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db.create_all()

if __name__ == '__main__':
    app.run()