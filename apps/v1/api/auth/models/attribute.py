from core.db.db_attribute import BaseAttributes
from core.utils import constant_variable as constant


class SsoType(BaseAttributes):
    google = constant.STATUS_ONE
    facebook = constant.STATUS_TWO
    apple = constant.STATUS_THREE
