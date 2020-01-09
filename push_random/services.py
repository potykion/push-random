import datetime as dt
import random
import uuid
from typing import List, Any, Dict

from notifiers import notify
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
    """Интерфейс для отправки уведомлений"""
    def __call__(self, message: str, **settings: Any) -> Any:
        ...


def pushover_sender(message, **settings):
    """
    Отправляет уведомления с помощью Pushover
    https://pushover.net/
    https://github.com/notifiers/notifiers#basic-usage
    """
    return notify("pushover", message=message, **settings)


def fake_sender(message, **settings):
    """Не отправляет уведомления с помощью Pushover"""
    return


class NotificationScheduler:
    """Класс для работы с планировщиком уведомлений"""

    def __init__(self, rq_scheduler: Scheduler, sender: NotificationSender, sender_settings: Dict) -> None:
        self.rq_scheduler = rq_scheduler
        self.sender = sender
        self.sender_settings = sender_settings

    def schedule(self, notifications) -> None:
        """Планирует уведомления (ставит в очередь)"""
        for notification in notifications:
            self.rq_scheduler.enqueue_at(
                notification.sending_dt,
                self.sender,
                notification.message,
                **self.sender_settings
            )

    def get_scheduled_notifications(self) -> List[Notification]:
        """Получает список запланированных уведомлений"""
        scheduled = list(self.rq_scheduler.get_jobs())
        return scheduled


class NotificationService:
    """
    Класс для работы с уведомлениями и расписаниями уведомлений
    """

    def __init__(
        self,
        repo: NotificationScheduleRepository,
        scheduler: NotificationScheduler,
    ) -> None:
        self.schedule_repo = repo
        self.notification_scheduler = scheduler

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
