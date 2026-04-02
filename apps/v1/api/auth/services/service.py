"""This module contains API's specific functionality."""
import uuid

from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.v1.api.auth.models.methods.method1 import UserAuthMethod
from apps.v1.api.auth.models.model import Users
from core.utils import db_method
from core.utils import ValidationMethods
from apps.constant import constant
from core.utils.message_variable import ErrorMessage, InfoMessage
from core.utils.standard_response import StandardResponse


class UserAuthService:
    """This class represents the user creation service"""
    def create_user_service(self, db: Session, body: dict):
        """This function is used to create user
        Args:
            db (Session): database connection
            body (dict): dictionary to user information data

        Returns:
            response (dict): user object representing the user
        """
        username = body['username']
        email = body['email'] or None
        password = body['password']

        # check Email exists in body or not
        if "email" not in body or not email:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None, ErrorMessage.emailRequired
                )

        # check Email exists in Db or not
        if (user_object := UserAuthMethod(Users).find_by_email(db, email)):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, 
                constant.STATUS_NULL, ErrorMessage.emailAlreadyExist
                ).make

        # For password validation
        if not ValidationMethods().password_validator(password):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                constant.STATUS_NULL, ErrorMessage.invalidPasswordFormat
            ).make

        user_object = Users(
            uuid = uuid.uuid4(),
            first_name=body['first_name'],
            last_name=body['last_name'],
            username=username,
            email=email,
            password=password
        )

        # Store user object in database
        if not(db_method.BaseMethods(Users).save(user_object, db)):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, 
                constant.STATUS_NULL, ErrorMessage.userNotSaved
            )

        # check email exists or not
        if user_object := UserAuthMethod(Users).find_by_email(db, email):
            data = {
                "username": user_object.username,
                "first_name": user_object.first_name,
                "last_name": user_object.last_name,
                "email": user_object.email,
                "password": user_object.password,
            }

        else:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, 
                constant.STATUS_NULL, ErrorMessage.userInvalid
            ).make

        return StandardResponse(
            True, status.HTTP_200_OK, data, InfoMessage.userCreated
        ).make

    def get_user_service(self, db):
        """This function returns the user service list."""
        if not (user_object := db_method.BaseMethods(Users).find_by_uuid(db)):
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                ErrorMessage.userNotFound
            )
        # convert the object data into json
        user_data = jsonable_encoder(user_object)

        return StandardResponse(
            True,
            status.HTTP_200_OK,
            user_data,
            InfoMessage.retriveInfoSuccessfully
        )
