import click

from push_random.containers import AppContainer
from push_random.models import NotificationSchedule


@click.group()
def cli() -> None:
    ...


@cli.command()
@click.argument("message")
@click.argument("from_time")
@click.argument("to_time")
@click.argument("freq")
def create_sch(message: str, from_time: str, to_time: str, freq: int) -> None:
    """
    cli для создания расписания уведомлений

    Пример:
    python manage.py create-sch test 13:00 01:00 2

    Создает расписание уведомления с текстом "test", которое будет отправляться c 13:00 по 01:00 2 раза в день
    """
    sch = NotificationSchedule(message=message, from_time=from_time, to_time=to_time, freq=freq)
    AppContainer.notification_service().create_schedule(sch)
    click.echo("Расписание создано")


@cli.command()
def create_notifications() -> None:
    """
    cli для создания уведомлений

    Пример:
    python manage.py create-notifications

    Берет все расписания, для каждого создает уведомления.
    """
    service = AppContainer.notification_service()
    schedules = service.get_schedules()
    click.echo(f"Получено расписаний: {len(schedules)}")
    for sch in schedules:
        service.create_notifications(sch)
        click.echo(f"Созданы уведомления для расписания: {sch}")
