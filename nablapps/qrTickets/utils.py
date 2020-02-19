from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

FROM_EMAIL_ADDRESS = "noreply-tickets@nabla.no"


def send_template_email(template, context, subject, emails):
    """Send email using a django-template"""
    from_email = FROM_EMAIL_ADDRESS

    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=from_email,
        recipient_list=emails,
        html_message=html_content,
    )
