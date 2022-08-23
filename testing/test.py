from unittest import TestCase
from inspect import signature
from unittest.mock import patch
from main import datetime

from testing.test_cases import Tests, MockedTests, Mocks


# TODO: Fix up this method
def add_unit_tests(test_class, tests):
    for test in tests:
        def wrapper(self, test_info=test):
            with self.subTest(input=test_info):

                for exception_case in test_info.exception_cases:
                    with self.assertRaises(exception_case.expected):
                        test_info.function(exception_case.input)

                for case in test_info.cases:
                    result = test_info.function(case.input) \
                        if len(signature(test_info.function).parameters) == 1 \
                        else test_info.function(*case.input)
                    return self.assertEqual(
                        list(result) if (type(result) is not datetime) and
                                        (type(result) is map or type(result) is zip or type(result) is filter)
                        else result,
                        case.expected,
                        msg='function: {}, case: {} FAILED'
                            .format(test_info.function.__name__, test_info.cases.index(case)))

        setattr(test_class, 'test_' + test.function.__name__, wrapper)


def patch_mocks(test_class, mocks):
    for mock in mocks:
        patch(mock.name, mock.function)(test_class)


class UnitTests(TestCase):
    pass


add_unit_tests(UnitTests, Tests)


class MockTests(TestCase):
    @patch('config.key', 'MyKey')
    @patch('config.token', 'MyToken')
    def test_main(self):
        import io
        import sys
        from main import main
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "{}\n".format(['Success']*5))


add_unit_tests(MockTests, MockedTests)
patch_mocks(MockTests, Mocks)

if __name__ == "__main__":
    from structs import ROOT_DIR
    from coverage.cmdline import main
    import os
    import webbrowser

    os.chdir(ROOT_DIR)
    print(ROOT_DIR)
    # TODO: Investigate why this is not working while bash script is

    os.system('cmd /k "coverage html --omit="*/testing*" --directory=testing/htmlcov"')
    main(['run', '-m', 'unittest', 'testing/test.py'])
    main(['html', '--omit="*/testing*"', '--directory=testing/htmlcov'])
    webbrowser.open('file://' + os.path.realpath('testing/htmlcov/index.html'))
