from flask import (
    Flask,
    jsonify,
    request,
    flash,
    redirect,
    url_for,
    send_from_directory,
    session
)

import logging
from logging.handlers import RotatingFileHandler
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from app.config import Config
from app.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError
)



db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
swagger = Swagger()


@jwt.unauthorized_loader
def missing_jwt_token(reason):

    return jsonify({
        "error": "Authentication required."
    }), 401


@jwt.invalid_token_loader
def invalid_jwt_token(reason):

    return jsonify({
        "error": "Invalid authentication token."
    }), 401


@jwt.expired_token_loader
def expired_jwt_token(jwt_header, jwt_payload):

    return jsonify({
        "error": "Authentication token has expired."
    }), 401



def create_app(config_override=None):

    app = Flask(__name__)

    app.config.from_object(Config)

    if config_override:
        app.config.update(config_override)

    app.config["SWAGGER"] = {
    "title": "Postly API",
    "description": "REST API for the Postly application.",
    "version": "1.0.0",
    "specs_route": "/api/docs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <JWT>"
        }
    }
}

    swagger.init_app(app)

    log_folder = app.config["LOG_FOLDER"]
    log_file = app.config["LOG_FILE"]

    os.makedirs(
        log_folder,
        exist_ok=True
    )

    app_logger = app.logger

    app_logger.setLevel(logging.INFO)

    for handler in app_logger.handlers[:]:
        app_logger.removeHandler(handler)

   
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    app_logger.addHandler(file_handler)

    app_logger.propagate = False

    
    application_logger = logging.getLogger("app")

    application_logger.setLevel(logging.INFO)

    application_logger.propagate = False

    if file_handler not in application_logger.handlers:
        application_logger.addHandler(file_handler)

    app_logger.info(
        "Application started."
    )

    
    @app.after_request
    def log_request(response):

        user_id = session.get("user_id", "anonymous")
        role = session.get("role", "ANONYMOUS")

        app_logger.info(
            "Request | user_id=%s | role=%s | method=%s | "
            "path=%s | status=%s",
            user_id,
            role,
            request.method,
            request.path,
            response.status_code
        )

        return response

    from app.utils.datetime_utils import format_ist_datetime

    app.jinja_env.filters["ist_datetime"] = format_ist_datetime


    @app.errorhandler(AppException)
    def handle_app_exception(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": error.message
            }), error.status_code

        flash(
            error.message,
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": error.message
            }), error.status_code

        flash(
            error.message,
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": error.message
            }), error.status_code

        flash(
            error.message,
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found_error(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": error.message
            }), error.status_code

        flash(
            error.message,
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": error.message
            }), error.status_code

        flash(
            error.message,
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    @app.errorhandler(404)
    def handle_not_found(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": "Resource not found."
            }), 404

        flash(
            "The requested page could not be found.",
            "warning"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    @app.errorhandler(413)
    def handle_request_entity_too_large(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": "File size exceeds maximum limit of 5MB."
            }), 413

        flash(
            "File size exceeds maximum limit of 5MB.",
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(error):

        if request.path.startswith("/api/"):
            return jsonify({
                "error": "Too many requests. Please try again later."
            }), 429

        flash(
            "Too many requests. Please try again later.",
            "warning"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):

        app.logger.exception(
            "Unhandled application exception: %s",
            error
        )

        if request.path.startswith("/api/"):
            return jsonify({
                "error": "An unexpected server error occurred."
            }), 500

        flash(
            "An unexpected server error occurred.",
            "danger"
        )

        return redirect(
            request.referrer or url_for("home.home")
        )

    
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    
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
    from app.controllers.moderator_controller import moderator_bp
    from app.controllers.admin_controller import admin_bp

    
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
    from app.api.v1.moderator_api import moderator_api_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(follow_bp)
    app.register_blueprint(bookmark_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(moderator_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(moderator_api_bp)

    
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


    from app.services.file_service import FileService


    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):

        safe_path = FileService.get_safe_file_path(
            f"/uploads/{filename}"
        )

        if not safe_path or not os.path.exists(safe_path):

            return jsonify({
                "error": "File not found."
            }), 404

        directory = os.path.dirname(safe_path)
        base_name = os.path.basename(safe_path)

        return send_from_directory(
            directory,
            base_name
        )

    
    return app