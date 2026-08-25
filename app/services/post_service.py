from datetime import datetime

from app import db

from app.dao.post_dao import PostDAO
from app.dao.hashtag_dao import HashtagDAO
from app.dao.post_hashtag_dao import PostHashtagDAO
from app.dao.follow_dao import FollowDAO

from app.models.post import Post
from app.models.hashtag import Hashtag
from app.models.post_hashtag import PostHashtag

from app.services.file_service import FileService
from app.utils.hashtag_utils import extract_hashtags

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.validation_exceptions import ValidationError
from app.exceptions.authorization_exceptions import AuthorizationError

class PostService:

    @staticmethod
    def create_post(user_id, content, visibility, image_file=None, image_path=None):
        if not content or not content.strip():
            raise ValueError("Post content cannot be empty.")

        allowed_visibility = {"PUBLIC", "FOLLOWERS", "PRIVATE"}
        if visibility not in allowed_visibility:
            raise ValueError("Invalid post visibility.")

        saved_image_path = None
        if image_file and hasattr(image_file, "filename") and image_file.filename:
            saved_image_path = FileService.save_upload(image_file, "post_images")
        elif image_path:
            saved_image_path = image_path

        clean_content = content.strip()
        post = Post(
            user_id=user_id,
            content=clean_content,
            visibility=visibility,
            image_path=saved_image_path,
            status="ACTIVE"
        )

        try:
            PostDAO.create(post)
            db.session.flush()
            hashtag_names = extract_hashtags(clean_content)
            for hashtag_name in hashtag_names:
                hashtag = HashtagDAO.find_by_name(hashtag_name)
                if not hashtag:
                    hashtag = Hashtag(name=hashtag_name)
                    HashtagDAO.create(hashtag)
                    db.session.flush()
                post_hashtag = PostHashtag(post=post, hashtag=hashtag)
                db.session.add(post_hashtag)
            db.session.commit()
        except Exception:
            db.session.rollback()
            if saved_image_path:
                FileService.cleanup_file(saved_image_path)
            raise

        return post

    @staticmethod
    def get_feed(viewer_id=None, page=1, per_page=10):

            pagination = PostDAO.find_active_posts(
            page=page,
            per_page=per_page
        )
            visible_posts = []
            for post in pagination.items:
                try:
                    visible_posts.append(
                    PostService.get_post_for_viewer(
                        post.id,
                        viewer_id
                    )
                )

                except AuthorizationError:
                 continue

            return visible_posts, pagination

    @staticmethod
    def get_user_posts(user_id, viewer_id=None):
        posts = PostDAO.find_active_by_user(user_id)
        if viewer_id is None:
            return posts

        visible_posts = []
        for post in posts:
            try:
                visible_posts.append(PostService.get_post_for_viewer(post.id, viewer_id))
            except AuthorizationError:
                continue
        return visible_posts

    @staticmethod
    def get_post_for_viewer(post_id, viewer_id):
        post = PostDAO.find_by_id(post_id)

        if not post or post.status != "ACTIVE":
            raise ResourceNotFoundError("Post not found.")

        if post.visibility == "PRIVATE" and post.user_id != viewer_id:
            raise AuthorizationError("You cannot view this private post.")

        if (
            post.visibility == "FOLLOWERS"
            and post.user_id != viewer_id
            and not FollowDAO.find_follow(viewer_id, post.user_id)
        ):
            raise AuthorizationError("You must follow this user to view the post.")

        return post

    @staticmethod
    def update_post(
        post_id,
        user_id,
        content=None,
        visibility=None,
        image_file=None,
        image_path=None
    ):
        post = PostDAO.find_by_id(post_id)
        if not post:
            raise ResourceNotFoundError("Post not found.")
        if post.status == "DELETED":
            raise ValidationError("Cannot edit a deleted post.")
        if post.user_id != user_id:
            raise AuthorizationError("You cannot edit another user's post.")

        has_image_file = image_file and hasattr(image_file, "filename") and bool(image_file.filename)
        has_image_path = image_path is not None

        if content is None and visibility is None and not has_image_file and not has_image_path:
            raise ValidationError("Provide content, visibility, or an image to update.")

        if content is None:
            content = post.content
        if visibility is None:
            visibility = post.visibility

        if not content or not content.strip():
            raise ValidationError("Post content cannot be empty.")

        allowed_visibility = {"PUBLIC", "FOLLOWERS", "PRIVATE"}
        if visibility not in allowed_visibility:
            raise ValidationError("Invalid post visibility.")

        clean_content = content.strip()
        old_image = post.image_path

        new_image_path = None
        if has_image_file:
            new_image_path = FileService.save_upload(image_file, "post_images")
        elif has_image_path:
            new_image_path = image_path

        post.content = clean_content
        post.visibility = visibility
        if new_image_path is not None:
            post.image_path = new_image_path

        try:
            PostHashtagDAO.delete_by_post_id(post.id)
            db.session.flush()
            hashtag_names = extract_hashtags(clean_content)
            for hashtag_name in hashtag_names:
                hashtag = HashtagDAO.find_by_name(hashtag_name)
                if not hashtag:
                    hashtag = Hashtag(name=hashtag_name)
                    HashtagDAO.create(hashtag)
                    db.session.flush()
                post_hashtag = PostHashtag(post=post, hashtag=hashtag)
                db.session.add(post_hashtag)
            PostDAO.update(post)
            db.session.commit()
        except Exception:
            db.session.rollback()
            if new_image_path and new_image_path != old_image:
                FileService.cleanup_file(new_image_path)
            raise

        if old_image and new_image_path and old_image != new_image_path:
            FileService.cleanup_file(old_image)

        return post

    @staticmethod
    def delete_post(post_id, user_id):
        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ValidationError("Post not found.")

        if post.status == "DELETED":
            raise ValidationError("Post is already deleted.")

        if post.user_id != user_id:
            raise AuthorizationError("You cannot delete another user's post.")

        post.status = "DELETED"
        post.deleted_at = datetime.utcnow()

        PostDAO.update(post)

        return post
