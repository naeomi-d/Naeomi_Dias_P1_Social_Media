from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import Config


db = SQLAlchemy()
jwt = JWTManager()


@jwt.unauthorized_loader
def missing_jwt_token(reason):
    """Keep JWT failures consistent with the V1 API error format."""
    return jsonify({"error": "Authentication required."}), 401


@jwt.invalid_token_loader
def invalid_jwt_token(reason):
    return jsonify({"error": "Invalid authentication token."}), 401


@jwt.expired_token_loader
def expired_jwt_token(jwt_header, jwt_payload):
    return jsonify({"error": "Authentication token has expired."}), 401

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.models import (
        User,
        Post,
        Comment,
        Like,
        Follow,
        Bookmark,
        Hashtag,
        PostHashtag,
        Notification,
        Report,
        AdminAuditLog
    )

    with app.app_context():
        db.create_all()

    from app.controllers.health_controller import health_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.home_controller import home_bp
    from app.controllers.post_controller import post_bp
    from app.controllers.follow_controller import follow_bp
    from app.controllers.bookmark_controller import bookmark_bp
    from app.controllers.report_controller import report_bp
    from app.controllers.notification_controller import notification_bp
    from app.api.v1.notification_api import notification_api_bp
    from app.api.v1.auth_api import auth_api_bp
    from app.api.v1.user_api import user_api_bp
    from app.api.v1.post_api import post_api_bp
    from app.api.v1.comment_api import comment_api_bp
    from app.api.v1.like_api import like_api_bp
    from app.api.v1.follow_api import follow_api_bp
    from app.api.v1.bookmark_api import bookmark_api_bp
    from app.api.v1.hashtag_api import hashtag_api_bp
    from app.api.v1.report_api import report_api_bp
    from app.api.v1.admin_api import admin_api_bp

    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(follow_bp)
    app.register_blueprint(bookmark_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(notification_api_bp)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(user_api_bp)
    app.register_blueprint(post_api_bp)
    app.register_blueprint(comment_api_bp)
    app.register_blueprint(like_api_bp)
    app.register_blueprint(follow_api_bp)
    app.register_blueprint(bookmark_api_bp)
    app.register_blueprint(hashtag_api_bp)
    app.register_blueprint(report_api_bp)
    app.register_blueprint(admin_api_bp)

    from flask import send_from_directory

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app

