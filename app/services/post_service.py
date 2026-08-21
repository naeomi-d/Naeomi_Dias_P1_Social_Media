from datetime import datetime

from app import db

from app.dao.post_dao import PostDAO
from app.dao.hashtag_dao import HashtagDAO
from app.dao.post_hashtag_dao import PostHashtagDAO
from app.dao.follow_dao import FollowDAO

from app.models.post import Post
from app.models.hashtag import Hashtag
from app.models.post_hashtag import PostHashtag

from app.utils.hashtag_utils import extract_hashtags


class PostService:

    # ==================== CREATE POST ====================

    @staticmethod
    def create_post(user_id, content, visibility):

        if not content or not content.strip():
            raise ValueError(
                "Post content cannot be empty."
            )

        allowed_visibility = {
            "PUBLIC",
            "FOLLOWERS",
            "PRIVATE"
        }

        if visibility not in allowed_visibility:
            raise ValueError(
                "Invalid post visibility."
            )

        clean_content = content.strip()

        post = Post(
            user_id=user_id,
            content=clean_content,
            visibility=visibility,
            status="ACTIVE"
        )

        PostDAO.create(post)

        db.session.flush()

        hashtag_names = extract_hashtags(
            clean_content
        )

        for hashtag_name in hashtag_names:

            hashtag = HashtagDAO.find_by_name(
                hashtag_name
            )

            if not hashtag:

                hashtag = Hashtag(
                    name=hashtag_name
                )

                HashtagDAO.create(hashtag)

                db.session.flush()

            post_hashtag = PostHashtag(
                post=post,
                hashtag=hashtag
            )

            db.session.add(post_hashtag)

        db.session.commit()

        return post


    # ==================== GET FEED ====================

    @staticmethod
    def get_feed(viewer_id=None):
        posts = PostDAO.find_active_posts()
        if viewer_id is None:
            return posts

        visible_posts = []
        for post in posts:
            try:
                visible_posts.append(PostService.get_post_for_viewer(post.id, viewer_id))
            except PermissionError:
                continue
        return visible_posts

    @staticmethod
    def get_user_posts(user_id, viewer_id=None):
        posts = PostDAO.find_active_by_user(user_id)
        if viewer_id is None:
            return posts

        visible_posts = []
        for post in posts:
            try:
                visible_posts.append(PostService.get_post_for_viewer(post.id, viewer_id))
            except PermissionError:
                continue
        return visible_posts

    @staticmethod
    def get_post_for_viewer(post_id, viewer_id):
        post = PostDAO.find_by_id(post_id)

        if not post or post.status != "ACTIVE":
            raise ValueError("Post not found.")

        if post.visibility == "PRIVATE" and post.user_id != viewer_id:
            raise PermissionError("You cannot view this private post.")

        if (
            post.visibility == "FOLLOWERS"
            and post.user_id != viewer_id
            and not FollowDAO.find_follow(viewer_id, post.user_id)
        ):
            raise PermissionError("You must follow this user to view the post.")

        return post


    # ==================== UPDATE POST ====================

    @staticmethod
    def update_post(
        post_id,
        user_id,
        content,
        visibility
    ):

        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ValueError(
                "Post not found."
            )

        if post.status == "DELETED":
            raise ValueError(
                "Cannot edit a deleted post."
            )

        if post.user_id != user_id:
            raise PermissionError(
                "You cannot edit another user's post."
            )

        if content is None:
            content = post.content

        if visibility is None:
            visibility = post.visibility

        if not content or not content.strip():
            raise ValueError(
                "Post content cannot be empty."
            )

        allowed_visibility = {
            "PUBLIC",
            "FOLLOWERS",
            "PRIVATE"
        }

        if visibility not in allowed_visibility:
            raise ValueError(
                "Invalid post visibility."
            )

        clean_content = content.strip()

        post.content = clean_content
        post.visibility = visibility

        # Remove old hashtag relationships

        PostHashtagDAO.delete_by_post_id(post.id)

        db.session.flush()

        # Extract new hashtags

        hashtag_names = extract_hashtags(
            clean_content
        )

        for hashtag_name in hashtag_names:

            hashtag = HashtagDAO.find_by_name(
                hashtag_name
            )

            if not hashtag:

                hashtag = Hashtag(
                    name=hashtag_name
                )

                HashtagDAO.create(hashtag)

                db.session.flush()

            post_hashtag = PostHashtag(
                post=post,
                hashtag=hashtag
            )

            db.session.add(post_hashtag)

        PostDAO.update(post)

        db.session.commit()

        return post


    # ==================== DELETE POST ====================

    @staticmethod
    def delete_post(post_id, user_id):

        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ValueError(
                "Post not found."
            )

        if post.status == "DELETED":
            raise ValueError(
                "Post is already deleted."
            )

        if post.user_id != user_id:
            raise PermissionError(
                "You cannot delete another user's post."
            )

        post.status = "DELETED"
        post.deleted_at = datetime.utcnow()

        PostDAO.update(post)

        return post
