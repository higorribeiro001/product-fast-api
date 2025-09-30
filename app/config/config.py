from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from app.routes.v1.product import product_ns
from app.routes.v1.user import user_ns
from app.utils.blacklist import BLACKLIST
from flask_cors import CORS
from app.utils.sql_alchemy import db

app = Flask(__name__)
db = db
migrate = Migrate(app, db)
load_dotenv()

class Config:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config['REDIS_URL'] = os.getenv('REDIS_URL')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    
    api = Api(
        blueprint,
        title="RESTFull API Teste Tech Solutio",
        version="1.0",
        description="Documentação da RESTFul api do teste da Tech Solutio",
        doc="/docs" 
    )

    @jwt.token_in_blocklist_loader
    def verifica_blacklist(self, token):
        return token['jti'] in BLACKLIST

    @jwt.revoked_token_loader
    def token_de_acesso_invalidado(jwt_header, jwt_payload):
        return jsonify({ 'message': 'You have been logged out.' }), 401

    api.add_namespace(product_ns)
    api.add_namespace(user_ns)

    app.register_blueprint(blueprint)

    CORS(app)
