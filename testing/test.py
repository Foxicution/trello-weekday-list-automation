from unittest import TestCase
from inspect import signature
from unittest.mock import patch

from testing.test_cases import Tests


# TODO: Rewrite adding unit tests
def add_unit_tests(test_class, tests):
    for test in tests:
        def wrapper(self, test_info=test):
            for case in test_info.cases:
                with self.subTest(input=case.input):
                    result = test_info.function(case.input) \
                        if len(signature(test_info.function).parameters) == 1 \
                        else test_info.function(*case.input)
                    return self.assertEqual(list(result) if type(result) == (map or zip or filter) else result,
                                            case.expected,
                                            msg='function: {}, case: {} FAILED'
                                            .format(test_info.function.__name__, test_info.cases.index(case)))

        setattr(test_class, 'test_' + test.function.__name__, wrapper)


class UnitTests(TestCase):
    pass


add_unit_tests(UnitTests, Tests)


# TODO: Automate mock tests
@patch('main.get')
class MockTests(TestCase):
    def test_get_lists(self, get):
        from main import get_lists
        get.json.return_value = {}
        get_lists("myKey", "myToken", "")
        get.assert_called_once()

    @patch('main.datetime')
    def test_today(self, datetime):
        from main import today
        today()
        datetime.today.assert_called_with()

    @patch('main.today')
    @patch('main.get_lists')
    def test_get_id_daytime(self, today, get_lists):
        from main import get_id_daytime


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

