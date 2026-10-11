from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app(config_object=None) -> Flask:
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(
            JWT_SECRET_KEY="dev-secret-change-in-prod"
        )

    CORS(app)
    JWTManager(app)
    
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://" 
    )

    from app.api.auth import blp as auth_blp
    app.register_blueprint(auth_blp)
    
    from app.web.routes import web_blp
    app.register_blueprint(web_blp)
    
    @app.route("/health/live")
    def liveness():
        return jsonify({"status": "ok"})
        
    return app
