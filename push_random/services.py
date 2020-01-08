import random
from typing import List
from typing_extensions import Protocol
import datetime as dt

from notifiers import Response, notify

from push_random.db import NotificationRepository
from push_random.models import NotificationSchedule, Notification


class NotificationSender(Protocol):
    def send(self, message: str) -> bool:
        ...


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


class FakeNotificationSender:
    """Класс для отправки фейковых уведомлений"""

    def send(self, message: str) -> bool:
        return True


class NotificationService:
    """
    Класс для работы с уведомлениями: создание/получение расписания уведомлений, создание/планирование/отправка уведомлений
    """

    def __init__(self, repo: NotificationRepository, sender: NotificationSender) -> None:
        self.repo = repo
        self.sender = sender

    def create_schedule(self, sch: NotificationSchedule) -> None:
        """Создает расписание уведомления"""
        self.repo.insert_schedule(sch)

    def get_schedules(self) -> List[NotificationSchedule]:
        """Получает все расписания уведомлений"""
        return self.repo.get_schedules()

    def create_notifications(self, sch: NotificationSchedule) -> List[Notification]:
        """По расписанию создает рандомные уведомления и сует в очередь задач"""
        # считаем диапазон, в котором будем отправлять уведомления
        datetime_diff = (sch.to_datetime - sch.from_datetime).total_seconds()
        # создаем даты, в которые будет отправлять уведомления
        notification_datetimes = [
            sch.from_datetime + dt.timedelta(seconds=random.randint(0, datetime_diff))
            for _ in range(sch.freq)
        ]
        # создаем уведомления
        notifications = [
            Notification(message=sch.message, sending_dt=datetime)
            for datetime in notification_datetimes
        ]
        # суем все это в редиску
        self.repo.insert_notifications(notifications)

        return notifications

    def send_notification(self, notification: Notification) -> None:
        """Отправляет уведомление"""
        self.sender.send(notification.message)
