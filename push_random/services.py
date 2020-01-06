from typing import List

from notifiers import Response, notify

from push_random.db import NotificationRepository
from push_random.models import NotificationSchedule, Notification


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


class NotificationService:
    """
    Класс для работы с уведомлениями: создание/получение расписания уведомлений, создание/планирование/отправка уведомлений
    """

    def __init__(self, repo: NotificationRepository, sender: PushoverNotificationSender) -> None:
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
        pass

    def send_notification(self, notification: Notification) -> None:
        """Отправляет уведомление"""
        self.sender.send(notification.text)

