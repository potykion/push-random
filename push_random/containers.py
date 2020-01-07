import os
from collections import Callable

import redis
from dependency_injector import containers, providers


from push_random.db import NotificationRepository
from push_random.services import PushoverNotificationSender, FakeNotificationSender, NotificationService, \
    NotificationSender


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


class TestContainer(AppContainer):
    import fakeredis

    redis_cli = providers.Singleton(fakeredis.FakeStrictRedis)
    notification_sender: NotificationSender = providers.Singleton(FakeNotificationSender)
