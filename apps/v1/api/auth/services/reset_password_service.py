import bcrypt
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils.token_authentication import JWTOAuth2
from core.utils import db_method, constant_variable, message_variable
from core.utils.standard_response import StandardResponse


class ResetPasswordService:
    async def reset_password_service(self, db: AsyncSession, body):
        try:
            decoded_token = JWTOAuth2().decode_reset_password_token(body.token)
            user_auth_method = UserAuthMethod(Users)
            user_object = await user_auth_method.find_by_email(
                db, decoded_token.get("receiver_email")
            )
            if not user_object:
                return StandardResponse(
                    False,
                    status.HTTP_400_BAD_REQUEST,
                    constant_variable.STATUS_NULL,
                    message_variable.INVALID_USER_CREDENTIAL,
                ).make

            # Check if new password and confirm password match
            if body.new_password != body.confirm_password:
                return StandardResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    message=message_variable.ERROR_PASSWORD_MISMATCH,
                ).make

            hashed_password = bcrypt.hashpw(
                body.new_password.encode("utf-8"), bcrypt.gensalt()
            )
            body = body.dict()
            body["password"] = hashed_password
            user_object = Users(**body)
            if not (
                client_save := await db_method.DataBaseMethod(Users).save(
                    user_object, db
                )
            ):
                return StandardResponse(
                    False,
                    status.HTTP_400_BAD_REQUEST,
                    constant_variable.STATUS_NULL,
                    message_variable.GENERIC_ERROR,
                ).make
            user_data = jsonable_encoder(user_object)
            del user_data["password"]
            db.commit()  # Commit the transaction
            if client_save is not None:
                return StandardResponse(
                    True,
                    status.HTTP_201_CREATED,
                    data=user_data,
                    message=message_variable.SUCCESS_USER_CREATE,
                ).make
        except Exception as e:
            return StandardResponse(
                status.HTTP_400_BAD_REQUEST,
                constant_variable.STATUS_NULL,
                message_variable.GENERAL_TRY_AGAIN,
            ).make
