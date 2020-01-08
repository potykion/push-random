import random
import uuid
from typing import List
import datetime as dt

from notifiers import Response, notify
from redis import Redis
from rq_scheduler import Scheduler
from typing_extensions import Protocol

from push_random.models import NotificationSchedule, Notification


class NotificationScheduleRepository:
    """Класс для работы с хранилищем расписаний уведомлений"""

    SCHEDULE_PREFIX = "sch"

    def __init__(self, redis: Redis):
        self.redis = redis

    def insert_schedule(self, sch: NotificationSchedule) -> None:
        """Сует расписание уведомления в бд"""
        id_ = self._generate_id()
        self.redis.set(id_, sch.json())

    def _generate_id(self, prefix: str = SCHEDULE_PREFIX) -> str:
        """Генерит рандом айди, чекает что айди не занят, возвращает незанятый айди"""
        while True:
            id_ = str(uuid.uuid4())
            if self.redis.get(f"{prefix}-{id}"):
                continue
            else:
                return f"{prefix}-{id_}"

    def get_schedules(self) -> List[NotificationSchedule]:
        """Получает все расписания"""
        keys = self.redis.keys(f"{self.SCHEDULE_PREFIX}-*")
        schedules = [NotificationSchedule.from_json_str(self.redis.get(key)) for key in keys]
        return schedules


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


class NotificationScheduler:
    """Класс для работы с планировщиком уведомлений"""

    def __init__(self, redis: Redis, sender: NotificationSender):
        self.rq_scheduler = Scheduler(connection=redis)
        self.sender = sender

    def schedule(self, notifications) -> None:
        """Планирует уведомления (ставит в очередь)"""
        for notification in notifications:
            self.rq_scheduler.enqueue_at(notification.sending_dt, self.sender.send, notification.message)

    def get_scheduled_notifications(self) -> List[Notification]:
        """Получает список запланированных уведомлений"""
        scheduled = list(self.rq_scheduler.get_jobs())
        return scheduled


class NotificationService:
    """
    Класс для работы с уведомлениями: создание/получение расписания уведомлений, создание/планирование/отправка уведомлений
    """

    def __init__(
        self,
        repo: NotificationScheduleRepository,
        scheduler: NotificationScheduler,
        sender: NotificationSender
    ) -> None:
        self.schedule_repo = repo
        self.notification_scheduler = scheduler
        self.notification_sender = sender

    def create_schedule(self, sch: NotificationSchedule) -> None:
        """Создает расписание уведомления"""
        self.schedule_repo.insert_schedule(sch)

    def get_schedules(self) -> List[NotificationSchedule]:
        """Получает все расписания уведомлений"""
        return self.schedule_repo.get_schedules()

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
        # планируем уведомления
        self.notification_scheduler.schedule(notifications)

        return notifications

    def send_notification(self, notification: Notification) -> None:
        """Отправляет уведомление"""
        self.notification_sender.send(notification.message)
