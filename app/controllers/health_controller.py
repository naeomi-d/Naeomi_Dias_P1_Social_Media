from flask import Blueprint


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return {
        "status": "success",
        "message": "P1 Social Media API is running"
    }, 200