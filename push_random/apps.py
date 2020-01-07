from typing import cast

import click

from push_random.containers import AppContainer
from push_random.models import NotificationSchedule


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj["container"] = AppContainer()


@cli.command()
@click.argument("message")
@click.argument("from_time")
@click.argument("to_time")
@click.argument("freq")
@click.pass_context
def create_sch(ctx:click.Context, message: str, from_time: str, to_time: str, freq: int):
    """
    cli для создания расписания уведомлений

    Пример:
    python manage.py create-sch test 13:00 01:00 2

    Создает расписание уведомления с текстом "test", которое будет отправляться c 13:00 по 01:00 2 раза в день
    """
    sch = NotificationSchedule(message=message, from_time=from_time, to_time=to_time, freq=freq)
    cast(AppContainer, ctx.obj["container"]).notification_service().create_schedule(sch)
    click.echo("Расписание создано")
