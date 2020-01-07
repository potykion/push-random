import datetime as dt

import pytest

from push_random.containers import TestContainer
from push_random.models import NotificationSchedule


@pytest.fixture(scope="session")
def container() -> TestContainer:
    return TestContainer()


def test_create_schedule(container: TestContainer):
    sch = NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    container.notification_service().create_schedule(sch)
    assert container.notification_repo().get_schedules() == [sch]
