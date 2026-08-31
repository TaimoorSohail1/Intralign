from unittest.mock import MagicMock, patch

from oslo_api.application import DatabaseSliceOneApplication


def _application_with_single_connection():
    engine = MagicMock()
    connection = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=MagicMock(),
        mailer=MagicMock(),
        web_url="http://localhost:3000",
    )
    return application, engine, connection


def test_new_account_activation_reuses_the_advisory_lock_connection() -> None:
    application, engine, connection = _application_with_single_connection()
    expected = object()

    with patch.object(application, "_activate_invitation_once", return_value=expected) as once:
        result = application.activate_invitation(
            token="invite-token",
            display_name="New member",
            password="Password123!",
        )

    assert result is expected
    engine.begin.assert_called_once_with()
    assert "pg_advisory_xact_lock" in str(connection.execute.call_args.args[0])
    once.assert_called_once_with(
        connection=connection,
        token="invite-token",
        display_name="New member",
        password="Password123!",
    )


def test_existing_account_acceptance_reuses_the_advisory_lock_connection() -> None:
    application, engine, connection = _application_with_single_connection()
    expected = object()

    with patch.object(
        application,
        "_accept_invitation_for_existing_user_once",
        return_value=expected,
    ) as once:
        result = application.accept_invitation_for_existing_user(
            token="invite-token",
            email="member@example.com",
            password="Password123!",
        )

    assert result is expected
    engine.begin.assert_called_once_with()
    assert "pg_advisory_xact_lock" in str(connection.execute.call_args.args[0])
    once.assert_called_once_with(
        connection=connection,
        token="invite-token",
        email="member@example.com",
        password="Password123!",
    )
