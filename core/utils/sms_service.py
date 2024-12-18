import os
import json
import requests
from twilio.rest import Client

from core.utils import constant_variable as constant
from config import kaleyra_config, twilio_config


class SendSMS:
    def send_sms_twilio(self, phone_number, message, subject):
        """Publishes a text message directly to a phone number without need for a
        subscription.
        :param phone_number: The phone number that receives the message. This must be in E.164 format.
        For example, a United States phonenumber might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        client = Client(
            twilio_config.TWILIO_ACCOUNT_SID, twilio_config.TWILIO_AUTH_TOKEN
        )

        try:
            response = client.messages.create(
                messaging_service_sid=twilio_config.TWILIO_SIMPLE_MESSAGE_SERVICE_SID,
                body=message,
                to=phone_number,
            )
            message_id = response.sid
            # logger.info("Published message to %s.", phone_number)
        except Exception as e:
            print("TWILIO error", e)
            return False
        else:
            return message_id

    def send_sms_Kaleyra(self, phone_number: str, ticket_link: str):
        try:
            origin_url = f"{kaleyra_config.KALEYRA_URL}v1/{kaleyra_config.SID}/messages"
            headers = {
                "channel": "SMS",
                "api-key": kaleyra_config.APIKEY,
                "Content-Type": kaleyra_config.CONTENT_TYPE,
            }
            slug = os.environ.get("BUSINESS_SLUG")
            payload = json.dumps(
                {
                    "to": phone_number,
                    "sender": kaleyra_config.SENDERID,
                    "type": kaleyra_config.SMSTYPE,
                    "body": f"EveryTicket: Thank you for purchase at {slug}, "
                    + "Use link {url} to get digital tickets! -VIITORCLOUD.",
                    "url_data": {
                        "shorten_url": constant.STATUS_ONE,
                        "url": ticket_link,
                        "track_user": constant.STATUS_ONE,
                    },
                }
            )
            response = requests.request(
                "POST", origin_url, headers=headers, data=payload
            )
            response_content = response.json()
            response_id = response_content.get("id")
            if response.status_code not in [
                constant.STATUS_CODE_202,
                constant.STATUS_CODE_200,
            ]:
                return constant.STATUS_FALSE
            return response_id
        except Exception as e:
            print("KALEYRA error", e)
            return constant.STATUS_FALSE
