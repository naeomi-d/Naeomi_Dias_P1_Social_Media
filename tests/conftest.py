import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import BigInteger
from flask_jwt_extended import create_access_token
import bcrypt

from app import create_app, db
from app.models.user import User


@compiles(BigInteger, "sqlite")
def _compile_bigint_sqlite(type_, compiler, **kw):
    return "INTEGER"


def _hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


@pytest.fixture
def app(tmp_path):
    upload_folder = str(tmp_path / "uploads")
    override_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_ENGINE_OPTIONS": {"poolclass": StaticPool},
        "JWT_SECRET_KEY": "super_secret_jwt_key_32_bytes_long_exact",
        "SECRET_KEY": "test_session_secret_key",
        "UPLOAD_FOLDER": upload_folder,
        "WTF_CSRF_ENABLED": False
    }
    app = create_app(override_config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            username="regular_user",
            email="regular@example.com",
            password_hash=_hash_password("UserPassword123"),
            first_name="Regular",
            last_name="User",
            role="USER",
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def test_moderator(app):
    with app.app_context():
        mod = User(
            username="mod_user",
            email="mod@example.com",
            password_hash=_hash_password("ModPassword123"),
            first_name="Moderator",
            last_name="User",
            role="MODERATOR",
            is_active=True
        )
        db.session.add(mod)
        db.session.commit()
        db.session.refresh(mod)
        return mod


@pytest.fixture
def test_admin(app):
    with app.app_context():
        admin = User(
            username="admin_user",
            email="admin@example.com",
            password_hash=_hash_password("AdminPassword123"),
            first_name="Admin",
            last_name="User",
            role="ADMIN",
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)
        return admin


@pytest.fixture
def user_headers(app, test_user):
    with app.app_context():
        token = create_access_token(
            identity=str(test_user.id),
            additional_claims={"role": test_user.role}
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def moderator_headers(app, test_moderator):
    with app.app_context():
        token = create_access_token(
            identity=str(test_moderator.id),
            additional_claims={"role": test_moderator.role}
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(app, test_admin):
    with app.app_context():
        token = create_access_token(
            identity=str(test_admin.id),
            additional_claims={"role": test_admin.role}
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def tmp_upload_dir(app):
    return app.config["UPLOAD_FOLDER"]
