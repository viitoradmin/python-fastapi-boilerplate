import os
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


class OtpVerificationService:
    async def otp_verification_service(self, db: AsyncSession, body: dict):
        try:
            body = body.dict()
            user_type = int(body["user_type"])
            password = body["password"]
            ref_id = str(body["otp_referenceId"])

            if user_type == constant.STATUS_ZERO:
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.ERROR_INVALID_REQUEST_BODY,
                ).make

            phone_no = body["phone_no"]
            otp = str(body["otp"])
            user_object = UserAuthMethod(Users).find_verified_phone_user(
                db, phone_no, user_type
            )

            if not user_object:
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.ERROR_USER_NOT_FOUND,
                ).make

            if (
                user_object.phone_number != os.environ.get("TESTING_MOBILE")
                and otp != os.environ.get("TESTING_OTP")
                and os.environ.get("OTP_LIVE_MODE") == "True"
            ):
                country_code = "+".join(user_object.country_code) or "+91"

                if os.environ.get("MOBILE_OTP_SERVICE") == "KALEYRA":
                    if not (otp_service.OTPUtils().verify_kaleyra_otp(otp, ref_id)):
                        return StandardResponse(
                            status.HTTP_400_BAD_REQUEST,
                            constant.STATUS_NULL,
                            message_variable.ERROR_OTP_VERIFICATION,
                        ).make
                elif os.environ.get("MOBILE_OTP_SERVICE") == "TWILLIO":
                    if not (
                        otp_service.OTPUtils().verify_otp(
                            f"{country_code}{user_object.phone_number}",
                            otp,
                        )
                    ):
                        return StandardResponse(
                            status.HTTP_400_BAD_REQUEST,
                            constant.STATUS_NULL,
                            message_variable.ERROR_OTP_VERIFICATION,
                        ).make
                else:
                    return StandardResponse(
                        status.HTTP_400_BAD_REQUEST,
                        constant.STATUS_NULL,
                        message_variable.ERROR_SMS_SERVICE,
                    ).make

            user_object.password = helper.PasswordUtils().hash_password(password)
            if user_object.verified_at is constant.STATUS_NULL:
                user_object.verified_at = helper.DateTimeUtils().get_time()

            if not (db_method.DataBaseMethod(Users).save(user_object, db)):
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.GENERIC_ERROR,
                ).make

            token = JWTOAuth2().encode_access_token(identity=user_object.email)
            user_data = jsonable_encoder(user_object)
            data = {"data": user_data, "access_token": token["access_token"]}
            db.commit()  # Commit the transaction
            return StandardResponse(
                status.HTTP_200_OK, data, message_variable.SUCCESS_USER_LOGGED_IN
            ).make
        except Exception as e:
            return StandardResponse(
                status.HTTP_400_BAD_REQUEST,
                constant_variable.STATUS_NULL,
                message_variable.GENERAL_TRY_AGAIN,
            ).make
