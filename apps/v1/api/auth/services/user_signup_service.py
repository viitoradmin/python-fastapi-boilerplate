import uuid
import bcrypt
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils import db_method, constant_variable, message_variable
from core.utils.standard_response import StandardResponse


class UserAuthService:
    """This class represents the user creation service"""

    async def signup_user_service(self, db: AsyncSession, body):
        try:
            body = body.dict()
            # Check body's Email already exist
            user_auth_method = UserAuthMethod(Users)
            if user_object := await user_auth_method.find_by_email(db, body["email"]):
                return StandardResponse(
                    False,
                    status.HTTP_400_BAD_REQUEST,
                    constant_variable.STATUS_NULL,
                    message_variable.EMAIL_ALLREADY_EXISTS,
                ).make

            # For password hashing
            hashed_password = bcrypt.hashpw(
                body["password"].encode("utf-8"), bcrypt.gensalt()
            )

            body["password"] = hashed_password
            body["uuid"] = uuid.uuid4()
            # Add the body into the database
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
