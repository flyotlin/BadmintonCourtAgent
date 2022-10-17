import json
import mechanicalsoup
import re
import requests

from datetime import datetime
from typing import Literal, TypedDict, List, Tuple

from src.object import VacantCourt


class BadmintonReserveAgent():
    BaseCookie = TypedDict('Cookie', {'PHPSESSID': str, 'XSRF-TOKEN': str, '17fit_system_session': str})
    Court = TypedDict('Court', {'member_id': int, 'member_name': str, 'role_relationships_id': int, 'level_price': int})
    Datetime = TypedDict('Datetime', {'available_role_relationship_ids': List[int], 'date': str, 'datetime': str, 'time': str})
    CourtAndDatetime = TypedDict('CourtAndDatetime', {'court': Court, 'datetime': Datetime})

    COURTS = Literal['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']
    COURTS_LIST = ['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']

    def __init__(self, cookie: BaseCookie) -> None:
        self.browser = mechanicalsoup.StatefulBrowser(
            raise_on_404=True,
        )

        self.browser.set_cookiejar(requests.cookies.cookiejar_from_dict(cookie))

    def _get_courts(self) -> List[Court]:
        GET_COURT_PATTERNS = r'\[\{.*"member_id".*:.*,.*"member_name".*:.*\}\]'
        GET_COURT_URL = 'https://17fit.com/service-flow-sp'
        GET_COURT_BODY = {
            'currency': 'NT$',
            'studio_id': '1090',
            'branch_id': '1275',
            'selected_services': '28055',
            'selected_services_namelist': '羽球館場地預約',
            'selected_services_timetotal': '1+小時0+分鐘',
            'selected_services_pricetotal': '400',
            'service_url': 'https://17fit.com/NCUsportscenter/01?tab=appointments',
        }

        html = self.browser.post(GET_COURT_URL, GET_COURT_BODY).text
        courts_json = re.compile(GET_COURT_PATTERNS).findall(html)
        assert len(courts_json) == 1, 'courts: pattern did not matched'
        return json.loads(courts_json[0])

    def _set_current_court(self, court: Court) -> None:
        """前往羽球館的某一個場地，目的是在 session 中設定場地資訊

        Args:
            court (Court): _description_
        """
        SET_CURRENT_COURT_URL = 'https://17fit.com/service-flow-dt'

        self.browser.post(SET_CURRENT_COURT_URL, court)

    def _get_provider_datetimes(self, date: str) -> List[Datetime]:
        """取得該場地目前所有日期

        Args:
            date (str): 日期 (e.g., 2022/05/09)

        Returns:
            List[Datetime]: _description_
        """
        GET_PROVIDER_DATETIME_URL = 'https://17fit.com/getServiceProviderDateTimeApi'
        # TODO: post with date
        datetimes_json = self.browser.post(GET_PROVIDER_DATETIME_URL, data={'date': date}).json()
        return datetimes_json

    def _set_current_datetime(self, time: Datetime) -> str:
        SET_CURRENT_DATETIME_URL = 'https://17fit.com/service-flow-confirm'
        SET_CURRENT_DATETIME_PATTERNS = r'\[\{.*"id".*:.*,.*"studio_id".*:.*\}\]'

        html = self.browser.post(SET_CURRENT_DATETIME_URL, {
            'is_cash': 0,
            'selected_time': time['time'],
            'selected_day': time['date'],
        }).text
        datetimes_json = re.compile(SET_CURRENT_DATETIME_PATTERNS).findall(html)
        assert len(datetimes_json) == 1, 'datetimes: pattern did not matched'
        return json.loads(datetimes_json[0])[0]['id']

    def _reserve(self, id=28055) -> None:
        # id is 羽球館 service id
        SET_RESERVE_URL = 'https://17fit.com/service-flow-make-appointment'

        self.browser.post(SET_RESERVE_URL, {
            'client_booking_note': 'ya',
            'pay_method': 'cash',
            'contract_selected': '{' + f'"{id}": 0' + '}',
            'studio_payment_method_id': 1,
        })

    # TODO: the spec of batch reserve need to discuss
    def _batch_go(self, court_and_datetimes: List[CourtAndDatetime], maximun_at_the_same_time: int) -> None:
        count_of_the_same_time = {x['datetime']['datetime']: 0 for x in court_and_datetimes}
        for court_and_datetime in court_and_datetimes:
            if count_of_the_same_time[court_and_datetime['datetime']['datetime']] < maximun_at_the_same_time:
                self.go(court_and_datetime)

                count_of_the_same_time[court_and_datetime['datetime']['datetime']] += 1

    def check(self, date: str, courts: Tuple[int]) -> List[VacantCourt]:
        """_summary_

        Args:
            date (str): 日期 (e.g., 05/09)
            courts (Tuple[int]): 場地 (e.g., (1,2,4))

        Returns:
            List[VacantCourt]: _description_
        """
        if not re.match("^(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$", date):
            raise ValueError(f"{date} not match format %m-%d")

        if type(courts) != tuple:
            raise ValueError("Courts is not a tuple")

        for i in courts:
            if type(i) != int:
                raise ValueError("Courts element is not an int")
            if i < 1 or i > 6:
                raise ValueError("Courts element not between 1 and 6")

        courts_names = tuple(map(lambda x: self.COURTS_LIST[x - 1], courts))
        all_courts = self._get_courts()
        matched_courts = [x for x in all_courts if x['member_name'].endswith(courts_names)]

        result = []
        for (court_idx, court) in zip(courts, matched_courts):
            self._set_current_court(court)
            all_datetimes = self._get_provider_datetimes(f'{datetime.now().year}-{date}')
            for i in all_datetimes:
                result.append(VacantCourt(court_idx, i['date'], i['time']))
        return result

    def go(self, court: int, date: str, time: str) -> bool:
        """預約 courts, time 的場地

        Args:
            court (int): 場地 (1-6)
            date (str): "04-29" 要預約的日期
            time (str): "18:00" 要預約的時間

        Returns:
            _type_: _description_
        """
        # prepare court
        courts_names = self.COURTS_LIST[court - 1]
        all_courts = self._get_courts()
        courts_info = [x for x in all_courts if x['member_name'].endswith(courts_names)][0]
        matched_courts = [x for x in all_courts if x['member_name'].endswith(courts_names)]

        # prepare datetime
        datetimes_info = None

        for _court in matched_courts:
            self._set_current_court(_court)
            all_datetimes = self._get_provider_datetimes(f'{datetime.now().year}-{date}')
            for i in all_datetimes:
                if i['time'] == time:
                    datetimes_info = i

        if not datetimes_info:
            return False

        self._set_current_court(courts_info)
        self._set_current_datetime(datetimes_info)
        self._reserve()
        return True
