from typing import NamedTuple, Callable, Any, Type
from structs import Info
from main import datetime
from main import construct_week, moving_week, filter_lists, add_positions, get_lists, unpack, set_list, today, \
    compose_info_week, main
from unittest.mock import Mock


class TestData(NamedTuple):
    input: Any
    expected: Any


class ExceptionData(NamedTuple):
    input: Any
    expected: Type[Exception]


class TestInfo(NamedTuple):
    function: Callable
    cases: list[TestData] = []
    exception_cases: list[ExceptionData] = []


class MockInfo(NamedTuple):
    name: str
    function: Callable


Tests = [
    TestInfo(
        function=construct_week,
        cases=[
            TestData(input=datetime(2022, 9, 1),
                     expected=[datetime(2022, 9, 5), datetime(2022, 9, 6),
                               datetime(2022, 9, 7), datetime(2022, 9, 1),
                               datetime(2022, 9, 2)]),

            TestData(input=datetime(2020, 5, 6),
                     expected=[datetime(2020, 5, 11), datetime(2020, 5, 12),
                               datetime(2020, 5, 6), datetime(2020, 5, 7),
                               datetime(2020, 5, 8)])
        ]),

    TestInfo(
        function=moving_week,
        cases=[
            TestData(input=(datetime(2022, 7, 8), 1),
                     expected=datetime(2022, 7, 11)),

            TestData(input=(datetime(2022, 7, 13), 5),
                     expected=datetime(2022, 7, 15))
        ]),

    TestInfo(
        function=filter_lists,
        cases=[
            TestData(input=[{'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                            {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}],
                     expected=[Info(0, 'PIRMADIENIS', True), Info(2, 'TREČIADIENIS', True)]),

            TestData(input=[{'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum ANTRADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum KETVIRTADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum PENKTADIENIS'},
                            {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                            {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}],
                     expected=[Info(0, 'PIRMADIENIS', True), Info(1, 'ANTRADIENIS', True),
                               Info(2, 'TREČIADIENIS', True), Info(3, 'KETVIRTADIENIS', True),
                               Info(4, 'PENKTADIENIS', True)])
        ]),

    TestInfo(
        function=add_positions,
        cases=[
            TestData(input=[('Tue', datetime(2022, 1, 4)), ('Mon', datetime(2022, 1, 3)),
                            ('Thr', datetime(2022, 1, 6)),
                            ('Wed', datetime(2022, 1, 5)), ('Fri', datetime(2022, 1, 7))],
                     expected=[('Mon', datetime(2022, 1, 3), 162046.82031345367),
                               ('Tue', datetime(2022, 1, 4), 210302.4804701805),
                               ('Wed', datetime(2022, 1, 5), 234430.31054854393),
                               ('Thr', datetime(2022, 1, 6), 258558.14062690735),
                               ('Fri', datetime(2022, 1, 7), 258558.57031345367)])
        ]),

    TestInfo(
        function=unpack,
        cases=[
            TestData(input=(lambda a, b: [a, b], ('arg1', 'arg2')),
                     expected=['arg1', 'arg2'])
        ]),

    TestInfo(
        function=compose_info_week,
        cases=[
            TestData(input=([{'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                             {'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                             {'id': True, 'pos': True, 'name': 'lorem ipsum ANTRADIENIS'},
                             {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                             {'id': True, 'pos': True, 'name': 'lorem ipsum KETVIRTADIENIS'},
                             {'id': True, 'pos': True, 'name': 'lorem ipsum PENKTADIENIS'},
                             {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                             {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}], datetime(2022, 8, 23)),
                     expected=[(Info(0, 'PIRMADIENIS', True), datetime(2022, 8, 29)),
                               (Info(1, 'ANTRADIENIS', True), datetime(2022, 8, 23)),
                               (Info(2, 'TREČIADIENIS', True), datetime(2022, 8, 24)),
                               (Info(3, 'KETVIRTADIENIS', True), datetime(2022, 8, 25)),
                               (Info(4, 'PENKTADIENIS', True), datetime(2022, 8, 26))])
        ]
    )
]


def mock_get(url, query):
    if url == 'https://api.trello.com/1/boards/{}/lists/all'.format('6244703a8200242a5fba9fa4') and query == {
        'key': 'MyKey',
        'token': 'MyToken',
    }:
        mock = Mock(name='get')
        mock.json.return_value = [{'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                                  {'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                                  {'id': True, 'pos': True, 'name': 'lorem ipsum ANTRADIENIS'},
                                  {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                                  {'id': True, 'pos': True, 'name': 'lorem ipsum KETVIRTADIENIS'},
                                  {'id': True, 'pos': True, 'name': 'lorem ipsum PENKTADIENIS'},
                                  {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                                  {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}]
        return mock
    else:
        raise Exception('Wrong URL or QUERY')


class MockDatetime(datetime):
    today = lambda: datetime(2022, 8, 24)


def mock_put(url, query):
    from re import compile
    pattern = compile(r'\d{2}.\d{2} - [A-Z]*')
    if url == 'https://api.trello.com/1/lists/{}/name'.format(True) and query['key'] == 'MyKey' and \
            query['token'] == 'MyToken' and pattern.search(query['value']):
        mock = Mock(name='put')
        mock.text = 'Success'
        return mock
    else:
        raise Exception('Wrong URL or QUERY')


Mocks = [MockInfo('main.get', mock_get), MockInfo('main.datetime', MockDatetime), MockInfo('main.put', mock_put)]

# TODO: 100% code coverage, add more tests, finish all mocks
MockedTests = [
    TestInfo(
        function=get_lists,
        cases=[
            TestData(input=('MyKey', 'MyToken'),
                     expected=[{'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                               {'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                               {'id': True, 'pos': True, 'name': 'lorem ipsum ANTRADIENIS'},
                               {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                               {'id': True, 'pos': True, 'name': 'lorem ipsum KETVIRTADIENIS'},
                               {'id': True, 'pos': True, 'name': 'lorem ipsum PENKTADIENIS'},
                               {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'},
                               {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}])
        ],
        exception_cases=[
            ExceptionData(input=('NotMyKey', 'NotMyToken'),
                          expected=Exception)]),
    TestInfo(
        function=today,
        cases=[
            TestData(input=(),
                     expected=datetime(2022, 8, 24))
        ]),
    TestInfo(
        function=set_list,
        cases=[
            TestData(input=('MyKey', 'MyToken', (Info(0, 'PIRMADIENIS', True), datetime(2022, 8, 29), 0.0)),
                     expected='Success')
        ],
        exception_cases=[
            ExceptionData(input=('NotMyKey', 'NotMyToken', True),
                          expected=Exception)])

]
