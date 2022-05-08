import unittest

from src.job_worker.parser import JobWorkerParser
from src.enums import SubCommand
from src.exceptions import JobWorkerParseError


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = JobWorkerParser()
        return super().setUp()

    def test_parse_empty_args(self):
        _args = []

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def test_parse_too_many_args(self):
        _args = [str(x) for x in range(1, 4)]

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def test_parse_check(self):
        _args = ['check']
        expected = SubCommand.CHECK

        actual = self.parser.parse(_args)

        self.assertEqual(expected, actual)

    def test_parse_wrong_check(self):
        _args = ['checj']

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def test_parse_delete_correctly(self):
        _args = ['delete', '2']
        expected = SubCommand.DELETE

        actual = self.parser.parse(_args)

        self.assertEqual(expected, actual)

    def test_parse_delete_with_wrong_id(self):
        _args = ['delete', 'a2']

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def test_parse_create_with_1_days_1_times(self):
        _args = ['1', '08:20']
        expected = SubCommand.CREATE

        actual = self.parser.parse(_args)

        self.assertEqual(expected, actual)

    def test_parse_create_with_1_days_multiple_times(self):
        _args = ['1', '08:20,16:59']
        expected = SubCommand.CREATE

        actual = self.parser.parse(_args)

        self.assertEqual(expected, actual)

    def test_parse_create_with_multiple_days_1_times(self):
        _args = ['1,2,4', '23:59']
        expected = SubCommand.CREATE

        actual = self.parser.parse(_args)

        self.assertEqual(expected, actual)

    def test_parse_create_with_wrong_days(self):
        _args = ['03-05', '00:01']

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def test_parse_create_with_wrong_times(self):
        _args = ['1,3,5', '1,03-05.00:01']

        with self.assertRaises(JobWorkerParseError):
            self.parser.parse(_args)

    def tearDown(self) -> None:
        return super().tearDown()
