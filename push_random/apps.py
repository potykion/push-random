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

    Создает расписание уведомления с текстом "test", которое будет отправляться c 13:00 по 01:00 (по utc) 2 раза в день
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
    """
    create_notifications_for_all_schedules()


def create_notifications_for_all_schedules():
    """
    Берет все расписания, для каждого создает уведомления.
    """
    service = AppContainer.notification_service()
    schedules = service.get_schedules()
    click.echo(f"Получено расписаний: {len(schedules)}")
    for sch in schedules:
        notifications = service.create_notifications(sch)
        click.echo(f"Создано {sch.freq} уведомлений для расписания: {sch}:")
        for index, notification in enumerate(notifications):
            click.echo(f"  - {index + 1}. {notification}")


@cli.command()
@click.argument("cron_str")
def create_create_notifications_cron(cron_str: str) -> None:
    """
    cli для создания крона для создания уведомлений

    Пример:
    python manage.py create-create-notifications-cron "0 0 * * *"

    Создает rq-scheduler крон, который будет дергать create_notifications каждый день в 21:00 по utc
    """
    scheduler = AppContainer.rq_scheduler()
    scheduler.cron(cron_str, create_notifications_for_all_schedules)
    click.echo("Крон создан")
