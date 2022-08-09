from unittest import TestCase, main
from inspect import signature
from test_cases import Tests


class UnitTests(TestCase):
    pass


for test in Tests:
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
    setattr(UnitTests, 'test_' + test.function.__name__, wrapper)

if __name__ == '__main__':
    main()
