from datetime import datetime

from app.models.report import Report

from app.dao.report_dao import ReportDAO
from app.dao.post_dao import PostDAO
from app.dao.user_dao import UserDAO

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.authorization_exceptions import AuthorizationError
from app.exceptions.validation_exceptions import ValidationError

class ReportService:

    @staticmethod
    def report_post(
        reporter_id,
        post_id,
        reason,
        description
    ):

        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ResourceNotFoundError(
                "Post not found."
            )

        if post.status == "DELETED":
            raise ValidationError(
                "Cannot report a deleted post."
            )

        if not reason or not reason.strip():
            raise ValidationError(
                "Report reason is required."
            )

        report = Report(
            reporter_id=reporter_id,
            post_id=post_id,
            reason=reason.strip(),
            description=description.strip()
            if description else None,
            status="PENDING"
        )

        return ReportDAO.create(report)


    @staticmethod
    def report_user(
        reporter_id,
        reported_user_id,
        reason,
        description
    ):

        user = UserDAO.find_by_id(
            reported_user_id
        )

        if not user:
            raise ResourceNotFoundError(
                "User not found."
            )

        if reporter_id == reported_user_id:
            raise ValidationError(
                "You cannot report yourself."
            )

        if not reason or not reason.strip():
            raise ValidationError(
                "Report reason is required."
            )

        report = Report(
            reporter_id=reporter_id,
            reported_user_id=reported_user_id,
            reason=reason.strip(),
            description=description.strip()
            if description else None,
            status="PENDING"
        )

        return ReportDAO.create(report)


    @staticmethod
    def get_pending_reports():

        return ReportDAO.find_pending_reports()

    @staticmethod
    def get_my_reports(reporter_id):
        return ReportDAO.find_by_reporter(reporter_id)

    @staticmethod
    def get_report(report_id, requester_id, can_moderate=False):
        report = ReportDAO.find_by_id(report_id)
        if not report:
            raise ResourceNotFoundError("Report not found.")
        if not can_moderate and report.reporter_id != requester_id:
            raise AuthorizationError("You cannot view another user's report.")
        return report

    @staticmethod
    def cancel_report(report_id, reporter_id):
        report = ReportService.get_report(report_id, reporter_id)
        if report.status != "PENDING":
            raise ValidationError("Only pending reports can be cancelled.")
        ReportDAO.delete(report)


    @staticmethod
    def review_report(
        report_id,
        reviewer_id,
        status
    ):

        report = ReportDAO.find_by_id(
            report_id
        )

        if not report:
            raise ResourceNotFoundError(
                "Report not found."
            )

        allowed_statuses = {
            "REVIEWED",
            "REJECTED"
        }

        if status not in allowed_statuses:
            raise ValidationError(
                "Invalid report status."
            )

        report.status = status
        report.reviewed_by = reviewer_id
        report.reviewed_at = datetime.utcnow()

        ReportDAO.update(report)

        return report
