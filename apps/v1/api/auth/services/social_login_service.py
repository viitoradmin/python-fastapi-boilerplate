from fastapi import status
from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.token_authentication import JWTOAuth2
from core.utils import constant_variable, message_variable
from core.utils.standard_response import StandardResponse
from config import social_login
from apps.v1.api.auth.models.attribute import SsoType


class SsologinService:
    """This class represents the user creation service"""

    def get_google_account(self, access_token: str):
        """
        This function is used to get the user's facebook profile.
        Args:
            access_token(str): This is the token of user's
                                to fetch the data from facebook.

        return:
            dict: It returns the user's profile information like,
                    email, full_name, etc,.
        """
        try:
            # Specify the CLIENT_ID of the app that accesses the backend
            profile = id_token.verify_oauth2_token(
                access_token, requests.Request(), social_login.GOOGLE_CLIENT_ID
            )
            return profile

        except Exception as e:
            profile = constant_variable.STATUS_NULL

    async def sso_login_user_service(self, db: AsyncSession, body):
        try:
            body = body.dict()
            # TODO: as per database architecture retrive user object from sso login table
            user_data = {}
            # Login with google
            provider_token = body["provider_token"]
            provider = body["provider"]
            if provider == SsoType.google.value:
                if not (profile := self.get_google_account(provider_token)):
                    return StandardResponse(
                        status.HTTP_400_BAD_REQUEST,
                        constant_variable.STATUS_NULL,
                        message_variable.INVALID_PROVIDER_TOKEN,
                    ).make

                email, full_name = (
                    profile["email"],
                    profile["given_name"],
                )
                provider_unique_id = profile["sub"]
            access_token = JWTOAuth2().encode_access_token(
                identity={
                    "email": profile["email"],
                    "id": profile["uuid"],
                    "user_type": "user",
                }
            )
            # user_data = jsonable_encoder(user_object)
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
