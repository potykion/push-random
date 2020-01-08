import datetime as dt
import json
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class FromJsonStringMixin(BaseModel):
    @classmethod
    def from_json_str(cls, json_str: str) -> T:
        return cls(**json.loads(json_str))


class NotificationSchedule(FromJsonStringMixin):
    """
    Расписание уведомления
    Пример: присылать 2 раза в день пуш в промежуток от 13 до 01
    >>> NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    """
    message: str
    from_time: dt.time
    to_time: dt.time
    freq: int


class Notification(FromJsonStringMixin):
    """
    Уведомление
    Пример: прислать уведомление с текстом "test" 2020-01-06 в 14:49
    >>> Notification(text="test", datetime=dt.datetime(2020, 1, 6, 14, 49))
    """
    text: str
    datetime: dt.datetime
