import logging

from app.services.report_service import ReportService
from app.services.admin_audit_log_service import AdminAuditLogService
from app.services.user_service import UserService

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.authorization_exceptions import AuthorizationError
from app.exceptions.validation_exceptions import ValidationError


logger = logging.getLogger(__name__)


class AdminService:

    
    @staticmethod
    def deactivate_user(user_id, admin_id):

        user = UserService.get_user(user_id)

        if user.id == admin_id:
            raise AuthorizationError(
                "You cannot deactivate your own account."
            )

        if user.role == "ADMIN":
            raise AuthorizationError(
                "An admin account cannot be deactivated."
            )

        if not user.is_active:
            raise ValidationError(
                "User account is already inactive."
            )

        user.is_active = False

        UserService.update_user_record(user)

        details = (
            f"User @{user.username} was deactivated."
        )

        AdminAuditLogService.record(
            admin_id=admin_id,
            action="DEACTIVATE_USER",
            entity_type="USER",
            entity_id=user.id,
            details=details
        )

        logger.info(
            "Admin %s deactivated user %s (@%s).",
            admin_id,
            user.id,
            user.username
        )

        return user


    @staticmethod
    def activate_user(user_id, admin_id):

        user = UserService.get_user(user_id)

        if user.is_active:
            raise ValidationError(
                "User account is already active."
            )

        user.is_active = True

        UserService.update_user_record(user)

        details = (
            f"User @{user.username} was activated."
        )

        AdminAuditLogService.record(
            admin_id=admin_id,
            action="ACTIVATE_USER",
            entity_type="USER",
            entity_id=user.id,
            details=details
        )

        logger.info(
            "Admin %s activated user %s (@%s).",
            admin_id,
            user.id,
            user.username
        )

        return user


    @staticmethod
    def change_user_role(user_id, admin_id, new_role):

        user = UserService.get_user(user_id)

        allowed_roles = {
            "USER",
            "MODERATOR"
        }

        if new_role not in allowed_roles:
            raise ValidationError(
                "Invalid role. Allowed roles are USER and MODERATOR."
            )

        if user.id == admin_id:
            raise AuthorizationError(
                "You cannot change your own role."
            )

        if user.role == "ADMIN":
            raise AuthorizationError(
                "An admin account cannot be modified here."
            )

        if user.role == new_role:
            raise ValidationError(
                f"User already has the {new_role} role."
            )

        old_role = user.role

        user.role = new_role

        UserService.update_user_record(user)

        details = (
            f"User @{user.username} role changed "
            f"from {old_role} to {new_role}."
        )

        AdminAuditLogService.record(
            admin_id=admin_id,
            action="CHANGE_USER_ROLE",
            entity_type="USER",
            entity_id=user.id,
            details=details
        )

        logger.info(
            "Admin %s changed user %s (@%s) role from %s to %s.",
            admin_id,
            user.id,
            user.username,
            old_role,
            new_role
        )

        return user

   
    @staticmethod
    def get_users():
        return UserService.get_users()

    @staticmethod
    def get_paginated_users(page=1, per_page=20):
        return UserService.get_paginated_users(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_user_count():
        return UserService.get_user_count()

    @staticmethod
    def get_active_user_count():
        return UserService.get_active_user_count()

    @staticmethod
    def get_inactive_user_count():
        return UserService.get_inactive_user_count()

    @staticmethod
    def get_moderator_count():
        return UserService.get_role_count("MODERATOR")

    
    @staticmethod
    def get_pending_reports():
        return ReportService.get_pending_reports()

    @staticmethod
    def review_report(report_id, reviewer_id, status):

        report = ReportService.review_report(
            report_id,
            reviewer_id,
            status
        )

        details = (
            f"Report status set to {report.status}."
        )

        AdminAuditLogService.record(
            admin_id=reviewer_id,
            action="REVIEW_REPORT",
            entity_type="REPORT",
            entity_id=report.id,
            details=details
        )

        logger.info(
            "Privileged user %s reviewed report %s with status %s.",
            reviewer_id,
            report.id,
            report.status
        )

        return report

    
    @staticmethod
    def get_audit_logs():
        return AdminAuditLogService.get_logs()

    @staticmethod
    def get_paginated_audit_logs(page=1, per_page=20):
        return AdminAuditLogService.get_paginated_logs(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_audit_log_count():
        return AdminAuditLogService.get_log_count()