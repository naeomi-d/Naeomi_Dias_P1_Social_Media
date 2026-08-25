from flask import Blueprint, jsonify, request

from app.api.v1.common import (
    current_user_id,
    error_response,
    serialize_report
)

from app.services.moderator_service import ModeratorService
from app.utils.auth_utils import role_required


moderator_api_bp = Blueprint(
    "moderator_api",
    __name__,
    url_prefix="/api/v1/moderator"
)


@moderator_api_bp.get("/reports")
@role_required("MODERATOR", "ADMIN")
def get_pending_reports():
    """
    Get all pending reports.
    ---
    tags:
      - Moderator
    security:
      - Bearer: []
    responses:
      200:
        description: List of pending reports.
      401:
        description: Authentication required or invalid token.
      403:
        description: User does not have moderator or admin privileges.
    """

    reports = ModeratorService.get_pending_reports()

    return jsonify({
        "reports": [
            serialize_report(report)
            for report in reports
        ]
    }), 200


@moderator_api_bp.get("/reports/<int:report_id>")
@role_required("MODERATOR", "ADMIN")
def get_report_detail(report_id):
    """
    Get details of a specific pending report.
    ---
    tags:
      - Moderator
    security:
      - Bearer: []
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
        description: ID of the report to inspect.
    responses:
      200:
        description: Report details including reported post and user.
      401:
        description: Authentication required or invalid token.
      403:
        description: User does not have moderator or admin privileges.
      404:
        description: Report not found.
      422:
        description: Report has already been reviewed.
    """

    try:

        report, post, user = ModeratorService.get_report_for_review(
            report_id
        )

        return jsonify({
            "report": serialize_report(report),
            "post": (
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "content": post.content,
                    "image_path": post.image_path,
                    "visibility": post.visibility,
                    "status": post.status,
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat()
                }
                if post else None
            ),
            "reported_user": (
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_active": user.is_active
                }
                if user else None
            )
        }), 200

    except ValueError as error:

        return error_response(
            str(error),
            404 if "not found" in str(error).lower()
            else 422
        )


@moderator_api_bp.patch("/reports/<int:report_id>")
@role_required("MODERATOR", "ADMIN")
def review_report(report_id):
    """
    Review a pending report.
    ---
    tags:
      - Moderator
    security:
      - Bearer: []
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
        description: ID of the report to review.
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - REVIEWED
                - REJECTED
              example: REVIEWED
    responses:
      200:
        description: Report reviewed successfully.
      400:
        description: Missing status in request body.
      401:
        description: Authentication required or invalid token.
      403:
        description: User does not have moderator or admin privileges.
      404:
        description: Report not found.
      422:
        description: Invalid report status or report already reviewed.
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "status" not in data:

        return error_response(
            "A JSON body with status is required.",
            400
        )

    try:

        report = ModeratorService.review_report(
            report_id,
            current_user_id(),
            data["status"]
        )

        return jsonify({
            "message": "Report reviewed successfully.",
            "report": serialize_report(report)
        }), 200

    except ValueError as error:

        return error_response(
            str(error),
            404 if "not found" in str(error).lower()
            else 422
        )



@moderator_api_bp.post(
    "/reports/<int:report_id>/remove-post"
)
@role_required("MODERATOR", "ADMIN")
def remove_reported_post(report_id):

    try:

        report = ModeratorService.remove_reported_post(
            report_id,
            current_user_id()
        )

        return jsonify({
            "message": "Reported post has been removed.",
            "report": serialize_report(report)
        }), 200

    except ValueError as error:

        return error_response(
            str(error),
            404 if "not found" in str(error).lower()
            else 422
        )



@moderator_api_bp.post(
    "/reports/<int:report_id>/deactivate-user"
)
@role_required("MODERATOR", "ADMIN")
def deactivate_reported_user(report_id):

    try:

        report = ModeratorService.deactivate_reported_user(
            report_id,
            current_user_id()
        )

        return jsonify({
            "message": "Reported user has been deactivated.",
            "report": serialize_report(report)
        }), 200

    except (ValueError, PermissionError) as error:

        return error_response(
            str(error),
            404 if "not found" in str(error).lower()
            else 422
        )