import datetime as dt

import pytest

from push_random.containers import AppContainer
from push_random.models import NotificationSchedule


@pytest.fixture()
def container():
    return AppContainer()


def test_create_schedule(container):
    sch = NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    container.notification_service().create_schedule(sch)
    assert container.notification_repo().get_schedules() == [sch]
