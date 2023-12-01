from fastapi import status
from config import database
from fastapi import Depends
from sqlalchemy.orm import Session
from apps.api.auth import schema
from fastapi import APIRouter
from apps.constant import constant
from fastapi_versioning import version
from apps.api.auth.service import UserAuthService
from apps.utils.standard_response import StandardResponse

## Load API's
router = APIRouter()
router_v1 = APIRouter()
getdb = database.get_db

## Define verison 1 API's here
class UserCrudApi():
    """This class is for user's CRUD operation with version 1 API's"""
    
    @router_v1.get('/users')
    @version(1)
    async def list_user(db: Session = Depends(getdb)):
        """This API is for list user.
        Args: None
        Returns: 
            response: will return users list."""
        try:
            response = UserAuthService().get_user_service(db)
            return response
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)
    
    @router_v1.post('/create/user')
    @version(1)
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
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)


## Define version 2 API's here
router_v2 = APIRouter()

class UserVersionApi():
    """This class provides version 2 API's for users"""
    @router_v2.get("/list")
    @version(2)
    async def get_list():
        """ This API will list version 2 Api's
        Args: None
        Returns:
            response: list 
        """
        try:
            response = { "data": "User's list data" }
            return StandardResponse(True, status.HTTP_200_OK, response, constant.STATUS_SUCCESS)
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)