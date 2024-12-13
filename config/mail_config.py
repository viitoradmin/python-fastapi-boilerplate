import os
import pathlib

from fastapi_mail import ConnectionConfig
from core.utils import constant_variable
from pydantic import SecretStr

from config import project_path


conf = ConnectionConfig(
    MAIL_USERNAME=str(os.environ.get("EMAIL_USERNAME", "")),
    MAIL_PASSWORD=SecretStr(os.environ.get("EMAIL_HOST_PASSWORD", "")),
    MAIL_FROM=str(os.environ.get("DEFAULT_FROM_EMAIL", "")),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_SERVER=str(os.environ.get("EMAIL_HOST", "")),
    MAIL_FROM_NAME=str(os.environ.get("DEFAULT_FROM_EMAIL", "")),
    MAIL_STARTTLS=bool(os.environ.get("MAIL_STARTTLS", constant_variable.STATUS_FALSE)),
    MAIL_SSL_TLS=bool(os.environ.get("MAIL_SSL_TLS", constant_variable.STATUS_FALSE)),
    USE_CREDENTIALS=bool(
        os.environ.get("USE_CREDENTIALS", constant_variable.STATUS_TRUE)
    ),
    TEMPLATE_FOLDER=pathlib.Path(project_path.PROJECT_TEMPLATES_ROOT),
)
