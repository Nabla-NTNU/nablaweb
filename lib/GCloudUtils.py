import base64  # Emcoding email
from email.message import EmailMessage  # Handling email

from google.oauth2 import service_account  # Auth
from googleapiclient.discovery import build  # API wrapper
from googleapiclient.errors import HttpError  # Error handler help

from lib import config


def colorStr(string: str, color: str) -> str:
    if color == "error":
        return "\033[91m" + string + "\033[0m"
    elif color == "red":
        return "\033[91m" + string + "\033[0m"
    elif color == "green":
        return "\033[92m" + string + "\033[0m"
    elif color == "warning":
        return "\033[93m" + string + "\033[0m"
    elif color == "yellow":
        return "\033[93m" + string + "\033[0m"
    elif color == "blue":
        return "\033[94m" + string + "\033[0m"
    elif color == "purple":
        return "\033[95m" + string + "\033[0m"
    elif color == "cyan":
        return "\033[96m" + string + "\033[0m"
    elif color == "bold":
        return "\033[1m" + string + "\033[0m"
    elif color == "underline":
        return "\033[4m" + string + "\033[0m"
    else:
        return "\033[0m" + string + "\033[0m"


def progressBar(progress: int, total: int, len: int) -> str:
    # just having fun now
    scaledProgress = round(progress / total * (len))
    return f"[%s] {progress}/{total}" % (
        "#" * scaledProgress + "-" * (len - scaledProgress)
    )


class GCloudMember:
    """
        A record of a person's subscription to put into a group

        ...

    Attributes
    ----------
    email : str
        Member's desired email

    Methods
    -------
    GCloudMember(email: str)
        Intended use for creating a member
    """

    email: str = ""

    def __init__(self, email: str = None, _response: dict = {}):
        if email is None:
            self.kind = _response["kind"] if "kind" in _response else None
            self.email = _response["email"] if "email" in _response else email
            self.role = _response["role"] if "role" in _response else None
            self.etag = _response["etag"] if "etag" in _response else None
            self.type = _response["type"] if "type" in _response else None
            self.status = _response["status"] if "status" in _response else None
            self.delivery_settings = (
                _response["delivery_settings"]
                if "delivery_settings" in _response
                else None
            )
            self.id = _response["id"] if "id" in _response else None
        else:
            self.kind: str = None
            self.email: str = email
            self.role: str = "MEMBER"
            self.etag: str = None
            self.type: str = "EXTERNAL"
            self.status: str = None
            self.delivery_settings: str = "ALL_MAIL"
            self.id: str = None

    def getJSON(self):
        return {
            "kind": self.kind,
            "email": self.email,
            "role": self.role,
            "etag": self.etag,
            "type": self.type,
            "status": self.status,
            "delivery_settings": self.delivery_settings,
            "id": self.id,
        }

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email

    def __str__(self):
        return self.email


