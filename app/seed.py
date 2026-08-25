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

    user = User.query.filter_by(username=username).first()

    if user:
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
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



def get_or_create_hashtag(name):

    clean_name = name.lower().strip()

    tag = Hashtag.query.filter_by(
        name=clean_name
    ).first()

    if tag:
        return tag

    tag = Hashtag(
        name=clean_name
    )

    db.session.add(tag)
    db.session.flush()

    return tag



def get_or_create_post(
    user_id,
    content,
    visibility="PUBLIC",
    status="ACTIVE"
):

    post = Post.query.filter_by(
        user_id=user_id,
        content=content
    ).first()

    if post:
        return post

    post = Post(
        user_id=user_id,
        content=content,
        visibility=visibility,
        status=status
    )

    db.session.add(post)
    db.session.flush()

    return post
 

def get_or_create_comment(
    post_id,
    user_id,
    content
):

    comment = Comment.query.filter_by(
        post_id=post_id,
        user_id=user_id,
        content=content
    ).first()

    if comment:
        return comment

    comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content
    )

    db.session.add(comment)
    db.session.flush()

    return comment


def get_or_create_like(
    user_id,
    post_id
):

    like = Like.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if like:
        return like

    like = Like(
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(like)

    return like


def get_or_create_follow(
    follower_id,
    following_id
):

    if follower_id == following_id:
        return None

    follow = Follow.query.filter_by(
        follower_id=follower_id,
        following_id=following_id
    ).first()

    if follow:
        return follow

    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.session.add(follow)

    return follow


def get_or_create_bookmark(
    user_id,
    post_id
):

    bookmark = Bookmark.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if bookmark:
        return bookmark

    bookmark = Bookmark(
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(bookmark)

    return bookmark


def get_or_create_post_hashtag(
    post_id,
    hashtag_id
):

    post_hashtag = PostHashtag.query.filter_by(
        post_id=post_id,
        hashtag_id=hashtag_id
    ).first()

    if post_hashtag:
        return post_hashtag

    post_hashtag = PostHashtag(
        post_id=post_id,
        hashtag_id=hashtag_id
    )

    db.session.add(post_hashtag)

    return post_hashtag


def get_or_create_report(
    reporter_id,
    reason,
    description,
    post_id=None,
    reported_user_id=None,
    status="PENDING",
    reviewed_by=None
):

    query = Report.query.filter_by(
        reporter_id=reporter_id,
        post_id=post_id,
        reported_user_id=reported_user_id,
        reason=reason
    )

    report = query.first()

    if report:
        return report

    report = Report(
        reporter_id=reporter_id,
        post_id=post_id,
        reported_user_id=reported_user_id,
        reason=reason,
        description=description,
        status=status,
        reviewed_by=reviewed_by
    )

    db.session.add(report)
    db.session.flush()

    return report

def get_or_create_notification(
    recipient_id,
    actor_id,
    type_name,
    post_id=None,
    comment_id=None
):

    notification = Notification.query.filter_by(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=type_name,
        post_id=post_id,
        comment_id=comment_id
    ).first()

    if notification:
        return notification

    notification = Notification(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=type_name,
        post_id=post_id,
        comment_id=comment_id,
        is_read=False
    )

    db.session.add(notification)

    return notification


def get_or_create_audit_log(
    admin_id,
    action,
    entity_type,
    entity_id,
    details=None
):

    log = AdminAuditLog.query.filter_by(
        admin_id=admin_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id
    ).first()

    if log:
        return log

    log = AdminAuditLog(
        admin_id=admin_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )

    db.session.add(log)

    return log

def seed_database():

    print()
    print("======================================")
    print("STARTING P1 DEMO DATABASE SEED")
    print("======================================")
    print()

    users_data = [

        (
            "alexandra_reed",
            "alexandra.reed@example.com",
            "Admin@123",
            "Alexandra",
            "Reed",
            "ADMIN"
        ),

        (
            "daniel_carter",
            "daniel.carter@example.com",
            "Admin@123",
            "Daniel",
            "Carter",
            "ADMIN"
        ),

        (
            "sophia_morgan",
            "sophia.morgan@example.com",
            "Moderator@123",
            "Sophia",
            "Morgan",
            "MODERATOR"
        ),

        (
            "liam_bennett",
            "liam.bennett@example.com",
            "Moderator@123",
            "Liam",
            "Bennett",
            "MODERATOR"
        ),

        (
            "emma_wilson",
            "emma.wilson@example.com",
            "User@123",
            "Emma",
            "Wilson",
            "USER"
        ),

        (
            "oliver_harris",
            "oliver.harris@example.com",
            "User@123",
            "Oliver",
            "Harris",
            "USER"
        ),

        (
            "ava_thompson",
            "ava.thompson@example.com",
            "User@123",
            "Ava",
            "Thompson",
            "USER"
        ),

        (
            "noah_martin",
            "noah.martin@example.com",
            "User@123",
            "Noah",
            "Martin",
            "USER"
        ),

        (
            "mia_clark",
            "mia.clark@example.com",
            "User@123",
            "Mia",
            "Clark",
            "USER"
        ),

        (
            "ethan_lewis",
            "ethan.lewis@example.com",
            "User@123",
            "Ethan",
            "Lewis",
            "USER"
        ),

        (
            "isabella_walker",
            "isabella.walker@example.com",
            "User@123",
            "Isabella",
            "Walker",
            "USER"
        ),

        (
            "mason_hall",
            "mason.hall@example.com",
            "User@123",
            "Mason",
            "Hall",
            "USER"
        ),

        (
            "sophia_young",
            "sophia.young@example.com",
            "User@123",
            "Sophia",
            "Young",
            "USER"
        ),

        (
            "james_king",
            "james.king@example.com",
            "User@123",
            "James",
            "King",
            "USER"
        ),

        (
            "charlotte_wright",
            "charlotte.wright@example.com",
            "User@123",
            "Charlotte",
            "Wright",
            "USER"
        ),

        (
            "benjamin_scott",
            "benjamin.scott@example.com",
            "User@123",
            "Benjamin",
            "Scott",
            "USER"
        ),

        (
            "amelia_green",
            "amelia.green@example.com",
            "User@123",
            "Amelia",
            "Green",
            "USER"
        ),

        (
            "henry_adams",
            "henry.adams@example.com",
            "User@123",
            "Henry",
            "Adams",
            "USER"
        ),

        (
            "grace_baker",
            "grace.baker@example.com",
            "User@123",
            "Grace",
            "Baker",
            "USER"
        )
    ]

    users = {}

    for (
        username,
        email,
        password,
        first_name,
        last_name,
        role
    ) in users_data:

        users[username] = get_or_create_user(
            username,
            email,
            password,
            first_name,
            last_name,
            role
        )

    db.session.commit()

    print(f"Users verified: {len(users)}")

    hashtag_names = [
        "python",
        "flask",
        "webdevelopment",
        "programming",
        "technology",
        "opensource",
        "databases",
        "sqlalchemy",
        "career",
        "learning",
        "softwareengineering",
        "productivity"
    ]

    hashtags = {}

    for name in hashtag_names:

        hashtags[name] = get_or_create_hashtag(name)

    db.session.commit()

    print(f"Hashtags verified: {len(hashtags)}")

    
    post_data = [

        (
            "emma_wilson",
            "Spent the weekend building a small Flask application. "
            "Really enjoying how simple it is to structure APIs and services.",
            "PUBLIC"
        ),

        (
            "oliver_harris",
            "Finally finished my SQLAlchemy relationships today. "
            "Understanding how the models connect makes the rest of the application much easier.",
            "PUBLIC"
        ),

        (
            "ava_thompson",
            "Started learning more about backend architecture and "
            "how service and DAO layers help keep Flask applications maintainable.",
            "PUBLIC"
        ),

        (
            "noah_martin",
            "A good reminder that writing tests early can save a lot of "
            "debugging time later.",
            "PUBLIC"
        ),

        (
            "mia_clark",
            "Working on a personal productivity dashboard this week. "
            "Small projects are a great way to experiment with new ideas.",
            "PUBLIC"
        ),

        (
            "ethan_lewis",
            "Reading about API security today. Authentication is only "
            "one part of building a secure application.",
            "PUBLIC"
        ),

        (
            "isabella_walker",
            "Coffee, code and a quiet afternoon. Sometimes that's all "
            "you need to make progress.",
            "PUBLIC"
        ),

        (
            "mason_hall",
            "Exploring open-source projects and learning how experienced "
            "developers structure their repositories.",
            "PUBLIC"
        ),

        (
            "sophia_young",
            "Just completed another Python practice session. "
            "Consistency really does make a difference.",
            "PUBLIC"
        ),

        (
            "james_king",
            "Thinking about moving some of my older projects to a cleaner "
            "layered architecture.",
            "PUBLIC"
        ),

        (
            "charlotte_wright",
            "Working through database indexing and query optimization. "
            "There is always something new to learn.",
            "PUBLIC"
        ),

        (
            "benjamin_scott",
            "Trying out a new approach to organizing my development workflow. "
            "Keeping tasks small makes everything feel more manageable.",
            "PUBLIC"
        ),

        (
            "amelia_green",
            "Sharing a few notes from my latest web development project. "
            "Documentation is definitely worth the extra effort.",
            "PUBLIC"
        ),

        (
            "henry_adams",
            "Learning more about REST API design and how good endpoint "
            "structure improves the developer experience.",
            "PUBLIC"
        ),

        (
            "grace_baker",
            "Taking some time this evening to review Python fundamentals "
            "and clean up some old code.",
            "PUBLIC"
        ),

        
        (
            "oliver_harris",
            "You are completely useless at programming. "
            "Stop pretending you know what you're doing.",
            "PUBLIC"
        ),

        (
            "mason_hall",
            "BUY NOW!!! Guaranteed money-making opportunity. "
            "Send me your details and I will show you how to double your income.",
            "PUBLIC"
        ),

        (
            "james_king",
            "This community is full of idiots. "
            "Nobody here knows anything about software development.",
            "PUBLIC"
        ),

        (
            "ethan_lewis",
            "Free premium account available. "
            "Message me privately with your login information to activate it.",
            "PUBLIC"
        )
    ]

    posts = {}

    for (
        username,
        content,
        visibility
    ) in post_data:

        post = get_or_create_post(
            users[username].id,
            content,
            visibility=visibility
        )

        posts[content] = post

    db.session.commit()

    print(f"Posts verified: {len(posts)}")

    hashtag_mapping = {

        "emma_wilson": ["python", "flask"],

        "oliver_harris": ["sqlalchemy", "databases"],

        "ava_thompson": [
            "softwareengineering",
            "webdevelopment"
        ],

        "noah_martin": [
            "programming",
            "productivity"
        ],

        "ethan_lewis": [
            "technology",
            "webdevelopment"
        ],

        "isabella_walker": [
            "productivity",
            "learning"
        ],

        "mason_hall": [
            "opensource",
            "programming"
        ],

        "sophia_young": [
            "python",
            "learning"
        ],

        "charlotte_wright": [
            "databases",
            "sqlalchemy"
        ],

        "henry_adams": [
            "webdevelopment",
            "technology"
        ]
    }

    for username, tags in hashtag_mapping.items():

        user_posts = Post.query.filter_by(
            user_id=users[username].id
        ).all()

        for post in user_posts:

            if post.content not in posts:
                continue

            for tag_name in tags:

                get_or_create_post_hashtag(
                    post.id,
                    hashtags[tag_name].id
                )

    db.session.commit()

    
    comments = [

        (
            "emma_wilson",
            "oliver_harris",
            "The SQLAlchemy relationships were one of the trickier parts for me too."
        ),

        (
            "ava_thompson",
            "emma_wilson",
            "Agreed. Flask makes it really easy to experiment with architecture."
        ),

        (
            "noah_martin",
            "mia_clark",
            "Absolutely. Testing early saves so much time."
        ),

        (
            "ethan_lewis",
            "isabella_walker",
            "Security is definitely something I want to understand better."
        ),

        (
            "sophia_young",
            "grace_baker",
            "Consistency is probably the hardest part!"
        ),

        (
            "charlotte_wright",
            "henry_adams",
            "Database optimization is surprisingly interesting."
        ),

        (
            "mason_hall",
            "ava_thompson",
            "Layered architecture makes larger projects much easier to navigate."
        ),

        (
            "james_king",
            "benjamin_scott",
            "Keeping the workflow simple definitely helps."
        )
    ]

    for (
        commenter,
        post_author,
        content
    ) in comments:

        author_posts = Post.query.filter_by(
            user_id=users[post_author].id
        ).all()

        if not author_posts:
            continue

        get_or_create_comment(
            author_posts[0].id,
            users[commenter].id,
            content
        )

    db.session.commit()

    print("Comments verified.")

    follow_pairs = [

        ("emma_wilson", "oliver_harris"),
        ("emma_wilson", "ava_thompson"),
        ("emma_wilson", "mia_clark"),

        ("oliver_harris", "emma_wilson"),
        ("oliver_harris", "noah_martin"),

        ("ava_thompson", "emma_wilson"),
        ("ava_thompson", "sophia_young"),

        ("noah_martin", "ethan_lewis"),

        ("mia_clark", "isabella_walker"),
        ("mia_clark", "grace_baker"),

        ("ethan_lewis", "mason_hall"),

        ("isabella_walker", "emma_wilson"),

        ("mason_hall", "james_king"),

        ("sophia_young", "charlotte_wright"),

        ("charlotte_wright", "henry_adams"),

        ("henry_adams", "benjamin_scott"),

        ("grace_baker", "amelia_green"),

        ("amelia_green", "grace_baker")
    ]

    for follower, following in follow_pairs:

        get_or_create_follow(
            users[follower].id,
            users[following].id
        )

    db.session.commit()

    print(f"Follow relationships verified: {len(follow_pairs)}")

    all_posts = list(posts.values())

    like_pairs = [

        ("emma_wilson", 0),
        ("ava_thompson", 0),
        ("noah_martin", 0),
        ("mia_clark", 0),

        ("emma_wilson", 1),
        ("sophia_young", 1),
        ("ethan_lewis", 1),

        ("oliver_harris", 2),
        ("emma_wilson", 2),
        ("mason_hall", 2),

        ("noah_martin", 3),
        ("charlotte_wright", 3),

        ("isabella_walker", 4),
        ("grace_baker", 4),

        ("benjamin_scott", 5),
        ("henry_adams", 5)
    ]

    for username, index in like_pairs:

        if index < len(all_posts):

            get_or_create_like(
                users[username].id,
                all_posts[index].id
            )

    db.session.commit()

    print("Likes verified.")

   
    bookmark_pairs = [

        ("emma_wilson", 1),
        ("ava_thompson", 2),
        ("noah_martin", 3),
        ("mia_clark", 4),
        ("ethan_lewis", 5),
        ("isabella_walker", 6),
        ("sophia_young", 8),
        ("charlotte_wright", 10),
        ("henry_adams", 13)
    ]

    for username, index in bookmark_pairs:

        if index < len(all_posts):

            get_or_create_bookmark(
                users[username].id,
                all_posts[index].id
            )

    db.session.commit()

    print("Bookmarks verified.")

   
    normal_users = [
        "emma_wilson",
        "ava_thompson",
        "noah_martin",
        "mia_clark",
        "isabella_walker",
        "charlotte_wright"
    ]

    reportable_posts = [

        posts[
            "You are completely useless at programming. "
            "Stop pretending you know what you're doing."
        ],

        posts[
            "BUY NOW!!! Guaranteed money-making opportunity. "
            "Send me your details and I will show you how to double your income."
        ],

        posts[
            "This community is full of idiots. "
            "Nobody here knows anything about software development."
        ],

        posts[
            "Free premium account available. "
            "Message me privately with your login information to activate it."
        ]
    ]

    
    get_or_create_report(
        reporter_id=users["emma_wilson"].id,
        post_id=reportable_posts[0].id,
        reason="HARASSMENT",
        description=(
            "The post contains insulting language directed "
            "at other members of the community."
        ),
        status="PENDING"
    )

    
    get_or_create_report(
        reporter_id=users["ava_thompson"].id,
        post_id=reportable_posts[1].id,
        reason="SPAM",
        description=(
            "The post appears to promote a suspicious "
            "money-making scheme."
        ),
        status="PENDING"
    )

    
    get_or_create_report(
        reporter_id=users["noah_martin"].id,
        post_id=reportable_posts[2].id,
        reason="OFFENSIVE",
        description=(
            "The post contains insulting and disrespectful "
            "language toward the community."
        ),
        status="PENDING"
    )

   
    get_or_create_report(
        reporter_id=users["mia_clark"].id,
        reported_user_id=users["ethan_lewis"].id,
        reason="SPAM",
        description=(
            "This account repeatedly posts promotional "
            "content and suspicious offers."
        ),
        status="PENDING"
    )

    
    get_or_create_report(
        reporter_id=users["isabella_walker"].id,
        post_id=reportable_posts[3].id,
        reason="SPAM",
        description=(
            "The post requests sensitive account information."
        ),
        status="REVIEWED",
        reviewed_by=users["sophia_morgan"].id
    )

    # --------------------------------------------------------
    # REJECTED REPORT
    # --------------------------------------------------------

    get_or_create_report(
        reporter_id=users["charlotte_wright"].id,
        post_id=all_posts[0].id,
        reason="OTHER",
        description=(
            "Reported because the content was considered "
            "unhelpful by the reporter."
        ),
        status="REJECTED",
        reviewed_by=users["liam_bennett"].id
    )

    db.session.commit()

    print("Moderation reports verified.")

    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    notification_data = [

        (
            "emma_wilson",
            "oliver_harris",
            "FOLLOW",
            None
        ),

        (
            "emma_wilson",
            "ava_thompson",
            "LIKE",
            all_posts[0]
        ),

        (
            "oliver_harris",
            "emma_wilson",
            "COMMENT",
            all_posts[1]
        ),

        (
            "ava_thompson",
            "noah_martin",
            "LIKE",
            all_posts[2]
        ),

        (
            "mia_clark",
            "isabella_walker",
            "FOLLOW",
            None
        ),

        (
            "sophia_young",
            "charlotte_wright",
            "COMMENT",
            all_posts[10]
        )
    ]

    for (
        recipient,
        actor,
        notification_type,
        post
    ) in notification_data:

        get_or_create_notification(
            recipient_id=users[recipient].id,
            actor_id=users[actor].id,
            type_name=notification_type,
            post_id=post.id if post else None
        )

    db.session.commit()

    print("Notifications verified.")

    # ========================================================
    # AUDIT LOGS
    # ========================================================

    # Existing moderation activity
    reviewed_report = Report.query.filter_by(
        status="REVIEWED"
    ).first()

    rejected_report = Report.query.filter_by(
        status="REJECTED"
    ).first()

    if reviewed_report:

        get_or_create_audit_log(
            admin_id=users["sophia_morgan"].id,
            action="REVIEW_REPORT",
            entity_type="REPORT",
            entity_id=reviewed_report.id,
            details=(
                "Moderator reviewed a report concerning "
                "suspicious account information."
            )
        )

    if rejected_report:

        get_or_create_audit_log(
            admin_id=users["liam_bennett"].id,
            action="DISMISS_REPORT",
            entity_type="REPORT",
            entity_id=rejected_report.id,
            details=(
                "Report dismissed because the reported content "
                "did not violate community guidelines."
            )
        )

    # Administrative activity

    get_or_create_audit_log(
        admin_id=users["alexandra_reed"].id,
        action="UPDATE_USER",
        entity_type="USER",
        entity_id=users["emma_wilson"].id,
        details=(
            "Administrator updated user account information."
        )
    )

    get_or_create_audit_log(
        admin_id=users["daniel_carter"].id,
        action="UPDATE_USER",
        entity_type="USER",
        entity_id=users["oliver_harris"].id,
        details=(
            "Administrator reviewed and updated user account."
        )
    )

    db.session.commit()

    print("Audit logs verified.")

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("======================================")
    print("P1 DEMO DATABASE READY")
    print("======================================")
    print()

    print("ADMIN ACCOUNTS")
    print("--------------------------------------")
    print("alexandra_reed  / Admin@123")
    print("daniel_carter   / Admin@123")
    print()

    print("MODERATOR ACCOUNTS")
    print("--------------------------------------")
    print("sophia_morgan   / Moderator@123")
    print("liam_bennett    / Moderator@123")
    print()

    print("DEMO USER ACCOUNTS")
    print("--------------------------------------")
    print("emma_wilson     / User@123")
    print("oliver_harris   / User@123")
    print("ava_thompson    / User@123")
    print("noah_martin     / User@123")
    print("mia_clark       / User@123")
    print("ethan_lewis     / User@123")
    print("isabella_walker / User@123")
    print("mason_hall     / User@123")
    print("sophia_young    / User@123")
    print("james_king      / User@123")
    print("charlotte_wright / User@123")
    print("benjamin_scott  / User@123")
    print("amelia_green    / User@123")
    print("henry_adams     / User@123")
    print("grace_baker     / User@123")
    print()

    print("======================================")
    print("MODERATION DEMO DATA")
    print("======================================")
    print()
    print("Pending post reports : 3")
    print("Pending user reports : 1")
    print("Reviewed reports     : 1")
    print("Rejected reports     : 1")
    print()
    print("The database is ready for demonstration.")
    print("======================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    with app.app_context():

        seed_database()