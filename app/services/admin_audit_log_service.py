from app.dao.admin_audit_log_dao import AdminAuditLogDAO
from app.models.admin_audit_log import AdminAuditLog

from app.exceptions.resource_exceptions import ResourceNotFoundError


class AdminAuditLogService:

    @staticmethod
    def record(
        admin_id,
        action,
        entity_type,
        entity_id,
        details=None
    ):
        audit_log = AdminAuditLog(
            admin_id=admin_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details
        )

        return AdminAuditLogDAO.create(audit_log)

    
    @staticmethod
    def get_logs():
        return AdminAuditLogDAO.find_all()

    
    @staticmethod
    def get_paginated_logs(
        page=1,
        per_page=20
    ):
        return AdminAuditLogDAO.find_paginated(
            page=page,
            per_page=per_page
        )

    
    @staticmethod
    def get_log_count():
        return AdminAuditLogDAO.count_all()

    
    @staticmethod
    def get_log(audit_log_id):

        audit_log = AdminAuditLogDAO.find_by_id(
            audit_log_id
        )

        if not audit_log:
            raise ResourceNotFoundError(
                "Audit log not found."
            )

        return audit_log