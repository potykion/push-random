from notifiers import Response, notify


class PushoverNotificationSender:
    """
    Класс для отправки уведомлений с помощью Pushover
    https://pushover.net/
    https://github.com/notifiers/notifiers
    """

    def __init__(self, user: str, token: str) -> None:
        self.service = 'pushover'
        self.user = user
        self.token = token

    def send(self, message: str) -> bool:
        res: Response = notify(self.service, user=self.user, token=self.token, message=message)
        return res.ok