class GCloudGroup:
    """
        A Google Cloud group

        ...

    Attributes
    ----------
    members : [GCloudMember]
        List of all members
    email : str
        Unique group email

    Methods
    -------
    getGroups() -> list[GCloudGroup]
        Returns a list of all groups, populated with their members

    getGroup(groupEmail: str) -> GCloudGroup
        Returns specific group from the groups ID email
    """

    members: list[GCloudMember] = []
    groupEmail: str = ""
    settings: dict = {}

    def __init__(self, email: str = None, _response: dict = {}):
        self.id = _response["id"] if "id" in _response else None
        self.groupEmail = _response["email"] if "email" in _response else email
        self.name = _response["name"] if "name" in _response else None
        self.description = (
            _response["description"] if "description" in _response else None
        )
        self.adminCreated = (
            _response["adminCreated"] if "adminCreated" in _response else None
        )
        self.directMembersCount = (
            _response["directMembersCount"]
            if "directMembersCount" in _response
            else None
        )
        self.kind = _response["kind"] if "kind" in _response else None
        self.etag = _response["etag"] if "etag" in _response else None
        self.aliases = _response["aliases"] if "aliases" in _response else None
        self.nonEditableAliases = (
            _response["nonEditableAliases"]
            if "nonEditableAliases" in _response
            else None
        )

    def _getMembers(self, service):
        """Private function to populate group's member list"""
        try:
            membersJSON = (
                service.members().list(groupKey=self.groupEmail).execute()
            ).get("members", [])
            self.members = [
                GCloudMember(_response=memberJSON) for memberJSON in membersJSON
            ]
        except HttpError as err:
            print("Request failed. Message return from API:")
            print(err.error_details[0]["message"])

    def _getSettings(self, service):
        handler = GCloudHandler()
        creds = service_account.Credentials.from_service_account_file(
            handler.SERVICE_ACCOUNT_FILE_PATH, scopes=handler.SCOPES
        ).with_subject(handler.SUPER_ADMIN)
        handler.service = build("groupssettings", "v1", credentials=creds)

        settings = service.groups().get(groupKey=self.groupEmail).execute()
        print(settings)
        pass

    # Undocumented and as of yet unused helper function
    def getDirectMembers(self) -> list[GCloudMember]:
        return [member for member in self.members if member.email[-9:] != "@nabla.no"]

    # Undocumented and as of yet unused helper function
    def getIndirectMembers(self) -> list[GCloudMember]:
        return [member for member in self.members if member.email[-9:] == "@nabla.no"]

    def insertMember(self, member: GCloudMember, _handler=None) -> None:
        if not _handler:
            print(
                "Inserting %s to group %s"
                % (colorStr(member.email, "blue"), colorStr(self.name, "green"))
            )
            _handler = GCloudHandler()
        try:
            _handler.service.members().insert(
                groupKey=self.groupEmail, body=member.getJSON()
            ).execute()
        except HttpError as err:
            if err.error_details[0]["message"] == "Member already exists.":
                print(
                    "\r%s %s %s  %s"
                    % (
                        colorStr("API Warning:", "warning"),
                        colorStr(member.email, "blue"),
                        colorStr("already in group", "warning"),
                        colorStr(self.name, "green"),
                    ),
                    end="",
                )
            else:
                print(
                    "%s"
                    % colorStr(
                        "API Error: %s" % err.error_details[0]["message"], "error"
                    )
                )
                print(
                    "%s %s"
                    % (colorStr("Group key:", "error"))
                    % (
                        colorStr("Group key:", "error"),
                        colorStr(f"{self.groupEmail}", "blue"),
                    )
                )
                print(
                    "%s %s"
                    % (
                        colorStr("body:", "error"),
                        colorStr(f"{member.getJSON()}", "green"),
                    ),
                    end="",
                )
            print()
        return

    # TODO: test insertOwner
    def insertOwner(self, member: GCloudMember, _handler=None) -> None:
        member.role = "OWNER"
        self.insertMember(member, _handler)

    def deleteMember(self, member: GCloudMember, _handler=None) -> None:
        if not _handler:
            print(
                "Deleting %s from group %s"
                % (colorStr(member.email, "blue"), colorStr(self.name, "green"))
            )
            _handler = GCloudHandler()

        try:
            _handler.service.members().delete(
                groupKey=self.groupEmail, memberKey=member.email
            ).execute()
        except HttpError as err:
            if err.error_details[0]["message"] == "Resource Not Found: memberKey":
                print(
                    "\r%s %s %s  %s"
                    % (
                        colorStr("API Warning:", "warning"),
                        colorStr(member.email, "blue"),
                        colorStr("not found in group", "warning"),
                        colorStr(self.name, "green"),
                    ),
                    end="",
                )
            else:
                print(
                    "%s"
                    % colorStr(
                        "API Error: %s" & err.error_details[0]["message"], "error"
                    )
                )
                print(
                    "%s %s"
                    % (
                        colorStr("Group key:", "error"),
                        colorStr("%s" % self.groupEmail, "green"),
                    )
                )
                print(
                    "%s %s"
                    % (
                        colorStr("Member key:", "error"),
                        colorStr("%s" % member.email, "blue"),
                    ),
                    end="",
                )
            print()
        return

    def insertMembers(self, members: list[GCloudMember]) -> None:
        handler = GCloudHandler()
        print(
            f"Inserting {colorStr(f'{len(members)}', 'blue')} members to group {colorStr(self.name, 'green')}"
        )
        for member, n in zip(members, range(len(members))):
            print(f"\r  {progressBar(n, len(members), 20)}", end="")
            self.insertMember(member, handler)
        print(f"\r  {progressBar(n + 1, len(members), 20)}")
        print(f"Insertions to group {colorStr(self.name, 'green')} complete\n")
        return

    def deleteMembers(self, members: list[GCloudMember]) -> None:
        handler = GCloudHandler()
        print(
            f"Deleting {colorStr(f'{len(members)}', 'blue')} members from group {colorStr(self.name, 'green')}"
        )
        for member, n in zip(members, range(len(members))):
            print(f"\r  {progressBar(n, len(members), 20)}", end="")
            self.deleteMember(member, handler)
        print(f"\r  {progressBar(n + 1, len(members), 20)}")
        print(f"Deletions from group {colorStr(self.name, 'green')} complete\n")
        return

    def __eq__(self, other):
        return self.groupEmail == other.groupEmail

    def __ne__(self, other):
        return self.groupEmail != other.groupEmail

    def __str__(self):
        return self.groupEmail


