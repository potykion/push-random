import datetime as dt

from push_random.containers import AppContainer
from push_random.models import NotificationSchedule


def test_create_schedule(container: AppContainer):
    sch = NotificationSchedule(message="test", from_time=dt.time(13), to_time=dt.time(1), freq=2)
    container.notification_service().create_schedule(sch)
    assert container.notification_repo().get_schedules() == [sch]
