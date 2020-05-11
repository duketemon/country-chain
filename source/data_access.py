import os
import redis

from string import Template


REDIS_CLIENT = redis.Redis.from_url(os.getenv('REDIS_URL'))
USED_COUNTRIES_BY_USER = Template("used-countries:$user_id")
COUNTRIES_SEPARATOR = '|'


def clear_user_data(user_id: int):
    REDIS_CLIENT.delete(USED_COUNTRIES_BY_USER.substitute(user_id=user_id))


def get_used_countries(user_id: int):
    used_countries = REDIS_CLIENT.get(USED_COUNTRIES_BY_USER.substitute(user_id=user_id))
    if used_countries is not None:
        return [int(c) for c in used_countries.decode("utf-8").split(COUNTRIES_SEPARATOR)]
    return []


def set_used_countries(user_id: int, used_countries: [int]):
    REDIS_CLIENT.set(
        name=USED_COUNTRIES_BY_USER.substitute(user_id=user_id),
        value=COUNTRIES_SEPARATOR.join([str(c) for c in used_countries]).encode("utf-8"),
        ex=int(os.getenv('REDIS_KEY_LIFETIME'))
    )
