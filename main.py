from requests import get, put
from datetime import datetime, timedelta
from toolz.functoolz import pipe
from functools import partial as p
from structs import Info


def today() -> datetime:
    return datetime.today()


def construct_week(curr_day: datetime) -> list[datetime]:
    return pipe(range(1, 6), p(map, p(moving_week, curr_day)))


def moving_week(curr_day: datetime, x: int) -> datetime:
    if x < curr_day.weekday() + 1:
        return curr_day + timedelta(x - (curr_day.weekday() + 1) + 7)
    else:
        return curr_day + timedelta(x - (curr_day.weekday() + 1))


def get_lists(secret_key, secret_token, board_id='6244703a8200242a5fba9fa4'):
    url = 'https://api.trello.com/1/boards/{}/lists/all'.format(board_id)
    query = {
        'key': secret_key,
        'token': secret_token,
    }
    return get(url, query).json()


# noinspection PyTypeChecker
def filter_lists(lst: list[dict]) -> list[Info]:
    weekdays = [('PIRMADIENIS', 0), ('ANTRADIENIS', 1), ('TREČIADIENIS', 2), ('KETVIRTADIENIS', 3), ('PENKTADIENIS', 4)]
    dictionary = {}
    for item in lst:
        for weekday in weekdays:
            if weekday[0] in item['name']:
                weekdays.remove(weekday)
                dictionary[weekday] = item['id']
        if not weekdays:
            break  # pragma: no cover
    return [Info(i[1], i[0], item) for i, item in sorted(dictionary.items(), key=lambda i: i[0][1])]


def get_id_daytime(secret_key, secret_token):
    return zip(pipe(get_lists(secret_key, secret_token), filter_lists),
               pipe(today(), construct_week))


def add_positions(lst: list[tuple[Info, datetime]]) -> list[tuple[Info, datetime, float]]:
    positions = [162046.82031345367, 210302.4804701805, 234430.31054854393, 258558.14062690735, 258558.57031345367]
    return pipe(lst, p(sorted, key=lambda x: x[1].day), p(zip, positions), p(map, lambda x: (x[1][0], x[1][1], x[0])))


def set_list(secret_key, secret_token, item: tuple[Info, datetime, float]):
    url = 'https://api.trello.com/1/lists/{}/name'.format(item[0].id)
    query = {
        'key': secret_key,
        'token': secret_token,
        'value': '{:02d}.{:02d} - {}'.format(item[1].month, item[1].day, item[0].name),
        'pos': item[2]
    }
    return put(url, query).text


if __name__ == "__main__":
    from config import key, token

    pipe(get_id_daytime(key, token), add_positions, p(map, p(set_list, key, token)), list, print)
