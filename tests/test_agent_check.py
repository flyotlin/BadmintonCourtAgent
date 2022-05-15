import unittest

from datetime import datetime
from typing import List

from src.agent import BadmintonReserveAgent


class TestAgentCheck(unittest.TestCase):
    def setUp(self) -> None:
        self._time = '14:00'
        self.agent = FakeAgentWhenTestingCheck(time=self._time)

    def test_correct_date_and_courts(self):
        _date = '05-10'
        _courts = (1, 2, 4)
        expected_result = {
            'court_idx': None,
            'date': f'{datetime.now().year}-{_date}',
            'time': self._time
        }
        all_expected_results = []
        for i in _courts:
            expected_result['court_idx'] = i
            all_expected_results.append(expected_result.copy())

        actual = self.agent.check(date=_date, courts=_courts)

        self.assertEqual(all_expected_results, actual)

    def test_wrong_date_delimiter(self):
        _date = '05/10'
        _courts = (1, 2, 4)

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not match format", str(value_error.exception))

    def test_date_month_without_zero_padding(self):
        _date = '5/10'
        _courts = (1, 2, 4)

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not match format", str(value_error.exception))

    def test_date_day_without_zero_padding(self):
        _date = '05/1'
        _courts = (1, 2, 4)

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not match format", str(value_error.exception))

    def test_multiple_invalid_dates(self):
        _dates = ['13-10', '12-33', '0-0']
        _courts = (1, 2, 4)

        for i in _dates:
            with self.assertRaises(ValueError) as value_error:
                self.agent.check(date=i, courts=_courts)
            self.assertIn("not match format", str(value_error.exception))

    def test_courts_is_a_list(self):
        _date = '05-10'
        _courts = [1, 2, 4]

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not a tuple", str(value_error.exception))

    def test_courts_elements_are_str(self):
        _date = '05-10'
        _courts = ('1', '2', '4')

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not an int", str(value_error.exception))

    def test_courts_elements_not_between_1_and_6(self):
        _date = '05-10'
        _courts = (-1, 0, 2, 7)

        with self.assertRaises(ValueError) as value_error:
            self.agent.check(date=_date, courts=_courts)
        self.assertIn("not between 1 and 6", str(value_error.exception))


class FakeAgentWhenTestingCheck(BadmintonReserveAgent):
    def __init__(self, time: str) -> None:
        self.time = time

    def _get_courts(self) -> List[BadmintonReserveAgent.Court]:
        all_courts_stub_value = [
            {'member_id': 0, 'member_name': '不指定', 'role_relationships_id': 0, 'level_price': 0},
            {'member_id': 735523, 'member_name': '中大羽球場01 近講臺右', 'role_relationships_id': 23456, 'level_price': 0},
            {'member_id': 735525, 'member_name': '中大羽球場02  近講臺中', 'role_relationships_id': 23752, 'level_price': 0},
            {'member_id': 735529, 'member_name': '中大羽球場03  近講臺左', 'role_relationships_id': 23458, 'level_price': 0},
            {'member_id': 735531, 'member_name': '中大羽球場04  近門口右', 'role_relationships_id': 23459, 'level_price': 0},
            {'member_id': 735533, 'member_name': '中大羽球場05  近門口中', 'role_relationships_id': 23753, 'level_price': 0},
            {'member_id': 735536, 'member_name': '中大羽球場06  近門口左', 'role_relationships_id': 23461, 'level_price': 0}
        ]
        return all_courts_stub_value

    def _set_current_court(self, court: BadmintonReserveAgent.Court) -> None:
        pass

    def _get_provider_datetimes(self, date: str) -> List[BadmintonReserveAgent.Datetime]:
        stub_value = [{'datetime': f'{date} {self.time}:00', 'date': f'{date}', 'time': f'{self.time}', 'available_role_relationship_ids': [23752]}]
        return stub_value
