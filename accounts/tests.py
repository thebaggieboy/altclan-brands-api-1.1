from unittest.mock import patch

from django.test import SimpleTestCase

from core.email_utils import send_html_email


class EmailDeliveryTests(SimpleTestCase):
    @patch("core.email_utils.EmailMultiAlternatives")
    @patch("core.email_utils.render_to_string", return_value="<p>Account created</p>")
    def test_email_provider_failure_is_logged_and_non_fatal(self, render_email, email_class):
        email_class.return_value.send.side_effect = RuntimeError("Invalid email API key")

        with self.assertLogs("core.email_utils", level="ERROR"):
            result = send_html_email(
                "email/default_email.html",
                {"plain_message": "Account created"},
                "Welcome",
                ["brand@example.com"],
            )

        self.assertEqual(result, 0)
        email_class.return_value.send.assert_called_once_with(fail_silently=False)
