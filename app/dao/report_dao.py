from app import db

from app.models.report import Report


class ReportDAO:

    @staticmethod
    def create(report):

        db.session.add(report)
        db.session.commit()

        return report


    @staticmethod
    def find_by_id(report_id):

        return Report.query.get(report_id)


    @staticmethod
    def find_pending_reports():

        return Report.query.filter_by(
            status="PENDING"
        ).order_by(
            Report.created_at.desc()
        ).all()

    @staticmethod
    def find_by_reporter(reporter_id):
        return (
            Report.query.filter_by(reporter_id=reporter_id)
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
