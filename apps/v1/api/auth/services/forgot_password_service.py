from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils.token_authentication import JWTOAuth2
from core.utils import constant_variable, message_variable
from core.utils.standard_response import StandardResponse


class ForgotPasswordService:

    async def forgot_password_service(self, db: AsyncSession, body):
        try:
            user_auth_method = UserAuthMethod(Users)
            user_object = await user_auth_method.find_by_email(db, body.email)
            if not user_object:
                return StandardResponse(
                    False,
                    status.HTTP_400_BAD_REQUEST,
                    constant_variable.STATUS_NULL,
                    message_variable.INVALID_USER_CREDENTIAL,
                ).make
            reset_link = JWTOAuth2().encode_reset_password_link(body.email)
            db.commit()  # Commit the transaction
            return StandardResponse(
                True,
                status.HTTP_200_OK,
                data=reset_link,
                message=message_variable.SUCCESS_RESET_LINK,
            ).make
        except Exception as e:
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                constant_variable.STATUS_NULL,
                message_variable.GENERAL_TRY_AGAIN,
            )
