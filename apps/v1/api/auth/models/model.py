"""This module contains database model implementations."""

from core.utils.helper import DateTimeUtils
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from core.utils import constant_variable as constant
from config.db_config import Base


class Users(Base):
    """
    Table used for stored the users information
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(100), nullable=False, unique=True, doc="unique_id")
    first_name = Column(String(255), doc="First name of user", nullable=True)
    last_name = Column(String(255), doc="Last name of user", nullable=True)
    email = Column(String(100), doc="Email ID of the user", nullable=True)
    username = Column(String(100), doc="Username of the user", nullable=True)
    password = Column(String(100), doc="Password of the user", nullable=True)
    created_at = Column(
        DateTime,
        default=DateTimeUtils().get_time,
        nullable=False,
        doc="its generate automatically when data create",
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=DateTimeUtils().get_time,
        doc="its generate automatically when data update",
    )
    deleted_at = Column(
        DateTime, nullable=True, doc="its generate automatically when data deleted"
    )


class UserSocialLogin(Base):
    """
    Table used for stored the users social login information
    """

    __tablename__ = "users_social_login"

    id = Column(
        Integer, primary_key=constant.STATUS_TRUE, nullable=constant.STATUS_FALSE
    )
    uuid = Column(
        String(100),
        nullable=constant.STATUS_FALSE,
        unique=constant.STATUS_TRUE,
        doc="unique_id",
    )
    user_uuid = Column(String(100), ForeignKey("users.uuid", ondelete="CASCADE"))
    provider = Column(
        String(50), doc="social login provider name", nullable=constant.STATUS_TRUE
    )
    provider_token = Column(
        String(255), doc="social login provider token", nullable=constant.STATUS_TRUE
    )
    status = Column(
        Boolean,
        default=constant.STATUS_TRUE,
        doc="This flag is define userlogin active or not active",
    )
    created_at = Column(
        DateTime,
        nullable=constant.STATUS_FALSE,
        default=DateTimeUtils().get_time,
        doc="its generate automatically when userlogin create",
    )
    updated_at = Column(
        DateTime,
        nullable=constant.STATUS_TRUE,
        default=DateTimeUtils().get_time,
        onupdate=DateTimeUtils().get_time,
        doc="its generate automatically when userlogin update",
    )
    deleted_at = Column(
        DateTime,
        nullable=constant.STATUS_TRUE,
        doc="its generate automatically when userlogin deleted",
    )
