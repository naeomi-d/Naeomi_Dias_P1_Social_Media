import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


class Config:

    
    SECRET_KEY = os.getenv("SECRET_KEY")


    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=30
    )


    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    BASE_DIR = os.path.abspath(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "uploads")
    )

    LOG_FOLDER = os.path.join(
        BASE_DIR,
        "logs"
    )

    LOG_FILE = os.path.join(
        LOG_FOLDER,
        "app.log"
    )


    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "gif"
    }