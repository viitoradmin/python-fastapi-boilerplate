import os

from config import env_config

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SERVICE_SID = os.environ.get("TWILIO_SERVICE_SID")
TWILIO_SIMPLE_MESSAGE_SERVICE_SID = os.environ.get("TWILIO_SIMPLE_MESSAGE_SERVICE_SID")