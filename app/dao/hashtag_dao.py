from app import db
from app.models.hashtag import Hashtag


class HashtagDAO:

    @staticmethod
    def find_by_name(name):
        return Hashtag.query.filter_by(name=name).first()

    @staticmethod
    def create(hashtag):
        db.session.add(hashtag)
        return hashtag

    @staticmethod
    def find_all():
        return Hashtag.query.order_by(Hashtag.name.asc()).all()

    @staticmethod
    def search(query):
        return (
            Hashtag.query
            .filter(Hashtag.name.ilike(f"%{query}%"))
            .order_by(Hashtag.name.asc())
            .all()
        )
