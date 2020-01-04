import datetime as dt
from typing import Optional

from pydantic import BaseModel


class NotificationSchedule(BaseModel):
    """
    Расписание уведомления
    Пример: присылать 2 раза в день пуш в промежуток от 13 до 01
    >>> NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), times=2)
    """
    id: Optional[int]
    message: str
    from_time: dt.time
    to_time: dt.time
    times: int