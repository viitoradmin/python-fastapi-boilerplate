"""This module is for swager and request parameter schema"""
from pydantic import BaseModel, Extra


class UserAuth(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    username: str

    class Config:
        extra = Extra.forbid
        orm_mode = True
        extra = Extra.allow
        schema_extra = {
            "example": {
                    "first_name": "John",
                    "last_name": "Smith",
                    "email": "jhohnsmith@example.com",
                    "password": "Abc@123",
                    "username": "Jhon123"
                }
        }