import bcrypt

from app import create_app, db

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.follow import Follow
from app.models.bookmark import Bookmark
from app.models.hashtag import Hashtag
from app.models.post_hashtag import PostHashtag
from app.models.notification import Notification
from app.models.report import Report
from app.models.admin_audit_log import AdminAuditLog


app = create_app()


def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def get_or_create_user(
    username,
    email,
    password,
    first_name,
    last_name,
    role="USER"
):

    user = User.query.filter_by(
        username=username
    ).first()

    if user:
        user.role = role
        user.is_active = True
        return user

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_active=True
    )

    db.session.add(user)
    db.session.flush()

    return user

def seed_database():

    print("Starting database seed...")

    # --------------------------------------------------
    # USERS
    # --------------------------------------------------

    admin = get_or_create_user(
        username="p1_admin",
        email="p1_admin@gmail.com",
        password="Admin@123",
        first_name="P1",
        last_name="Admin",
        role="ADMIN"
    )

    moderator = get_or_create_user(
    username="p1_moderator",
    email="p1_moderator@gmail.com",
    password="Moderator@123",
    first_name="P1",
    last_name="Moderator",
    role="MODERATOR"
    )

    xena = get_or_create_user(
        username="p1_xena",
        email="p1_xena@gmail.com",
        password="Xena@123",
        first_name="Xena",
        last_name="Pereira",
        role="USER"
    )

    john = get_or_create_user(
        username="p1_john",
        email="p1_john@gmail.com",
        password="John@123",
        first_name="John",
        last_name="Doe",
        role="USER"
    )

    db.session.commit()

    print("Users created/verified.")

    # --------------------------------------------------
    # POSTS
    # --------------------------------------------------

    xena_post = Post.query.filter_by(
        user_id=xena.id,
        content="Learning Flask and building my P1 social media project!"
    ).first()

    if not xena_post:

        xena_post = Post(
            user_id=xena.id,
            content="Learning Flask and building my P1 social media project!",
            visibility="PUBLIC",
            status="ACTIVE"
        )

        db.session.add(xena_post)
        db.session.flush()

    john_post = Post.query.filter_by(
        user_id=john.id,
        content="Building production-ready APIs with Flask and JWT."
    ).first()

    if not john_post:

        john_post = Post(
            user_id=john.id,
            content="Building production-ready APIs with Flask and JWT.",
            visibility="PUBLIC",
            status="ACTIVE"
        )

        db.session.add(john_post)
        db.session.flush()

    second_xena_post = Post.query.filter_by(
        user_id=xena.id,
        content="Python, SQLAlchemy and Flask are a great combination."
    ).first()

    if not second_xena_post:

        second_xena_post = Post(
            user_id=xena.id,
            content="Python, SQLAlchemy and Flask are a great combination.",
            visibility="PUBLIC",
            status="ACTIVE"
        )

        db.session.add(second_xena_post)
        db.session.flush()

    db.session.commit()

    print("Posts created/verified.")

    # --------------------------------------------------
    # COMMENTS
    # --------------------------------------------------

    comment_1 = Comment.query.filter_by(
        post_id=john_post.id,
        user_id=xena.id,
        content="This is looking great!"
    ).first()

    if not comment_1:

        comment_1 = Comment(
            post_id=john_post.id,
            user_id=xena.id,
            content="This is looking great!"
        )

        db.session.add(comment_1)
        db.session.flush()

    comment_2 = Comment.query.filter_by(
        post_id=xena_post.id,
        user_id=john.id,
        content="Flask is really useful for API development."
    ).first()

    if not comment_2:

        comment_2 = Comment(
            post_id=xena_post.id,
            user_id=john.id,
            content="Flask is really useful for API development."
        )

        db.session.add(comment_2)
        db.session.flush()

    db.session.commit()

    print("Comments created/verified.")

    # --------------------------------------------------
    # LIKES
    # --------------------------------------------------

    like_1 = Like.query.filter_by(
        user_id=xena.id,
        post_id=john_post.id
    ).first()

    if not like_1:

        like_1 = Like(
            user_id=xena.id,
            post_id=john_post.id
        )

        db.session.add(like_1)

    like_2 = Like.query.filter_by(
        user_id=john.id,
        post_id=xena_post.id
    ).first()

    if not like_2:

        like_2 = Like(
            user_id=john.id,
            post_id=xena_post.id
        )

        db.session.add(like_2)

    db.session.commit()

    print("Likes created/verified.")

    # --------------------------------------------------
    # FOLLOWS
    # --------------------------------------------------

    follow_1 = Follow.query.filter_by(
        follower_id=xena.id,
        following_id=john.id
    ).first()

    if not follow_1:

        follow_1 = Follow(
            follower_id=xena.id,
            following_id=john.id
        )

        db.session.add(follow_1)

    follow_2 = Follow.query.filter_by(
        follower_id=john.id,
        following_id=xena.id
    ).first()

    if not follow_2:

        follow_2 = Follow(
            follower_id=john.id,
            following_id=xena.id
        )

        db.session.add(follow_2)

    db.session.commit()

    print("Follows created/verified.")

    # --------------------------------------------------
    # BOOKMARK
    # --------------------------------------------------

    bookmark = Bookmark.query.filter_by(
        user_id=xena.id,
        post_id=john_post.id
    ).first()

    if not bookmark:

        bookmark = Bookmark(
            user_id=xena.id,
            post_id=john_post.id
        )

        db.session.add(bookmark)

    db.session.commit()

    print("Bookmarks created/verified.")

    # --------------------------------------------------
    # HASHTAGS
    # --------------------------------------------------

    python_tag = Hashtag.query.filter_by(
        name="python"
    ).first()

    if not python_tag:

        python_tag = Hashtag(
            name="python"
        )

        db.session.add(python_tag)
        db.session.flush()

    flask_tag = Hashtag.query.filter_by(
        name="flask"
    ).first()

    if not flask_tag:

        flask_tag = Hashtag(
            name="flask"
        )

        db.session.add(flask_tag)
        db.session.flush()

    social_tag = Hashtag.query.filter_by(
        name="socialmedia"
    ).first()

    if not social_tag:

        social_tag = Hashtag(
            name="socialmedia"
        )

        db.session.add(social_tag)
        db.session.flush()

    db.session.commit()

    # --------------------------------------------------
    # POST HASHTAGS
    # --------------------------------------------------

    post_hashtag_1 = PostHashtag.query.filter_by(
        post_id=xena_post.id,
        hashtag_id=python_tag.id
    ).first()

    if not post_hashtag_1:

        db.session.add(
            PostHashtag(
                post_id=xena_post.id,
                hashtag_id=python_tag.id
            )
        )

    post_hashtag_2 = PostHashtag.query.filter_by(
        post_id=xena_post.id,
        hashtag_id=flask_tag.id
    ).first()

    if not post_hashtag_2:

        db.session.add(
            PostHashtag(
                post_id=xena_post.id,
                hashtag_id=flask_tag.id
            )
        )

    post_hashtag_3 = PostHashtag.query.filter_by(
        post_id=john_post.id,
        hashtag_id=flask_tag.id
    ).first()

    if not post_hashtag_3:

        db.session.add(
            PostHashtag(
                post_id=john_post.id,
                hashtag_id=flask_tag.id
            )
        )

    post_hashtag_4 = PostHashtag.query.filter_by(
        post_id=john_post.id,
        hashtag_id=social_tag.id
    ).first()

    if not post_hashtag_4:

        db.session.add(
            PostHashtag(
                post_id=john_post.id,
                hashtag_id=social_tag.id
            )
        )

    db.session.commit()

    print("Hashtags created/verified.")

    # --------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------

    notification_1 = Notification.query.filter_by(
        recipient_id=john.id,
        actor_id=xena.id,
        type="LIKE",
        post_id=john_post.id
    ).first()

    if not notification_1:

        notification_1 = Notification(
            recipient_id=john.id,
            actor_id=xena.id,
            type="LIKE",
            post_id=john_post.id,
            is_read=False
        )

        db.session.add(notification_1)

    notification_2 = Notification.query.filter_by(
        recipient_id=john.id,
        actor_id=xena.id,
        type="COMMENT",
        post_id=john_post.id,
        comment_id=comment_1.id
    ).first()

    if not notification_2:

        notification_2 = Notification(
            recipient_id=john.id,
            actor_id=xena.id,
            type="COMMENT",
            post_id=john_post.id,
            comment_id=comment_1.id,
            is_read=False
        )

        db.session.add(notification_2)

    notification_3 = Notification.query.filter_by(
        recipient_id=john.id,
        actor_id=xena.id,
        type="FOLLOW"
    ).first()

    if not notification_3:

        notification_3 = Notification(
            recipient_id=john.id,
            actor_id=xena.id,
            type="FOLLOW",
            is_read=False
        )

        db.session.add(notification_3)

    notification_4 = Notification.query.filter_by(
        recipient_id=xena.id,
        actor_id=john.id,
        type="LIKE",
        post_id=xena_post.id
    ).first()

    if not notification_4:

        notification_4 = Notification(
            recipient_id=xena.id,
            actor_id=john.id,
            type="LIKE",
            post_id=xena_post.id,
            is_read=False
        )

        db.session.add(notification_4)

    db.session.commit()

    print("Notifications created/verified.")

    # --------------------------------------------------
    # REPORT
    # --------------------------------------------------

    report = Report.query.filter_by(
        reporter_id=xena.id,
        post_id=john_post.id
    ).first()

    if not report:

        report = Report(
            reporter_id=xena.id,
            post_id=john_post.id,
            reason="SPAM",
            description="Test report for P1 API testing.",
            status="PENDING"
        )

        db.session.add(report)
        db.session.flush()

    db.session.commit()

    print("Report created/verified.")

    # --------------------------------------------------
    # ADMIN AUDIT LOG
    # --------------------------------------------------

    audit_log = AdminAuditLog.query.filter_by(
        admin_id=admin.id,
        action="REVIEW_REPORT",
        entity_type="REPORT",
        entity_id=report.id
    ).first()

    if not audit_log:

        audit_log = AdminAuditLog(
            admin_id=admin.id,
            action="REVIEW_REPORT",
            entity_type="REPORT",
            entity_id=report.id,
            details="Seed audit log for P1 API testing."
        )

        db.session.add(audit_log)

    db.session.commit()

    print()
    print("======================================")
    print("DATABASE SEED COMPLETED SUCCESSFULLY")
    print("======================================")
    print()
    print("Test users:")
    print()
    print("ADMIN")
    print("Username: p1_admin")
    print("Password: Admin@123")
    print()
    print("MODERATOR")
    print("Username: p1_moderator")
    print("Password: Moderator@123")
    print()
    print("USER")
    print("Username: p1_xena")
    print("Password: Xena@123")
    print()
    print("USER")
    print("Username: p1_john")
    print("Password: John@123")
    print()
    print("======================================")


if __name__ == "__main__":

    with app.app_context():
        seed_database()