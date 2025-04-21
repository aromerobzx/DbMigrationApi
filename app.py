from flask import Flask
from models import Base
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from routes.upload import upload_bp
from routes.stats import stats_bp

app = Flask(__name__)
app.register_blueprint(upload_bp)
app.register_blueprint(stats_bp)

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)