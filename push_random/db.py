from typing import List

from redis import Redis

from push_random.models import NotificationSchedule, Notification


class NotificationRepository:
    """Класс для работы с бд (redis) уведомлений и их расписаний"""

    def __init__(self, redis: Redis):
        self.redis = redis

    def insert_schedule(self, sch: NotificationSchedule) -> None:
        """Сует расписание уведомления в бд"""
        pass

    def get_schedules(self) -> List[NotificationSchedule]:
        """Получает все расписания"""
        pass

    def insert_notifications(self, notifications: List[Notification]) -> None:
        """Сует уведомления в бд"""
        pass
