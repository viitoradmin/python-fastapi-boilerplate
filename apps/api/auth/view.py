from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from apps.constant import constant
from apps.utils.standard_response import StandardResponse

## Load API's
router = InferringRouter()

## Define API's here
@cbv(router)
class UserCrudApi():
    """This class is for user's CRUD operation with version 1 API's"""
    
    @router.get('/list/user')
    async def list_user(self):
        """This API is for list user.
        """
        try:
            response = "Hello there, welcome to fastapi bolierplate"
            return response
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)