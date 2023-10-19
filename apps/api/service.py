from apps.utils.standard_response import StandardResponse
from fastapi import status
from apps.constant import constant

def get_str_name(name: str):
    if name is not None:
        return StandardResponse(
            True, status.HTTP_200_OK, {"success": "Welcome"}, 
            constant.STATUS_SUCCESS
            )
    else:
        return StandardResponse(
            True, status.HTTP_400_BAD_REQUEST, {"success": "Error"}, 
            constant.STATUS_ERROR
            )