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
    Пример: присылать 2 раза в день пуш в промежуток от 13 до 01 (по utc)
    >>> NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    """
    message: str
    from_time: dt.time
    to_time: dt.time
    freq: int

    @property
    def from_datetime(self):
        return (
            dt.datetime.now()
                .replace(
                    hour=self.from_time.hour,
                    minute=self.from_time.minute,
                    second=self.from_time.second,
                    microsecond=self.from_time.microsecond
                )
        )

    @property
    def to_datetime(self):
        delta_days = 1 if self.from_time > self.to_time else 0
        return (
            (dt.datetime.now() + dt.timedelta(delta_days))
                .replace(
                    hour=self.to_time.hour,
                    minute=self.to_time.minute,
                    second=self.to_time.second,
                    microsecond=self.to_time.microsecond
                )
        )


class Notification(FromJsonStringMixin):
    """
    Уведомление
    Пример: прислать уведомление с текстом "test" 2020-01-06 в 14:49
    >>> Notification(message="test", sending_dt=dt.datetime(2020, 1, 6, 14, 49))
    """
    message: str
    sending_dt: dt.datetime
