from __future__ import absolute_import, unicode_literals
from typing import Sequence
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from celery.utils.log import get_task_logger
from home_property_project.celery import app
from .email import send_created_property_email


logger = get_task_logger(__name__)


@app.task(name="send_create_property_email_task")
def send_create_property_email_task(title, status, description, receiver: Sequence[str] | None=None):
    send_created_property_email(title, status, description, receiver)
    logger.info("Email sent")


@app.task(name="password_reset_email_task")
def send_password_reset_email_task(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    context['user'] = User.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
    logger.info("Password reset email sent")
