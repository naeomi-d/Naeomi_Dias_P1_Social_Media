from app.services.report_service import ReportService
from app.services.admin_audit_log_service import AdminAuditLogService
from app.services.user_service import UserService


class AdminService:

    @staticmethod
    def review_report(report_id, reviewer_id, status):
        report = ReportService.review_report(report_id, reviewer_id, status)
        AdminAuditLogService.record(
            admin_id=reviewer_id,
            action="REVIEW_REPORT",
            entity_type="REPORT",
            entity_id=report.id,
            details=f"Report status set to {report.status}.",
        )
        return report

    @staticmethod
    def get_users():
        return UserService.get_users()
