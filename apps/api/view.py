from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
from apps.constant import constant
from fastapi_versioning import version
from apps.utils.standard_response import StandardResponse

## Load API's
defaultrouter = APIRouter()
router = APIRouter()

## Define verison 1 API's here
@cbv(defaultrouter)
class UserCrudApi():
    """This class is for user's CRUD operation with version 1 API's"""
    
    @defaultrouter.get('/list/user')
    @version(1)
    async def list_user(self):
        """This API is for list user.
        Args: None
        Returns: 
            response: will return list."""
        try:
            data = {"List:" : "Hello there, welcome to fastapi bolierplate"}
            return StandardResponse(True, status.HTTP_200_OK, data, constant.STATUS_SUCCESS)
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)
    
    @defaultrouter.post('/create/user')
    @version(1)
    async def create_user(self):
        """This API is for create user.
        Args: 
            body(dict) : user's data
        Returns:
            response: will return the user's data"""
        try:
            data = {"user": "user's data"}
            return StandardResponse(True, status.HTTP_200_OK, data, constant.STATUS_SUCCESS)
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)


## Define version 2 API's here
@cbv(router)
class UserVersionApi():
    @router.get("/list")
    @version(2)
    async def get_list(self):
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