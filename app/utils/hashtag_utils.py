import re


def extract_hashtags(content):

    if not content:
        return set()

    hashtags = re.findall(
        r"#([A-Za-z0-9_]+)",
        content
    )

    return {
        hashtag.lower()
        for hashtag in hashtags
    }