from io import BytesIO
from typing import Union

from fastapi import BackgroundTasks, UploadFile
from fastapi_mail import FastMail, MessageSchema, MessageType

from config import mail_config


class EmailService:

    def send_email_service(
        self,
        subject: str,
        email_to: Union[str, list[str]],
        body: dict,
        html_file,
        background_tasks: BackgroundTasks,
        attachment: list = [],
        email_cc: Union[str, list[str]] = "",
    ):
        """
        Sends an email with attachments in the background using the provided `background_tasks` object.

        Args:
            background_tasks (BackgroundTasks): The object used to add tasks to the background.
            subject (str): The subject of the email.
            email_to (str): The recipient of the email.
            body (dict): The body of the email.
            attachment (list): A list of file paths representing the attachments.
            html_file (str): The file containing the HTML template for the email.
            email_cc (str, optional): The CC recipients of the email. Defaults to None.

        Returns:
            None
        """
        attachment_file = []
        for attach in attachment:
            file_name = attach.split("/")[-1]
            with open(attach, "rb") as fil:
                fil = BytesIO(fil.read())
                attachment_file.append(UploadFile(filename=file_name, file=fil))

        email_to = self.prepare_email_list(email_to) or []
        email_cc = self.prepare_email_list(email_cc) or []

        message = MessageSchema(
            subject=subject,
            recipients=email_to,
            cc=email_cc,
            template_body=body,
            subtype=MessageType.html,
            attachments=attachment_file,
        )
        fm = FastMail(mail_config.conf)
        background_tasks.add_task(fm.send_message, message, template_name=html_file)

    def prepare_email_list(self, emails: Union[str, list[str]]) -> list:
        """
        Prepare a list of email addresses by splitting the input
        string and removing any leading or trailing whitespace.

        Args:
            email (Union[str, list[str]]): email addresses.

        Returns:
            list: A list of EmailStr objects representing the email addresses.
        """
        if isinstance(emails, str):
            emails = emails.split(",")
        return [email.strip() for email in emails]
