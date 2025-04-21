from flask import Flask
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.routes.upload import upload_bp
from app.routes.stats import stats_bp

def create_app():
    app = Flask(__name__)

    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

    app.register_blueprint(upload_bp)
    app.register_blueprint(stats_bp)

    return app