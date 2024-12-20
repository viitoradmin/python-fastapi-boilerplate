import os
import pyotp
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.token_authentication import JWTOAuth2
from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils import constant_variable as constant
from core.utils import (
    db_method,
    constant_variable,
    message_variable,
    helper,
    otp_service,
    sms_service,
)
from core.utils.standard_response import StandardResponse


class ResendOTPService:

    async def otp_resend_service(self, db: AsyncSession, body: dict):
        try:
            body = body.dict()
            response = {}
            if "email" in body and body["email"]:
                email = body["email"]
                user_object = UserAuthMethod(Users).find_verified_email_user(db, email)

                if not user_object:
                    return StandardResponse(
                        status.HTTP_400_BAD_REQUEST,
                        constant.STATUS_NULL,
                        message_variable.ERROR_USER_NOT_FOUND,
                    ).make

                channel_name = constant.EMAIL_CHANNEL
                otp_source = email
                user_object.otp_referenceId = pyotp.random_base32()
                response["email"] = body["email"]
                response["otp_referenceId"] = user_object.otp_referenceId
            elif ("phone_no" in body and body["phone_no"]) and (
                "country_code" in body and body["country_code"]
            ):
                phone_no = body["phone_no"]
                user_object = UserAuthMethod(Users).find_verified_phone_user(
                    db, phone_no
                )

                if not user_object:
                    return StandardResponse(
                        status.HTTP_400_BAD_REQUEST,
                        constant.STATUS_NULL,
                        message_variable.ERROR_USER_NOT_FOUND,
                    ).make

                channel_name = constant.SMS_CHANNEL
                country_code = body["country_code"] or "+91"
                response["phone_no"] = phone_no
                response["country_code"] = country_code
                otp_source = f"{country_code}{phone_no}"
            else:
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.ERROR_INVALID_REQUEST_BODY,
                ).make

            # OTP generate
            if os.environ.get("OTP_LIVE_MODE") == "True":
                if (
                    os.environ.get("MOBILE_OTP_SERVICE") == "KALEYRA"
                    and channel_name == constant.SMS_CHANNEL
                ):
                    if not (
                        otp_send_status := otp_service.OTPUtils().generate_otp_kaleyra(
                            otp_source
                        )
                    ):
                        return StandardResponse(
                            status.HTTP_400_BAD_REQUEST,
                            constant.STATUS_NULL,
                            message_variable.ERROR_OTP_SEND,
                        ).make
                    otp_referenceId = otp_send_status["data"]["verify_id"]
                    user_object.otp_referenceId = otp_referenceId
                    response["otp_referenceId"] = otp_referenceId
                elif (os.environ.get("MOBILE_OTP_SERVICE") == "TWILLIO") or (
                    os.environ.get("EMAIL_OTP_SERVICE") == "TWILLIO"
                    and channel_name == constant.EMAIL_CHANNEL
                ):
                    if not (
                        otp_send_status := otp_service.OTPUtils().send_otp(
                            otp_source, channel_name
                        )
                    ):
                        return StandardResponse(
                            status.HTTP_400_BAD_REQUEST,
                            constant.STATUS_NULL,
                            message_variable.ERROR_OTP_SEND,
                        ).make
                else:
                    return StandardResponse(
                        status.HTTP_400_BAD_REQUEST,
                        constant.STATUS_NULL,
                        message_variable.ERROR_SMS_SERVICE,
                    ).make

            # save user data
            if not (db_method.DataBaseMethod(Users).save(user_object, db)):
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.GENERIC_ERROR,
                ).make
            db.commit()  # Commit the transaction
            return StandardResponse(
                status.HTTP_200_OK, response, message_variable.SUCCESS_OTP_SENT
            ).make
        except Exception as e:
            return StandardResponse(
                status.HTTP_400_BAD_REQUEST,
                constant.STATUS_NULL,
                message_variable.GENERAL_TRY_AGAIN,
            ).make
