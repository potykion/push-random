from typing import cast

import pytest
from dependency_injector import containers, providers

from push_random.containers import AppContainer
from push_random.services import fake_sender


@containers.copy(AppContainer)
class TestContainer(containers.DeclarativeContainer):
    import fakeredis

    redis_cli = providers.Singleton(fakeredis.FakeStrictRedis)
    notification_sender = providers.Object(fake_sender)
    notification_sender_settings = providers.Object({})


@pytest.fixture()
def container() -> AppContainer:
    return cast(AppContainer, TestContainer)