class GCloudHandler:
    """
        Class to work with Google Cloud API

        ...

    Attributes
    ----------
    All attributes are intended as private

    Methods
    -------
    getGroups() -> list[GCloudGroup]
        Returns a list of all groups, populated with their members

    getGroup(groupEmail: str) -> GCloudGroup:
        Returns specific group from the groups ID email

    """

    SCOPES: list[str] = [
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/gmail.send",
    ]  # https://developers.google.com/admin-sdk/directory/v1/guides/authorizing < Relevant scopes
    service: any = None
    _creds: any

    # Init made for group manipulation. Refactor if used for other purposes.
    def __init__(self):
        self._creds = service_account.Credentials.from_service_account_file(
            config.SERVICE_ACCOUNT_FILE_PATH, scopes=self.SCOPES
        ).with_subject(config.SUPER_ADMIN)
        self.service = build("admin", "directory_v1", credentials=self._creds)

    def get_group(self, groupEmail: str) -> GCloudGroup:
        """Takes the unique email of a group

        Returns a group populated by its members"""
        try:
            response = self.service.groups().get(groupKey=groupEmail).execute()
            group = GCloudGroup(_response=response)
            group._getMembers(self.service)
            # group._getSettings(self.service)
            return group
        except HttpError as err:
            print("Request failed. Message return from API:")
            print(err.error_details[0]["message"])

    def get_groups(self) -> list[GCloudGroup]:
        """Returns a list of all groups populated by their members"""
        try:
            groupsJSON = (
                self.service.groups().list(domain=config.ROOT_DOMAIN).execute()
            )["groups"]
            groups = [GCloudGroup(_response=groupJSON) for groupJSON in groupsJSON]
            print(
                f"Getting group members from {colorStr(f'{len(groups)}', 'green')} groups"
            )
            for i in range(len(groups)):
                print(f"\r  {progressBar(i, len(groups), 20)}", end="")
                groups[i]._getMembers(self.service)
                # groups[i]._getSettings(self.service)
            print(f"\r  {progressBar(i + 1, len(groups), 20)}")
            totalMembers = sum([len(group.members) for group in groups])
            print(
                f"Collected all {colorStr(f'{totalMembers}', 'blue')} members from {colorStr(f'{len(groups)}', 'green')} groups\n"
            )
            return groups
        except HttpError as err:
            print("Request failed. Message return from API:")
            print(err.error_details[0]["message"])

    def send_email(
        self, to: str, subject: str, message: str, bcc: str, cc: str, reply_to: str
    ):
        service = build("gmail", "v1", credentials=self._creds)

        mail = EmailMessage()
        mail.set_content(message)
        mail["To"] = to
        mail["From"] = (
            config.SUPER_ADMIN
        )  # Gmail overrides "From" field to be superuser anyways
        mail["Subject"] = subject
        if cc:
            mail["CC"] = cc
        if bcc:
            mail["BCC"] = bcc
        if reply_to:
            mail["Reply-To"] = reply_to

        encoded_email = base64.urlsafe_b64encode(mail.as_bytes()).decode()
        encoded_package = {"raw": encoded_email}

        try:
            email_attempt = (
                service.users()
                .messages()
                .send(userId="me", body=encoded_package)
                .execute()
            )
            print("Messafe ID: %s" % email_attempt["id"])
        except HttpError as error:
            print("Error: %s" % error)


if __name__ == "__main__":
    print("∇")

# This library is intended to make the following unnecessary. However, since it took me
#     a while to figure out, here is a summary of how Google's API works.

# Authenitcation is done by connecting the service account set up on the cloud.google.com
#     console and set up with domain-wide authority in on the admin panel. This is what
#     the lines in the GCloudHandler __init__ function
#         creds = (service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE_PATH,
#             scopes = SCOPES
#             ).with_subject(SUPER_ADMIN)
#         )
#     is for. As we are doing sensitive admin work, we need to impersonate a superadmin,
#     which is what .with_subject does.

# This then needs to be built into a service object that actually makes the call. This is
#     done (for the admin SDK API, version 1)
#         service = build("admin", "directory_v1", credentials = creds)

# API calls are done by specifiying which API wr're using, and calling the HTTP request like
#         response = (
#                 service.groups()
#                     .get(groupKey = groupEmail)
#                     .execute()
#                 )
#     Here we use the service object to access the groups API, run a get function giving it
#     what it asks for in the documentation, and actually calling it by .excecute().
