from app import db
from app.models.user import User

class UserDAO:
    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_id(user_id):

        return User.query.filter_by(
            id=user_id
    ).first()
    
    @staticmethod
    def find_all():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def update(user):
        db.session.add(user)
        db.session.commit()
        return user
    
