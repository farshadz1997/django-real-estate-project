from typing import Sequence
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_created_property_email(title, status, description, receivers: Sequence[str] | None=None):
    context = {
        "title": title,
        "status": status,
        "description": description,
    }
    subject = "Property Created"
    email = EmailMessage(
        subject,
        render_to_string("property_created_email.txt", context),
        settings.DEFAULT_FROM_EMAIL,
        receivers
    )
    return email.send(fail_silently=False)