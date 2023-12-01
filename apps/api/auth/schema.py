"""This module is for swager and request parameter schema"""
from pydantic import BaseModel, Extra, validator, Field
from apps.api.core import validation


class UserAuth(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    password: str 
    username: str 

    class Config:
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
    
    @validator('first_name', pre=True)
    def first_name_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'first_name')
    
    @validator('last_name', allow_reuse=True)
    def last_name_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'last_name')
    
    @validator('email', allow_reuse=True)
    def email_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'email')
    
    @validator('username', allow_reuse=True)
    def username_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'username')
    
    @validator('email', allow_reuse=True)
    def email_field_validator(cls, v):
        return validation.ValidationMethods().email_validator(v)