import bcrypt
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils.token_authentication import JWTOAuth2
from core.utils import constant_variable, message_variable
from core.utils.standard_response import StandardResponse


class LoginService:

    async def login_user_service(self, db: AsyncSession, body):
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
            if not bcrypt.checkpw(
                body.password.encode("utf-8"), user_object.password.encode("utf-8")
            ):
                return StandardResponse(
                    False,
                    status.HTTP_400_BAD_REQUEST,
                    constant_variable.STATUS_NULL,
                    message_variable.INVALID_USER_CREDENTIAL,
                ).make

            # generate token
            access_token = JWTOAuth2().encode_access_token(
                identity=user_object.email
                # identity={
                #     "email": user_object.email,
                #     "id": user_object.id,
                #     "user_type": "user",
                # }
            )
            user_data = jsonable_encoder(user_object)
            user_data["access_token"] = access_token
            del user_data["password"]
            db.commit()  # Commit the transaction
            return StandardResponse(
                True,
                status.HTTP_200_OK,
                data=user_data,
                message=message_variable.SUCCESS_USER_LOGIN,
            ).make
        except Exception as e:
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                constant_variable.STATUS_NULL,
                message_variable.GENERAL_TRY_AGAIN,
            )
