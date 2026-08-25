import logging
from datetime import datetime
from app import db
from app.dao.user_dao import UserDAO
from app.dao.post_dao import PostDAO
from app.dao.report_dao import ReportDAO

from app.services.report_service import ReportService
from app.services.admin_audit_log_service import AdminAuditLogService

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.authorization_exceptions import AuthorizationError
from app.exceptions.validation_exceptions import ValidationError


logger = logging.getLogger(__name__)


class ModeratorService:

    @staticmethod
    def get_pending_reports():

        return ReportService.get_pending_reports()


    @staticmethod
    def dismiss_report(report_id, moderator_id):

        report = ReportDAO.find_by_id(report_id)

        if not report:
            raise ResourceNotFoundError(
                "Report not found."
            )

        if report.status != "PENDING":
            raise ValidationError(
                "Only pending reports can be dismissed."
            )

        report.status = "REJECTED"
        report.reviewed_by = moderator_id
        report.reviewed_at = datetime.utcnow()

        ReportDAO.update(report)

        # Database audit trail
        AdminAuditLogService.record(
            admin_id=moderator_id,
            action="DISMISS_REPORT",
            entity_type="REPORT",
            entity_id=report.id,
            details="Report dismissed by moderator."
        )

        logger.info(
            "Moderator %s dismissed report %s.",
            moderator_id,
            report.id
        )

        return report


    @staticmethod
    def remove_reported_post(report_id, moderator_id):

            report = ReportDAO.find_by_id(report_id)

            if not report:
                raise ResourceNotFoundError(
                    "Report not found."
                )

            if report.status != "PENDING":
                raise ValidationError(
                    "Only pending reports can be acted upon."
                )

            if not report.post_id:
                raise ValidationError(
                    "This report does not target a post."
                )

            post = PostDAO.find_by_id(
                report.post_id
            )

            if not post:
                raise ResourceNotFoundError(
                    "Reported post not found."
                )

            if post.status == "DELETED":
                raise ValidationError(
                    "Post is already deleted."
                )

            try:

                post.status = "DELETED"
                post.deleted_at = datetime.utcnow()

                db.session.add(post)

                pending_reports = ReportDAO.find_pending_by_post_id(
                    post.id
                )

                reviewed_at = datetime.utcnow()

                for pending_report in pending_reports:

                    pending_report.status = "REVIEWED"
                    pending_report.reviewed_by = moderator_id
                    pending_report.reviewed_at = reviewed_at

                    db.session.add(pending_report)

                AdminAuditLogService.record(
                    admin_id=moderator_id,
                    action="REMOVE_REPORTED_POST",
                    entity_type="POST",
                    entity_id=post.id,
                    details=(
                        f"Post removed after report #{report.id}. "
                        f"Resolved {len(pending_reports)} "
                        f"pending report(s)."
                    )
                )

                db.session.commit()

            except Exception:

                db.session.rollback()

                logger.exception(
                    "Failed to remove post %s after report %s.",
                    post.id,
                    report.id
                )

                raise

            logger.info(
                "Moderator %s removed post %s after report %s. "
                "Resolved %s pending report(s).",
                moderator_id,
                post.id,
                report.id,
                len(pending_reports)
            )

            return report


    @staticmethod
    def deactivate_reported_user(
        report_id,
        moderator_id
    ):

        report = ReportDAO.find_by_id(report_id)

        if not report:
            raise ResourceNotFoundError(
                "Report not found."
            )

        if report.status != "PENDING":
            raise ValidationError(
                "Only pending reports can be acted upon."
            )

        if not report.reported_user_id:
            raise ValidationError(
                "This report does not target a user."
            )

        user = UserDAO.find_by_id(
            report.reported_user_id
        )

        if not user:
            raise ResourceNotFoundError(
                "Reported user not found."
            )

        if user.id == moderator_id:
            raise AuthorizationError(
                "You cannot deactivate your own account."
            )

        if user.role == "ADMIN":
            raise AuthorizationError(
                "Moderators cannot deactivate an admin account."
            )

        if user.role == "MODERATOR":
            raise AuthorizationError(
                "Moderators cannot deactivate another moderator."
            )

        if not user.is_active:
            raise ValidationError(
                "User account is already inactive."
            )

        
        user.is_active = False

        UserDAO.update(user)

        
        report.status = "REVIEWED"
        report.reviewed_by = moderator_id
        report.reviewed_at = datetime.utcnow()

        ReportDAO.update(report)

        AdminAuditLogService.record(
            admin_id=moderator_id,
            action="DEACTIVATE_REPORTED_USER",
            entity_type="USER",
            entity_id=user.id,
            details=(
                f"User deactivated after report #{report.id}."
            )
        )

        logger.info(
            "Moderator %s deactivated user %s after report %s.",
            moderator_id,
            user.id,
            report.id
        )

        return report

   
    @staticmethod
    def review_report(report_id, moderator_id, status):

        report = ReportDAO.find_by_id(report_id)

        if not report:
            raise ResourceNotFoundError(
                "Report not found."
            )

        if report.status != "PENDING":
            raise ValidationError(
                "Only pending reports can be reviewed."
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
        report.reviewed_by = moderator_id
        report.reviewed_at = datetime.utcnow()

        ReportDAO.update(report)

        AdminAuditLogService.record(
            admin_id=moderator_id,
            action="REVIEW_REPORT",
            entity_type="REPORT",
            entity_id=report.id,
            details=(
                f"Report reviewed with status {status}."
            )
        )

        
        logger.info(
            "Moderator %s reviewed report %s with status %s.",
            moderator_id,
            report.id,
            status
        )

        return report
    
    @staticmethod
    def get_report_for_review(report_id):

        report = ReportDAO.find_by_id(report_id)

        if not report:
            raise ResourceNotFoundError(
                "Report not found."
            )

        if report.status != "PENDING":
            raise ValidationError(
                "This report has already been reviewed."
            )

        post = None
        user = None

        if report.post_id:

            post = PostDAO.find_by_id(
                report.post_id
            )

            if not post:
                raise ResourceNotFoundError(
                    "Reported post not found."
                )
        if report.reported_user_id:

            user = UserDAO.find_by_id(
                report.reported_user_id
            )

            if not user:
                raise ResourceNotFoundError(
                    "Reported user not found."
                )

        return report, post, user