# Redis 

Redis - хранилище типа ключ-значение, юзается как кешик, как бекенд для очереди задач 

## Как играться

Создать .env файл с REDIS_URL:

```dotenv
REDIS_URL=redis://...
```

Создать расписание - чтобы в редисе что-то было:

```shell script
python manage.py create-sch test 13:00 01:00 2
```

Начать играться:

```pydocstring
>>> import os
>>> from dotenv import load_dotenv
>>> import redis
>>> load_dotenv()
>>> redis_url = os.environ["REDIS_URL"]
>>> redis_cli = redis.from_url(redis_url)
>>> redis_cli.keys()
[b'sch-0c4d92c2-a15a-4548-a6f6-9d150bcc7178']
>>> redis_cli.get("sch-0c4d92c2-a15a-4548-a6f6-9d150bcc7178")
b'{"message": "test", "from_time": "13:00:00", "to_time": "01:00:00", "freq": 2}'
>>> redis_cli.keys("sch-*")
[b'sch-0c4d92c2-a15a-4548-a6f6-9d150bcc7178']
```

## Ссылки

- Redis + Python: https://github.com/andymccurdy/redis-py
- Redis commands: https://redis.io/commands