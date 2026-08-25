from sqlalchemy.orm import joinedload

from app import db
from app.models.report import Report
from app.models.post import Post


class ReportDAO:

    @staticmethod
    def create(report):

        db.session.add(report)
        db.session.commit()

        return report


    @staticmethod
    def find_by_id(report_id):

        return (
            Report.query
            .options(
                joinedload(Report.reporter),
                joinedload(Report.reported_user),
                joinedload(Report.reviewer),
                joinedload(Report.post).joinedload(Post.user)
            )
            .filter_by(id=report_id)
            .first()
        )


    @staticmethod
    def find_pending_reports():

        return (
            Report.query
            .options(
                joinedload(Report.reporter),
                joinedload(Report.reported_user),
                joinedload(Report.post).joinedload(Post.user)
            )
            .filter_by(status="PENDING")
            .order_by(Report.created_at.desc())
            .all()
        )


    @staticmethod
    def find_by_reporter(reporter_id):

        return (
            Report.query
            .options(
                joinedload(Report.reported_user),
                joinedload(Report.post).joinedload(Post.user)
            )
            .filter_by(reporter_id=reporter_id)
            .order_by(Report.created_at.desc())
            .all()
        )


    @staticmethod
    def update(report):

        db.session.commit()

        return report


    @staticmethod
    def delete(report):

        db.session.delete(report)
        db.session.commit()

    @staticmethod
    def find_pending_by_post_id(post_id):

        return (
            Report.query
            .filter_by(
                post_id=post_id,
                status="PENDING"
            )
            .all()
        )