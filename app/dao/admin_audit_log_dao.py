from app import db
from app.models.admin_audit_log import AdminAuditLog


class AdminAuditLogDAO:

    @staticmethod
    def create(audit_log):
        db.session.add(audit_log)
        db.session.commit()
        return audit_log

    @staticmethod
    def find_by_id(audit_log_id):
        return AdminAuditLog.query.filter_by(
            id=audit_log_id
        ).first()

    @staticmethod
    def find_all():
        return AdminAuditLog.query.order_by(
            AdminAuditLog.created_at.desc()
        ).all()

    @staticmethod
    def find_paginated(page=1, per_page=20):
        return (
            AdminAuditLog.query
            .order_by(
                AdminAuditLog.created_at.desc()
            )
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        )

    @staticmethod
    def count_all():
        return AdminAuditLog.query.count()