from flask import Blueprint, jsonify, request

from app.api.v1.common import current_user_id, error_response, serialize_audit_log, serialize_report, serialize_user
from app.services.admin_audit_log_service import AdminAuditLogService
from app.services.admin_service import AdminService
from app.services.report_service import ReportService
from app.utils.auth_utils import role_required


admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


@admin_api_bp.get("/reports")
@role_required("ADMIN")
def get_pending_reports():
    reports = ReportService.get_pending_reports()
    return jsonify({"reports": [serialize_report(report) for report in reports]}), 200


@admin_api_bp.patch("/reports/<int:report_id>")
@role_required("ADMIN")
def review_report(report_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "status" not in data:
        return error_response("A JSON body with status is required.", 400)
    try:
        report = AdminService.review_report(report_id, current_user_id(), data["status"])
        return jsonify({"message": "Report reviewed successfully.", "report": serialize_report(report)}), 200
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 422)


@admin_api_bp.get("/audit-logs")
@role_required("ADMIN")
def get_audit_logs():
    logs = AdminAuditLogService.get_logs()
    return jsonify({"audit_logs": [serialize_audit_log(log) for log in logs]}), 200


@admin_api_bp.get("/audit-logs/<int:audit_log_id>")
@role_required("ADMIN")
def get_audit_log(audit_log_id):
    try:
        return jsonify({"audit_log": serialize_audit_log(AdminAuditLogService.get_log(audit_log_id))}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@admin_api_bp.get("/users")
@role_required("ADMIN")
def get_users():
    return jsonify({"users": [serialize_user(user, True) for user in AdminService.get_users()]}), 200
