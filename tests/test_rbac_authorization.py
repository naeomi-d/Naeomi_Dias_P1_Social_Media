from datetime import datetime
from types import SimpleNamespace

import pytest
from flask import Flask
from flask_jwt_extended import create_access_token

from app import jwt
from app.api.v1.report_api import report_api_bp
from app.dao.report_dao import ReportDAO
from app.services.report_service import ReportService


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.update(TESTING=True, JWT_SECRET_KEY="super_secret_jwt_key_32_bytes_long_exact")
    jwt.init_app(app)
    app.register_blueprint(report_api_bp)
    return app


def _token(app, user_id, role):
    with app.app_context():
        return create_access_token(
            identity=str(user_id),
            additional_claims={"role": role},
        )


def _headers(app, user_id, role):
    return {"Authorization": f"Bearer {_token(app, user_id, role)}"}


def _report(reporter_id=10):
    return SimpleNamespace(
        id=1,
        reporter_id=reporter_id,
        reported_user_id=None,
        post_id=5,
        reason="Spam",
        description=None,
        status="PENDING",
        reviewed_by=None,
        reviewed_at=None,
        created_at=datetime.utcnow(),
    )


def test_user_cannot_list_reports(app):
    response = app.test_client().get(
        "/api/v1/reports",
        headers=_headers(app, 10, "USER"),
    )
    assert response.status_code == 403
    assert response.get_json() == {"error": "Access denied."}


@pytest.mark.parametrize("role", ["MODERATOR", "ADMIN"])
def test_moderator_and_admin_can_list_reports(app, monkeypatch, role):
    monkeypatch.setattr(ReportService, "get_pending_reports", lambda: [])

    response = app.test_client().get(
        "/api/v1/reports",
        headers=_headers(app, 20, role),
    )

    assert response.status_code == 200
    assert response.get_json() == {"reports": []}


def test_user_cannot_review_report(app):
    response = app.test_client().patch(
        "/api/v1/reports/1",
        json={"status": "REVIEWED"},
        headers=_headers(app, 10, "USER"),
    )
    assert response.status_code == 403


@pytest.mark.parametrize("role", ["MODERATOR", "ADMIN"])
def test_moderator_and_admin_can_review_report(app, monkeypatch, role):
    report = _report()

    def review_report(report_id, reviewer_id, status):
        assert report_id == 1
        assert reviewer_id == 20
        assert status == "REVIEWED"
        report.status = status
        report.reviewed_by = reviewer_id
        report.reviewed_at = datetime.utcnow()
        return report

    from app.services.admin_service import AdminService

    monkeypatch.setattr(AdminService, "review_report", review_report)

    response = app.test_client().patch(
        "/api/v1/reports/1",
        json={"status": "REVIEWED"},
        headers=_headers(app, 20, role),
    )

    assert response.status_code == 200
    assert response.get_json()["report"]["reviewed_by"] == 20


def test_report_service_allows_owner_but_denies_other_user(monkeypatch):
    report = _report(reporter_id=10)
    monkeypatch.setattr(ReportDAO, "find_by_id", lambda report_id: report)

    assert ReportService.get_report(1, requester_id=10) is report

    with pytest.raises(PermissionError):
        ReportService.get_report(1, requester_id=11)


def test_user_can_view_own_report_but_not_another_users(app, monkeypatch):
    monkeypatch.setattr(ReportDAO, "find_by_id", lambda report_id: _report(10))
    client = app.test_client()

    own_response = client.get(
        "/api/v1/reports/1",
        headers=_headers(app, 10, "USER"),
    )
    other_response = client.get(
        "/api/v1/reports/1",
        headers=_headers(app, 11, "USER"),
    )

    assert own_response.status_code == 200
    assert other_response.status_code == 403


@pytest.mark.parametrize("role", ["MODERATOR", "ADMIN"])
def test_moderation_roles_can_view_any_report(app, monkeypatch, role):
    monkeypatch.setattr(ReportDAO, "find_by_id", lambda report_id: _report(10))

    response = app.test_client().get(
        "/api/v1/reports/1",
        headers=_headers(app, 20, role),
    )

    assert response.status_code == 200
