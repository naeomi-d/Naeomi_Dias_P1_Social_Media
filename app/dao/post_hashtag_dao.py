from app.models.post_hashtag import PostHashtag


class PostHashtagDAO:

    @staticmethod
    def delete_by_post_id(post_id):
        PostHashtag.query.filter_by(post_id=post_id).delete(
            synchronize_session=False
        )

    @staticmethod
    def find_by_post(post_id):
        return PostHashtag.query.filter_by(post_id=post_id).all()

    @staticmethod
    def find_by_hashtag(hashtag_id):
        return PostHashtag.query.filter_by(hashtag_id=hashtag_id).all()
