import json
import pyotp
import requests
from twilio.rest import Client

from core.utils import constant_variable as constant
from config import env_config, kaleyra_config, twilio_config


class OTPUtils:
    def send_otp(self, data: str, channel_name: str):
        try:
            # Send the OTP via channel name SMS/Email
            client = Client(
                twilio_config.TWILIO_ACCOUNT_SID, twilio_config.TWILIO_AUTH_TOKEN
            )

            verification = client.verify.v2.services(
                twilio_config.TWILIO_SERVICE_SID
            ).verifications.create(to=data, channel=channel_name)
            return constant.STATUS_TRUE
        except Exception as e:
            print("TWILIO error", e)
            return constant.STATUS_FALSE

    def verify_otp(self, data: str, otp: str):
        try:
            # Verify OTP
            client = Client(
                twilio_config.TWILIO_ACCOUNT_SID, twilio_config.TWILIO_AUTH_TOKEN
            )

            verification_check = client.verify.v2.services(
                twilio_config.TWILIO_SERVICE_SID
            ).verification_checks.create(to=data, code=otp)
            if verification_check.status != "approved":
                return constant.STATUS_FALSE
            return constant.STATUS_TRUE
        except Exception as e:
            print("TWILIO error", e)
            return constant.STATUS_FALSE

    def generate_otp_kaleyra(self, data: str):
        try:
            url = f"{kaleyra_config.KALEYRA_URL}v1/{kaleyra_config.SID}/verify"
            headers = {
                "Content-Type": kaleyra_config.CONTENT_TYPE,
                "api-key": kaleyra_config.APIKEY,
            }
            payload = json.dumps(
                {"flow_id": kaleyra_config.FLOW_ID, "to": {"mobile": data}}
            )
            response = requests.request("POST", url, headers=headers, data=payload)
            otp_data = response.json()
            if response.status_code not in [
                constant.STATUS_CODE_202,
                constant.STATUS_CODE_200,
            ]:
                return constant.STATUS_FALSE
            return otp_data
        except Exception as e:
            print("KALEYRA error", e)
            return constant.STATUS_FALSE

    def verify_kaleyra_otp(self, otp: str, ref_id: str):
        try:
            url = f"{kaleyra_config.KALEYRA_URL}v1/{kaleyra_config.SID}/verify/validate"
            headers = {
                "Content-Type": kaleyra_config.CONTENT_TYPE,
                "api-key": kaleyra_config.APIKEY,
            }
            payload = json.dumps({"verify_id": ref_id, "otp": otp})
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code not in [
                constant.STATUS_CODE_202,
                constant.STATUS_CODE_200,
            ]:
                return constant.STATUS_FALSE
            return constant.STATUS_TRUE
        except Exception as e:
            print("KALEYRA error", e)
            return constant.STATUS_FALSE


class EmailOTPUtils:
    def generate_otp(self, otp_referenceId):
        try:
            secret_key = otp_referenceId
            totp = pyotp.TOTP(secret_key, digits=constant.STATUS_SIX, interval=120)
            return totp.now()
        except Exception:
            return constant.STATUS_NULL

    def verify_otp(self, otp: str, otp_referenceId: str):
        try:
            # Verify OTP
            secret_key = otp_referenceId
            totp = pyotp.TOTP(secret_key, digits=constant.STATUS_SIX, interval=120)
            return totp.verify(otp)
        except Exception:
            return constant.STATUS_FALSE
