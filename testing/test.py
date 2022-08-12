from unittest import TestCase, main
from inspect import signature
from unittest.mock import MagicMock

import coverage.__main__

from testing.test_cases import Tests


def add_unit_tests(test_class, tests):
    for test in tests:
        def wrapper(self, test_info=test):
            for case in test_info.cases:
                with self.subTest(input=case.input):
                    result = test_info.function(case.input) \
                        if len(signature(test_info.function).parameters) == 1 \
                        else test_info.function(*case.input)
                    return self.assertEqual(list(result) if type(result) == (map or zip) else result,
                                            case.expected,
                                            msg='function: {}, case: {} FAILED'
                                            .format(test_info.function.__name__, test_info.cases.index(case)))

        setattr(test_class, 'test_' + test.function.__name__, wrapper)


class UnitTests(TestCase):
    pass


add_unit_tests(UnitTests, Tests)


class MockTests(TestCase):
    def test_something(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    from coverage import Coverage
    cov = Coverage()
    cov.start()
    main()
    cov.stop()
    cov.html_report(directory='covhtml')

