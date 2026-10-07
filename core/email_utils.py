import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def send_html_email(template_name: str, context: Dict, subject: str, recipient_list: List[str]):
    """Keep notifications disabled without interrupting account operations."""
    logger.info("Email notifications are disabled; skipped %r.", subject)
    return 0
