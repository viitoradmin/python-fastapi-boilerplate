"""This module is responsible to contain API's endpoint"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.v1.api.auth import schema
from apps.v1.api.auth.service import UserAuthService
from apps.constant import constant
from core.utils.standard_response import StandardResponse
from config import db_config

## Load API's
router = APIRouter()
getdb = db_config.get_db

## Define verison 1 API's here
class UserCrudApi():
    """This class is for user's CRUD operation with version 1 API's"""
    @router.get('/users')
    async def list_user(db: Session = Depends(getdb)):
        """This API is for list user.
        Args: None
        Returns: 
            response: will return users list."""
        try:
            response = UserAuthService().get_user_service(db)
            return response
        except Exception:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)

    @router.post('/create/user')
    async def create_user(body: schema.UserAuth,
                          db: Session = Depends(getdb)):
        """This API is for create user.
        Args: 
            body(dict) : user's data
        Returns:
            response: will return the user's data"""
        try:
            # as per pydantic version 2.
            body = body.model_dump()
            response = UserAuthService().create_user_service(db, body)
            return response
        except Exception:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)