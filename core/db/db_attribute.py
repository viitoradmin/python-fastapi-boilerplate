from enum import Enum

from core.utils import constant_variable as constant


class BaseAttributes(Enum):
    @classmethod
    def fetch_dict(cls):
        user_status_dict = {i.name: i.value for i in cls}
        return user_status_dict

    @classmethod
    def fetch_by_name(cls, name):
        return cls[name].value

    @classmethod
    def fetch_by_id(cls, id: int):
        if user_status := [i.name for i in cls if i.value == id]:
            return user_status[0]
        return constant.STATUS_NULL


class Status(BaseAttributes):
    inactive = constant.STATUS_ZERO
    active = constant.STATUS_ONE
