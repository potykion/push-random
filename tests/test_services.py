import datetime as dt

import pytest

from push_random.containers import AppContainer
from push_random.models import NotificationSchedule


def test_create_schedule(container: AppContainer) -> None:
    sch = NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    container.notification_service().create_schedule(sch)
    assert container.schedule_repo().get_schedules() == [sch]


@pytest.fixture()
def schedule():
    return NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)


def test_create_notifications(container: AppContainer, schedule: NotificationSchedule) -> None:
    notifications = container.notification_service().create_notifications(schedule)

    assert len(notifications) == schedule.freq
    assert all(schedule.to_datetime >= notif.sending_dt >= schedule.from_datetime for notif in notifications)
    assert len(container.notification_scheduler().get_scheduled_notifications()) == 3
