from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
from apps.constant import constant
from fastapi_versioning import version
from fastapi_utils.inferring_router import InferringRouter
from apps.utils.standard_response import StandardResponse

## Load API's
defaultrouter = APIRouter()

## Define API's here
@cbv(defaultrouter)
class UserCrudApi():
    """This class is for user's CRUD operation with version 1 API's"""
    
    @defaultrouter.get('/v1/list/user')
    @version(1)
    async def list_user(self):
        """This API is for list user.
        """
        try:
            data = "Hello there, welcome to fastapi bolierplate"
            return data
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)
    
    @defaultrouter.post('/v1/create/user')
    @version(1)
    async def list_user(self):
        """This API is for list user.
        """
        try:
            data = "Hello there, welcome to fastapi bolierplate"
            return data
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)
        
    @defaultrouter.get("/v2/list")
    @version(2)
    async def get_list(self):
        try:
            response = { "data": "User's list data" }
            return StandardResponse(True, status.HTTP_200_OK, response, constant.STATUS_SUCCESS)
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)