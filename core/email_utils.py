import os
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from typing import List, Dict

def send_html_email(template_name: str, context: Dict, subject: str, recipient_list: List[str]):
    """Render an HTML template and send a multipart email.

    Args:
        template_name: Path relative to the configured template dirs, e.g. 'email/welcome_email.html'.
        context: Dictionary passed to the template. Must contain at least ``subject`` for the title.
        subject: Email subject line.
        recipient_list: List of email addresses.
    """
    plain_message = context.get('plain_message', '')
    html_content = render_to_string(template_name, context)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@altclan.shop")
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message or subject,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
