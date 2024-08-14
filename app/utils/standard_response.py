from fastapi.responses import JSONResponse
from typing import Union, Dict, List


class StandardResponse:
    """A class to encapsulate the standard API response format.

    Attributes:
        status (str): The status indicating success or failure.
        status_code (int): The HTTP status code for the response.
        data (Union[Dict, List]): The data returned by the API.
        message (str): The message accompanying the API response.
    """

    def __init__(self, status: str, status_code: int, data: Union[Dict, List], message: str) -> None:
        """Initializes a StandardResponse instance.

        Args:
            status (str): The status indicating success or failure.
            status_code (int): The HTTP status code for the response.
            data (Union[Dict, List]): The data returned by the API.
            message (str): The message accompanying the API response.
        """
        self._status = status
        self._status_code = status_code
        self._data = data
        self._message = message

    def to_dict(self) -> Dict[str, Union[str, Dict, List]]:
        """Converts the response object to a dictionary.

        Returns:
            Dict[str, Union[str, Dict, List]]: The response formatted as a dictionary.
        """
        return {
            'status': self._status,
            'data': self._data,
            'message': self._message
        }

    def to_json_response(self) -> JSONResponse:
        """Generates a JSONResponse from the response data.

        Returns:
            JSONResponse: A FastAPI JSONResponse containing the status, data, and message.
        """
        return JSONResponse(content=self.to_dict(), status_code=self._status_code)
