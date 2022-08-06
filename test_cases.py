from typing import NamedTuple, Callable, Any
from structs import Info
from main import datetime
from main import construct_week, moving_week, filter_lists, add_positions


class TestData(NamedTuple):
    input: Any
    expected: Any


class TestInfo(NamedTuple):
    cases: list[TestData]
    function: Callable


Tests = [
    TestInfo(
        cases=[
            TestData(input=datetime(2022, 9, 1),
                     expected=[datetime(2022, 9, 5), datetime(2022, 9, 6),
                               datetime(2022, 9, 7), datetime(2022, 9, 1),
                               datetime(2022, 9, 2)]),

            TestData(input=datetime(2020, 5, 6),
                     expected=[datetime(2020, 5, 11), datetime(2020, 5, 12),
                               datetime(2020, 5, 6), datetime(2020, 5, 7),
                               datetime(2020, 5, 8)])
        ],
        function=construct_week
    ),

    TestInfo(
        cases=[
            TestData(input=(datetime(2022, 7, 8), 1),
                     expected=datetime(2022, 7, 11)),

            TestData(input=(datetime(2022, 7, 13), 5),
                     expected=datetime(2022, 7, 15))
        ],
        function=moving_week),

    TestInfo(
        cases=[
            TestData(input=[{'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                            {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                            {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}],
                     expected=[Info(0, 'PIRMADIENIS', True), Info(2, 'TREČIADIENIS', True)])],
        function=filter_lists
    ),

    TestInfo(
        cases=[
            TestData(input=[('Tue', datetime(2022, 1, 4)), ('Mon', datetime(2022, 1, 3)),
                            ('Thr', datetime(2022, 1, 6)),
                            ('Wed', datetime(2022, 1, 5)), ('Fri', datetime(2022, 1, 7))],
                     expected=[('Mon', datetime(2022, 1, 3), 162046.82031345367),
                               ('Tue', datetime(2022, 1, 4), 210302.4804701805),
                               ('Wed', datetime(2022, 1, 5), 234430.31054854393),
                               ('Thr', datetime(2022, 1, 6), 258558.14062690735),
                               ('Fri', datetime(2022, 1, 7), 258558.57031345367)])
        ],
        function=add_positions
    )

]
