from unittest.mock import patch

from django.test import SimpleTestCase

from core.email_utils import send_html_email
from .signals import send_account_email


class EmailDeliveryTests(SimpleTestCase):
    def test_email_notifications_are_disabled(self):
        result = send_html_email(
            "email/default_email.html",
            {"plain_message": "Account created"},
            "Welcome",
            ["brand@example.com"],
        )

        self.assertEqual(result, 0)

    @patch("core.email_utils.send_html_email", side_effect=RuntimeError("Invalid email API key"))
    def test_account_signal_email_failure_does_not_escape(self, send_email):
        with self.assertLogs("accounts.signals", level="ERROR"):
            send_account_email("brand@example.com", "Welcome", "Account created")

        send_email.assert_called_once()
