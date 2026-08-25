from datetime import datetime

from app import db


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    reporter_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )


    reported_user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True
    )

    post_id = db.Column(
        db.BigInteger,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=True
    )

    reason = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    
    reviewed_by = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


    reporter = db.relationship(
        "User",
        foreign_keys=[reporter_id],
        backref="submitted_reports"
    )

    reported_user = db.relationship(
        "User",
        foreign_keys=[reported_user_id],
        backref="received_reports"
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewed_by],
        backref="reviewed_reports"
    )

    post = db.relationship(
        "Post",
        foreign_keys=[post_id],
        backref="reports"
    )

    __table_args__ = (
        db.Index(
            "idx_reports_status_created",
            "status",
            "created_at"
        ),
        db.Index(
            "idx_reports_reporter",
            "reporter_id"
        ),
    )