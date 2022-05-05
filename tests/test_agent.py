import unittest

from src.agent import BadmintonReserveAgent


class TestAgent(unittest.TestCase):
    def setUp(self) -> None:
        _token = {
            'PHPSESSID': '',
            'XSRF-TOKEN': '',
            '17fit_system_session': ''
        }
        self.agent = BadmintonReserveAgent(_token)

    @unittest.skip
    def test_check(self):
        expected_keys = ['court_idx', 'date', 'time']

        court_datetime_list = self.agent.check("05-07", courts=(1,2,3,4,5,6))

        self.assertIsInstance(court_datetime_list, list)
        for i in court_datetime_list:
            for j in expected_keys:
                self.assertIn(j, i.keys())

    def test_go(self):
        _court = 3
        _date = "05-09"
        _time = "07:00"

        ret = self.agent.go(court=_court, date=_date, time=_time)

        self.assertTrue(ret)

    def tearDown(self) -> None:
        return super().tearDown()
