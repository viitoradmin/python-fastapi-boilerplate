from fastapi_utils.inferring_router import InferringRouter
from fastapi_versioning import version
from fastapi_utils.cbv import cbv
from apps.utils.standard_response import StandardResponse
from fastapi import status
from apps.constant import constant

authrouter = InferringRouter()


@cbv(authrouter)
class APIView():
    @authrouter.get("/list")
    @version(2)
    def get_list(self):
        try:
            response = { "data": "User's list data" }
            return StandardResponse(True, status.HTTP_200_OK, response, constant.STATUS_SUCCESS)
        except Exception as e:
            return StandardResponse(False, status.HTTP_400_BAD_REQUEST, None, constant.ERROR_MSG)