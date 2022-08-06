import datetime
import unittest
import sys
from collections import namedtuple
from main import construct_week, moving_week, filter_lists, add_positions


def test_cases(*parameters):
    def tuplify(x):
        if not isinstance(x, tuple):
            return (x,)
        return x

    def decorator(method, parameters=parameters):
        for parameter in (tuplify(x) for x in parameters):
            def method_for_parameter(self, method=method, parameter=parameter):
                method(self, *parameter)

            args_for_parameter = ",".join(repr(v) for v in parameter)
            name_for_parameter = method.__name__ + '(' + args_for_parameter + ')'
            frame = sys._getframe(1)  # pylint: disable-msg=W0212
            frame.f_locals[name_for_parameter] = method_for_parameter
        return None

    return decorator


class UnitTests(unittest.TestCase):
    TestCase = namedtuple('TestCase', ['input', 'output'])

    @test_cases(
        TestCase(input=datetime.datetime(2022, 9, 1),
                 output=[datetime.datetime(2022, 9, 5), datetime.datetime(2022, 9, 6),
                         datetime.datetime(2022, 9, 7), datetime.datetime(2022, 9, 1),
                         datetime.datetime(2022, 9, 2)]),

        TestCase(input=datetime.datetime(2020, 5, 6),
                 output=[datetime.datetime(2020, 5, 11), datetime.datetime(2020, 5, 12),
                         datetime.datetime(2020, 5, 6), datetime.datetime(2020, 5, 7),
                         datetime.datetime(2020, 5, 8)])
    )
    def test_construct_week(self, args, exp):
        self.assertEqual(list(construct_week(args)), exp)

    @test_cases(
        TestCase(input=(datetime.datetime(2022, 7, 8), 1),
                 output=datetime.datetime(2022, 7, 11)),

        TestCase(input=(datetime.datetime(2022, 7, 13), 5),
                 output=datetime.datetime(2022, 7, 15))
    )
    def test_moving_week(self, args, exp):
        self.assertEqual(moving_week(args[0], args[1]), exp)

    from structs import Info

    @test_cases(
        TestCase(input=[{'id': True, 'pos': True, 'name': 'lorem ipsum PIRMADIENIS'},
                        {'id': True, 'pos': True, 'name': 'lorem ipsum TREČIADIENIS'},
                        {'id': False, 'pos': False, 'name': 'lorem ipsum et dolor amet'}],
                 output=[Info(0, 'PIRMADIENIS', True), Info(2, 'TREČIADIENIS', True)])
    )
    def test_filter_lists(self, args, exp):
        self.assertEqual(filter_lists(args), exp)

    @test_cases(
        TestCase(input=[('Tue', datetime.datetime(2022, 1, 4)), ('Mon', datetime.datetime(2022, 1, 3)),
                        ('Thr', datetime.datetime(2022, 1, 6)),
                        ('Wed', datetime.datetime(2022, 1, 5)), ('Fri', datetime.datetime(2022, 1, 7))],
                 output=[('Mon', datetime.datetime(2022, 1, 3), 162046.82031345367),
                         ('Tue', datetime.datetime(2022, 1, 4), 210302.4804701805),
                         ('Wed', datetime.datetime(2022, 1, 5), 234430.31054854393),
                         ('Thr', datetime.datetime(2022, 1, 6), 258558.14062690735),
                         ('Fri', datetime.datetime(2022, 1, 7), 258558.57031345367)])
    )
    def test_add_positions(self, args, exp):
        self.assertEqual(list(add_positions(args)), exp)


if __name__ == '__main__':
    unittest.main()
