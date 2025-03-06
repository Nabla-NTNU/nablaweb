# Raw email encoding
import base64
from email.message import EmailMessage

# Django's email backend parent class
from django.core.mail.backends.base import BaseEmailBackend

# Google API authentication
from google.oauth2 import service_account  # Authentication
from googleapiclient.discovery import build  # API wrapper
from googleapiclient.errors import HttpError  # Interpreting returned errors

# Private key filepath
SERVICE_ACCOUNT_FILE_PATH: str = "lib/privateKey.json"

# Email of admin to be impersonated. Used as true from email.
IMPERSONATED_ADMIN: str = "noreply@nabla.no"

# Domain name of the soc website
ROOT_DOMAIN: str = "nabla.no"


class Nabla_email_backend(BaseEmailBackend):
    _SCOPES: list[str] = [
        "https://www.googleapis.com/auth/gmail.send",
    ]  # https://developers.google.com/admin-sdk/directory/v1/guides/authorizing < Relevant scopes

    # Generate credentials and object to send API calls
    def __init__(self, **kwargs):
        _creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE_PATH, scopes=self._SCOPES
        ).with_subject(IMPERSONATED_ADMIN)
        self._service = build("gmail", "v1", credentials=_creds)

    def send_message(self, email_message):
        mail = EmailMessage()
        mail.set_content(email_message.body)

        # Override to send mail to outselves for debugging
        mail["To"] = email_message.to
        mail["From"] = IMPERSONATED_ADMIN
        mail["Subject"] = email_message.subject
        mail["BCC"] = email_message.bcc

        if email_message.from_email != IMPERSONATED_ADMIN:
            mail["CC"] = email_message.from_email
            mail["Reply-To"] = email_message.from_email
        else:
            mail["CC"] = ", ".join(email_message.cc)
            mail["Reply-To"] = ", ".join(email_message.reply_to)

        # Encode email to binary
        encoded_email = base64.urlsafe_b64encode(mail.as_bytes()).decode()
        encoded_package = {"raw": encoded_email}

        try:
            email_attempt = (
                self._service.users()
                .messages()
                .send(userId="me", body=encoded_package)
                .execute()
            )
            print("Sent email of ID: %s" % email_attempt["id"])
        except HttpError as error:
            print("Error: %s" % error)

    def send_messages(self, email_messages):
        for email_message in email_messages:
            self.send_message(email_message)


# Authenitcation is done by connecting the service account set up on the cloud.google.com
#     console and set up with domain-wide authority in on the admin panel. This is what
#     open() does. As we are doing sensitive admin work, we need to impersonate an admin,
#     which is what .with_subject does.

# This then needs to be built into a service object that actually makes the call. This is
#     done (for the gmail API, version 1)
#         self._service = build("gmail", "v1", credentials=_creds)

# API calls are done by specifiying which API wr're using, and calling the HTTP request like
#           email_attempt = (
#               self._service.users()
#               .messages()
#               .send(userId="me", body=encoded_package)
#               .execute()
#           )
#     Here we use the service object to access the groups API, run a get function giving it
#     what it asks for in the documentation, and actually calling it by .excecute().
