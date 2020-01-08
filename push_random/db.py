import uuid
from typing import List

from redis import Redis

from push_random.models import NotificationSchedule, Notification


class NotificationRepository:
    """Класс для работы с бд (redis) уведомлений и их расписаний"""

    SCHEDULE_PREFIX = "sch"
    NOTIFICATION_PREFIX = "notif"

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

    def insert_notifications(self, notifications: List[Notification]) -> None:
        """Сует уведомления в бд"""
        for notification in notifications:
            id_ = self._generate_id(self.NOTIFICATION_PREFIX)
            self.redis.set(id_, notification.json())

    def get_notifications(self) -> List[Notification]:
        """Получает все уведомления"""
        keys = self.redis.keys(f"{self.NOTIFICATION_PREFIX}-*")
        notifications = [Notification.from_json_str(self.redis.get(key)) for key in keys]
        return notifications

