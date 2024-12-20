"""This module is for swager and request parameter schema"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from core.utils import constant_variable as constant
from core.utils.validation import ValidationMethods


class CreateUser(BaseModel):
    """This class is for user schema."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    username: str

    class Config:
        """This class is the schema for user configuration."""

        from_attributes = constant.STATUS_TRUE
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Smith",
                "email": "johnsmith@example.com",
                "password": "Abc@123",
                "username": "John123",
            }
        }

    @field_validator("password")
    def password_validation(cls, v):
        return ValidationMethods().validate_password(v)


class LoginUser(BaseModel):
    """This class is for user schema."""

    email: EmailStr
    password: str

    class Config:
        """This class is the schema for user configuration."""

        from_attributes = constant.STATUS_TRUE
        extra = "forbid"
        json_schema_extra = {
            "example": {"email": "johnsmith@example.com", "password": "Abc@123"}
        }

    @field_validator("password")
    def password_validation(cls, v):
        return ValidationMethods().validate_password(v)


class ForgotPassword(BaseModel):
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=constant.STATUS_TRUE,
        extra="forbid",
        json_schema_extra={
            "example": {
                "email": "johnsmith@gmail.com",
            }
        },
    )


class ResetPassword(BaseModel):
    token: str
    new_password: str
    confirm_password: str

    model_config = ConfigDict(
        from_attributes=constant.STATUS_TRUE,
        extra="forbid",
        json_schema_extra={
            "example": {
                "token": "1234567890",
                "new_password": "Test@123",
                "confirm_password": "Test@123",
            }
        },
    )

    @field_validator("new_password")
    def password_validation(cls, value):
        return ValidationMethods().validate_password(value)

    @field_validator("confirm_password")
    def password_validation(cls, value):
        return ValidationMethods().validate_password(value)


class SocialLogin(BaseModel):
    provider: int
    provider_token: str

    class Config:
        model_config = ConfigDict(
            from_attributes=constant.STATUS_TRUE,
            extra="forbid",
            json_schema_extra={
                "example": {
                    "provider": "1234567890",
                    "provider_token": "Test@123",
                }
            },
        )

    @field_validator("provider_token")
    def provider_token_must_be_required(cls, v):
        return ValidationMethods().not_null_validator(v, "provider_token")


class EmailVerification(BaseModel):
    otp: str
    otp_referenceId: str
    is_exist: bool
    password: str

    class Config:
        model_config = ConfigDict(
            from_attributes=constant.STATUS_TRUE,
            extra="forbid",
            json_schema_extra={
                "example": {
                    "otp": "123456",
                    "otp_referenceId": "123456",
                    "is_exist": True,
                    "password": "Test@123",
                }
            },
        )

    @field_validator("otp")
    def otp_must_be_required(cls, v):
        return ValidationMethods().not_null_validator(v, "otp")

    @field_validator("otp_referenceId")
    def otp_referenceId_must_be_required(cls, v):
        return ValidationMethods().not_null_validator(v, "otp_referenceId")

    @field_validator("password")
    def password_validation(cls, v):
        return ValidationMethods().validate_password(v)


class VerifyOtp(BaseModel):
    user_type: int
    phone_no: str
    otp: str
    is_exist: bool
    password: str
    otp_referenceId: str

    class Config:
        model_config = ConfigDict(
            from_attributes=constant.STATUS_TRUE,
            extra="forbid",
            json_schema_extra={
                "example": {
                    "user_type": "123456",
                    "phone_no": "123456",
                    "otp": "123456",
                    "is_exist": True,
                    "password": "Test@123",
                    "otp_referenceId": "123456",
                }
            },
        )

    @field_validator("otp")
    def otp_must_be_required(cls, v):
        return ValidationMethods().not_null_validator(v, "otp")

    @field_validator("otp_referenceId")
    def otp_referenceId_must_be_required(cls, v):
        return ValidationMethods().not_null_validator(v, "otp_referenceId")

    @field_validator("password")
    def password_validation(cls, v):
        return ValidationMethods().validate_password(v)


class ResendOtp(BaseModel):
    email: Optional[EmailStr] = constant.STATUS_NULL
    country_code: Optional[str] = constant.STATUS_NULL
    phone_no: Optional[str] = constant.STATUS_NULL

    class Config:
        model_config = ConfigDict(
            from_attributes=constant.STATUS_TRUE,
            extra="forbid",
            json_schema_extra={
                "example": {
                    "email": "johnsmith@example.com",
                    "country_code": "+91",
                    "phone_no": "1234567890",
                }
            },
        )


@field_validator("phone_no")
def phone_no_must_be_required(cls, v):
    return ValidationMethods().not_null_validator(v, "phone_no")


@field_validator("country_code")
def country_code_must_be_required(cls, v):
    return ValidationMethods().not_null_validator(v, "country_code")


@field_validator("email")
def email_must_be_required(cls, v):
    return ValidationMethods().not_null_validator(v, "email")
