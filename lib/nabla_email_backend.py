from django.core.mail.backends.base import BaseEmailBackend

from lib import GCloudUtils as gcu


class Nabla_email_backend(BaseEmailBackend):
    handler = gcu.GCloudHandler()

    def send_messages(self, email_messages):
        for email_message in email_messages:
            self.handler.send_email(
                # to = email_message.to,
                to="webkom@nabla.no",  # FOR TESTING PURPOSES ONLY, RESET BEFORE MERGE
                subject=email_message.subject,
                message=email_message.body,
                bcc=email_message.bcc,  # Gmail overrides author as
                cc=email_message.cc
                + [email_message.from_email],  # impersonated superuser.
                reply_to=email_message.reply_to,  # Therefore we CC them instead.
            )


# TODO: Fix DEFAULT_FROM_EMAIL                          Impossible. Added as CC and text in mail instead.
# TODO: Fix sending to list of recipient addresses      We seem not to use send_message

# TODO: Confirm connection not needed                   Can be implemented, not yer
# TODO: Confirm headers not needed                      As of yet unused

# TODO: Add versioning to google lib & clean            Semantic major version locked down

# TODO: See how lots of mail is sent by nablaweb atm    We seem not to send lots of mail atm
# TODO: See django's send_mass_email()                  UNUSED
