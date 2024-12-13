from fastapi.responses import JSONResponse

from core.utils import constant_variable


class StandardResponse:
    """This class is universal to return standard API responses

    Attributes:
        status (int): The http status response from API
        data (dict/list): The Data from API
        message (str): The message from the API
    """

    def __init__(
        self,
        status,
        status_code: int,
        data: dict,
        message: str,
        cookies: dict = {},
    ) -> None:
        """This function defines arguments that are used in the class

        Arguments:
            status (str): The success/failure status.
            status_code (int): The http status response from API
            data (dict/list): The Data from API
            message (str): The message from the API

        Returns:
            Returns the API standard response
        """
        self.status = status
        self.status_code = status_code
        self.data = data
        self.message = message
        self.cookies = cookies or {}

    @property
    def make(self) -> JSONResponse:
        self.status = (
            constant_variable.STATUS_SUCCESS
            if self.status_code in [201, 200]
            else constant_variable.STATUS_FAIL
        )
        content = {"status": self.status, "data": self.data, "message": self.message}
        response = JSONResponse(content=content, status_code=self.status_code)

        # Set cookies
        for key, value in self.cookies.items():
            response.set_cookie(
                key=key,
                value=value["value"],
                httponly=value.get("httponly", constant_variable.STATUS_TRUE),
                secure=value.get("secure", constant_variable.STATUS_TRUE),
                samesite=value.get("samesite", "Strict"),
                max_age=value.get("max_age"),  # Optional expiration
            )
        return response
