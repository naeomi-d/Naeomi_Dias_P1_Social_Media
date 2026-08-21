from datetime import datetime

from app import db


class AdminAuditLog(db.Model):
    __tablename__ = "admin_audit_logs"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    admin_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    action = db.Column(
        db.String(50),
        nullable=False
    )

    entity_type = db.Column(
        db.String(30),
        nullable=False
    )

    entity_id = db.Column(
        db.BigInteger,
        nullable=False
    )

    details = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.Index(
            "idx_audit_admin_created",
            "admin_id",
            "created_at"
        ),
        db.Index(
            "idx_audit_entity",
            "entity_type",
            "entity_id"
        ),
    )

    admin = db.relationship(
        "User",
        foreign_keys=[admin_id],
        back_populates="audit_logs"
    )