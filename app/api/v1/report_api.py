from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_report
from app.services.report_service import ReportService
from app.services.admin_service import AdminService
from app.utils.auth_utils import has_any_role, role_required


report_api_bp = Blueprint("report_api", __name__, url_prefix="/api/v1")


def _report_data():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("A JSON request body is required.")
    return data


@report_api_bp.post("/posts/<int:post_id>/reports")
@jwt_required()
def report_post(post_id):
    try:
        data = _report_data()
        report = ReportService.report_post(current_user_id(), post_id, data.get("reason"), data.get("description"))
        return jsonify({"message": "Post reported successfully.", "report": serialize_report(report)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 422)


@report_api_bp.post("/users/<int:user_id>/reports")
@jwt_required()
def report_user(user_id):
    try:
        data = _report_data()
        report = ReportService.report_user(current_user_id(), user_id, data.get("reason"), data.get("description"))
        return jsonify({"message": "User reported successfully.", "report": serialize_report(report)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 422)


@report_api_bp.get("/reports/me")
@jwt_required()
def get_my_reports():
    return jsonify({"reports": [serialize_report(report) for report in ReportService.get_my_reports(current_user_id())]}), 200


@report_api_bp.get("/reports")
@role_required("MODERATOR", "ADMIN")
def get_reports_for_moderation():
    reports = ReportService.get_pending_reports()
    return jsonify({"reports": [serialize_report(report) for report in reports]}), 200


@report_api_bp.get("/reports/<int:report_id>")
@jwt_required()
def get_report(report_id):
    try:
        report = ReportService.get_report(
            report_id,
            current_user_id(),
            has_any_role("MODERATOR", "ADMIN"),
        )
        return jsonify({"report": serialize_report(report)}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@report_api_bp.patch("/reports/<int:report_id>")
@role_required("MODERATOR", "ADMIN")
def review_report(report_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "status" not in data:
        return error_response("A JSON body with status is required.", 400)

    try:
        report = AdminService.review_report(
            report_id,
            current_user_id(),
            data["status"],
        )
        return jsonify({
            "message": "Report reviewed successfully.",
            "report": serialize_report(report),
        }), 200
    except ValueError as error:
        return error_response(
            str(error),
            404 if "not found" in str(error).lower() else 422,
        )


@report_api_bp.delete("/reports/<int:report_id>")
@jwt_required()
def cancel_report(report_id):
    try:
        ReportService.cancel_report(report_id, current_user_id())
        return "", 204
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)
    except PermissionError as error:
        return error_response(str(error), 403)
