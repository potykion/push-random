import os

from dotenv import load_dotenv
from notifiers import notify, Response

# грузим енвы
load_dotenv()
PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

# тестим отправку пушей (https://pushover.net/, https://github.com/notifiers/notifiers)
message = 'test'
res: Response = notify('pushover', user=PUSHOVER_USER, token=PUSHOVER_TOKEN, message=message)
assert res.ok


