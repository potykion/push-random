import os
from typing import Callable

import redis
from dependency_injector import containers, providers
from dotenv import load_dotenv

from push_random.db import NotificationRepository
from push_random.services import PushoverNotificationSender, NotificationService, FakeNotificationSender

load_dotenv()


class AppContainer(containers.DeclarativeContainer):
    redis_cli = providers.Singleton(redis.from_url, os.getenv("REDIS_URL"))
    notification_repo: Callable[[], NotificationRepository] = providers.Factory(
        NotificationRepository,
        redis=redis_cli
    )

    notification_sender = providers.Singleton(
        PushoverNotificationSender,
        os.getenv("PUSHOVER_USER"),
        os.getenv("PUSHOVER_TOKEN")
    )

    notification_service: Callable[[], NotificationService] = providers.Factory(
        NotificationService,
        repo=notification_repo,
        sender=notification_sender
    )


@containers.copy(AppContainer)
class TestContainer(containers.DeclarativeContainer):
    import fakeredis

    redis_cli = providers.Singleton(fakeredis.FakeStrictRedis)
    notification_sender = providers.Singleton(FakeNotificationSender)
