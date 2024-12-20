from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils import constant_variable as constant
from core.utils import db_method, message_variable
from core.utils.standard_response import StandardResponse


class EmailVerificationService:

    def user_verification_service(self, db: AsyncSession, body: dict):
        """
        TODO: Impliment verification Logic as per requirement
        """
        try:
            body = body.dict()
            otp_referenceId = body["otp_referenceId"]
            otp = body["otp"]
            password = body["password"]

            # Get the user
            if not (
                user_object := UserAuthMethod(Users).find_user_by_otp_referenceId(
                    db, otp_referenceId
                )
            ):
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.ERROR_USER_NOT_FOUND,
                ).make

            user_data = jsonable_encoder(user_object)
            if user_data["otp_referenceId"] != otp_referenceId:
                return StandardResponse(
                    status.HTTP_400_BAD_REQUEST,
                    constant.STATUS_NULL,
                    message_variable.INVALID_OTP,
                ).make

            data = {}
            db.commit()  # Commit the transaction
            return StandardResponse(
                status.HTTP_200_OK, data, message_variable.SUCCESS_USER_VERIFIED
            ).make
        except Exception as e:
            return StandardResponse(
                status.HTTP_400_BAD_REQUEST,
                constant.STATUS_NULL,
                message_variable.SOMETHING_WENT_WRONG,
            ).make
