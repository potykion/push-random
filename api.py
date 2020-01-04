import os
import datetime as dt
from typing import Optional

from dotenv import load_dotenv
from notifiers import notify, Response
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


class PushoverNotificationSender:
    """
    Класс для отправки уведомлений с помощью Pushover
    https://pushover.net/
    https://github.com/notifiers/notifiers
    """

    def __init__(self, user: str, token: str) -> None:
        self.service = 'pushover'
        self.user = user
        self.token = token

    def send(self, message: str) -> bool:
        res: Response = notify(self.service, user=self.user, token=self.token, message=message)
        return res.ok


def main() -> None:
    load_dotenv()
    PUSHOVER_USER = os.environ["PUSHOVER_USER"]
    PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

    sender = PushoverNotificationSender(PUSHOVER_USER, PUSHOVER_TOKEN)
    message = 'test'
    sender.send(message)

    # todo уведомления:


if __name__ == '__main__':
    main()
