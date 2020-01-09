import os
from typing import Callable

import redis
from dependency_injector import containers, providers
from dotenv import load_dotenv
from rq_scheduler import Scheduler

from push_random.services import NotificationService, NotificationScheduleRepository, NotificationScheduler, \
    pushover_sender, fake_sender

load_dotenv()


class AppContainer(containers.DeclarativeContainer):
    redis_cli = providers.Singleton(redis.from_url, os.getenv("REDIS_URL"))
    rq_scheduler: Callable[[], Scheduler] = providers.Singleton(Scheduler, connection=redis_cli)

    schedule_repo: Callable[[], NotificationScheduleRepository] = providers.Factory(
        NotificationScheduleRepository,
        redis_cli
    )

    notification_sender = providers.Object(pushover_sender)
    notification_sender_settings = providers.Object({
        "user": os.getenv("PUSHOVER_USER"),
        "token": os.getenv("PUSHOVER_TOKEN")
    })

    notification_scheduler: Callable[[], NotificationScheduler] = providers.Factory(
        NotificationScheduler,
        rq_scheduler=rq_scheduler,
        sender=notification_sender,
        sender_settings=notification_sender_settings
    )

    notification_service: Callable[[], NotificationService] = providers.Factory(
        NotificationService,
        repo=schedule_repo,
        scheduler=notification_scheduler,
    )


@containers.copy(AppContainer)
class TestContainer(containers.DeclarativeContainer):
    import fakeredis

    redis_cli = providers.Singleton(fakeredis.FakeStrictRedis)
    notification_sender = providers.Object(fake_sender)
    notification_sender_settings = providers.Object({})
