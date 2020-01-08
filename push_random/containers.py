import os
from typing import Callable

import redis
from dependency_injector import containers, providers
from dotenv import load_dotenv

from push_random.services import NotificationService, NotificationScheduleRepository, NotificationScheduler, \
    PushoverNotificationSender, FakeNotificationSender

load_dotenv()


class AppContainer(containers.DeclarativeContainer):
    redis_cli = providers.Singleton(redis.from_url, os.getenv("REDIS_URL"))
    schedule_repo: Callable[[], NotificationScheduleRepository] = providers.Factory(
        NotificationScheduleRepository,
        redis_cli
    )

    notification_sender = providers.Singleton(
        PushoverNotificationSender,
        os.getenv("PUSHOVER_USER"),
        os.getenv("PUSHOVER_TOKEN")
    )

    notification_scheduler: Callable[[], NotificationScheduler] = providers.Factory(
        NotificationScheduler,
        redis_cli,
        notification_sender
    )

    notification_service: Callable[[], NotificationService] = providers.Factory(
        NotificationService,
        schedule_repo,
        notification_scheduler,
        notification_sender
    )


@containers.copy(AppContainer)
class TestContainer(containers.DeclarativeContainer):
    import fakeredis

    redis_cli = providers.Singleton(fakeredis.FakeStrictRedis)
    notification_sender = providers.Singleton(FakeNotificationSender)
