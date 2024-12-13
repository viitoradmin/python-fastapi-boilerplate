"""This module is for swager and request parameter schema"""
from pydantic import BaseModel


class UserAuth(BaseModel):
    """This class is for user schema."""
    first_name: str
    last_name: str
    email: str
    password: str
    username: str

    class Config:
        """This class is the schema for user configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "first_name": "John",
                    "last_name": "Smith",
                    "email": "jhohnsmith@example.com",
                    "password": "Abc@123",
                    "username": "Jhon123"
                }
        }
