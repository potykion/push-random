import datetime as dt

from pydantic import BaseModel


class NotificationSchedule(BaseModel):
    """
    Расписание уведомления
    Пример: присылать 2 раза в день пуш в промежуток от 13 до 01
    >>> NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), times=2)
    """
    message: str
    from_time: dt.time
    to_time: dt.time
    times: int


class Notification(BaseModel):
    """
    Уведомление
    Пример: прислать уведомление с текстом "test" 2020-01-06 в 14:49
    >>> Notification(text="test", datetime=dt.datetime(2020, 1, 6, 14, 49))
    """
    text: str
    datetime: dt.datetime
