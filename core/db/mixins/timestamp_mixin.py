from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import DateTimeUtils, constant_variable


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=DateTimeUtils().get_time(),
        nullable=constant_variable.STATUS_FALSE,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=DateTimeUtils().get_time(),
        onupdate=DateTimeUtils().get_time(),
        nullable=constant_variable.STATUS_FALSE,
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=constant_variable.STATUS_TRUE,
    )
