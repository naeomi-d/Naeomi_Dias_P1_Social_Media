import pytest
from app.services.post_service import PostService
from app.services.report_service import ReportService
from app.services.admin_audit_log_service import AdminAuditLogService


def test_user_access_moderator_dashboard_forbidden(client, test_user):
    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username
        sess["role"] = "USER"

    res = client.get("/moderator/dashboard")
    assert res.status_code == 403


def test_moderator_access_moderator_dashboard_success(client, test_moderator):
    with client.session_transaction() as sess:
        sess["user_id"] = test_moderator.id
        sess["username"] = test_moderator.username
        sess["role"] = "MODERATOR"

    res = client.get("/moderator/dashboard")
    assert res.status_code == 200
    assert b"Moderator Dashboard" in res.data


def test_admin_access_moderator_dashboard_success(client, test_admin):
    with client.session_transaction() as sess:
        sess["user_id"] = test_admin.id
        sess["username"] = test_admin.username
        sess["role"] = "ADMIN"

    res = client.get("/moderator/dashboard")
    assert res.status_code == 200
    assert b"Moderator Dashboard" in res.data


def test_admin_access_admin_dashboard_success(client, test_admin):
    with client.session_transaction() as sess:
        sess["user_id"] = test_admin.id
        sess["username"] = test_admin.username
        sess["role"] = "ADMIN"

    res = client.get("/admin/dashboard")
    assert res.status_code == 200
    assert b"Admin Dashboard" in res.data


def test_moderator_access_admin_dashboard_forbidden(client, test_moderator):
    with client.session_transaction() as sess:
        sess["user_id"] = test_moderator.id
        sess["username"] = test_moderator.username
        sess["role"] = "MODERATOR"

    res = client.get("/admin/dashboard")
    assert res.status_code == 403


def test_user_access_admin_dashboard_forbidden(client, test_user):
    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username
        sess["role"] = "USER"

    res = client.get("/admin/dashboard")
    assert res.status_code == 403


def test_moderator_review_report_action(
    client,
    test_user,
    test_moderator
):
    post = PostService.create_post(
        test_user.id,
        "Reportable post content",
        "PUBLIC"
    )

    report = ReportService.report_post(
        test_user.id,
        post.id,
        "Spam post",
        "Test description"
    )

    with client.session_transaction() as sess:
        sess["user_id"] = test_moderator.id
        sess["username"] = test_moderator.username
        sess["role"] = "MODERATOR"

    res = client.post(
        f"/moderator/reports/{report.id}/review",
        data={
            "status": "REVIEWED"
        },
        follow_redirects=True
    )

    assert res.status_code == 200

    updated_report = ReportService.get_report(
        report.id,
        test_moderator.id,
        can_moderate=True
    )

    assert updated_report.status == "REVIEWED"
    assert updated_report.reviewed_by == test_moderator.id

    logs = AdminAuditLogService.get_logs()

    matching_logs = [
        log
        for log in logs
        if (
            log.admin_id == test_moderator.id
            and log.action == "REVIEW_REPORT"
            and log.entity_type == "REPORT"
            and log.entity_id == report.id
        )
    ]

    assert len(matching_logs) == 1

    audit_log = matching_logs[0]

    assert audit_log.details == (
        "Report reviewed with status REVIEWED."
    )