import os

from config import env_config

KALEYRA_URL = os.environ.get("KALEYRA_URL")
APIKEY = os.environ.get("APIKEY")
SMSTYPE = os.environ.get("SMSTYPE")
SENDERID = os.environ.get("SENDERID")


CONTENT_TYPE = os.environ.get("CONTENT_TYPE")
OTPTYPE = os.environ.get("OTPTYPE")
SMS_TEMPLATE_ID = os.environ.get("SMS_TEMPLATE_ID")
OTP_TEMPLATE_ID = os.environ.get("OTP_TEMPLATE_ID")
SID = os.environ.get("SID")
FLOW_ID = os.environ.get("FLOW_ID")
