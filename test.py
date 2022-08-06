from unittest import TestCase
from inspect import signature
from test_cases import Tests


class UnitTests(TestCase):
    pass


for test in Tests:
    def wrapper(self):
        for case in test.cases:
            with self.subTest(input=case.input):
                result = test.function(case.input) \
                    if len(signature(test.function).parameters) == 1 \
                    else test.function(case.input)
                return self.assertEqual(list(result) if type(result) == map or zip else result, case.expected)
    setattr(UnitTests, 'test_' + test.function.__name__, wrapper)

if __name__ == '__main__':
    UnitTests.main()
