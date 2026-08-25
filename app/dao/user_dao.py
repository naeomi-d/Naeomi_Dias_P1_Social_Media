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
        return User.query.filter_by(
            username=username
        ).first()


    @staticmethod
    def find_by_id(user_id):
        return User.query.filter_by(
            id=user_id
        ).first()

    
    @staticmethod
    def find_all():
        return (
            User.query
            .order_by(User.created_at.desc())
            .all()
        )

    @staticmethod
    def find_active_users(current_user_id=None):

        query = User.query.filter(
            User.is_active.is_(True)
        )

        if current_user_id is not None:
            query = query.filter(
                User.id != current_user_id
            )

        return (
            query
            .order_by(User.created_at.desc())
            .all()
        )

   
    @staticmethod
    def find_paginated(page=1, per_page=20):

        return (
            User.query
            .order_by(User.created_at.desc())
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        )

    
    @staticmethod
    def count_all():
        return User.query.count()

    @staticmethod
    def count_active():
        return (
            User.query
            .filter(User.is_active.is_(True))
            .count()
        )

    @staticmethod
    def count_inactive():
        return (
            User.query
            .filter(User.is_active.is_(False))
            .count()
        )

    @staticmethod
    def count_by_role(role):
        return (
            User.query
            .filter_by(role=role)
            .count()
        )

    
    @staticmethod
    def find_recent_users(limit=6):

        return (
            User.query
            .filter(User.is_active.is_(True))
            .order_by(User.created_at.desc())
            .limit(limit)
            .all()
        )

    
    @staticmethod
    def update(user):
        db.session.add(user)
        db.session.commit()
        return user

    
    @staticmethod
    def search_users(search_term, current_user_id):

        search_pattern = f"%{search_term.strip()}%"

        return (
            User.query
            .filter(
                User.is_active.is_(True)
            )
            .filter(
                User.id != current_user_id
            )
            .filter(
                db.or_(
                    User.username.ilike(search_pattern),
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern)
                )
            )
            .order_by(User.created_at.desc())
            .all()
        )