from app.dao.hashtag_dao import HashtagDAO
from app.dao.post_hashtag_dao import PostHashtagDAO
from app.dao.post_dao import PostDAO
from app.services.post_service import PostService


class HashtagService:

    @staticmethod
    def get_hashtags():
        return HashtagDAO.find_all()

    @staticmethod
    def get_hashtag(name):
        hashtag = HashtagDAO.find_by_name(name.lower().lstrip("#"))
        if not hashtag:
            raise ValueError("Hashtag not found.")
        return hashtag

    @staticmethod
    def search_hashtags(query):
        if not query or not query.strip():
            raise ValueError("Search query is required.")
        return HashtagDAO.search(query.strip().lower().lstrip("#"))

    @staticmethod
    def get_posts_for_hashtag(name, viewer_id):
        hashtag = HashtagService.get_hashtag(name)
        posts = [link.post for link in PostHashtagDAO.find_by_hashtag(hashtag.id)]
        visible_posts = []
        for post in posts:
            try:
                visible_posts.append(PostService.get_post_for_viewer(post.id, viewer_id))
            except (ValueError, PermissionError):
                continue
        return visible_posts

    @staticmethod
    def get_post_hashtags(post_id, viewer_id):
        PostService.get_post_for_viewer(post_id, viewer_id)
        return [link.hashtag for link in PostHashtagDAO.find_by_post(post_id)]
